# Proof Lab verification - 2026-09-04 UTC

Scope: local in-app Chromium browser at http://127.0.0.1:8765, existing Python pipeline, saved sanitized inputs. No new government data was fetched. Implementer performed these checks; no independent audit is claimed.

| Check | Observed result |
| --- | --- |
| Historical noise example | Seven versions, six pairs, zero tracked changes, six Ignore decisions |
| Historical cancellation | Two versions, five changed fields, Review with missing category/value/deadline reasons |
| Synthetic default maximum 5,000,000 | Act on the deadline extension |
| Synthetic maximum 300,000 | Ignore, VALUE_ABOVE_MAXIMUM; changed-field values unchanged |
| Edit after a result | Result invalidated until rerun |
| Run automated checks button | Actual unittest output: 17 tests passed, 0.530 seconds in the recorded run |
| JSON and CSV buttons | Browser clicks produced HTTP 200 for the selected run's attachment routes; payload equality tested through HTTP integration tests |
| Actual Python code panel | Rendered the diff and qualification functions read from the runtime module |
| Optional WebMCP tool | Valid cancellation run executed visibly; unknown case rejected |
| Browser console | No warnings or errors in the checked log |

Download completion in the operating-system downloads folder was not independently inspected. Initial blob download detection timed out in browser automation; the implementation was changed to explicit same-origin attachment endpoints and those requests succeeded. Do not claim an OS-level download audit.

The 17-test suite includes fresh engine calls, stable results, rule sensitivity, missing-data routing, normalization privacy, unknown-case rejection, invalid profile rejection, cross-origin rejection, fixed-route access, and JSON/CSV exports.

Screenshots: `*-full.png` are browser originals; `*-crop.json` are DOM-measured result bounds; the PDF builder creates the corresponding result crops without changing their content. The screenshot walkthrough is a sequence, not a continuous recording.

Remaining scope: public hosting, independent review, main integration, release tag and portfolio publication require separate decisions. A local replay does not prove current live collection, uptime, completeness, scale or commercial impact.
