# Independent validation protocol

Mandatory for WS-002 onward. WS-001 remains a historical same-agent-verified release, not retrospectively certified. Same-agent exceptions no longer satisfy release readiness.

## Before implementation

The orchestrator records `evidence/VALIDATION_PLAN.json` in the project, with `iterationId`, all `builderAgentIds`, repository-relative `artifactPaths` (final PDF plus shared code/config outside the project), and `checks`. Each check has a unique `id`, `category`, explicit `procedure` and `expected` result. Cover exactly these category names: `tests`, `demo`, `edge_case`, `exports`, `pdf_visual`, `claims`, `boundaries`. Multiple checks per category are allowed. Include exact test commands and real expected outcomes, not simply "tests pass". Commit the plan before building; scope changes require a recorded rationale and review before implementation continues. For an existing build such as WS-002, declare the plan retroactive and freeze it before separate verification; never invent pre-build history.

## Handoff

Reserve budget for one separate validator and a repair recheck. Spawn with no inherited conversation (`fork_turns: none`), supplying repository/project paths, approved brief, plan, evidence standard and build commit. The validator must not have implemented any part of this project's code or evidence package. A different model is optional; a genuinely different agent session is mandatory. Record actual agent IDs and the dispatch in the tracking log. If tools or budget cannot provide a separate validator, stop at VERIFYING and ask for the missing resources.

The builder commits a stable candidate. The validator independently reads requirements, runs the predefined commands, assesses whether those tests are meaningful, operates the demo, tests changed inputs and failures, and inspects every rendered PDF page. Add adversarial checks when the plan misses a risk; do not rubber-stamp builder output. The validator may write review evidence but must send implementation fixes back to the builder.

## Report contract

Write logs and visual findings under `evidence/validation-runs/`. Write `evidence/INDEPENDENT_VALIDATION.json` with:

- `iterationId`, `validatorAgentId`, `verdict` (`PASS` or `FAIL`), `unresolvedFindings` (empty only when resolved);
- `planSha256`: SHA-256 of the frozen plan;
- `artifactSha256`: repository-relative path to SHA-256 map covering all project files and declared external artifacts, following `scripts/validation_gate.py` exclusions;
- `checks`: one result per plan check, containing `id`, `status`, `observed`, `evidencePath`, `evidenceSha256`.

Hash bytes after finishing checks. Excluded review outputs are the report itself, `evidence/RELEASE_CHECKLIST.md` and `evidence/validation-runs/`; generated dependency/cache directories are also excluded. Validation logs are individually hash-checked through the report. Every other project file, including tests and the plan, is included. Add shared dependencies outside the project to `artifactPaths`. A PDF must be present. Do not include credentials or private inputs in public evidence.

Run `python scripts/validation_gate.py` through the release-stage state check. `ws_state.py transition --to RELEASE_READY --next-action "..."` rejects missing, failed, same-builder or stale evidence. CI's archive check applies the same gate even if someone edits the state JSON directly. After any implementation, fixture, test, plan, PDF or covered dependency changes, send the new candidate back to the validator and regenerate the report. Use REPAIRING -> VERIFYING for the recheck; preserve previous failed reports in the validation-runs history.

This gate validates evidence structure, declared role separation and exact file hashes. It cannot authenticate agent identity or judge screenshot quality; the recorded orchestration and independent agent remain essential. It does not run arbitrary commands from JSON. Project test commands must actually be executed by the validator and be wired into CI when appropriate. Publication and hosting approval remain separate from passing validation.
