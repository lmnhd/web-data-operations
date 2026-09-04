# WS-001 Vertical-Proof Notes

## Result

The bounded fixture run passed on 2026-09-03.

| Measure | Observed |
|---|---:|
| Input releases | 8 |
| Procurement processes | 4 |
| Consecutive-release comparisons | 4 |
| Comparisons carrying an update tag | 4 |
| Diff-derived material changes | 3 |
| Accepted | 1 |
| Rejected | 2 |
| Review needed | 1 |
| Automated tests | 6 passed |

The fixture is synthetic and intentionally covers one unchanged republication, one qualified deadline change, one unqualified deadline change, and one material change with missing qualification evidence. These numbers demonstrate deterministic behavior only; they do not measure live-source frequency, coverage, recall, latency, or business impact.

## Reproduce

From the repository root:

```powershell
python -m unittest discover -s projects\WS-001-qualified-tender-change-intelligence\tests -v
python projects\WS-001-qualified-tender-change-intelligence\src\run_pipeline.py --input projects\WS-001-qualified-tender-change-intelligence\tests\fixtures\release-package.json --profile projects\WS-001-qualified-tender-change-intelligence\examples\qualification-profile.json --output-dir projects\WS-001-qualified-tender-change-intelligence\evidence\latest-run --source-url fixture://synthetic-fts-release-package --retrieved-at 2026-09-03T16:00:00Z
```

The JSON report and three CSV queues in this directory are generated reviewer evidence.
