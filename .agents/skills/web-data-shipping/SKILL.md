---
name: web-data-shipping
description: Select, build, verify, and release distinct web-data portfolio projects through the repository's bounded multi-agent Shipping Pipeline. Use for WS iteration planning, portfolio concept gates, vertical proofs, project builds, verification, manifests, or releases in this repository.
---

# Web Data Shipping

Ship credible portfolio evidence with bounded agent use. Optimize for a small verified release, not exhaustive pre-build debate.

## Start here

1. Run `python .agents/skills/web-data-shipping/scripts/ws_state.py show`.
2. Read `ACTIVE_ITERATION.json` and only the files named in its `requiredFiles` list.
3. Read the full tracking log only when resolving a referenced historical claim or collision. Do not send the whole log to every agent.
4. Confirm the current stage, authorized scope, next action, and remaining delegated-turn budget.
5. Preserve unrelated working-tree changes and follow `SOURCE_CONTROL_AND_PUBLIC_ARCHIVE.md`.
6. For new iteration planning, build verification or release, read `docs/shipping-pipeline/REVIEWER_EVIDENCE_STANDARD.md` from the repository root. Add it to the new active state's `requiredFiles` and carry its runnable-demo, visual-PDF and creative-problem-solving requirements into the brief. Use `START_NEXT_ITERATION.md` when initializing a new iteration.

## Operating rules

- The root agent owns the decision and integration. Delegated agents receive one bounded question and the minimum evidence packet.
- Default to no delegation for mechanical inspection, state transitions or file assembly. Release validation always requires a separate non-builder agent.
- Use at most two research agents in parallel during discovery, one consolidated critic, three bounded build agents, and one independent verifier per iteration. The active-state budget is authoritative. More delegation requires explicit human approval.
- Do not create separate agents to restate another agent's answer, rewrite logs, or perform mechanical schema checks.
- Use deterministic scripts for state, scoring arithmetic, schema validation, fixture comparison, and release checks.
- Allow one repair pass after review. If material blockers remain, return a concise human decision instead of automatically promoting another candidate.
- Never promote a runner-up automatically.
- Build the smallest end-to-end vertical proof before producing extensive design or marketing documents.

## Decision standard

Read [references/decision-gates.md](references/decision-gates.md) when selecting, repairing, approving, or rejecting a concept.

Only these are fatal before a vertical proof:

- the required access is prohibited or depends on bypassing controls;
- no lawful and usable source/data path exists;
- no recognizable buyer problem or operational output exists;
- the central claim cannot be tested honestly even on a bounded fixture;
- the concept materially duplicates a **released** project without a new buyer outcome or capability.

Record other weaknesses as repairable conditions or limitations. Missing optional features, undocumented numeric rate ceilings, overlap with rejected concepts, and a metric needing redefinition are not automatically fatal when a conservative lawful scope exists.

## Stage behavior

### Discovery

- Ground the concept in actual buyer evidence when available.
- Compare no more than three candidates in one pass.
- Check source permission before detailed design.
- Use one critic to classify findings as `fatal`, `repairable`, or `limitation`.
- Human approval selects the concept; a score never does so automatically.

### Approved vertical proof

- Implement one complete path from permitted acquisition or fixture through provenance, normalization, validation, and useful output.
- Use bounded sample data and fixed conservative access. Never probe a service to discover its limit.
- Verify the central claim before expanding scope.
- Stop after the proof and present observed results for the next decision.

### Build and verification

- Expand only from a passing vertical proof.
- Follow `docs/shipping-pipeline/INDEPENDENT_VALIDATION.md` from planning through release: freeze acceptance checks, reserve validator/recheck budget, and dispatch a fresh-context non-builder validator. No same-agent exception satisfies this gate.
- Metrics remain `TBD` until a recorded run produces them.
- Treat adversarial findings as severity-classified issues, not automatic rejection votes.

### Release

- Require the artifact-linked `evidence/RELEASE_CHECKLIST.md` specified by the reviewer evidence standard. State validation alone does not certify the PDF, demo or publication.
- Require a completed Manifest, reproducible evidence, sanitized public data, passing checks, reviewed default-branch integration, and a release tag.
- Verify reviewer links while signed out.
- Append the durable outcome to the tracking log, then reset `ACTIVE_ITERATION.json` for the next iteration.

## State changes

Use `ws_state.py validate` before work and after edits. Use `ws_state.py transition --to <stage> --next-action "..."` only when the transition is authorized. The script enforces legal transitions but does not grant approval; record human approval in the active state first.

The legacy `.claude/workflows/` scripts are historical input only. Do not run them unless the human explicitly requests a comparison or rollback.
