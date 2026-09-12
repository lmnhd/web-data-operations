# Municipal 311 SLA Operations Desk v1.0.0

WS-003 demonstrates an adapter-ready service-response evaluation workflow over 15 explicitly synthetic 311-style records.

## Included

- Python engine and no-login reviewer workbench.
- Configurable hypothetical response targets.
- Timestamp normalization, lifecycle mapping, and explicit review routing.
- Synthetic ward scenario aggregation.
- Machine-readable `synthetic_sla_scenario` labels in JSON/CSV exports.
- Predeclared fixture-label agreement of 15/15 and fourteen automated tests, including adversarial timestamp, chronology, category, and rule-input regressions.
- Three-page plain-English case study with a screenshot of the working output.
- Fresh-context independent validation and SHA-256 artifact coverage.

## Source correction

The City of Toronto public 311 schema is used as licensed context only. The current 2026 public export lacks target and closure timestamps, so the bundled IDs, categories, SLA rules, target dates, closure dates, and results are synthetic. No official Toronto SLA performance claim is made.

## Boundary

This portfolio project is not a live collector, production municipal system, staffing instruction, dispatch tool, or legal SLA certification. It contains no personal data.

Public demo target: https://municipal-311-sla-operations-desk.vercel.app
