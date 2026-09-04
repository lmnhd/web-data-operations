# Expansion benchmark repair record

## Fixed evaluation boundary

- Inputs: `tests/fixtures/benchmark-catalog.json` and the recorded `tests/fixtures/recalls.json`.
- Oracle: `tests/fixtures/benchmark-labels.json`, declared independently from program output.
- Labels: `match`, `no_match` and `review_needed` for 20 synthetic catalog rows.
- Oracle labels were not changed during repair.

## Observed sequence

1. The initial expansion implementation reproduced **7 of 20** labels. Broad Jaccard-style text overlap underweighted short names, and strength tokens were compared as a single set, allowing package volume to hide a conflicting drug strength.
2. The single authorized repair pass changed reusable matcher logic: overlap coefficient for short names, per-unit strength comparison, an explicit 30-point review threshold, and review-safe handling of exact identifiers with a strength conflict.
3. An intermediate run reproduced 19 of 20 labels. Inspection showed Optiray 320 and 350 both included `500 mL`; per-unit comparison was required so shared volume could not cancel the conflicting mg/mL value.
4. The completed repair reproduced **20 of 20** labels: 13 match, 1 no-match and 6 review-needed.

No result row was hand-edited and no benchmark label was tuned after observing output. This is a bounded fixture result, not an estimate of production accuracy.
