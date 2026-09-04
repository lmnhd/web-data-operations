export const meta = {
  name: 'ws-discovery',
  description: 'WS Shipping Pipeline Run 1: preflight, demand evidence, candidate scoring, compliance and uniqueness gates, then stop at AWAITING_APPROVAL',
  phases: [
    { title: 'Preflight', detail: 'Read log + policy, confirm branch/iteration, claim work', model: 'haiku' },
    { title: 'Demand', detail: 'Public, dated, cited demand evidence across four search modes', model: 'sonnet' },
    { title: 'Candidates', detail: 'Three concepts developed and source-feasibility checked in parallel chains', model: 'sonnet' },
    { title: 'Gate', detail: 'Uniqueness/relevance gate and adversarial refutation of the leader', model: 'opus' },
    { title: 'Handoff', detail: 'Scorecard, iteration brief, tracking-log update, approval request', model: 'sonnet' },
  ],
}

// ---------------------------------------------------------------------------
// Shared context. Every agent gets this; the README makes preflight mandatory.
// ---------------------------------------------------------------------------
const REPO = String((args && args.repo) || 'c:/Users/cclem/Dropbox/Source/Halimede_Concepts/Upwork/Web_Scraping_Data_Operations')
const TODAY = String((args && args.today) || '2026-09-02')
const ITER = String((args && args.iteration) || 'WS-001')

const PREFLIGHT = `
You are an agent in the Web Scraping & Data Operations multi-agent Shipping Pipeline.
Repository root: ${REPO}
Active iteration: ${ITER}. Today's UTC date: ${TODAY}.

MANDATORY PREFLIGHT (README.md "Global tracking log - mandatory preflight"):
Before writing anything, read these files in the repo root:
  README.md, PORTFOLIO_TRACKING_LOG.md, SOURCE_CONTROL_AND_PUBLIC_ARCHIVE.md,
  PHASE_01_DISCOVERY_AND_EVIDENCE_PLAN.md, PROJECT_MANIFEST_TEMPLATE.md
Use them as the governing contract. They outrank your own instincts about how to do the work.

NON-NEGOTIABLE RULES:
- Never fabricate demand data, metrics, dates, URLs, benchmark results, or agent activity.
- Anything not yet measured stays literally "TBD". Do not estimate and present it as measured.
- Distinguish evidence (recorded fact) from interpretation (your reading of it).
- Never propose work that bypasses authentication, defeats CAPTCHAs, evades access
  controls, or collects restricted personal data. Reject such concepts outright.
- Preserve existing file content. Append or edit surgically; never rewrite history,
  never delete rejected concepts or superseded decisions from the tracking log.
- Do not run git commit, git push, git tag, or gh. The orchestrator owns integration.
- Your final message IS your return value. Return data, not conversational filler.
`

// ---------------------------------------------------------------------------
// Schemas
// ---------------------------------------------------------------------------
const PREFLIGHT_SCHEMA = {
  type: 'object',
  required: ['branch', 'cleanTree', 'iterationId', 'collisions', 'priorConcepts', 'proceed'],
  properties: {
    branch: { type: 'string' },
    cleanTree: { type: 'boolean' },
    iterationId: { type: 'string' },
    remote: { type: 'string' },
    collisions: { type: 'array', items: { type: 'string' }, description: 'Active work claims that overlap this run' },
    priorConcepts: { type: 'array', items: { type: 'string' }, description: 'Completed/active/rejected/archived concepts found in the log' },
    blockers: { type: 'array', items: { type: 'string' } },
    proceed: { type: 'boolean', description: 'false if the log, branch ownership, or an existing project conflicts' },
    notes: { type: 'string' },
  },
}

const DEMAND_SCHEMA = {
  type: 'object',
  required: ['signals', 'gaps'],
  properties: {
    signals: {
      type: 'array',
      items: {
        type: 'object',
        required: ['deliverable', 'sourceUrl', 'accessedDate', 'evidenceTier'],
        properties: {
          deliverable: { type: 'string' },
          sourceUrl: { type: 'string' },
          accessedDate: { type: 'string' },
          sourceTypes: { type: 'string' },
          toolsRequested: { type: 'string' },
          cadence: { type: 'string', description: 'one-time extraction vs recurring monitoring' },
          volume: { type: 'string' },
          outputDestination: { type: 'string' },
          antibotOrAuthExpectation: { type: 'string' },
          cleaningOrMatchingNeeds: { type: 'string' },
          proofRequestedByClients: { type: 'string' },
          riskySignals: { type: 'string', description: 'signs of prohibited or risky work' },
          evidenceTier: { type: 'string', enum: ['DIRECT_POSTING', 'AGGREGATE_REPORT', 'SECONDARY_COMMENTARY'] },
        },
      },
    },
    gaps: { type: 'array', items: { type: 'string' }, description: 'What this search mode could NOT establish' },
  },
}

const CANDIDATE_SCHEMA = {
  type: 'object',
  required: ['name', 'slug', 'targetBuyer', 'operationalDecision', 'technicalProof', 'portfolioGap', 'noveltyStatement', 'reusableContribution', 'demandRefs'],
  properties: {
    name: { type: 'string' },
    slug: { type: 'string', description: 'kebab-case' },
    targetBuyer: { type: 'string', description: 'who would pay for this operation' },
    operationalDecision: { type: 'string', description: 'what action the resulting data enables' },
    demandRefs: { type: 'array', items: { type: 'string' }, description: 'sourceUrls from the demand matrix supporting this' },
    sourceProfile: { type: 'string' },
    technicalProof: { type: 'string', description: 'the difficult collection/normalization/reliability problem demonstrated' },
    portfolioGap: { type: 'string' },
    noveltyStatement: { type: 'string' },
    reusableContribution: { type: 'string' },
    dimensionsDiffered: { type: 'array', items: { type: 'string' }, description: 'which of the 7 README dimensions this differs on' },
    verticalProofScope: { type: 'string', description: 'the smallest end-to-end vertical proof' },
    explicitNonGoals: { type: 'array', items: { type: 'string' } },
  },
}

const FEASIBILITY_SCHEMA = {
  type: 'object',
  required: ['candidateSlug', 'sources', 'verdict'],
  properties: {
    candidateSlug: { type: 'string' },
    sources: {
      type: 'array',
      items: {
        type: 'object',
        required: ['owner', 'url', 'accessPath', 'permitted'],
        properties: {
          owner: { type: 'string' },
          url: { type: 'string' },
          fieldsNeeded: { type: 'string' },
          accessPath: { type: 'string', enum: ['OFFICIAL_API', 'BULK_DOWNLOAD', 'FEED', 'HTML', 'DOCUMENT', 'DYNAMIC_BROWSER'] },
          robotsGuidance: { type: 'string' },
          publishedTerms: { type: 'string' },
          authOrPaywall: { type: 'string' },
          personalDataExposure: { type: 'string' },
          reasonableFrequency: { type: 'string' },
          attributionOrRetention: { type: 'string' },
          fallbackIfUnavailable: { type: 'string' },
          permitted: { type: 'boolean' },
          verifiedHow: { type: 'string', description: 'Did you actually fetch robots.txt/terms, or is this inference? Say which.' },
        },
      },
    },
    browserAutomationJustification: { type: 'string', description: 'legitimate technical need, NOT access-control bypass' },
    verdict: { type: 'string', enum: ['FEASIBLE', 'FEASIBLE_WITH_CONSTRAINTS', 'NOT_FEASIBLE'] },
    killReasons: { type: 'array', items: { type: 'string' } },
  },
}

const SCORE_SCHEMA = {
  type: 'object',
  required: ['candidateSlug', 'criteria', 'total'],
  properties: {
    candidateSlug: { type: 'string' },
    criteria: {
      type: 'array',
      items: {
        type: 'object',
        required: ['name', 'score', 'rationale'],
        properties: {
          name: { type: 'string' },
          score: { type: 'number', description: '1-5' },
          rationale: { type: 'string' },
        },
      },
      description: 'Exactly the 7 Phase-1 criteria: similarity to paid work; lawful stable sources; difficult extraction/data-quality demonstration; dataset usefulness; measurable results without fabrication; time to convincing first release; reusable-service potential',
    },
    total: { type: 'number' },
    weakestLink: { type: 'string' },
  },
}

const GATE_SCHEMA = {
  type: 'object',
  required: ['candidateSlug', 'passes', 'dimensionsDiffered', 'netNewCapability', 'reasoning'],
  properties: {
    candidateSlug: { type: 'string' },
    passes: { type: 'boolean' },
    dimensionsDiffered: { type: 'array', items: { type: 'string' } },
    netNewCapability: { type: 'string' },
    duplicationRisk: { type: 'string' },
    reasoning: { type: 'string' },
    requiredChanges: { type: 'array', items: { type: 'string' } },
  },
}

const REFUTE_SCHEMA = {
  type: 'object',
  required: ['refuted', 'lens', 'reasoning'],
  properties: {
    refuted: { type: 'boolean' },
    lens: { type: 'string' },
    reasoning: { type: 'string' },
    fatalFlaw: { type: 'string' },
  },
}

const WRITE_SCHEMA = {
  type: 'object',
  required: ['filesWritten', 'summary'],
  properties: {
    filesWritten: { type: 'array', items: { type: 'string' } },
    summary: { type: 'string' },
    tbdFieldsRemaining: { type: 'array', items: { type: 'string' } },
  },
}

// ---------------------------------------------------------------------------
// Phase 1 - Preflight. Mandatory per README; blocks everything downstream.
// ---------------------------------------------------------------------------
phase('Preflight')
log('Reading tracking log, source-control policy, and repository state...')

const pre = await agent(`${PREFLIGHT}

TASK: Perform the mandatory agent preflight for iteration ${ITER}.

1. Read the five governing files listed above.
2. Run: git -C "${REPO}" status --short && git -C "${REPO}" branch --show-current && git -C "${REPO}" remote -v
   (read-only git only; no commit/push/checkout).
3. From PORTFOLIO_TRACKING_LOG.md extract: every concept in the catalog and the
   candidate/duplication register with its state, and every row in "Active work claims".
4. Report collisions: any active claim whose expected outputs overlap
   research/, design/, or portfolio/ files for ${ITER}.
5. Set proceed=false ONLY if there is a genuine conflict of ownership or an
   unexplained dirty working tree containing another contributor's work.

Do not write any files in this task. Report only.`, {
  label: 'preflight',
  phase: 'Preflight',
  model: 'haiku',
  effort: 'low',
  schema: PREFLIGHT_SCHEMA,
})

if (!pre) {
  return { stopped: 'Preflight agent returned no result. Re-run before proceeding.' }
}
if (pre.proceed === false) {
  log(`HALT: preflight blocked. ${(pre.blockers || []).join('; ')}`)
  return {
    stopped: 'PREFLIGHT_BLOCKED',
    branch: pre.branch,
    blockers: pre.blockers,
    collisions: pre.collisions,
    notes: pre.notes,
    action: 'README requires stopping and returning a revised direction to the orchestrator when work conflicts with the log or branch ownership.',
  }
}

log(`Preflight OK on branch "${pre.branch}" (clean=${pre.cleanTree}). ${(pre.priorConcepts || []).length} prior concepts registered.`)

// ---------------------------------------------------------------------------
// Phase 2 - Demand evidence. Multi-modal sweep: four blind search angles.
// Barrier is correct here: candidates must see the FULL matrix, and the
// dedup/synthesis genuinely needs every mode's signals at once.
// ---------------------------------------------------------------------------
phase('Demand')
log('Sweeping public demand evidence across four independent search modes...')

const DEMAND_MODES = [
  {
    key: 'job-boards',
    angle: `Search PUBLICLY VISIBLE freelance job listings for intermediate web scraping / data mining /
workflow automation work. Try Upwork public job-search pages, Freelancer, PeoplePerHour,
Contra, RemoteOK, WeWorkRemotely and similar. Classify what clients ACTUALLY ask to be
delivered, not what technologies are named.`,
  },
  {
    key: 'market-reports',
    angle: `Search dated industry/market reporting on web-data extraction demand: freelance marketplace
skill reports, web-scraping industry surveys, data-vendor category analyses, alternative-data
buyer research. Prefer sources with an explicit publication date.`,
  },
  {
    key: 'practitioner',
    angle: `Search practitioner discussion where buyers describe what they need and what goes wrong:
r/webscraping, r/datasets, r/freelance, Hacker News threads, Stack Overflow question trends,
scraping-tool vendor case studies. Focus on recurring deliverables and recurring failure points.`,
  },
  {
    key: 'procurement',
    angle: `Search for organizations publicly soliciting data-collection, monitoring, or enrichment
services: RFPs, public procurement notices, data-as-a-service product pages, and
competitor/price/location monitoring vendor offerings. These reveal what buyers pay for.`,
  },
]

const demandResults = await parallel(DEMAND_MODES.map((mode) => () =>
  agent(`${PREFLIGHT}

ROLE: Demand and concept agent (search mode: ${mode.key}).

${mode.angle}

METHOD: Use WebSearch and WebFetch. You must load their schemas first via ToolSearch
(query: "select:WebSearch,WebFetch").

For every signal you record you MUST capture a real, working sourceUrl you actually
retrieved, plus the date you accessed it (${TODAY}). Set evidenceTier honestly:
- DIRECT_POSTING: an actual job posting or RFP you read
- AGGREGATE_REPORT: a dated report/survey summarizing demand
- SECONDARY_COMMENTARY: forum/blog discussion

Capture per the Phase 1 plan: source types and access constraints, requested tools and
languages, one-time vs recurring, expected volume and update frequency, output
destinations, anti-bot or auth expectations, cleaning/enrichment/matching requirements,
proof or prior-work evidence clients request, and common failure points or signs of
risky/prohibited work.

CRITICAL: If you cannot find real evidence for a field, leave it empty and record the
limitation in "gaps". Never invent a posting, a URL, a date, or a statistic. An honest
thin result is correct; a rich fabricated one is a total failure of this task.
Do not copy client data or reproduce private job material beyond what analysis requires.
Aim for 6-12 well-evidenced signals. Do not write files.`, {
    label: `demand:${mode.key}`,
    phase: 'Demand',
    model: 'sonnet',
    schema: DEMAND_SCHEMA,
  })
))

const signals = demandResults.filter(Boolean).flatMap((r) => r.signals || [])
const demandGaps = demandResults.filter(Boolean).flatMap((r) => r.gaps || [])
const modesFailed = DEMAND_MODES.length - demandResults.filter(Boolean).length

if (modesFailed > 0) log(`NOTE: ${modesFailed}/${DEMAND_MODES.length} demand search modes returned nothing. Recorded as an evidence gap.`)
log(`Collected ${signals.length} demand signals (${signals.filter((s) => s.evidenceTier === 'DIRECT_POSTING').length} direct postings). ${demandGaps.length} declared gaps.`)

if (signals.length === 0) {
  return {
    stopped: 'NO_DEMAND_EVIDENCE',
    gaps: demandGaps,
    action: 'README forbids approving a concept without demand evidence. Supply real postings in research/raw_postings.md and re-run, or check network/WebSearch availability.',
  }
}

// Persist the matrix before scoring, so the evidence exists in repo files
// independent of this conversation (README: state lives in repository files).
const demandDoc = await agent(`${PREFLIGHT}

ROLE: Demand and concept agent (synthesis + scribe).

Write ${REPO}/research/UPWORK_DEMAND_MATRIX.md from the collected signals below.
Create the research/ directory if needed.

Required structure:
- "# Upwork and Public Demand Matrix"
- "## Evidence tier" — state prominently: PUBLIC-PRELIMINARY. Logged-in Upwork job search
  is not accessible to automated collection. This matrix is built from publicly visible
  postings, dated reports, and practitioner/procurement signals. It may be upgraded to
  VERIFIED-SAMPLE if the operator supplies a real posting sample.
- "## Signals" — a markdown table with columns: Deliverable | Source | Accessed | Tier |
  Cadence | Volume | Output destination | Anti-bot/auth | Cleaning & matching | Proof requested
  Make Source a working markdown link.
- "## Synthesis" — 5-9 bullets on what buyers actually pay for, grouped by recurring
  deliverable. Label each bullet as evidence or interpretation.
- "## Common failure points and risky-work signals"
- "## Evidence gaps" — every declared gap, verbatim, plus the ${modesFailed} search modes
  that returned nothing (if any).

Do not add any signal not present in the data below. Do not invent dates or URLs.

SIGNALS:
${JSON.stringify(signals, null, 1)}

DECLARED GAPS:
${JSON.stringify(demandGaps, null, 1)}`, {
  label: 'write:demand-matrix',
  phase: 'Demand',
  model: 'sonnet',
  schema: WRITE_SCHEMA,
})

log(`Demand matrix written: ${((demandDoc && demandDoc.filesWritten) || []).join(', ') || 'FAILED'}`)

// ---------------------------------------------------------------------------
// Phase 3 - Candidates. pipeline(): each concept flows develop -> feasibility
// -> score independently. Candidate B is scored while C is still fetching
// robots.txt. No barrier needed between these stages.
// ---------------------------------------------------------------------------
phase('Candidates')

const CANDIDATE_SEEDS = [
  {
    key: 'opportunity-intelligence',
    seed: `Public opportunity intelligence: collect and reconcile government or institutional
solicitations, amendments, deadlines, contacts, and attached documents. The tracking log
warns this "may overlap with Local Contract Scouter if framed only as lead discovery" —
it becomes distinct only via solicitation documents, amendments, provenance, deadline
change tracking, and structured qualification.`,
  },
  {
    key: 'location-monitoring',
    seed: `Business-location monitoring: track multi-location business details, services, hours,
and material changes across permitted public sources. The tracking log warns this
"could become a generic directory scraper" — it becomes distinct only via cross-source
entity resolution, operating-detail change detection, conflict review, and scheduled
monitoring.`,
  },
  {
    key: 'price-intelligence',
    seed: `Product and price intelligence: monitor a carefully bounded group of public product
pages for price, availability, specifications, and changes. The tracking log warns this
is a "highly common portfolio category" — it becomes distinct only via variant resolution,
availability history, change alerts, and resilient incremental collection.`,
  },
]

const candidateChains = await pipeline(
  CANDIDATE_SEEDS,

  // Stage 1: develop the concept against real demand evidence.
  (seed) => agent(`${PREFLIGHT}

ROLE: Demand and concept agent (concept development).

Develop this candidate into a fully specified portfolio concept:
${seed.seed}

You must complete every element of the README "Relevance and uniqueness gate":
target buyer, operational decision, demand evidence, source profile, technical proof,
portfolio gap, novelty statement, reusable contribution.

Ground it in the ACTUAL demand signals below. In demandRefs, cite only sourceUrls that
appear in this data. If the evidence does not support this concept, say so plainly in
the novelty statement rather than inflating it — a candidate that loses honestly is
more useful than one that wins by fabrication.

The working hypothesis in PHASE_01 favors a multi-source monitoring and enrichment
pipeline over a single-site scraper. Treat that as a hypothesis to test, not a mandate.

dimensionsDiffered must list which of these 7 README dimensions this differs on versus
completed and active projects: buyer/industry problem; source and content types;
extraction difficulty; normalization/matching/validation problem; monitoring or
change-detection behavior; delivery destination and operator workflow; benchmark or
reliability evidence.

verticalProofScope must be the SMALLEST end-to-end vertical proof — collection through
verified delivery — not the full system.

PRIOR AND ACTIVE CONCEPTS (must not duplicate):
${JSON.stringify(pre.priorConcepts || [], null, 1)}

DEMAND SIGNALS:
${JSON.stringify(signals, null, 1)}

Do not write files.`, {
    label: `concept:${seed.key}`,
    phase: 'Candidates',
    model: 'sonnet',
    schema: CANDIDATE_SCHEMA,
  }),

  // Stage 2: source + compliance feasibility. Real fetches, not assumptions.
  (concept, seed) => {
    if (!concept) throw new Error(`concept ${seed.key} failed`)
    return agent(`${PREFLIGHT}

ROLE: Source and compliance agent.

Assess real-world source feasibility for this candidate:
${JSON.stringify(concept, null, 1)}

METHOD: Load WebSearch and WebFetch via ToolSearch (query: "select:WebSearch,WebFetch").
For each proposed source you MUST attempt to actually retrieve:
  - the site's robots.txt
  - its published terms of use / acceptable use page
  - evidence of an official API, bulk download, or feed
In verifiedHow, state explicitly whether you FETCHED the document or are INFERRING.
Inference is acceptable when clearly labeled; passing inference off as verification is not.

Per PHASE_01 workstream 3, record for every source: public URL and owner, data fields
needed, whether an official API/feed/export/document exists, robots guidance, published
access terms, auth/paywall/personal-data/account restrictions, reasonable request
frequency and caching policy, attribution or retention requirements, and the allowed
fallback if collection becomes unavailable.

HARD RULES:
- Prefer an official API or bulk download when it provides the required data.
- Browser automation must demonstrate legitimate technical need (JS-rendered content),
  never access-control bypass.
- Set verdict NOT_FEASIBLE and populate killReasons if the concept depends on evading
  CAPTCHAs, defeating authentication, scraping behind a login or paywall, ignoring an
  explicit robots prohibition, or collecting restricted personal data.
- Personal data: flag any source where records are about identifiable private
  individuals rather than businesses or public entities.

Prefer 3-5 concrete named sources over a generic category description. Do not write files.`, {
      label: `compliance:${seed.key}`,
      phase: 'Candidates',
      model: 'sonnet',
      schema: FEASIBILITY_SCHEMA,
    })
  },

  // Stage 3: score against the 7 Phase-1 criteria.
  (feas, seed, i) => {
    if (!feas) throw new Error(`feasibility ${seed.key} failed`)
    return agent(`${PREFLIGHT}

ROLE: Demand and concept agent (scoring).

Score candidate "${seed.key}" against EXACTLY the seven Phase 1 criteria, 1-5 each:
1. similarity to paid Upwork work
2. availability of lawful, public, stable-enough sources
3. opportunity to demonstrate difficult extraction and data-quality work
4. usefulness of the resulting dataset
5. ability to show measurable results without fabricated claims
6. time to a convincing first release
7. potential to become a reusable service rather than a disposable demo

Score honestly and use the full range. If every candidate scores 4-5 on everything the
scorecard is worthless. Penalize hard for: unverified source permissions, personal-data
exposure, and "changing only the website, theme, keyword set, or industry label"
(README states this does not make a new portfolio project).

Criterion 2 must be driven by the compliance verdict below, not by optimism.
If the compliance verdict is NOT_FEASIBLE, criterion 2 scores 1.

weakestLink: the single thing most likely to sink this concept.

COMPLIANCE FINDING:
${JSON.stringify(feas, null, 1)}`, {
      label: `score:${seed.key}`,
      phase: 'Candidates',
      model: 'sonnet',
      effort: 'low',
      schema: SCORE_SCHEMA,
    })
  },
)

// Rejoin the three parallel chains. pipeline returns final-stage results in
// input order, so index alignment with CANDIDATE_SEEDS is safe.
const scored = CANDIDATE_SEEDS.map((seed, i) => ({ seed, score: candidateChains[i] })).filter((c) => c.score)

if (scored.length === 0) {
  return { stopped: 'ALL_CANDIDATES_FAILED', action: 'No candidate completed the develop -> compliance -> score chain. Inspect the journal and re-run.' }
}
if (scored.length < CANDIDATE_SEEDS.length) {
  log(`NOTE: only ${scored.length}/${CANDIDATE_SEEDS.length} candidate chains completed. Dropped: ${CANDIDATE_SEEDS.filter((s, i) => !candidateChains[i]).map((s) => s.key).join(', ')}`)
}

scored.sort((a, b) => (b.score.total || 0) - (a.score.total || 0))
const leader = scored[0]
log(`Leading candidate: ${leader.seed.key} (total ${leader.score.total}). Weakest link: ${leader.score.weakestLink}`)

// ---------------------------------------------------------------------------
// Phase 4 - Gate. Opus: uniqueness gate + three perspective-diverse refuters.
// This is where a wrong call is most expensive, so it gets the strongest model.
// ---------------------------------------------------------------------------
phase('Gate')
log('Running relevance/uniqueness gate and adversarial refutation on the leader...')

const REFUTE_LENSES = [
  { key: 'novelty', ask: 'Is this actually just a themed variation of an existing portfolio concept? The README says changing only the website, visual theme, keyword set, or industry label does NOT make a new project. Attack the novelty claim.' },
  { key: 'compliance', ask: 'Will this concept, as scoped, inevitably require scraping behind auth, ignoring robots, evading anti-bot measures, or collecting personal data about private individuals? Attack the compliance story.' },
  { key: 'provability', ask: 'Can this concept actually produce HONEST measured proof — a ground-truth benchmark, reproducible run metrics, real failure-recovery evidence — within a focused first release? Attack the provability. A concept that can only be demonstrated with unverifiable claims must be refuted.' },
]

const [gate, refutations] = await Promise.all([
  agent(`${PREFLIGHT}

ROLE: Portfolio orchestrator (relevance and uniqueness gate).

Apply the README "Relevance and uniqueness gate" to the leading candidate.

It passes ONLY if it adds at least one net-new technical capability AND differs
meaningfully from all completed and active projects in at least TWO of the seven
dimensions. Verify the claimed dimensions against the actual prior-concept list —
do not take the candidate's own dimensionsDiffered at face value.

Also verify against the candidate/duplication register in PORTFOLIO_TRACKING_LOG.md,
which already flags a specific duplication risk for this concept family and states
what would make it distinct. Check that the candidate actually does that thing.

If it fails, set passes=false and list requiredChanges that would make it pass.

CANDIDATE (winner by score):
${JSON.stringify(leader.score, null, 1)}
seed: ${leader.seed.seed}

PRIOR AND ACTIVE CONCEPTS:
${JSON.stringify(pre.priorConcepts || [], null, 1)}`, {
    label: 'uniqueness-gate',
    phase: 'Gate',
    model: 'opus',
    effort: 'high',
    schema: GATE_SCHEMA,
  }),

  parallel(REFUTE_LENSES.map((lens) => () =>
    agent(`${PREFLIGHT}

ROLE: Adversarial reviewer (lens: ${lens.key}).

Your job is to REFUTE this candidate, not to appreciate it. ${lens.ask}

Default to refuted=true when genuinely uncertain. A concept that survives three hostile
lenses is worth building; one that squeaks through on benefit-of-the-doubt is not.
Set refuted=false only if the candidate clearly withstands your specific lens.

CANDIDATE: ${leader.seed.key}
${leader.seed.seed}

SCORECARD:
${JSON.stringify(leader.score, null, 1)}`, {
      label: `refute:${lens.key}`,
      phase: 'Gate',
      model: 'opus',
      effort: 'high',
      schema: REFUTE_SCHEMA,
    })
  )),
])

const votes = refutations.filter(Boolean)
const refutedCount = votes.filter((v) => v.refuted).length
const gatePasses = gate && gate.passes && refutedCount < 2

log(`Gate: ${gate && gate.passes ? 'PASS' : 'FAIL'}. Adversarial refutation: ${refutedCount}/${votes.length} lenses refuted.`)

// A majority refutation promotes the runner-up rather than killing the run —
// but the record of the refutation is preserved for the tracking log.
let recommended = leader
let promotionNote = null
if (!gatePasses && scored.length > 1) {
  recommended = scored[1]
  promotionNote = `Leader "${leader.seed.key}" failed the gate (uniqueness passes=${gate && gate.passes}, ${refutedCount}/${votes.length} adversarial lenses refuted). Runner-up "${recommended.seed.key}" is recommended instead, and the orchestrator must confirm it clears the same gate before approval.`
  log(`Promoting runner-up: ${recommended.seed.key}`)
}

// ---------------------------------------------------------------------------
// Phase 5 - Handoff. Write artifacts, update the log, request approval.
// Ordered writes: the log update must see the final recommendation.
// ---------------------------------------------------------------------------
phase('Handoff')

const decisionPayload = {
  today: TODAY,
  iteration: ITER,
  branch: pre.branch,
  scored: scored.map((s) => ({ key: s.seed.key, score: s.score })),
  gate,
  refutations: votes,
  recommendedKey: recommended.seed.key,
  promotionNote,
  demandSignalCount: signals.length,
  directPostingCount: signals.filter((s) => s.evidenceTier === 'DIRECT_POSTING').length,
  demandGaps,
}

const [scorecard, brief] = await parallel([
  () => agent(`${PREFLIGHT}

ROLE: Demand and concept agent (scribe).

Write ${REPO}/research/CANDIDATE_SCORECARD.md.

Structure:
- "# Candidate Scorecard" with the evaluation date ${TODAY} and iteration ${ITER}.
- "## Method" — the seven Phase 1 criteria, scored 1-5, and a note that criterion 2 is
  bound to the compliance verdict.
- "## Scores" — one table, candidates as rows, seven criteria + total as columns.
- "## Per-candidate assessment" — for each: rationale per criterion, weakest link.
- "## Relevance and uniqueness gate" — the gate result and reasoning.
- "## Adversarial review" — a subsection per lens (novelty, compliance, provability)
  with the verdict and reasoning verbatim. Do not soften refutations.
- "## Recommendation" — the recommended concept and why. If a promotion note is present,
  state plainly that the highest scorer FAILED the gate and was displaced.
- "## Approval request" — the five Phase 1 approval-gate items awaiting human decision:
  selected use case and target client; target sources and compliance ledger; data contract
  and expected exports; proof metrics and benchmark method; Phase 2 minimum viable build scope.
  Mark items 3 and 4 as "to be drafted after approval" — they are Run 2 deliverables.

Selection must be evidence-based. State explicitly that prior career history did not
decide the winner. Do not present any metric as measured — no run has occurred.

DECISION DATA:
${JSON.stringify(decisionPayload, null, 1)}`, {
    label: 'write:scorecard',
    phase: 'Handoff',
    model: 'sonnet',
    schema: WRITE_SCHEMA,
  }),

  () => agent(`${PREFLIGHT}

ROLE: Portfolio orchestrator (iteration brief).

Write ${REPO}/iterations/${ITER.toLowerCase()}/ITERATION_BRIEF.md.
Create directories as needed.

This brief is the approval-gate document. It must contain, per the README per-iteration
template: Status (AWAITING_APPROVAL), target buyer, operational decision enabled, demand
evidence (linking to research/UPWORK_DEMAND_MATRIX.md), portfolio gap addressed, novelty
versus completed and active projects, net-new technical capability, shared capabilities
reused, proposed scope, explicit non-goals, assigned roles and work claims, dependencies
and blockers.

Add "## Proposed vertical proof" — the smallest end-to-end slice, collection through
verified delivery, that the README requires each iteration to begin with.

Add "## What approval authorizes" and "## What approval does NOT authorize" — the latter
must restate the PHASE_01 boundary: no authentication bypass, no large-scale
infrastructure, no paid data acquisition, no sensitive personal information, absent a
new explicit decision.

Add "## Open questions for the approver" — only genuine decisions, not busywork.

Every unmeasured value stays "TBD". Status is AWAITING_APPROVAL; you may NOT write
APPROVED — only the human orchestrator crosses that boundary.

DECISION DATA:
${JSON.stringify(decisionPayload, null, 1)}
RECOMMENDED CONCEPT SEED:
${recommended.seed.seed}`, {
    label: 'write:iteration-brief',
    phase: 'Handoff',
    model: 'sonnet',
    schema: WRITE_SCHEMA,
  }),
])

// Log update runs last and alone: it must reflect the artifacts just written,
// and concurrent edits to one markdown file would corrupt it.
const logUpdate = await agent(`${PREFLIGHT}

ROLE: Portfolio orchestrator (tracking-log update).

Update ${REPO}/PORTFOLIO_TRACKING_LOG.md. This file is the source of truth; edit
surgically and PRESERVE ALL EXISTING CONTENT. Never delete a rejected concept or a
superseded decision.

Make exactly these changes:

1. "## Portfolio catalog" — update the ${ITER} row: set Concept to the recommended
   concept name, Target buyer to the real buyer, Distinct proof to the net-new
   capability, Status to AWAITING_APPROVAL, and Evidence to links to
   research/CANDIDATE_SCORECARD.md and iterations/${ITER.toLowerCase()}/ITERATION_BRIEF.md.

2. "## Active work claims" — replace the ${ITER} orchestrator row's Status/blocker with
   "Discovery complete; AWAITING_APPROVAL — human approval gate", set Started UTC to
   ${TODAY}, and update Expected outputs to the files actually produced.

3. "## Candidate and duplication register" — update the State of all three candidates
   (RECOMMENDED / DEFERRED / REJECTED as the evidence dictates) and fill in the
   "Decision/evidence needed" column with what was actually decided and why. Preserve
   the rows; do not delete losing candidates.

4. "## Shared Shipping Pipeline capability ledger" — move "Relevance and uniqueness gate"
   to VERIFIED only if the gate genuinely ran with a recorded result (it did), citing
   the scorecard as verification evidence. Set "Source/compliance ledger" to IN_PROGRESS.
   Leave every other capability's state alone — nothing else has been verified by a run.

5. "## Iteration decision and handoff log" — APPEND a new dated entry
   "### ${TODAY} - ${ITER} discovery and candidate selection" recording: decision,
   reason, the demand-evidence tier (PUBLIC-PRELIMINARY) and signal count, the
   candidates compared and their totals, the gate and adversarial-review outcome,
   any runner-up promotion, what remains blocked, and the next decision (human approval).
   Note that agent assistance is recorded here per policy rather than by inventing
   contributors.

Do not mark anything RELEASED, APPROVED, or VERIFIED that has not actually happened.

DECISION DATA:
${JSON.stringify(decisionPayload, null, 1)}
ARTIFACTS WRITTEN:
${JSON.stringify({ scorecard, brief, demandDoc }, null, 1)}`, {
  label: 'write:tracking-log',
  phase: 'Handoff',
  model: 'sonnet',
  schema: WRITE_SCHEMA,
})

const written = [demandDoc, scorecard, brief, logUpdate].filter(Boolean).flatMap((r) => r.filesWritten || [])

return {
  run: 1,
  stoppedAt: 'AWAITING_APPROVAL',
  iteration: ITER,
  branch: pre.branch,
  recommended: recommended.seed.key,
  scoreTotal: recommended.score.total,
  weakestLink: recommended.score.weakestLink,
  gatePassed: !!(gate && gate.passes),
  adversarialRefutations: `${refutedCount}/${votes.length}`,
  promotionNote,
  demandEvidence: {
    tier: 'PUBLIC-PRELIMINARY',
    signals: signals.length,
    directPostings: signals.filter((s) => s.evidenceTier === 'DIRECT_POSTING').length,
    gaps: demandGaps.length,
  },
  filesWritten: written,
  approvalNeeded: [
    'Selected use case and target client',
    'Target sources and compliance ledger',
    'Phase 2 minimum viable build scope',
  ],
  nextStep: `Review iterations/${ITER.toLowerCase()}/ITERATION_BRIEF.md, then run the ws-build workflow to proceed through build, verification, and release preparation.`,
}
