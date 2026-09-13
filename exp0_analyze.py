"""Minimal analysis compatibility module used by ``exp4_within.py``.

The released within-Level audit imports only ``eff_auc`` from the historical
exploratory analysis module.  This standalone implementation makes the public
analysis closure explicit; it performs no data collection and has no external
dependencies.
"""


def eff_auc(labels, scores):
    """Return directional and direction-agnostic Mann--Whitney AUC.

    ``labels`` uses 1 for false consensus and 0 for true consensus.  Ties
    receive half credit.  The second return value is the folded ``|AUC|`` used
    throughout the audit tables.
    """
    pos = [score for label, score in zip(labels, scores) if label == 1]
    neg = [score for label, score in zip(labels, scores) if label == 0]
    if not pos or not neg:
        return float("nan"), float("nan")
    concordant = sum(
        1.0 if p > n else 0.5 if p == n else 0.0
        for p in pos for n in neg
    )
    auc = concordant / (len(pos) * len(neg))
    return auc, max(auc, 1.0 - auc)
