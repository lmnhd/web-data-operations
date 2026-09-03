# Source Control and Public Archive Policy

## Objective

Create an honest, navigable GitHub archive that lets an Upwork client, interviewer, or technical reviewer understand:

- which projects were shipped;
- why each project was selected;
- how the shared Shipping Pipeline evolved;
- how agents divided and handed off work;
- what a human approved;
- which code and evidence were independently verified;
- exactly which release the public claims describe.

## Canonical locations

- **Canonical implementation archive:** `https://github.com/lmnhd/web-data-operations`
- **Presentation site source:** `https://github.com/lmnhd/halimede-web`
- **Public portfolio:** link each selected project from the presentation site to its project README, Manifest, demo, and GitHub Release.

The implementation archive was created and verified on 2026-09-02. Agents must still confirm the configured remote and active branch during preflight rather than relying on this statement alone.

## Mandatory agent preflight

Before modifying files, every writing agent must:

1. Read the root README, tracking log, active iteration brief, and this policy.
2. Confirm the active iteration ID and assigned role.
3. Inspect repository status, current branch, remote, and outstanding changes.
4. Preserve unrelated user or agent work.
5. Check the active-work table for file or scope collisions.
6. Record the intended files and output in the tracking log.
7. Work only on the assigned branch or worktree.

If the working tree contains unexplained overlapping changes, stop and ask the orchestrator to resolve ownership. Never discard, reset, overwrite, or force-push another contributor's work.

## Branch and integration model

Use the following naming model:

```text
main
iteration/ws-001-<project-slug>
agent/ws-001-<role-or-bounded-task>
```

- `main` contains only reviewed, coherent portfolio state.
- The orchestrator owns the iteration branch and integrates verified agent work.
- Concurrent writing agents use separate feature branches or worktrees.
- Each feature branch changes a bounded area and returns a handoff to the orchestrator.
- Agents do not push directly to `main`.
- A completed iteration reaches `main` through a reviewed pull request.
- Never rewrite or force-push public release history.

For a very small, single-writer documentation change, the orchestrator may work directly on the iteration branch. The release and verification gates still apply.

## Commit requirements

Commits should be small enough to review and should state the outcome rather than the activity. Include trailers when agent-assisted work is material:

```text
Iteration: WS-001
Agent-Role: source-compliance
Human-Approval: pending
```

Use the configured human Git identity. The trailers document assistance and responsibility boundaries; they do not claim that an artificial agent is a legal contributor or independent account holder.

Do not commit:

- API keys, tokens, cookies, credentials, or local environment files;
- private client lists or proprietary source data;
- raw captures whose publication is restricted;
- personal data not explicitly approved for the public example;
- large generated caches, browser profiles, or machine-specific artifacts;
- benchmark claims without their reproducible evidence.

Public examples must be sanitized and accompanied by source/provenance notes where applicable.

## Pull-request handoff

Every iteration pull request must include:

- iteration ID and target buyer problem;
- approved scope and explicit non-goals;
- novelty versus existing portfolio projects;
- Manifest link;
- architecture and source/compliance links;
- tests and benchmark commands executed;
- measured results and evidence locations;
- agent-role and human-approval summary;
- known limitations and manual-review boundaries;
- screenshots or demonstration links when relevant;
- release readiness or remaining blockers.

Agent feature branches may use shorter pull requests, but each must identify changed files, validation performed, unresolved risks, and the expected orchestrator integration point.

## Automated gates

The default branch and release workflow should eventually require:

- formatting, linting, type checking, and tests appropriate to the project;
- deterministic fixture-based parser tests;
- secret scanning and dependency review;
- checks that released projects contain a Manifest and required artifacts;
- checks that no required Manifest field remains `TBD` at release;
- benchmark artifact and link validation;
- build verification for reviewer-facing documentation or demos.

Do not add ceremonial checks that do not test real project behavior. Record each verified gate in the shared capability ledger.

## Release model

Use immutable iteration-specific tags:

```text
ws-001-v1.0.0
ws-002-v1.0.0
```

A GitHub Release should contain or link to:

- the Project Manifest;
- the reviewer README and five-minute walkthrough;
- the three-page PDF work sample;
- sanitized example input and output;
- benchmark/run report;
- demonstration link;
- exact commit and reproduction instructions;
- limitations and compliance statement.

Later fixes receive a new semantic version. Do not silently replace released evidence.

## Reviewer-facing archive rules

The root page should optimize for a reviewer with five minutes:

1. State what the collection demonstrates.
2. Show a compact table of released projects and buyer outcomes.
3. Link directly to each Manifest, demo, proof, and release.
4. Explain the Shipping Pipeline without requiring the reviewer to read internal coordination logs.
5. Separate released work from experiments and future concepts.
6. Keep the default branch polished; preserve detailed history in pull requests, manifests, releases, and the tracking log.

Pin the strongest project repositories or archive on the `lmnhd` GitHub profile when appropriate. The portfolio site should link to specific project evidence, not merely to the account homepage.

## Release approval checklist

- [ ] Iteration pull request is reviewed and integrated into `main`.
- [ ] Required automated gates pass on the final commit.
- [ ] Manifest matches the released implementation and recorded decisions.
- [ ] Public example data is sanitized and publication-safe.
- [ ] Quantitative claims link to reproducible evidence.
- [ ] GitHub Release and immutable tag identify the exact reviewed commit.
- [ ] Links work while signed out of GitHub and the product demo.
- [ ] Tracking log contains the final handoff, release, and retrospective.
- [ ] `halimede-web` links to the specific reviewer entry point when the project is selected for the public portfolio.
