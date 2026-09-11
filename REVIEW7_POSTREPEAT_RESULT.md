# Independent post-repeat self-review

**Reviewer:** independent internal reviewer (not ARIS)  
**Decision:** conditional minor revision / substantively ready

## Scope checked

- The manuscript distinguishes a fixed archived trace from a stochastic
  generation population.
- The fresh P0 repetitions are reported for all requested feasible models:
  MATH Qwen2.5 3B/7B/14B and MMLU Qwen2.5 3B/7B/14B, Llama-3.1-8B, and
  Mistral-7B.
- The reported usable-record totals are unique-question totals: MATH
  225/235/238; MMLU 200 in each of five cells.
- The fresh point estimates are placed alongside the originals, and all eight
  paired item-bootstrap difference intervals include zero.

## Required revisions and disposition

1. **P0 — do not treat item-bootstrap intervals as generation-level intervals.**
   Resolved in REV8: setup, result text, table caption, and reproducibility
   appendix explicitly condition on the two archived traces.
2. **P0 — make the repeat observable rather than merely claiming it.**
   Resolved in REV8 with Table `tab:repeat`, all eight point estimates, and the
   record-count / exclusion rule.
3. **P1 — avoid a causal MATH-versus-MMLU conclusion.**
   Retained as a limitation: prompts and difficulty controls differ, so this is
   a domain stress observation only.

## Remaining publication checks

- Two traces are a useful robustness check but cannot characterize run-to-run
  generation variance; a future study needs several independent complete runs
  and a hierarchical analysis.
- The TeX dependency, references, labels, figures, and environments pass the
  repository static checker. A real TeX engine was unavailable in this
  workspace, so final submission should compile and visually inspect the PDF
  (especially the new wide table) before upload.
- Release the repeat JSONL files and analysis script alongside the paper so the
  table can be independently recomputed.
