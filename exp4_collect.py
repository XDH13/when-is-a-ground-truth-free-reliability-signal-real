"""Exp 4 (route 1) -- re-run the SAME 2-round debate protocol on a MULTI-LEVEL
MATH pool (Levels 1-5) so we finally have a NON-CIRCULAR, NON-DEGENERATE
difficulty ruler: the dataset's own human-annotated Level.

Why this fixes the audit's open limitation (see cqm memory):
  - D_model (solo_wrong_frac): strong but CIRCULAR.
  - D_ext (llama3.1:8b error): non-circular but CEILING-collapsed on all-L5.
  - official Level on all-L5: ZERO variance -> unusable.
  -> On a pool spanning L1..L5, official Level has real ordered variance and is
     immune to circularity. If CQM signals die after residualizing on Level,
     that is clean evidence they are a difficulty proxy.

Reuses exp0_math call/parse/prompts (IDENTICAL backbone qwen2.5:7b + protocol).
Persists per-agent raw answers/confidences (so exp3_audit + exp1_process both
work) PLUS an integer `level`. Resumable via exp4_multilevel_log.jsonl.

Collection order is LEVEL-INTERLEAVED (round-robin across levels) so a partial
run still covers all five difficulty tiers rather than front-loading easy ones.
"""
import os, json, random
import exp0_math as E

N_AGENTS = E.N_AGENTS
CONV_THRESH = E.CONV_THRESH
LIMIT = int(os.environ.get("EXP4_LIMIT", "200"))
SEED = int(os.environ.get("EXP0_SEED", "0"))
POOL = os.path.join(os.path.dirname(__file__), "math_multilevel_pool.json")
LOG = os.path.join(os.path.dirname(__file__),
                   os.environ.get("EXP4_LOG", "exp4_multilevel_log.jsonl"))


def level_int(level_str):
    """'Level 3' -> 3 ; robust to missing."""
    try:
        return int(str(level_str).strip().split()[-1])
    except Exception:
        return 0


def run_item_raw(q, gold, level, mtype):
    r1 = []
    for _ in range(N_AGENTS):
        txt, fin = E.call(E.SOLVE.format(q=q))
        if fin != "STOP":
            return {"invalid": True, "reason": f"round1 finish={fin}"}
        r1.append(E.parse_json(txt) or {"reasoning": "", "answer": None, "confidence": 0.5})
    r1a = [E.num(o.get("answer")) for o in r1]
    r1c = [float(o.get("confidence", 0.5) or 0.5) for o in r1]
    r1r = [o.get("reasoning", "") for o in r1]
    r1_agree, _ = E.agree_fraction(r1a)
    r1_div = E.divergence(r1r)
    solo_wrong = sum(1 for a in r1a if a is None or abs(a - gold) >= 1e-4) / N_AGENTS
    diff_len = E.mean_toklen(r1r)
    r2 = []
    for i in range(N_AGENTS):
        others = [r1a[j] for j in range(N_AGENTS) if j != i]
        txt, fin = E.call(E.REVISE.format(q=q, mine=r1a[i], others=others))
        if fin != "STOP":
            return {"invalid": True, "reason": f"round2 finish={fin}"}
        r2.append(E.parse_json(txt) or r1[i])
    r2a = [E.num(o.get("answer")) for o in r2]
    r2c = [float(o.get("confidence", 0.5) or 0.5) for o in r2]
    r2r = [o.get("reasoning", "") for o in r2]
    r2_agree, top = E.agree_fraction(r2a)
    if top is None:
        return {"invalid": True, "reason": "no valid round2 answers"}
    r2_div = E.divergence(r2r)
    mc = sum(r2c) / len(r2c); cv = sum((c - mc) ** 2 for c in r2c) / len(r2c)
    return {
        "q": q, "gold": gold, "level": level_int(level),
        "tier": "math-" + str(level).lower().replace(" ", "") + "-" + mtype.lower().replace(" ", "_"),
        "majority": top, "converged": r2_agree >= CONV_THRESH, "correct": abs(top - gold) < 1e-4,
        "features": {"r1_agree": r1_agree, "r2_agree": r2_agree, "agree_slope": r2_agree - r1_agree,
                     "r1_div": r1_div, "r2_div": r2_div, "div_slope": r2_div - r1_div,
                     "mean_conf": mc, "conf_var": cv},
        "difficulty": {"solo_wrong_frac": solo_wrong, "mean_r1_toklen": diff_len},
        "raw": {"r1_ans": r1a, "r1_conf": r1c, "r2_ans": r2a, "r2_conf": r2c},
    }


def load_done():
    done = set()
    if os.path.exists(LOG):
        for line in open(LOG, encoding="utf-8"):
            try:
                r = json.loads(line)
                if not r.get("invalid"):
                    done.add(r.get("q"))
            except Exception:
                pass
    return done


def interleave_by_level(pool):
    """Round-robin across levels so partial runs still span L1..L5."""
    buckets = {}
    for item in pool:
        buckets.setdefault(level_int(item[2]), []).append(item)
    for lv in buckets:
        random.Random(SEED + lv).shuffle(buckets[lv])
    order = []
    levels = sorted(buckets)
    idx = {lv: 0 for lv in levels}
    remaining = sum(len(b) for b in buckets.values())
    while remaining > 0:
        for lv in levels:
            if idx[lv] < len(buckets[lv]):
                order.append(buckets[lv][idx[lv]])
                idx[lv] += 1
                remaining -= 1
    return order


def main():
    pool = json.load(open(POOL, encoding="utf-8"))
    order = interleave_by_level(pool)
    done = load_done()
    print(f"backbone={E.MODEL} agents={N_AGENTS} pool={len(order)} "
          f"limit={LIMIT} seed={SEED} resume={len(done)}", flush=True)
    n = 0
    with open(LOG, "a", encoding="utf-8") as f:
        for prob, gold, level, mtype in order:
            if n >= LIMIT:
                break
            if prob in done:
                n += 1; continue
            res = run_item_raw(prob, float(gold), level, mtype)
            if res is None or res.get("invalid"):
                print(f"item: INVALID ({res.get('reason') if res else 'none'})", flush=True)
                continue
            f.write(json.dumps(res) + "\n"); f.flush(); n += 1
            print(f"item {n} L{res['level']} [{res['tier']}]: conv={res['converged']} "
                  f"correct={res['correct']} maj={res['majority']} gold={gold}", flush=True)


if __name__ == "__main__":
    main()
