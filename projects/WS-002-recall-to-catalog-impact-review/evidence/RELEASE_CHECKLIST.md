# WS-002 release checklist

Evidence assembled 2026-09-04 UTC. Status is **not RELEASE_READY** while the blocked items below remain unresolved.

| Gate | Status | Evidence |
|---|---|---|
| Local demo launches actual matcher | PASS | `python -B src/demo_server.py`; [browser verification](reviewer/BROWSER_VERIFICATION.md) |
| Meaningful input change changes result | PASS | CAT-005 review-needed -> match; input hash changes |
| Edge/safe state visible | PASS | Strength conflict retains two candidates and routes to review |
| JSON/CSV result inspection | PASS | HTTP export test and workbench download controls |
| Automated tests | PASS | `python -B -m unittest discover -s tests -v`: 21 passed |
| Larger independent-label benchmark | PASS | [20/20 run report](benchmark/run-report.json); 13 match / 1 no-match / 6 review-needed |
| Repair discipline | PASS | One bounded repair pass; [record](EXPANSION_REPAIR.md) |
| Desktop browser execution | PASS | [ambiguous](reviewer/ambiguous.png) and [clarified](reviewer/clarified.png) captures |
| Mobile browser layout | PASS | 390 x 844; no horizontal overflow; [capture](reviewer/mobile-clarified.png) |
| Visual PDF generated | PASS | [Product Recall Match Desk PDF](../../../output/pdf/Product-Recall-Match-Desk.pdf) |
| Every PDF page visually inspected | PASS | Three pages rendered at 144 dpi; page 3 overlap repaired; final pages legible and uncropped |
| PDF claims and links match implementation | PASS | 20/20, 21 tests, 13/1/6, one request; PDF contains public-demo and repository link annotations |
| Local reproduction instructions | PASS | [README](../README.md) and [Manifest walkthrough](../PROJECT_MANIFEST.md) |
| Independent verification | PASS | Fresh non-builder validator `/root/ws002_independent_validation` passed all 7 frozen checks and recertified the portable 54-file map at `f7f78f7`; prior FAIL is preserved in validation-runs |
| Public signed-out demo | PASS | [Public demo](https://product-recall-match-desk.vercel.app) returned anonymous HTTP 200; page and `/api/config` loaded without credentials on 2026-09-04 |
| Reviewed source integration | BLOCKED | Commit, pull request, default-branch integration and immutable tag are not yet authorized/recorded |
| Release authorization/publication | PASS | User authorized publication on 2026-09-04; GitHub release publication proceeds only after PR integration |

## Artifact integrity

- Matcher SHA-256: `18F5455515C86C193D433975BCAE82FA208C9CC91424D47972C197B5E77C9248`
- Benchmark catalog SHA-256: `74B247E59698197BCA3ABECD4C76DB633EFC4AD7500E8E67DE838965FDDCB127`
- Benchmark labels SHA-256: `1C6C8E4A1470C3B15599BCE6E444C2236ED0B3F4427A2FB97202543F4588DA67`
- PDF SHA-256: `2BAC7387BA7DA1688C2B7995C5DAA17B086A0DFC332DC034ABDF330757AFAE1E`

These hashes bind the assembled evidence before any publication-stage changes. If a blocked gate causes a file change, regenerate and reverify the affected artifact and update its hash.
