# Multi-Agent Web Scraping and Data Operations Portfolio

## Purpose

**Start another project:** use [START_NEXT_ITERATION.md](START_NEXT_ITERATION.md), the reusable project-wide prompt. Every new iteration must meet the [reviewer evidence standard](docs/shipping-pipeline/REVIEWER_EVIDENCE_STANDARD.md): runnable demo, visual plain-English PDF, creative problem-solving evidence and artifact-linked verification. This standard supersedes the looser live-or-recorded demonstration wording below; recordings supplement runnable evidence.

**Released WS-001:** [GitHub release and PDF](https://github.com/lmnhd/web-data-operations/releases/tag/ws-001-v1.0.0) | [Project Manifest](projects/WS-001-qualified-tender-change-intelligence/PROJECT_MANIFEST.md) | [Upwork profile](https://www.upwork.com/freelancers/~010d1d69f81d197489). Published as "Web Data Pipeline: Contract Changes, Qualification & Exports" with the live demo and three-page work sample.

**WS-002 publication candidate:** [Product Recall Match Desk - live demo](https://product-recall-match-desk.vercel.app) | [Project Manifest](projects/WS-002-recall-to-catalog-impact-review/PROJECT_MANIFEST.md). It demonstrates explainable product matching and an explicit ambiguity-review boundary using synthetic catalog rows and a recorded openFDA fixture.

**Try the current project:** [Government Contract Change Monitor - live Proof Lab](https://contract-monitor-proof-lab.vercel.app). Run the real Python pipeline, edit a rule, inspect the difference and export the result. [Source and local launch instructions](projects/WS-001-qualified-tender-change-intelligence/demo/README.md).

Build a continuously expanding collection of employer- and client-facing portfolio projects that prove more than the ability to retrieve web pages. Each project must demonstrate that Nathaniel can design, operate, validate, and explain a dependable data-collection workflow for a real business use case.

The collection is produced through a reusable multi-agent **Shipping Pipeline**. The pipeline is also part of the portfolio evidence: it demonstrates structured agentic development, coordinated handoffs, quality gates, measured delivery, and continuous improvement across multiple releases.

The finished work should support two outcomes:

1. Multiple credible Upwork work samples for intermediate web scraping, data mining, and workflow-automation jobs.
2. A reusable technical foundation that can be adapted into paid client work.
3. A demonstrable agentic workflow for repeatedly taking relevant concepts from demand evidence to verified release.

## Core positioning

> I build traceable web-data pipelines that collect permitted public information, preserve provenance, resolve messy records, detect failures, and deliver verified outputs a business can actually use.

## Success standard

Each portfolio project is successful when a prospective client can quickly verify:

- what business question the system answers;
- which sources and collection methods it uses;
- how it handles pagination, dynamic content, documents, retries, and change;
- how every output record can be traced to its source;
- how duplicates, missing fields, and conflicting facts are handled;
- which quality metrics were measured from real runs;
- what the operator can review, rerun, export, and audit;
- what the system deliberately refuses to collect or automate.

## Portfolio evidence package

The eventual work sample should include:

- a completed `PROJECT_MANIFEST.md` that explains why the project exists and how it was developed;
- a live or recorded product demonstration;
- a public repository or carefully selected code excerpts when appropriate;
- a sanitized example input and output dataset;
- automated test and run-quality results;
- an architecture/workflow diagram;
- a concise PDF case study optimized for Upwork's first-three-page preview.

The first three PDF pages should be reserved for:

1. **Result:** the business problem, finished output, and operator experience.
2. **Architecture:** collection stages, provenance, validation, storage, and export.
3. **Proof:** measured run results, failure handling, tests, and reproducibility.

No performance, accuracy, completeness, or scale claim may appear in the portfolio until it has been produced by a recorded run.

## Project Manifest - mandatory reviewer declaration

Every final project must include a human-readable `PROJECT_MANIFEST.md`. The Manifest is the reviewer's entry point into the project: it connects market need, project selection, implementation decisions, multi-agent development, and verified results in one coherent declaration.

The Manifest must explain:

- **Why this project was chosen:** the demand evidence, portfolio gap, candidate score, and approval decision.
- **Which alternatives were considered:** what was rejected or deferred and why this concept won.
- **Who has the problem:** the target buyer, current workflow, operational pain, and decision the data enables.
- **What the project does:** sources, inputs, processing stages, operator experience, and outputs.
- **How it solves the problem:** the important collection, provenance, normalization, validation, monitoring, and delivery choices.
- **How it was developed:** iteration history, agent roles, major handoffs, human approvals, reused components, and material design changes.
- **What was proven:** reproducible demonstrations, benchmark method, measured results, tests, and recovery evidence.
- **What remains limited:** known gaps, source fragility, manual-review requirements, compliance boundaries, and explicit non-goals.
- **What it contributes next:** reusable Shipping Pipeline capabilities and lessons that guide later iterations.

The Manifest must distinguish evidence from interpretation. It may summarize recorded facts from the tracking log and iteration artifacts, but it may not rewrite history, invent a market rationale after the build, or imply that an agent performed work not recorded in the handoff log.

Use [`PROJECT_MANIFEST_TEMPLATE.md`](./PROJECT_MANIFEST_TEMPLATE.md) as the required baseline. Project-specific sections may be added, but the required declarations may not be removed.

## The Shipping Pipeline

The Shipping Pipeline is a repeatable multi-agent workflow for researching, selecting, building, verifying, and publishing distinct portfolio projects. It should create continuity without turning the collection into a set of cosmetic variations of the same scraper.

```text
Demand signals and prior portfolio state
  -> concept candidates
  -> relevance and uniqueness gate
  -> approved iteration brief
  -> vertical proof
  -> integrated build
  -> independent verification
  -> evidence package and release
  -> tracking-log update and retrospective
  -> next iteration
```

The pipeline may be orchestrated by Claude, Codex, or another capable agent system, but its state and decisions must remain in repository files rather than inside one vendor's conversation history.

### Active Codex workflow

**Mandatory independent validation:** WS-002 onward uses the [separate-validator protocol](docs/shipping-pipeline/INDEPENDENT_VALIDATION.md). A non-builder agent executes predefined checks and reviews the demo/PDF; state transitions and CI reject missing, failed or stale evidence. WS-001 retains its documented historical same-agent verification status.

The active bounded workflow is the repository skill at [`.agents/skills/web-data-shipping/SKILL.md`](./.agents/skills/web-data-shipping/SKILL.md). Agents begin with [`ACTIVE_ITERATION.json`](./ACTIVE_ITERATION.json), not the complete historical tracking log. This keeps current scope, approval, blockers, required evidence, and delegated-turn budget compact.

The earlier `.claude/workflows/` implementation is retained as historical process evidence but paused by default. See [`docs/shipping-pipeline/CODEX_MIGRATION.md`](./docs/shipping-pipeline/CODEX_MIGRATION.md).

## Common source control and public archive

All approved web-data iterations should be developed and released from one domain-focused public repository:

> **Canonical repository:** `https://github.com/lmnhd/web-data-operations`

The repository is the public source of truth for released web-data projects and the evolution of the shared Shipping Pipeline.

Use a monorepo for this track so reviewers can see both the distinct projects and the progressive improvement of the shared Shipping Pipeline. Keep `lmnhd/halimede-web` as the presentation layer that links to selected projects and releases; do not mix the implementation archive into the portfolio website's source tree.

Recommended public layout:

```text
web-data-operations/
  README.md                         # Reviewer landing page and project catalog
  PORTFOLIO_TRACKING_LOG.md         # Durable iteration and decision history
  PROJECT_MANIFEST_TEMPLATE.md
  docs/shipping-pipeline/           # Workflow, governance, and measured evolution
  projects/
    WS-001-<project-slug>/
      README.md                     # Five-minute technical walkthrough
      PROJECT_MANIFEST.md           # Why, how, proof, limits, and history
      src/
      tests/
      examples/                     # Sanitized inputs and outputs only
      evidence/                     # Benchmarks, diagrams, and run reports
  packages/                         # Verified reusable pipeline components
  .github/
    workflows/                      # Test, quality, safety, and release gates
    pull_request_template.md
```

Every writing agent must follow [`SOURCE_CONTROL_AND_PUBLIC_ARCHIVE.md`](./SOURCE_CONTROL_AND_PUBLIC_ARCHIVE.md). The policy requires iteration-linked branches and commits, orchestrator-controlled integration, independent verification, secret/data checks, and tagged releases. A final project cannot enter `RELEASED` unless its Manifest links to the reviewed commit or pull request, passing automation, and immutable release tag.

The public history must be honest. Keep the user's configured Git identity as the accountable author; identify agent assistance through iteration records, pull-request summaries, and commit trailers rather than inventing human contributors or fake agent accounts.

## Global tracking log - mandatory preflight

[`PORTFOLIO_TRACKING_LOG.md`](./PORTFOLIO_TRACKING_LOG.md) is the source of truth for the portfolio program. **Every agent must read it before beginning a new iteration or accepting a major task.**

Before doing work, the agent must:

1. Read this README, the global tracking log, the active iteration brief, and any files linked from that log entry.
2. Read the source-control policy and verify the repository, branch, iteration ID, and clean working state before writing.
3. Check active claims and dependencies so it does not duplicate another agent's work.
4. Compare the proposed concept with completed, active, rejected, and archived concepts.
5. Confirm that the iteration answers a recognizable buyer problem supported by current demand evidence.
6. Complete the relevance and uniqueness gate described below.
7. Obtain or confirm a unique iteration ID and record its role, scope, expected outputs, and status in the log before implementation.
8. If the intended work conflicts with the log, branch ownership, or an existing project, stop and return a revised direction to the orchestrator.

An iteration is not authorized merely because it is technically interesting.

## Relevance and uniqueness gate

Every proposed portfolio item must document:

- **Target buyer:** who would pay for this operation?
- **Operational decision:** what action does the resulting data enable?
- **Demand evidence:** which current postings, requests, or market evidence support it?
- **Source profile:** which permitted source types and access methods are involved?
- **Technical proof:** which difficult collection, normalization, reliability, or delivery problem does it demonstrate?
- **Portfolio gap:** what evidence is missing from the existing collection?
- **Novelty statement:** exactly how this differs from all completed and active projects.
- **Reusable contribution:** what the shared Shipping Pipeline gains from this iteration.

A concept may reuse the common pipeline, but it should normally add at least one net-new technical capability and differ meaningfully from prior projects in at least two of these dimensions:

- buyer or industry problem;
- source and content types;
- extraction difficulty;
- normalization, matching, or validation problem;
- monitoring or change-detection behavior;
- delivery destination and operator workflow;
- benchmark or reliability evidence.

Changing only the website, visual theme, keyword set, or industry label does not make a new portfolio project.

## Multi-agent workflow

One orchestrator owns the iteration outcome and shared architecture. Other agents work in bounded roles and leave evidence-backed handoffs.

### 1. Portfolio orchestrator

- reads the global log and assigns the iteration ID;
- resolves collisions and dependencies;
- enforces approval and quality gates;
- owns integration and the final release decision;
- prevents agents from silently changing the approved business outcome.

### 2. Demand and concept agents

- examine current buyer requests and recurring deliverables;
- generate and score several concepts rather than defending the first idea;
- identify the strongest relevance and differentiation evidence;
- recommend one concept for approval without fabricating demand data.

### 3. Source and compliance agent

- identifies official APIs, downloads, feeds, HTML pages, documents, and dynamic sources;
- records terms, robots guidance, authentication boundaries, rate policies, and fallbacks;
- rejects concepts that depend on bypassing access controls or collecting restricted data.

### 4. Data and architecture agent

- defines raw, normalized, derived, and provenance schemas;
- specifies entity resolution, validation, review states, storage, exports, and observability;
- identifies which components should be shared and which must remain project-specific.

### 5. Build agents

- implement bounded collectors, parsers, quality stages, operator features, and exports;
- work from the approved contracts rather than inventing incompatible local designs;
- update their claimed task and handoff state in the tracking log.

### 6. Verification and evidence agent

- tests the completed path independently;
- runs the benchmark and verifies every public claim;
- checks failure recovery, provenance, output quality, and reproducibility;
- rejects unsupported metrics or demonstrations that rely on hidden manual repair.

### 7. Release and portfolio agent

- assembles the demonstration, sanitized data, diagrams, case study, and Upwork PDF;
- assembles the final Project Manifest from approved decisions and verified iteration evidence;
- gives the first three pages to result, architecture, and proof;
- updates the portfolio catalog and closes the iteration in the tracking log.
- prepares the tagged GitHub release and confirms that public links work for a signed-out reviewer.

Agents may combine roles on a small iteration, but responsibility for implementation and independent verification should remain distinct whenever possible.

## Iteration lifecycle

Use these standard states:

1. `PROPOSED` - recorded but not yet researched.
2. `RESEARCHING` - demand, source, feasibility, and uniqueness evidence is being collected.
3. `AWAITING_APPROVAL` - scorecard and recommendation are ready for human review.
4. `APPROVED` - the concept and a bounded vertical-proof scope are authorized.
5. `PROVING` - the smallest end-to-end proof is being implemented and measured.
6. `AWAITING_BUILD_APPROVAL` - proof results are ready for a human expansion decision.
7. `BUILDING` - the approved portfolio-grade system is being implemented.
8. `REPAIRING` - one bounded correction pass is active.
9. `VERIFYING` - implementation is frozen except for verified fixes.
10. `RELEASE_READY` - evidence is complete and awaiting release authorization.
11. `RELEASED` - the Manifest, evidence package, and reviewer-facing project are complete and published or ready for use.
12. `REJECTED` - concept failed a fatal gate; retain the reason to prevent rediscovery.
13. `ARCHIVED` - previously released or paused work is retained but no longer active.

Only the orchestrator may move an iteration across an approval or release boundary. Agents must not present `BUILDING` work as completed portfolio evidence.

An iteration cannot enter `RELEASED` without a completed Project Manifest reviewed against the tracking log, benchmark evidence, and approval history.

It also cannot enter `RELEASED` from an unreviewed working branch. The final commit must pass the repository's automated gates, be integrated into the default branch, and receive an iteration-specific release tag.

## Continuous-shipping sequence

Build the portfolio progressively:

- **Project 1:** establishes the shared collection, provenance, validation, export, and reporting foundation.
- **Project 2:** proves that the foundation adapts to a materially different source and buyer problem.
- **Project 3:** proves repeatability, monitoring, and operational delivery at a higher level.
- **Later projects:** target documented portfolio gaps and current demand instead of repeating earlier demonstrations.

Each iteration should begin with the smallest end-to-end vertical proof, then add only the capabilities required to create credible evidence. The goal is frequent, defensible releases rather than simultaneous unfinished projects.

## Shipping Pipeline evidence

The workflow itself may become a case study for agentic automation work. Record the following for each iteration when measurable:

- time from proposal to approval;
- time from approval to vertical proof and release;
- planned versus completed scope;
- tasks completed and handed off by each role;
- reusable components added or improved;
- automated checks and benchmark results;
- defects found before and after the verification gate;
- blocked or rejected paths and the decisions that resolved them;
- lessons applied to the next iteration.

These measurements must describe real repository history. Do not manufacture agent counts, cycle-time improvements, autonomy percentages, or productivity claims.

## Required iteration artifacts

Each approved project should eventually contain:

```text
iterations/<iteration-id>/
  ITERATION_BRIEF.md
  PROJECT_MANIFEST.md
  SOURCE_CONTROL_HANDOFF.md
  SOURCE_AND_COMPLIANCE_LEDGER.md
  DATA_CONTRACT.md
  ARCHITECTURE_BRIEF.md
  PROOF_AND_BENCHMARK_SPEC.md
  THREE_PAGE_STORYBOARD.md
  RETROSPECTIVE.md
```

Small projects may combine documents, but they may not omit the underlying decisions, evidence, boundaries, or measured proof.

## Current status

Phase 1 - convert discovery, evidence design, project selection, and delivery into the first tracked multi-agent iteration.

See [PHASE_01_DISCOVERY_AND_EVIDENCE_PLAN.md](./PHASE_01_DISCOVERY_AND_EVIDENCE_PLAN.md).
