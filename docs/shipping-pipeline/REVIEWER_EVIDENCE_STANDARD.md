# Reviewer evidence standard

Applies to every new portfolio iteration. This is the acceptance baseline established by the final WS-001 revisions, not an optional presentation enhancement.

## Plan the evidence before building

Include this file in the active state's `requiredFiles` and link it from the approved brief. Define one reviewer-operated scenario, its expected result and one meaningful failure or edge case. Select a candidate that can support executable evidence within the approved scope.

## Required final deliverables

### 1. Runnable demonstration

- Give reviewers a simple way to execute the actual project logic, inspect inputs and results, and export or otherwise inspect the produced artifact. A screenshot, animation, prerecorded video or hard-coded report alone does not satisfy this requirement.
- Show a meaningful input or rule change and its effect, plus an edge case or safe failure. Expose enough source provenance and implementation detail to connect the result to the code.
- Label historical replay, synthetic inputs, live acquisition and production limitations clearly. Recorded fixtures are acceptable when the implementation actually processes them.
- Supply reproducible local launch/test instructions. Plan an accessible public demo on an approved existing host; verify it signed out before claiming public availability. Hosting requires publication approval, and new charges require separate approval. If public hosting is unsuitable, request explicit approval for a reviewer-runnable alternative; retain runnable evidence even if a video is added.

### 2. Visual, plain-English PDF

The first three pages must work as a standalone client-facing case study, separate from the internal continuous-development process:

1. Buyer problem, useful result and an actual screenshot of the working output.
2. Creative problem solving: a real observed obstacle, why the obvious approach failed, the implemented correction and a short annotated code excerpt or diagram.
3. Reproducible proof: measured before/after or contrasting-case results, tests, limitations and a clickable working-demo link with a short try-it-yourself path.

Use project-specific screenshots from recorded executions and short excerpts from the actual implementation. Explain technical terms; avoid dense prose. If there was no major defect, explain a genuine design tradeoff and the tests validating it rather than inventing a dramatic failure.

Reuse `scripts/build_ws001_work_sample.py`, WS-001 screenshots and its final PDF only as structural references when useful. Generate new project-specific artifacts; never overwrite an earlier release or copy its metrics as new evidence.

### 3. Traceable evidence and Manifest

Provide sanitized inputs, output artifacts, test/run records and a Manifest explaining selection, buyer need, implementation, creative decisions, development roles and limitations. Every PDF claim must trace to the same version of the source and evidence used by the demo.

## Verification and release gate

For WS-002 onward, [independent validation](INDEPENDENT_VALIDATION.md) is mandatory. A fresh-context non-builder agent performs the checks and writes the machine-checked report. Human-approved presentation exceptions do not waive role separation or failing functional checks.

Before RELEASE_READY, write `evidence/RELEASE_CHECKLIST.md` in the project with PASS, BLOCKED or explicitly human-approved exception for each deliverable above. Link the exact artifacts and record:

- demo execution, changed-input/rule result, edge case and export checks;
- commands, dates and actual test results, distinguishing independent from same-agent verification;
- visual inspection of every rendered PDF page for legibility, cropping and layout;
- confirmation that screenshots, code excerpts, counts and links match the final implementation;
- local reproducibility and any public-hosting approval still needed.

Before RELEASED, finish signed-out public-link checks or the approved runnable-alternative check, confirm release authorization and actual publication, and record the immutable source release. Pending uploads or hosting are not completed publication. Keep each destination's status explicit.

The state validator and CI enforce the independent report, coverage and unchanged file hashes. The separate validator judges PDF quality and executes demo checks; the scripts cannot make those judgments or authenticate agent identities. Publication still requires direct verification.
