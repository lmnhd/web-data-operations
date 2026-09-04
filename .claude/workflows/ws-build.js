export const meta = {
  name: 'ws-build',
  description: 'WS Shipping Pipeline Run 2: post-approval design, vertical proof, integrated build, independent verification, evidence package and release-ready handoff',
  phases: [
    { title: 'Preflight', detail: 'Confirm APPROVED status and read the iteration brief', model: 'haiku' },
    { title: 'Design', detail: 'Compliance ledger, data contract, architecture, proof spec in parallel', model: 'sonnet' },
    { title: 'Vertical proof', detail: 'Smallest end-to-end slice: collect through verified delivery', model: 'sonnet' },
    { title: 'Build', detail: 'Bounded collectors, parsers, quality stages, exports, operator report', model: 'sonnet' },
    { title: 'Verify', detail: 'Independent testing, benchmark run, adversarial claim audit', model: 'opus' },
    { title: 'Evidence', detail: 'Storyboard, diagram, sanitized examples, run report', model: 'sonnet' },
    { title: 'Release', detail: 'Manifest assembly, integrity audit, tracking-log close', model: 'opus' },
  ],
}

const REPO = String((args && args.repo) || 'c:/Users/cclem/Dropbox/Source/Halimede_Concepts/Upwork/Web_Scraping_Data_Operations')
const TODAY = String((args && args.today) || '2026-09-02')
const ITER = String((args && args.iteration) || 'WS-001')
const ITER_LC = ITER.toLowerCase()
// Set args.allowPublish = true only when you have authorized push/PR/tag.
const ALLOW_PUBLISH = !!(args && args.allowPublish)

const PREFLIGHT = `
You are an agent in the Web Scraping & Data Operations multi-agent Shipping Pipeline.
Repository root: ${REPO}
Active iteration: ${ITER}. Today's UTC date: ${TODAY}.

MANDATORY PREFLIGHT (README.md "Global tracking log - mandatory preflight"):
Before writing anything, read in the repo root:
  README.md, PORTFOLIO_TRACKING_LOG.md, SOURCE_CONTROL_AND_PUBLIC_ARCHIVE.md,
  PROJECT_MANIFEST_TEMPLATE.md, PHASE_01_DISCOVERY_AND_EVIDENCE_PLAN.md,
  and iterations/${ITER_LC}/ITERATION_BRIEF.md (the APPROVED scope).
These outrank your own instincts about how to do the work.

NON-NEGOTIABLE RULES:
- The approved scope in the ITERATION_BRIEF is binding. You may not silently change the
  approved business outcome, expand scope, or substitute a different source or buyer.
  If the approved scope is unworkable, STOP and report the conflict.
- Never fabricate metrics, dates, URLs, run results, test outcomes, or agent activity.
  Anything not produced by a real run stays literally "TBD".
- No performance, accuracy, completeness, or scale claim may exist without a recorded run.
- Never bypass authentication, defeat CAPTCHAs, evade access controls, or collect
  restricted personal data.
- Never commit secrets, credentials, private client data, restricted raw captures,
  personal data, or large generated caches.
- Preserve existing content. Edit surgically; never rewrite history or delete
  superseded decisions from the tracking log.
${ALLOW_PUBLISH ? '- Publishing is authorized this run, but you still must not force-push or rewrite public history.' : '- Do NOT run git commit, git push, git tag, or gh. Publishing is NOT authorized this run.'}
- Your final message IS your return value. Return data, not conversational filler.
`

// ---------------------------------------------------------------------------
// Schemas
// ---------------------------------------------------------------------------
const APPROVAL_SCHEMA = {
  type: 'object',
  required: ['status', 'approved', 'concept', 'slug'],
  properties: {
    status: { type: 'string', description: 'the recorded status of the iteration in the tracking log' },
    approved: { type: 'boolean', description: 'true ONLY if the log/brief records APPROVED' },
    concept: { type: 'string' },
    slug: { type: 'string', description: 'kebab-case project slug' },
    targetBuyer: { type: 'string' },
    approvedScope: { type: 'string' },
    nonGoals: { type: 'array', items: { type: 'string' } },
    verticalProofScope: { type: 'string' },
    sources: { type: 'array', items: { type: 'string' } },
    branch: { type: 'string' },
    blockers: { type: 'array', items: { type: 'string' } },
  },
}

const WRITE_SCHEMA = {
  type: 'object',
  required: ['filesWritten', 'summary'],
  properties: {
    filesWritten: { type: 'array', items: { type: 'string' } },
    summary: { type: 'string' },
    decisions: { type: 'array', items: { type: 'string' }, description: 'material decisions made, for the Manifest development history' },
    tbdFieldsRemaining: { type: 'array', items: { type: 'string' } },
    risks: { type: 'array', items: { type: 'string' } },
  },
}

const BUILD_SCHEMA = {
  type: 'object',
  required: ['filesWritten', 'summary', 'worked'],
  properties: {
    filesWritten: { type: 'array', items: { type: 'string' } },
    summary: { type: 'string' },
    worked: { type: 'boolean', description: 'false if you could not produce running code' },
    commandsRun: { type: 'array', items: { type: 'string' } },
    observedOutput: { type: 'string', description: 'ACTUAL output you saw. Never invent this.' },
    decisions: { type: 'array', items: { type: 'string' } },
    blockers: { type: 'array', items: { type: 'string' } },
  },
}

const VERIFY_SCHEMA = {
  type: 'object',
  required: ['dimension', 'passed', 'findings'],
  properties: {
    dimension: { type: 'string' },
    passed: { type: 'boolean' },
    commandsRun: { type: 'array', items: { type: 'string' } },
    observedOutput: { type: 'string' },
    findings: {
      type: 'array',
      items: {
        type: 'object',
        required: ['severity', 'summary', 'evidence'],
        properties: {
          severity: { type: 'string', enum: ['BLOCKER', 'MAJOR', 'MINOR'] },
          summary: { type: 'string' },
          evidence: { type: 'string' },
          file: { type: 'string' },
        },
      },
    },
    unsupportedClaims: { type: 'array', items: { type: 'string' }, description: 'claims in docs not backed by a recorded run' },
  },
}

const AUDIT_SCHEMA = {
  type: 'object',
  required: ['releaseReady', 'checklist', 'blockers'],
  properties: {
    releaseReady: { type: 'boolean' },
    checklist: {
      type: 'array',
      items: {
        type: 'object',
        required: ['item', 'state'],
        properties: {
          item: { type: 'string' },
          state: { type: 'string', enum: ['PASS', 'FAIL', 'NOT_APPLICABLE'] },
          evidence: { type: 'string' },
        },
      },
    },
    blockers: { type: 'array', items: { type: 'string' } },
    fabricationsFound: { type: 'array', items: { type: 'string' }, description: 'any claim, metric, or history entry not supported by repository evidence' },
  },
}

// ---------------------------------------------------------------------------
// Phase 1 - Preflight. Hard gate: refuse to build unapproved work.
// ---------------------------------------------------------------------------
phase('Preflight')
log('Confirming approval status and reading the approved iteration brief...')

const appr = await agent(`${PREFLIGHT}

TASK: Confirm that ${ITER} is APPROVED and extract the approved scope.

1. Read iterations/${ITER_LC}/ITERATION_BRIEF.md and PORTFOLIO_TRACKING_LOG.md.
2. Determine the recorded status of ${ITER}.
3. Set approved=true ONLY if the status is literally APPROVED in the tracking log
   catalog or the iteration brief. AWAITING_APPROVAL is NOT approved. Do not infer
   approval from enthusiasm, from the presence of a brief, or from a scorecard
   recommendation. The README states only the orchestrator may cross this boundary.
4. Extract the approved scope, explicit non-goals, vertical-proof scope, target buyer,
   named sources, and a kebab-case project slug.
5. Run read-only: git -C "${REPO}" status --short && git -C "${REPO}" branch --show-current

Do not write files.`, {
  label: 'approval-check',
  phase: 'Preflight',
  model: 'haiku',
  effort: 'low',
  schema: APPROVAL_SCHEMA,
})

if (!appr) return { stopped: 'PREFLIGHT_FAILED', action: 'Approval-check agent returned nothing. Re-run.' }
if (!appr.approved) {
  log(`HALT: ${ITER} is "${appr.status}", not APPROVED.`)
  return {
    stopped: 'NOT_APPROVED',
    status: appr.status,
    action: `Run 2 builds only APPROVED work. Review iterations/${ITER_LC}/ITERATION_BRIEF.md, then set ${ITER} to APPROVED in PORTFOLIO_TRACKING_LOG.md and re-run.`,
    blockers: appr.blockers,
  }
}

const SLUG = appr.slug
const PROJ = `projects/${ITER}-${SLUG}`
const CTX = `
APPROVED CONCEPT: ${appr.concept}
TARGET BUYER: ${appr.targetBuyer}
APPROVED SCOPE: ${appr.approvedScope}
EXPLICIT NON-GOALS: ${JSON.stringify(appr.nonGoals || [])}
VERTICAL PROOF SCOPE: ${appr.verticalProofScope}
NAMED SOURCES: ${JSON.stringify(appr.sources || [])}
PROJECT DIRECTORY: ${REPO}/${PROJ}
`
log(`Approved: "${appr.concept}" -> ${PROJ}`)

// ---------------------------------------------------------------------------
// Phase 2 - Design. Barrier IS correct: the build needs all four contracts
// together, and the architecture must reconcile with the data contract.
// ---------------------------------------------------------------------------
phase('Design')
log('Drafting compliance ledger, data contract, architecture brief, and proof spec...')

const DESIGN_DOCS = [
  {
    key: 'compliance',
    role: 'Source and compliance agent',
    path: `iterations/${ITER_LC}/SOURCE_AND_COMPLIANCE_LEDGER.md`,
    body: `Produce the ledger required by PHASE_01 workstream 3. For EVERY source in the
approved scope record: public URL and owner; data fields needed; whether an official API,
feed, export, or downloadable document exists; robots.txt guidance; relevant published
access terms; authentication, paywall, personal-data, or account restrictions; reasonable
request frequency and caching policy; attribution or retention requirements; and the
allowed fallback if collection becomes unavailable.

Actually fetch robots.txt and the terms page for each source — load WebSearch/WebFetch via
ToolSearch ("select:WebSearch,WebFetch"). State per source whether you VERIFIED by fetching
or are INFERRING. Add a "## Refusals" section listing what this project deliberately will
NOT collect or automate (the README success standard requires this to be visible).

If any approved source turns out to prohibit the planned collection, say so as a BLOCKER
in risks rather than quietly working around it.`,
  },
  {
    key: 'data-contract',
    role: 'Data and architecture agent',
    path: `iterations/${ITER_LC}/DATA_CONTRACT.md`,
    body: `Produce the data contract required by PHASE_01 workstream 4: canonical identifier
and entity-matching keys; raw, normalized, and derived fields; required vs optional fields;
source URL, retrieval time, content fingerprint, and extraction method; field confidence and
conflict-handling rules; duplicate and version semantics; accepted/rejected/manual-review
states; export formats and deterministic sorting.

Include sanitized example records (raw, normalized, and a conflict case) as fenced JSON.
Keep raw evidence strictly separate from normalized and inferred values. State explicitly
that a source fact is never silently replaced by an AI-generated guess, and specify how
any AI-assisted field is labeled and bounded.`,
  },
  {
    key: 'architecture',
    role: 'Data and architecture agent',
    path: `iterations/${ITER_LC}/ARCHITECTURE_BRIEF.md`,
    body: `Produce the architecture brief required by PHASE_01 workstream 6, following the
pipeline shape: source registry -> compliant fetchers -> immutable raw capture -> parsers ->
normalized records -> validation and entity resolution -> accepted/rejected/review-needed ->
versioned storage and exports -> run report and operator controls.

Specify: configuration-driven source and rule changes, structured logging, safe concurrency,
retry policy, checkpoints, run IDs, and reproducible exports. Name which components are
candidates for packages/ (shared) and which stay project-specific.

Include a Mermaid diagram in a \`\`\`mermaid fence that can be reused in the PDF case study.
Keep it legible — boxes and arrows that a reviewer can follow in thirty seconds.`,
  },
  {
    key: 'proof-spec',
    role: 'Verification and evidence agent',
    path: `iterations/${ITER_LC}/PROOF_AND_BENCHMARK_SPEC.md`,
    body: `Produce the proof spec required by PHASE_01 workstream 5. Define how the system
will be tested and what its portfolio claims may say.

Specify the measurement method for: pages/items attempted, collected, rejected, retried;
successful request and parse rates; required-field completeness; duplicate rate before and
after resolution; number and type of source conflicts; incremental-run change counts;
checkpoint/resume behavior after an INJECTED failure; validation and regression test results;
elapsed time and request volume under the documented rate policy.

Define the ground-truth method: how many records are manually reviewed, by what procedure,
and how extraction/matching quality is scored against them.

EVERY metric value in this document must be the literal string "TBD". This is a spec for
future measurement, not a results document. Add a "## Claim rules" section stating that no
claim may appear in the portfolio until produced by a recorded run.`,
  },
]

const designResults = await parallel(DESIGN_DOCS.map((doc) => () =>
  agent(`${PREFLIGHT}

ROLE: ${doc.role}.
${CTX}

TASK: Write ${REPO}/${doc.path} (create directories as needed).

${doc.body}

Write for a technical reviewer who has five minutes. Concrete beats comprehensive.`, {
    label: `design:${doc.key}`,
    phase: 'Design',
    model: 'sonnet',
    schema: WRITE_SCHEMA,
  })
))

const designOk = designResults.filter(Boolean)
const designRisks = designOk.flatMap((r) => r.risks || [])
log(`Design docs: ${designOk.length}/${DESIGN_DOCS.length} written. ${designRisks.length} risks raised.`)

const complianceResult = designResults[0]
const complianceBlockers = ((complianceResult && complianceResult.risks) || []).filter((r) => /BLOCKER/i.test(r))
if (complianceBlockers.length > 0) {
  log('HALT: the compliance ledger raised a blocking source restriction.')
  return {
    stopped: 'COMPLIANCE_BLOCKER',
    blockers: complianceBlockers,
    filesWritten: designOk.flatMap((r) => r.filesWritten || []),
    action: 'A source in the approved scope prohibits the planned collection. The README requires rejecting such concepts rather than working around them. Revise the approved scope and re-run.',
  }
}

// ---------------------------------------------------------------------------
// Phase 3 - Vertical proof. README: begin with the SMALLEST end-to-end slice.
// Sequential and single-writer: it establishes the skeleton everything extends.
// ---------------------------------------------------------------------------
phase('Vertical proof')
log('Building the smallest end-to-end vertical proof...')

const vertical = await agent(`${PREFLIGHT}

ROLE: Build agent (vertical proof).
${CTX}

TASK: Implement the SMALLEST end-to-end vertical proof in ${REPO}/${PROJ}/.
One source, few records, but genuinely end-to-end: fetch -> raw capture with provenance ->
parse -> normalize -> validate -> export -> run report. The README requires each iteration
to begin here before adding capability.

Read the design docs first: iterations/${ITER_LC}/DATA_CONTRACT.md,
ARCHITECTURE_BRIEF.md, and SOURCE_AND_COMPLIANCE_LEDGER.md. Implement the approved
contracts — do not invent an incompatible local design.

Layout: ${PROJ}/src/, ${PROJ}/tests/, ${PROJ}/examples/, ${PROJ}/evidence/, ${PROJ}/README.md

Requirements:
- Python 3.12, standard library preferred; if you add dependencies, pin them in a
  requirements.txt and keep the set minimal.
- Respect the documented rate policy. Include real delays between requests.
- Persist raw captures with source URL, retrieval timestamp, and content fingerprint.
- Make the run reproducible: a run ID, deterministic export sorting, structured logging.
- Write at least one fixture-based parser test that runs offline.

THEN ACTUALLY RUN IT. Execute the pipeline and the tests. Report the REAL commands you ran
and the REAL output you observed in commandsRun and observedOutput. If it fails, fix it and
run again. If you cannot get it working, set worked=false and explain — do not report
success you did not observe.

Keep example data sanitized and publication-safe.`, {
  label: 'vertical-proof',
  phase: 'Vertical proof',
  model: 'sonnet',
  effort: 'high',
  schema: BUILD_SCHEMA,
})

if (!vertical || !vertical.worked) {
  log('HALT: the vertical proof did not run successfully.')
  return {
    stopped: 'VERTICAL_PROOF_FAILED',
    blockers: (vertical && vertical.blockers) || ['vertical proof agent returned nothing'],
    observedOutput: vertical && vertical.observedOutput,
    filesWritten: (vertical && vertical.filesWritten) || [],
    action: 'The README requires a working end-to-end slice before adding capability. Fix the blockers and re-run with resumeFromRunId to skip completed design work.',
  }
}
log(`Vertical proof running. ${(vertical.filesWritten || []).length} files.`)

// ---------------------------------------------------------------------------
// Phase 4 - Build. Worktree isolation: these agents mutate files in parallel.
// ---------------------------------------------------------------------------
phase('Build')
log('Extending the vertical proof into the integrated build...')

const BUILD_TASKS = [
  {
    key: 'collection',
    body: `Extend collection to the full approved source set: pagination, detail pages, any
JS-rendered source, and any document (PDF) source in scope. Implement retry policy with
backoff, checkpointing, and resume-after-failure. Every fetch records provenance.
Honor the rate policy in the compliance ledger.`,
  },
  {
    key: 'quality',
    body: `Implement the data-quality stages from DATA_CONTRACT.md: normalization, entity
resolution across sources, validation rules, duplicate detection, conflict handling with
field-level confidence, and reason-coded accepted/rejected/review-needed outputs. Every
exclusion carries a machine-readable reason code.`,
  },
  {
    key: 'delivery',
    body: `Implement exports and the operator experience: deterministic CSV/Excel and JSON
exports, a run report summarizing attempted/collected/rejected/retried counts and field
completeness, and the operator-facing review surface described in the architecture brief.
Exports must be byte-stable across identical runs.`,
  },
  {
    key: 'tests',
    body: `Build the test suite: deterministic fixture-based parser tests (no network),
validation and entity-resolution unit tests, an injected-failure test proving
checkpoint/resume works, and an export-determinism test. Add a documented command that
runs the whole suite. Do not write tests that assert on live network results.`,
  },
]

const buildResults = await parallel(BUILD_TASKS.map((task) => () =>
  agent(`${PREFLIGHT}

ROLE: Build agent (${task.key}).
${CTX}

The vertical proof already works in ${REPO}/${PROJ}/. Read it and the design docs
(DATA_CONTRACT.md, ARCHITECTURE_BRIEF.md, SOURCE_AND_COMPLIANCE_LEDGER.md) before writing.
Extend it — do not rewrite it, and do not invent a design incompatible with the contracts.

SCOPE — stay strictly inside this: ${task.body}

Other agents are working on the other areas concurrently. Confine your edits to files in
your area. If you need a change in shared code, make it minimal and note it in decisions.

THEN ACTUALLY RUN what you built and report the REAL commands and REAL observed output.
Set worked=false if you could not get it working. Never report unobserved success.`, {
    label: `build:${task.key}`,
    phase: 'Build',
    model: 'sonnet',
    effort: 'high',
    isolation: 'worktree',
    schema: BUILD_SCHEMA,
  })
))

const buildOk = buildResults.filter(Boolean)
const buildFailed = BUILD_TASKS.filter((t, i) => !buildResults[i] || !buildResults[i].worked).map((t) => t.key)
if (buildFailed.length > 0) log(`NOTE: build tasks reporting failure: ${buildFailed.join(', ')}. Verification will treat these as suspect.`)
log(`Build: ${BUILD_TASKS.length - buildFailed.length}/${BUILD_TASKS.length} tasks working.`)

// Integration is orchestrator-owned per the source-control policy, and must be
// single-writer to reconcile four worktrees' changes.
const integration = await agent(`${PREFLIGHT}

ROLE: Portfolio orchestrator (integration).
${CTX}

Four build agents worked in isolated worktrees on collection, quality, delivery, and tests.
Their changes are now in ${REPO}/${PROJ}/. Reconcile them into one coherent, running system.

TASK:
1. Read the current state of ${PROJ}/ and find integration breaks: duplicated helpers,
   incompatible function signatures, conflicting config, imports that no longer resolve,
   contract drift from DATA_CONTRACT.md.
2. Fix them. Prefer the design-doc contract when two agents disagree.
3. Run the FULL pipeline end-to-end and the FULL test suite.
4. Report the real commands and real output. Set worked=false if the integrated system
   does not run.

Build-agent reports:
${JSON.stringify(buildOk.map((b) => ({ summary: b.summary, decisions: b.decisions, blockers: b.blockers })), null, 1)}
Tasks that reported failure: ${JSON.stringify(buildFailed)}`, {
  label: 'integrate',
  phase: 'Build',
  model: 'sonnet',
  effort: 'high',
  schema: BUILD_SCHEMA,
})

if (!integration || !integration.worked) {
  return {
    stopped: 'INTEGRATION_FAILED',
    blockers: (integration && integration.blockers) || ['integration agent returned nothing'],
    observedOutput: integration && integration.observedOutput,
    action: 'The integrated system does not run. Fix and re-run with resumeFromRunId to reuse completed stages.',
  }
}
log('Integrated system runs end-to-end.')

// ---------------------------------------------------------------------------
// Phase 5 - Verify. Opus, perspective-diverse. The README requires this be
// independent of implementation, and it is where fabrication gets caught.
// ---------------------------------------------------------------------------
phase('Verify')
log('Independent verification across five dimensions...')

const VERIFY_DIMS = [
  { key: 'functional', ask: `Independently exercise the complete path. Run the pipeline yourself from a clean state. Does it actually do what the README and brief claim? Do the exports contain what the data contract specifies? Assume nothing the build agents reported.` },
  { key: 'provenance', ask: `Trace specific output records back to their source. Can EVERY output record be traced to a source URL, retrieval time, and extraction method? Pick concrete records and follow them. The README success standard requires this.` },
  { key: 'resilience', ask: `Attack the failure handling. Inject a failure mid-run (kill it, break the network, corrupt a checkpoint, feed malformed HTML) and verify checkpoint/resume actually works. Verify retries and rate limiting are real, not decorative.` },
  { key: 'reproducibility', ask: `Run the pipeline twice and diff the exports. Are they deterministic? Run the test suite from a clean checkout. Does the documented reproduction command actually work as written? Are dependencies pinned?` },
  { key: 'claims', ask: `Audit every quantitative and qualitative claim in ${PROJ}/README.md, the design docs, and the evidence directory against recorded runs. List in unsupportedClaims EVERY claim not backed by a real recorded run. The README forbids performance, accuracy, completeness, or scale claims without a recorded run, and forbids demonstrations relying on hidden manual repair — check for that too.` },
]

const verifications = await parallel(VERIFY_DIMS.map((dim) => () =>
  agent(`${PREFLIGHT}

ROLE: Verification and evidence agent (dimension: ${dim.key}).
${CTX}

You are INDEPENDENT of the build. Your job is to find what is broken, overstated, or
unproven — not to confirm the build agents' reports. Treat their claims as unverified.

${dim.ask}

Run real commands. Record the REAL commands and REAL output. A finding without evidence
you actually observed is not a finding. Set passed=false if you found any BLOCKER.

Do not fix anything. Report only.`, {
    label: `verify:${dim.key}`,
    phase: 'Verify',
    model: 'opus',
    effort: 'high',
    schema: VERIFY_SCHEMA,
  })
))

const vOk = verifications.filter(Boolean)
const allFindings = vOk.flatMap((v) => (v.findings || []).map((f) => ({ ...f, dimension: v.dimension })))
const blockers = allFindings.filter((f) => f.severity === 'BLOCKER')
const unsupported = vOk.flatMap((v) => v.unsupportedClaims || [])
log(`Verification: ${allFindings.length} findings (${blockers.length} blockers), ${unsupported.length} unsupported claims.`)

// Repair loop, bounded. Blockers must clear before evidence assembly, but an
// endless loop is worse than an honest stop.
let repairRounds = 0
let openBlockers = blockers
while (openBlockers.length > 0 && repairRounds < 2) {
  repairRounds++
  log(`Repair round ${repairRounds}: clearing ${openBlockers.length} blocker(s)...`)

  const repair = await agent(`${PREFLIGHT}

ROLE: Build agent (verified fixes only).
${CTX}

The iteration is in VERIFYING state: the implementation is FROZEN except for verified fixes.
Fix ONLY these blockers. Do not refactor, do not add features, do not expand scope.

BLOCKERS:
${JSON.stringify(openBlockers, null, 1)}

UNSUPPORTED CLAIMS (remove or downgrade the claim; do not invent evidence to support it):
${JSON.stringify(unsupported, null, 1)}

After fixing, run the full pipeline and full test suite. Report real commands and real output.`, {
    label: `repair:round-${repairRounds}`,
    phase: 'Verify',
    model: 'sonnet',
    effort: 'high',
    schema: BUILD_SCHEMA,
  })

  const recheck = await agent(`${PREFLIGHT}

ROLE: Verification and evidence agent (re-verification).
${CTX}

A repair agent claims to have fixed these blockers. Verify INDEPENDENTLY by running the
system yourself. Do not trust the repair report.

CLAIMED FIXED:
${JSON.stringify(openBlockers, null, 1)}
REPAIR REPORT:
${JSON.stringify({ summary: repair && repair.summary, observedOutput: repair && repair.observedOutput }, null, 1)}

Report any blocker that is still open, plus any NEW blocker the repair introduced.`, {
    label: `re-verify:round-${repairRounds}`,
    phase: 'Verify',
    model: 'opus',
    effort: 'high',
    schema: VERIFY_SCHEMA,
  })

  openBlockers = recheck ? (recheck.findings || []).filter((f) => f.severity === 'BLOCKER') : openBlockers
  log(`After round ${repairRounds}: ${openBlockers.length} blocker(s) remain.`)
}

if (openBlockers.length > 0) {
  return {
    stopped: 'BLOCKERS_UNRESOLVED',
    repairRounds,
    blockers: openBlockers,
    allFindings,
    unsupportedClaims: unsupported,
    action: `${openBlockers.length} blocker(s) survived ${repairRounds} repair rounds. The README forbids presenting BUILDING work as completed evidence. Resolve manually, then re-run with resumeFromRunId.`,
  }
}

// ---------------------------------------------------------------------------
// Phase 6 - Evidence. pipeline: each artifact drafts then gets fact-checked
// against the repo independently. No cross-artifact dependency, so no barrier.
// ---------------------------------------------------------------------------
phase('Evidence')
log('Assembling the evidence package...')

const EVIDENCE_ARTIFACTS = [
  { key: 'run-report', path: `${PROJ}/evidence/RUN_REPORT.md`, body: `Record the ACTUAL benchmark run: run ID, execution date ${TODAY}, environment, configuration, and the measured metrics named in PROOF_AND_BENCHMARK_SPEC.md. Run the pipeline to produce these numbers. Any metric you did not measure stays "TBD" — do not estimate. Include the exact reproduction command.` },
  { key: 'storyboard', path: `portfolio/${ITER}_THREE_PAGE_STORYBOARD.md`, body: `Draft the three-page case study per PHASE_01 workstream 7. Page 1 - The result: the business question in one sentence, the operator report, a sample verified output. Page 2 - How it works: the architecture diagram and the important collection and data-quality controls. Page 3 - Proof: real measured metrics from the run report, failure/recovery evidence, tests, and links. Avoid biography, long introductions, and unmeasured superlatives. Every number must come from evidence/RUN_REPORT.md.` },
  { key: 'walkthrough', path: `${PROJ}/README.md`, body: `Write the five-minute technical walkthrough: what business question it answers, which sources and methods, how it handles pagination/dynamic content/documents/retries/change, how outputs trace to sources, how duplicates and conflicts are handled, what the operator can review/rerun/export/audit, and what it deliberately refuses to collect. Include the exact run and test commands. This is a reviewer's entry point, not a tutorial.` },
  { key: 'examples', path: `${PROJ}/examples/`, body: `Produce sanitized example input and output datasets. Verify every file is publication-safe: no credentials, no private client data, no personal data about identifiable private individuals, no restricted raw captures. Add an EXAMPLES.md noting provenance and what was sanitized. If you find anything unsafe, remove it and record that in risks.` },
]

const evidenceChains = await pipeline(
  EVIDENCE_ARTIFACTS,

  (art) => agent(`${PREFLIGHT}

ROLE: Release and portfolio agent.
${CTX}

TASK: Produce ${REPO}/${art.path}

${art.body}

Ground everything in what the repository actually contains and what runs actually produced.
Read the verification findings below — do not repeat a claim verification already flagged
as unsupported.

VERIFICATION FINDINGS:
${JSON.stringify(allFindings.filter((f) => f.severity !== 'MINOR'), null, 1)}
PREVIOUSLY UNSUPPORTED CLAIMS (must not reappear):
${JSON.stringify(unsupported, null, 1)}`, {
    label: `evidence:${art.key}`,
    phase: 'Evidence',
    model: 'sonnet',
    schema: WRITE_SCHEMA,
  }),

  (draft, art) => {
    if (!draft) throw new Error(`evidence ${art.key} failed`)
    return agent(`${PREFLIGHT}

ROLE: Verification and evidence agent (fact-check).
${CTX}

Fact-check ${REPO}/${art.path} against the repository. For every factual and quantitative
statement, find the supporting evidence or flag it. Check specifically:
- metrics trace to evidence/RUN_REPORT.md or a recorded run
- links resolve to files that exist
- described behavior matches the actual implementation
- no credentials, private data, or personal data present
- nothing claims RELEASED/VERIFIED status that has not occurred

Fix what you can correct factually (downgrade or remove unsupported claims). Report what
you could not resolve. Do not add new claims.`, {
      label: `factcheck:${art.key}`,
      phase: 'Evidence',
      model: 'sonnet',
      effort: 'high',
      schema: WRITE_SCHEMA,
    })
  },
)

const evidenceOk = evidenceChains.filter(Boolean)
log(`Evidence package: ${evidenceOk.length}/${EVIDENCE_ARTIFACTS.length} artifacts drafted and fact-checked.`)

// ---------------------------------------------------------------------------
// Phase 7 - Release. Manifest, then an adversarial integrity audit, then close.
// ---------------------------------------------------------------------------
phase('Release')
log('Assembling the Project Manifest...')

const manifest = await agent(`${PREFLIGHT}

ROLE: Release and portfolio agent (Manifest assembly).
${CTX}

TASK: Write ${REPO}/${PROJ}/PROJECT_MANIFEST.md using PROJECT_MANIFEST_TEMPLATE.md as the
required baseline. Every required declaration must be present; project-specific sections
may be added but required ones may not be removed.

The Manifest is the reviewer's entry point. It must connect market need, project selection,
implementation decisions, multi-agent development, and verified results in one coherent
declaration.

SOURCES OF TRUTH — assemble from these, do not improvise:
- research/UPWORK_DEMAND_MATRIX.md and research/CANDIDATE_SCORECARD.md (sections 3, 4)
- iterations/${ITER_LC}/ITERATION_BRIEF.md (sections 1, 5, 10)
- iterations/${ITER_LC}/*.md design docs (sections 6, 8)
- ${PROJ}/evidence/RUN_REPORT.md (section 9 — metrics ONLY from here)
- PORTFOLIO_TRACKING_LOG.md (section 7 — agent roles and iteration history)

CRITICAL RULES from the README:
- Distinguish evidence from interpretation.
- You may NOT rewrite history, invent a market rationale after the build, or imply that an
  agent performed work not recorded in the handoff log.
- Section 7's role table must match the tracking log's actual recorded handoffs.
- Do not describe the workflow as autonomous: concept approval was a HUMAN decision. State
  which decisions required human approval.
- Section 9 metrics come only from recorded runs. Anything unmeasured stays "TBD".
- Section 1 Status: set to VERIFYING or RELEASE_READY — NOT RELEASED. ${ALLOW_PUBLISH ? 'Publishing is authorized but the release tag does not exist yet.' : 'The reviewed commit, PR, and release tag do not exist yet; leave those fields TBD.'}
- Record important pivots and abandoned approaches that explain the final design.

VERIFICATION RESULTS:
${JSON.stringify({ findings: allFindings, unsupportedClaims: unsupported, repairRounds }, null, 1)}
EVIDENCE ARTIFACTS:
${JSON.stringify(evidenceOk.map((e) => ({ files: e.filesWritten, tbd: e.tbdFieldsRemaining })), null, 1)}`, {
  label: 'manifest',
  phase: 'Release',
  model: 'opus',
  effort: 'high',
  schema: WRITE_SCHEMA,
})

log('Auditing the Manifest and release readiness adversarially...')

const audit = await agent(`${PREFLIGHT}

ROLE: Portfolio orchestrator (release integrity audit).
${CTX}

Audit ${REPO}/${PROJ}/PROJECT_MANIFEST.md and the whole iteration against BOTH checklists:
the Manifest's own section 13 "Declaration integrity checklist" and the
SOURCE_CONTROL_AND_PUBLIC_ARCHIVE.md "Release approval checklist".

Be adversarial. Your specific job is to catch:
- any metric, date, or result not traceable to a recorded run in the repository
- any agent role or handoff in the Manifest not recorded in PORTFOLIO_TRACKING_LOG.md
- any market rationale that appears to have been written after the build to justify it
- any description of the process as autonomous when concept approval was human
- any claim of RELEASED/VERIFIED status that has not occurred
- any credential, private data, personal data, or restricted capture in the repo
- any required Manifest field still "TBD" that should be filled
- broken internal links

Put anything you cannot trace to repository evidence in fabricationsFound — that list is
the single most important output of this audit.

Also run: python "${REPO}/scripts/validate_archive.py" and report the result.

releaseReady=true only if the project could genuinely be released today${ALLOW_PUBLISH ? '' : ' apart from the publishing steps (commit, PR, tag), which are not authorized this run'}.
Do not fix anything. Report only.`, {
  label: 'release-audit',
  phase: 'Release',
  model: 'opus',
  effort: 'high',
  schema: AUDIT_SCHEMA,
})

const fabrications = (audit && audit.fabricationsFound) || []
if (fabrications.length > 0) log(`WARNING: audit flagged ${fabrications.length} untraceable claim(s).`)

// Final log close, single-writer.
const close = await agent(`${PREFLIGHT}

ROLE: Portfolio orchestrator (tracking-log close).
${CTX}

Update ${REPO}/PORTFOLIO_TRACKING_LOG.md. Edit surgically; PRESERVE ALL EXISTING CONTENT.

1. Portfolio catalog — set ${ITER} Status to ${ALLOW_PUBLISH ? 'RELEASED only if a tag genuinely exists, otherwise VERIFYING' : 'VERIFYING'}, and point Evidence at
   ${PROJ}/PROJECT_MANIFEST.md and ${PROJ}/evidence/RUN_REPORT.md.
2. Active work claims — update the ${ITER} row to reflect completion of build and
   verification and name what remains (${ALLOW_PUBLISH ? 'release tagging' : 'human review, then commit/PR/tag'}).
3. Shared Shipping Pipeline capability ledger — move a capability to VERIFIED ONLY where a
   recorded test or run actually supports it, citing that evidence. Where the run did not
   exercise a capability, leave it PLANNED or IN_PROGRESS. Do not mass-promote.
4. Iteration decision and handoff log — APPEND "### ${TODAY} - ${ITER} build and verification"
   recording: what was built, the measured Shipping Pipeline results the README asks for
   (planned vs completed scope, tasks per role, reusable components added, automated checks
   and benchmark results, defects found before and after the verification gate, blocked or
   rejected paths), the ${repairRounds} repair round(s), and the next decision.
   Record ONLY real repository history. The README forbids manufacturing agent counts,
   cycle-time improvements, autonomy percentages, or productivity claims.
5. Append any audit blockers as open items.

AUDIT RESULT:
${JSON.stringify(audit, null, 1)}
VERIFICATION SUMMARY:
${JSON.stringify({ findings: allFindings.length, blockersResolved: blockers.length, repairRounds }, null, 1)}`, {
  label: 'close-log',
  phase: 'Release',
  model: 'sonnet',
  schema: WRITE_SCHEMA,
})

const allWritten = [...designOk, vertical, ...buildOk, integration, ...evidenceOk, manifest, close]
  .filter(Boolean).flatMap((r) => r.filesWritten || [])

return {
  run: 2,
  iteration: ITER,
  project: PROJ,
  concept: appr.concept,
  status: audit && audit.releaseReady ? 'RELEASE_READY' : 'VERIFYING',
  verification: {
    findings: allFindings.length,
    blockersFound: blockers.length,
    blockersResolved: blockers.length - openBlockers.length,
    repairRounds,
    unsupportedClaimsRemoved: unsupported.length,
  },
  audit: {
    releaseReady: !!(audit && audit.releaseReady),
    blockers: (audit && audit.blockers) || [],
    fabricationsFound: fabrications,
    checklist: (audit && audit.checklist) || [],
  },
  filesWritten: Array.from(new Set(allWritten)),
  publishAuthorized: ALLOW_PUBLISH,
  nextStep: ALLOW_PUBLISH
    ? 'Review the audit, then integrate via reviewed PR and tag the release.'
    : `Review ${PROJ}/PROJECT_MANIFEST.md and the audit findings. To publish, authorize the commit/PR/tag steps explicitly.`,
}
