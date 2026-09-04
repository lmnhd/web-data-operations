# Shipping Pipeline Workflows

> **PAUSED LEGACY WORKFLOW (2026-09-03):** Do not run these scripts by default. They are preserved as process evidence, but their repeated multi-agent adversarial loops proved too costly and rejection-oriented for routine portfolio delivery. The active Codex workflow is `.agents/skills/web-data-shipping/SKILL.md`, governed by `ACTIVE_ITERATION.json`. Run this legacy implementation only on explicit human request.

Executable implementation of the multi-agent Shipping Pipeline defined in the root
`README.md`. Pipeline state and decisions live in repository files, not in conversation
history, so any capable agent system can resume the work.

## The two runs

The pipeline splits at the one boundary the root README reserves for a human:
`AWAITING_APPROVAL -> APPROVED`. Only the orchestrator may cross an approval boundary,
so it is a run boundary rather than a mid-run stall.

| | Script | Covers | Ends at |
|---|---|---|---|
| Run 1 | `ws-discovery.js` | preflight, demand evidence, candidates, compliance, uniqueness gate | `AWAITING_APPROVAL` |
| Run 2 | `ws-build.js` | design contracts, vertical proof, build, verification, evidence, Manifest | `RELEASE_READY` |

```text
Run 1  Preflight -> Demand -> Candidates -> Gate -> Handoff
                                                      |
                                            [ HUMAN APPROVAL ]
                                                      |
Run 2  Preflight -> Design -> Vertical proof -> Build -> Verify -> Evidence -> Release
```

## Running

```text
Workflow({ scriptPath: ".claude/workflows/ws-discovery.js",
           args: { iteration: "WS-001", today: "<UTC date>" } })
```

Then review `iterations/ws-001/ITERATION_BRIEF.md`, set the status to `APPROVED` in
`PORTFOLIO_TRACKING_LOG.md`, and run:

```text
Workflow({ scriptPath: ".claude/workflows/ws-build.js",
           args: { iteration: "WS-001", today: "<UTC date>" } })
```

`args`: `iteration` (default `WS-001`), `today` (UTC date string — scripts cannot call
`Date.now()`), `repo` (absolute path), and for Run 2 `allowPublish` (default `false`).

To resume after a stop or a script edit, relaunch with the same `scriptPath` plus
`resumeFromRunId`. Unchanged agent calls return cached results; only the edited call and
everything after it re-runs.

## Hard stops

Both runs halt rather than degrade. Each returns a `stopped` code and the action needed:

- `PREFLIGHT_BLOCKED` — work conflicts with the log or branch ownership
- `NO_DEMAND_EVIDENCE` — no real signals found; approving anyway would mean fabricating demand
- `ALL_CANDIDATES_FAILED` — no candidate completed develop → compliance → score
- `NOT_APPROVED` — Run 2 refuses to build work that is not recorded as `APPROVED`
- `COMPLIANCE_BLOCKER` — an approved source prohibits the planned collection
- `VERTICAL_PROOF_FAILED` / `INTEGRATION_FAILED` — the code does not actually run
- `BLOCKERS_UNRESOLVED` — blockers survived two repair rounds

## How the governance is enforced

Every agent receives a shared preflight prompt carrying the mandatory reading list and the
non-negotiable rules: no fabricated metrics or demand data, unmeasured values stay `TBD`,
no access-control bypass, no secrets or personal data, surgical edits that preserve
superseded decisions, and no git write operations unless explicitly authorized.

Structural enforcement beyond the prompt:

- **Approval gate** — Run 2's first agent sets `approved=true` only on a literal recorded
  `APPROVED`; anything else returns `NOT_APPROVED` before any build agent spawns.
- **Independent verification** — five verification dimensions run on a stronger model and
  are told to treat build-agent reports as unverified.
- **Adversarial passes** — three refutation lenses on the concept (novelty, compliance,
  provability) defaulting to refuted-when-uncertain; a majority refutation promotes the
  runner-up. A release integrity audit hunts specifically for untraceable claims.
- **Claim discipline** — the proof spec is written with every metric as `TBD`; a `claims`
  verification dimension lists unsupported claims and the repair loop removes them.
- **Evidence fact-check** — each evidence artifact is drafted, then checked against the
  repository by a separate agent before it reaches the Manifest.

## Model tiering

Minimum viable model per task, since the pipeline runs iteratively:

| Tier | Work |
|---|---|
| `haiku` | preflight, approval check — mechanical reads |
| `sonnet` | research, scoring, design docs, build, evidence, log updates |
| `opus` | uniqueness gate, adversarial refutation, verification, Manifest, release audit |

Opus is reserved for the points where a wrong call is expensive: approving a duplicate
concept, or letting an unsupported claim reach a reviewer.

## Concurrency

Build agents use `isolation: 'worktree'` because four of them mutate project files
concurrently. Files that must stay coherent under a single writer — the tracking log,
integration, the Manifest — are sequential by construction.
