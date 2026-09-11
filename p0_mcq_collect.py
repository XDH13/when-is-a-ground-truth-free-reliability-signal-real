"""Resumable homogeneous three-sample/two-round collector for a generic MCQ pool."""
import json
import os
import random
import re
from collections import Counter
from pathlib import Path

import exp0_math as E

ROOT = Path(__file__).resolve().parent
POOL = ROOT / os.environ.get("P0_MCQ_POOL", "mmlu_holdout_pool.json")
LOG = ROOT / os.environ.get("P0_MCQ_LOG", "p0_mcq_log.jsonl")
LIMIT = int(os.environ.get("P0_MCQ_LIMIT", "200"))
SEED = int(os.environ.get("P0_MCQ_SEED", "20260910"))
DOMAIN = os.environ.get("P0_DOMAIN", "mmlu-holdout")
MAX_TOKENS = int(os.environ.get("P0_MCQ_MAX_TOKENS", "128"))
N = 3

SOLVE = (
    'Answer this multiple-choice question. Give only the single best option '
    'letter and confidence; do not explain. Respond ONLY as JSON: '
    '{{"answer": "<A|B|C|D>", "confidence": <0..1>}}.\n\n'
    'Question: {q}\nOptions:\n{opts}'
)
REVISE = (
    'You are one of several independent solvers of a multiple-choice question. '
    'Your answer was {mine}. Other solvers answered {others}. Reconsider '
    'critically and give only your best final option letter and confidence; do '
    'not explain. Respond ONLY as JSON: {{"answer": "<A|B|C|D>", '
    '"confidence": <0..1>}}.\n\nQuestion: {q}\nOptions:\n{opts}'
)


def letter(x):
    if x is None:
        return None
    s = str(x).strip().upper()
    m = re.search(r"\b([ABCD])\b", s)
    if m:
        return m.group(1)
    return s[0] if s and s[0] in "ABCD" else None


def confidence(obj):
    try:
        return min(1.0, max(0.0, float(obj.get("confidence", 0.5) or 0.5)))
    except Exception:
        return 0.5


def agree(ans):
    valid = [a for a in ans if a is not None]
    if not valid:
        return 0.0, None
    top, count = Counter(valid).most_common(1)[0]
    return count / N, top


def options_text(choices):
    return "\n".join(
        f"{lab}. {text}" for lab, text in zip(choices["label"], choices["text"])
    )


def run_item(q, choices, gold, tier):
    opts = options_text(choices)
    r1 = []
    for _ in range(N):
        txt, finish = E.call(SOLVE.format(q=q, opts=opts), max_tokens=MAX_TOKENS)
        if finish != "STOP":
            return {"invalid": True, "reason": f"round1 finish={finish}"}
        r1.append(E.parse_json(txt) or {"reasoning": "", "answer": None, "confidence": 0.5})
    r1a = [letter(x.get("answer")) for x in r1]
    r1c = [confidence(x) for x in r1]
    r1r = [x.get("reasoning", "") for x in r1]
    r1_agree, _ = agree(r1a)
    r2 = []
    for i in range(N):
        others = [r1a[j] for j in range(N) if j != i]
        txt, finish = E.call(
            REVISE.format(q=q, opts=opts, mine=r1a[i], others=others),
            max_tokens=MAX_TOKENS,
        )
        if finish != "STOP":
            return {"invalid": True, "reason": f"round2 finish={finish}"}
        r2.append(E.parse_json(txt) or r1[i])
    r2a = [letter(x.get("answer")) for x in r2]
    r2c = [confidence(x) for x in r2]
    r2r = [x.get("reasoning", "") for x in r2]
    r2_agree, majority = agree(r2a)
    if majority is None:
        return {"invalid": True, "reason": "no valid round2 answers"}
    mc = sum(r2c) / N
    return {
        "q": q,
        "gold": gold,
        "level": int(tier),
        "tier": f"{DOMAIN}-" + ("stem" if int(tier) else "humanities-social"),
        "model": E.MODEL,
        "majority": majority,
        "converged": r2_agree >= 2 / 3,
        "correct": majority == gold,
        "features": {
            "r1_agree": r1_agree,
            "r2_agree": r2_agree,
            "agree_slope": r2_agree - r1_agree,
            "r1_div": E.divergence(r1r),
            "r2_div": E.divergence(r2r),
            "div_slope": E.divergence(r2r) - E.divergence(r1r),
            "mean_conf": mc,
            "conf_var": sum((c - mc) ** 2 for c in r2c) / N,
        },
        "difficulty": {
            "solo_wrong_frac": sum(a != gold for a in r1a) / N,
            "mean_r1_toklen": E.mean_toklen(r1r),
        },
        "raw": {"r1_ans": r1a, "r1_conf": r1c, "r2_ans": r2a, "r2_conf": r2c},
        "protocol": {"temperature": 0.7, "num_predict": MAX_TOKENS, "seed_controls_order_only": True},
    }


def interleave(pool):
    buckets = {}
    for item in pool:
        buckets.setdefault(int(item[3]), []).append(item)
    for tier, rows in buckets.items():
        random.Random(SEED + tier).shuffle(rows)
    out = []
    while any(buckets.values()):
        for tier in sorted(buckets):
            if buckets[tier]:
                out.append(buckets[tier].pop())
    return out


def main():
    pool = interleave(json.loads(POOL.read_text(encoding="utf-8")))
    done = set()
    if LOG.exists():
        for line in LOG.read_text(encoding="utf-8").splitlines():
            try:
                rec = json.loads(line)
                if not rec.get("invalid"):
                    done.add(rec["q"])
            except Exception:
                pass
    print(f"model={E.MODEL} pool={POOL.name} log={LOG.name} resume={len(done)}", flush=True)
    completed = len(done)
    with LOG.open("a", encoding="utf-8") as fh:
        for q, choices, gold, tier in pool:
            if completed >= LIMIT:
                break
            if q in done:
                continue
            rec = run_item(q, choices, gold, tier)
            if rec.get("invalid"):
                print(f"INVALID: {rec['reason']}", flush=True)
                continue
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            fh.flush()
            completed += 1
            print(
                f"{completed}/{LIMIT} tier={tier} conv={rec['converged']} "
                f"correct={rec['correct']} r2={rec['features']['r2_agree']:.3f}",
                flush=True,
            )


if __name__ == "__main__":
    main()
