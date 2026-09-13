# WS-004 bounded proof report

**Executed:** 2026-09-13  
**Stage:** PROVING  
**Review status:** Consolidated builder review PASS; independent validation has not been dispatched

## Outcome

The approved six-case local proof reproduced its pre-implementation oracle exactly:

| Decision | Expected | Observed |
|---|---:|---:|
| RECONCILED | 2 | 2 |
| MISMATCH | 1 | 1 |
| REVIEW_REQUIRED | 3 | 3 |

Default run ID: `ws004-1984fbedb2ae05ca`.

The recorded electricity calculation for source `CH-09904577-2025` recomputed to `697.341060 tCO2e` versus `697.340000 tCO2e` disclosed, a `0.001060 tCO2e` variance within the frozen `0.010000 tCO2e` tolerance. The recorded electricity calculation for `CH-12976528-2025` recomputed to `73.705632 tCO2e` versus `72.540000 tCO2e` disclosed, a `1.165632 tCO2e` variance and therefore MISMATCH. This is an arithmetic comparison against the filing's declared 2025 factor basis, not a compliance or truthfulness finding.

The engine refused to compute three cases: ambiguous natural-gas gross/net calorific basis, unsupported image-only evidence, and aggregate energy without a compatible activity breakdown.

## Reviewer-operated change

Case `CASE-02-CONTROLLED-MWH-RECONCILED` is an explicitly labeled reviewer-supplied scenario. Changing only its activity unit from `MWh` to `kWh` while leaving the numeric value at `1000` produced:

| Field | Baseline | Changed input |
|---|---:|---:|
| Normalized activity | 1,000,000 kWh | 1,000 kWh |
| Computed emissions | 177.000 tCO2e | 0.177 tCO2e |
| Decision | RECONCILED | MISMATCH |
| Input SHA-256 | `eb25a296...7adffe8` | `2703686f...8b2052c` |

The source, factor-subset, factor-workbook, and engine hashes remain unchanged. Changed-input run ID: `ws004-52cd149712424e77`.

## Commands and actual results

```powershell
python -B -m unittest discover -s projects/WS-004-corporate-carbon-disclosure-reconciler/tests -v
```

Result: 13 passed, 0 failed, 0 errors.

```powershell
python -B projects/WS-004-corporate-carbon-disclosure-reconciler/src/reconcile.py `
  --output-json projects/WS-004-corporate-carbon-disclosure-reconciler/evidence/evaluated_run.json `
  --output-csv projects/WS-004-corporate-carbon-disclosure-reconciler/evidence/evaluated_run.csv
```

Result: six records exported in both formats with the same run ID, decisions, reason codes, values, locators, and hashes.

## Evidence trace

- Full 2025 workbook SHA-256: `8BFDB45B81EC4A88E3BDF4584637330F62E6BD09CE1940E654C5D7B7F736DE94`.
- Committed minimized factor subset SHA-256 in the executed run: `8e55b4c1f1c35c3f1cf26d517b48dc5d1725642604d30946d13ab65aa59372a0`.
- Engine SHA-256 in both executed runs: `2c7b6930672a817775e0fef76cedb5523e7bf9ce76a3a981f741328bb7c125da`.
- Three selected filing hashes and the bounded archive hash are recorded in `SOURCE_SELECTION.json`; the full documents and archive are not committed.

## Actual obstacle and correction

Preliminary feasibility named the 2026 factor file. Source inspection showed that the selected filings cite 2025 factors. The source contract and frozen validation plan were corrected to the official 2025 Version 1 / Final workbook before implementation, preventing a misleading cross-vintage comparison.

The first sandboxed export-test run also found that the host's default temporary directory was outside the workspace write boundary. The test was changed to create its disposable directory under the project and the exact frozen command then passed with normal workspace permissions. Product calculations and oracle values did not change.

## Limits and next gate

This is a bounded local proof using three minimized filing sources and two clearly labeled controlled scenarios. It does not establish production accuracy, exhaustive source coverage, regulatory compliance, audit assurance, emissions truth, environmental performance, or savings. There is no visual PDF, web UI, public host, release checklist, independent PASS, or executable release-gate result yet. Expansion requires new human approval.

## Consolidated builder review

One consolidated builder review completed on 2026-09-13 with zero findings and no repair pass:

- the exact frozen unit-test command passed 13/13;
- the default and changed-input JSON/CSV outputs matched their declared values and hashes;
- the archive and full-workbook SHA-256 values matched the frozen source records;
- JSON/CSV exports agreed and the minimized input rejected prohibited personal/display fields;
- `git diff --check` and the active-state validator passed.

This is explicitly same-agent review. It cannot substitute for the fresh non-builder PASS and executable hash-based release gate required after an approved expanded candidate exists.
