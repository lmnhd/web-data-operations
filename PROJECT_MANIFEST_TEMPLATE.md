# Project Manifest

> This document is the reviewer-facing declaration of why this project was selected, what problem it solves, how it was developed, and what the evidence proves. Replace every `TBD` before release. Delete instructional notes only after their requirements have been satisfied.

## 1. Project identity

- **Iteration ID:** TBD
- **Project name:** TBD
- **Version/release:** TBD
- **Status:** TBD
- **Release date:** TBD
- **Repository/demo:** TBD
- **Reviewed commit:** TBD
- **Pull request:** TBD
- **Release tag:** TBD
- **Primary reviewer audience:** TBD

## 2. Executive declaration

In two or three short paragraphs, state:

1. who experiences the problem;
2. what operational decision or workflow is currently difficult;
3. what this system collects, verifies, and delivers;
4. why the result is materially useful.

Do not begin with technologies or a personal biography.

## 3. Why this project was chosen

### Demand evidence

- Relevant client requests or market signals: TBD
- Recurring requested deliverables: TBD
- Evidence dates and source references: TBD
- Confidence and evidence gaps: TBD

### Portfolio gap

- Capability not already demonstrated: TBD
- Why another project was needed: TBD
- How this complements rather than duplicates prior work: TBD

### Candidate decision

- Concepts compared: TBD
- Scoring criteria used: TBD
- Winning factors: TBD
- Approval decision, approver, and date: TBD
- Link to scorecard and tracking-log decision: TBD

## 4. Alternatives considered

| Alternative | Potential value | Why rejected or deferred | Reconsider when |
|---|---|---|---|
| TBD | TBD | TBD | TBD |

Explain meaningful architectural or product alternatives as well as competing project concepts when they materially affected the result.

## 5. The buyer problem

- **Target buyer/user:** TBD
- **Current workflow:** TBD
- **Operational pain or risk:** TBD
- **Decision enabled by the data:** TBD
- **Definition of a useful outcome:** TBD
- **Consequences of incorrect, incomplete, or stale data:** TBD

## 6. Solution overview

### Inputs and permitted sources

TBD

### Processing sequence

```text
Sources
  -> collection
  -> raw evidence and provenance
  -> parsing and normalization
  -> validation and entity resolution
  -> accepted / rejected / review-needed states
  -> storage, monitoring, and exports
  -> operator decision
```

Replace or extend this diagram with the actual project flow.

### Outputs and operator experience

TBD

### Why this approach solves the problem

Connect each major design choice to an identified buyer need, failure risk, or data-quality requirement. Avoid listing features without explaining their purpose.

## 7. Development Manifest

### Multi-agent roles and human control

| Role/agent | Bounded responsibility | Recorded outputs | Handoff/approval |
|---|---|---|---|
| TBD | TBD | TBD | TBD |

State which decisions required human approval. Do not describe the workflow as autonomous if consequential selection, compliance, architecture, or release decisions were human-controlled.

### Iteration history

| Date/iteration | Planned outcome | Material result or decision | Evidence link |
|---|---|---|---|
| TBD | TBD | TBD | TBD |

### Shared versus project-specific work

- Shipping Pipeline components reused: TBD
- Components introduced by this project: TBD
- Project-specific implementation: TBD
- Changes contributed back to the shared pipeline: TBD

### Important pivots

Record substantial changes in direction, their evidence, and their effect on scope. Do not hide abandoned approaches that explain the final design.

## 8. Technical trust and operating boundaries

- Collection/access policy: TBD
- Provenance model: TBD
- Rate limiting and caching: TBD
- Retry, checkpoint, and resume behavior: TBD
- Duplicate and conflict handling: TBD
- Manual-review triggers: TBD
- Sensitive or restricted data boundaries: TBD
- Behavior when a source or required field is unavailable: TBD

## 9. Proof and measured results

### Benchmark method

- Dataset/run identifier: TBD
- Execution date: TBD
- Ground-truth or manual-review method: TBD
- Environment and configuration: TBD
- Reproduction instructions: TBD

### Results

| Metric | Measured result | Evidence | Interpretation/limit |
|---|---:|---|---|
| TBD | TBD | TBD | TBD |

### Failure and recovery proof

TBD

### Test evidence

TBD

For WS-002 onward, link `evidence/VALIDATION_PLAN.json` and `evidence/INDEPENDENT_VALIDATION.json`, identify builder and separate validator agent IDs, and reference the frozen artifact hashes. Follow the repository's `docs/shipping-pipeline/INDEPENDENT_VALIDATION.md`; same-agent review is not release sign-off.

Every public quantitative claim must trace to an entry in this section or its linked evidence.

## 10. Limitations and non-goals

- Known technical limitations: TBD
- Source or policy fragility: TBD
- Required human review: TBD
- Unsupported scale or environments: TBD
- Explicit non-goals: TBD
- Claims this project does **not** make: TBD

## 11. Reviewer walkthrough

Give a reviewer a short path through the evidence:

1. View the result: TBD
2. Inspect a source-to-output provenance example: TBD
3. Review benchmark and test results: TBD
4. Trigger or watch a failure-recovery example: TBD
5. Examine the most relevant implementation excerpt: TBD

Target a five-minute first review, with deeper evidence available for technical reviewers.

## 12. Contribution to the next iteration

- New reusable capability: TBD
- Shipping Pipeline lesson: TBD
- Measured process improvement, if any: TBD
- Portfolio gap that remains: TBD
- Recommended direction for the next project: TBD

## 13. Declaration integrity checklist

- [ ] The [reviewer evidence standard](../../docs/shipping-pipeline/REVIEWER_EVIDENCE_STANDARD.md) is satisfied and `evidence/RELEASE_CHECKLIST.md` links the runnable demo, rendered-PDF inspection and problem-solving evidence. Resolve this relative link for the final project's location.
- [ ] Project-selection claims match the candidate scorecard and approval record.
- [ ] Demand claims link to dated evidence.
- [ ] Agent roles and handoffs match the global tracking log.
- [ ] Architecture matches the released implementation.
- [ ] Metrics come from recorded reproducible runs.
- [ ] Limitations and compliance boundaries are visible.
- [ ] No private client data or restricted information is exposed.
- [ ] All demonstrations and links work from a reviewer's perspective.
- [ ] The reviewed commit, pull request, automated checks, and release tag are linked.
- [ ] No credentials, private data, restricted raw captures, or machine-specific secrets are present.
- [ ] The project is materially distinct from earlier portfolio items.
- [ ] Human approvals and agentic automation are described accurately.

## 14. Release approval

- **Manifest prepared by:** TBD
- **Evidence verified by:** TBD
- **Release approved by:** TBD
- **Approval date:** TBD
- **Tracking-log entry:** TBD
