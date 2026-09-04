export const meta = {
  name: 'ws-rediscovery',
  description: 'WS Shipping Pipeline Run 1b: license-first candidate round — clear sources by explicit reuse terms, then build concepts only onto cleared sources',
  phases: [
    { title: 'Source sweep', detail: 'Find sources with EXPLICIT permissive reuse licenses, four search modes', model: 'sonnet' },
    { title: 'Clearance', detail: 'Verify each shortlisted source by fetching its actual license and robots', model: 'sonnet' },
    { title: 'Concepts', detail: 'Build concepts onto cleared sources only, then score', model: 'sonnet' },
    { title: 'Gate', detail: 'Uniqueness gate plus three adversarial lenses on the leader', model: 'opus' },
    { title: 'Handoff', detail: 'Update scorecard and brief, record round-2 decision in the log', model: 'sonnet' },
  ],
}

const REPO = String((args && args.repo) || 'c:/Users/cclem/Dropbox/Source/Halimede_Concepts/Upwork/Web_Scraping_Data_Operations')
const TODAY = String((args && args.today) || '2026-09-02')
const ITER = String((args && args.iteration) || 'WS-001')
const ITER_LC = ITER.toLowerCase()

// Round 1 outcome. Recorded here so round 2 cannot rediscover the same dead ends.
const ROUND1_REJECTED = `
ROUND 1 REJECTED SOURCES — do NOT propose these again:
- SAM.gov (GSA): Terms of Use state verbatim "Automated data gathering, web scraping tools
  are prohibited." Amendment/attachment data requires a federal system account with
  Contracting Officer/Specialist role plus IP allowlisting. Public API returns only the
  LATEST version of a notice, so amendment recall has no denominator.
- Google Places API: terms bar caching/storing name, address, phone, hours, status beyond
  place_id and lat/lng — incompatible with any change-detection design.
- Google Business Profile API: unusable for arbitrary third-party businesses.
- webscraper.io and scrapingcourse.com: robots.txt Disallow verified by fetch.
- Synthetic sandboxes (books.toscrape.com, sandbox.oxylabs.io): lawful but the data is
  explicitly random/meaningless, so no commercially credible dataset can result.
`

const PREFLIGHT = `
You are an agent in the Web Scraping & Data Operations multi-agent Shipping Pipeline.
Repository root: ${REPO}
Active iteration: ${ITER}. Today's UTC date: ${TODAY}.

MANDATORY PREFLIGHT (README.md "Global tracking log - mandatory preflight"):
Before writing anything, read in the repo root:
  README.md, PORTFOLIO_TRACKING_LOG.md, SOURCE_CONTROL_AND_PUBLIC_ARCHIVE.md,
  PHASE_01_DISCOVERY_AND_EVIDENCE_PLAN.md, research/UPWORK_DEMAND_MATRIX.md,
  research/CANDIDATE_SCORECARD.md
These outrank your own instincts about how to do the work.

CONTEXT — THIS IS ROUND 2. Round 1 produced three candidates and ALL THREE hit source
restrictions discovered only at the compliance and adversarial stages. The lesson: concepts
were invented first and sources checked afterwards. This round inverts that order. A concept
may only be proposed on a source whose reuse terms have ALREADY been verified by fetching
the actual license text.
${ROUND1_REJECTED}

NON-NEGOTIABLE RULES:
- Never fabricate demand data, licenses, terms, URLs, dates, or metrics.
- Anything not yet measured stays literally "TBD".
- A license claim is worthless unless you FETCHED the license text. Always state whether you
  fetched it or are inferring, and quote the operative sentence.
- Never propose work that bypasses authentication, defeats CAPTCHAs, evades access controls,
  or collects restricted personal data.
- Preserve existing file content. Edit surgically; never delete rejected concepts or
  superseded decisions from the tracking log.
- Do not run git commit, git push, git tag, or gh.
- Your final message IS your return value. Return data, not conversational filler.
`

// ---------------------------------------------------------------------------
// Schemas
// ---------------------------------------------------------------------------
const SOURCE_SCHEMA = {
  type: 'object',
  required: ['sources'],
  properties: {
    sources: {
      type: 'array',
      items: {
        type: 'object',
        required: ['owner', 'url', 'licenseName', 'licenseUrl', 'permitsAutomatedCollection', 'permitsRepublication', 'verifiedHow'],
        properties: {
          owner: { type: 'string' },
          url: { type: 'string' },
          domain: { type: 'string', description: 'subject domain, e.g. procurement, transit, food safety' },
          licenseName: { type: 'string', description: 'e.g. CC-BY-4.0, OGL-3.0, US Public Domain, Open Data Commons' },
          licenseUrl: { type: 'string' },
          operativeQuote: { type: 'string', description: 'the exact sentence granting reuse rights' },
          permitsAutomatedCollection: { type: 'boolean' },
          permitsRepublication: { type: 'boolean' },
          accessPath: { type: 'string', enum: ['OFFICIAL_API', 'BULK_DOWNLOAD', 'FEED', 'HTML', 'DOCUMENT', 'DYNAMIC_BROWSER'] },
          hasDocuments: { type: 'boolean', description: 'does it expose PDFs or attachments?' },
          hasHistory: { type: 'boolean', description: 'does it retain prior versions/revisions? critical for honest change-detection metrics' },
          updateCadence: { type: 'string' },
          recordVolume: { type: 'string' },
          personalDataRisk: { type: 'string' },
          rateGuidance: { type: 'string' },
          verifiedHow: { type: 'string', description: 'FETCHED <url> or INFERRING — be exact' },
        },
      },
    },
  },
}

const CLEARANCE_SCHEMA = {
  type: 'object',
  required: ['url', 'cleared', 'reasoning'],
  properties: {
    url: { type: 'string' },
    owner: { type: 'string' },
    cleared: { type: 'boolean' },
    licenseName: { type: 'string' },
    operativeQuote: { type: 'string' },
    robotsFinding: { type: 'string' },
    termsFinding: { type: 'string' },
    apiOrBulkAvailable: { type: 'string' },
    retainsHistory: { type: 'boolean' },
    exposesDocuments: { type: 'boolean' },
    personalDataRisk: { type: 'string' },
    fetchesPerformed: { type: 'array', items: { type: 'string' } },
    disqualifiers: { type: 'array', items: { type: 'string' } },
    reasoning: { type: 'string' },
  },
}

const CANDIDATE_SCHEMA = {
  type: 'object',
  required: ['name', 'slug', 'targetBuyer', 'operationalDecision', 'technicalProof', 'noveltyStatement', 'sourcesUsed', 'provabilityStatement'],
  properties: {
    name: { type: 'string' },
    slug: { type: 'string' },
    targetBuyer: { type: 'string' },
    operationalDecision: { type: 'string' },
    demandRefs: { type: 'array', items: { type: 'string' } },
    sourcesUsed: { type: 'array', items: { type: 'string' }, description: 'URLs — MUST all be cleared sources' },
    technicalProof: { type: 'string' },
    portfolioGap: { type: 'string' },
    noveltyStatement: { type: 'string' },
    reusableContribution: { type: 'string' },
    dimensionsDiffered: { type: 'array', items: { type: 'string' } },
    verticalProofScope: { type: 'string' },
    provabilityStatement: { type: 'string', description: 'How ground truth is established and what the denominator is for every rate metric. Round 1 died here.' },
    explicitNonGoals: { type: 'array', items: { type: 'string' } },
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
        properties: { name: { type: 'string' }, score: { type: 'number' }, rationale: { type: 'string' } },
      },
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
// Phase 1 - Source sweep. Multi-modal: four blind angles on permissive sources.
// Barrier: clearance needs the full pool to pick the strongest shortlist.
// ---------------------------------------------------------------------------
phase('Source sweep')
log('Sweeping for sources with EXPLICIT permissive reuse licenses...')

const SWEEP_MODES = [
  { key: 'gov-open-data', angle: `National and municipal open-data portals with an EXPLICIT open licence: data.gov.uk (OGL), data.gov, EU Open Data Portal / data.europa.eu, Canada Open Government, Australia data.gov.au, and large city portals (NYC, Chicago, Toronto, London). Look specifically for portals whose terms explicitly PERMIT automated access and republication.` },
  { key: 'procurement-transparency', angle: `Procurement and contracting portals OUTSIDE the US federal system, since SAM.gov is disqualified: EU TED (Tenders Electronic Daily), UK Contracts Finder / Find a Tender, Canada BuyAndSell/CanadaBuys, US state and municipal procurement portals, and Open Contracting Data Standard (OCDS) publishers. OCDS publishers are especially interesting because the standard retains award and amendment history.` },
  { key: 'regulatory-registers', angle: `Regulatory and inspection registers that publish structured records AND documents under open terms: food-safety inspections, building permits, environmental permits, drug/device recalls (openFDA), vessel/aircraft registries, charity and company registers (e.g. UK Charity Commission, Companies House). Prioritise ones exposing BOTH structured records and PDFs.` },
  { key: 'versioned-datasets', angle: `Sources that explicitly RETAIN HISTORY or publish versioned snapshots — critical because Round 1 died on unfalsifiable change-detection metrics. Look for: portals publishing dated snapshot archives, OCDS releases with revision history, GTFS/GTFS-RT transit feeds with archives, data portals exposing a changelog or revision API, and any open dataset with an explicit "previous versions" facility.` },
]

const sweeps = await parallel(SWEEP_MODES.map((m) => () =>
  agent(`${PREFLIGHT}

ROLE: Source and compliance agent (sweep mode: ${m.key}).

TASK: Find real data sources with EXPLICIT permissive reuse terms.

${m.angle}

METHOD: Load WebSearch and WebFetch via ToolSearch ("select:WebSearch,WebFetch").
For every source you report you MUST fetch its licence or terms page and quote the
operative sentence in operativeQuote. If you did not fetch it, say INFERRING in
verifiedHow and expect it to be rejected at clearance.

A source qualifies only if the licence text affirmatively permits reuse. "Not explicitly
forbidden" is NOT permission — that ambiguity is exactly what sank Round 1.

Record hasHistory honestly: does the source retain prior versions or publish dated
snapshots? A source that only ever shows current state cannot support honest
change-detection recall metrics.

Report 5-10 sources. Quality over quantity — one source with a quoted CC-BY grant is worth
more than five maybes. Do not write files.`, {
    label: `sweep:${m.key}`,
    phase: 'Source sweep',
    model: 'sonnet',
    schema: SOURCE_SCHEMA,
  })
))

const pool = sweeps.filter(Boolean).flatMap((s) => s.sources || [])
const fetched = pool.filter((s) => /FETCHED/i.test(String(s.verifiedHow || '')))
log(`Source pool: ${pool.length} found, ${fetched.length} with fetched licence text.`)

if (fetched.length === 0) {
  return { stopped: 'NO_CLEARED_SOURCES', pool: pool.length, action: 'No source had verifiable permissive licence text. Check network/WebFetch, or supply a known-permissive source directly.' }
}

// Shortlist: prefer fetched + permits both collection and republication.
const shortlist = fetched
  .filter((s) => s.permitsAutomatedCollection && s.permitsRepublication)
  .slice(0, 12)
const shortlistUrls = Array.from(new Set(shortlist.map((s) => s.url)))
log(`Shortlisted ${shortlistUrls.length} sources for independent clearance.`)

if (shortlistUrls.length === 0) {
  return { stopped: 'NO_SOURCE_PERMITS_BOTH', pool: pool.length, fetched: fetched.length, action: 'No source both permits automated collection and republication. Relax republication (portfolio could use derived aggregates only) or supply a source directly.' }
}

// ---------------------------------------------------------------------------
// Phase 2 - Clearance. Independent re-verification. The sweep agent had an
// incentive to report finds; the clearance agent's job is to disqualify.
// ---------------------------------------------------------------------------
phase('Clearance')
log('Independently clearing each shortlisted source...')

const clearances = await parallel(shortlistUrls.map((url) => () =>
  agent(`${PREFLIGHT}

ROLE: Source and compliance agent (independent clearance).

A sweep agent proposed this source as permissively licensed. You are INDEPENDENT of that
agent. Your job is to DISQUALIFY it if you can. Assume the proposal is wrong until the
licence text proves otherwise.

SOURCE TO CLEAR: ${url}

Load WebSearch/WebFetch via ToolSearch ("select:WebSearch,WebFetch"), then actually fetch:
1. The site's robots.txt — quote any Disallow that affects the data paths.
2. The terms of use / acceptable use page — look specifically for any prohibition on
   automated collection, scraping, bots, or bulk download. Round 1's fatal miss was a ToU
   sentence banning "automated data gathering" on a site that otherwise looked open.
3. The licence page — quote the operative grant sentence.
4. Whether an official API or bulk download exists, and its documented rate guidance.
5. Whether the source retains prior versions / publishes dated snapshots (retainsHistory).
6. Whether it exposes documents such as PDFs (exposesDocuments).
7. Whether records concern identifiable private individuals (personalDataRisk).

List every URL you actually fetched in fetchesPerformed. Set cleared=true ONLY if:
- the licence affirmatively grants reuse, AND
- no ToU sentence prohibits automated collection, AND
- robots.txt does not disallow the needed paths, AND
- the records are not about identifiable private individuals.

Put every disqualifying finding in disqualifiers. Being wrong in the permissive direction
is the expensive error here — a whole build gets thrown away. Do not write files.`, {
    label: `clear:${String(url).replace(/^https?:\/\//, '').slice(0, 32)}`,
    phase: 'Clearance',
    model: 'sonnet',
    effort: 'high',
    schema: CLEARANCE_SCHEMA,
  })
))

const cleared = clearances.filter(Boolean).filter((c) => c.cleared)
const rejected = clearances.filter(Boolean).filter((c) => !c.cleared)
log(`Clearance: ${cleared.length} cleared, ${rejected.length} disqualified.`)

if (cleared.length === 0) {
  return {
    stopped: 'ALL_SOURCES_DISQUALIFIED',
    rejected: rejected.map((r) => ({ url: r.url, disqualifiers: r.disqualifiers })),
    action: 'Every shortlisted source failed independent clearance. Review the disqualifiers — if they are all marginal, consider supplying a source you know to be open.',
  }
}

const withHistory = cleared.filter((c) => c.retainsHistory)
const withDocs = cleared.filter((c) => c.exposesDocuments)
log(`Cleared pool: ${withHistory.length} retain history, ${withDocs.length} expose documents.`)

const CLEARED_BLOCK = JSON.stringify(cleared.map((c) => ({
  url: c.url, owner: c.owner, licence: c.licenseName, quote: c.operativeQuote,
  api: c.apiOrBulkAvailable, retainsHistory: c.retainsHistory,
  exposesDocuments: c.exposesDocuments, robots: c.robotsFinding,
})), null, 1)

// ---------------------------------------------------------------------------
// Phase 3 - Concepts, built ONTO cleared sources. pipeline: develop -> score
// per concept, independently.
// ---------------------------------------------------------------------------
phase('Concepts')

const CONCEPT_ANGLES = [
  { key: 'change-monitoring', angle: `A CHANGE-MONITORING operation. Prioritise cleared sources that retain history, so that change-detection recall has a real denominator and the metrics are falsifiable. This is the angle Round 1 failed on — do not repeat it on a source that only exposes current state.` },
  { key: 'cross-source-resolution', angle: `A CROSS-SOURCE ENTITY-RESOLUTION operation: reconcile records for the same entity across two or more cleared sources, handling conflicting facts with field-level confidence and a review queue. Ground truth comes from a manually reviewed sample.` },
  { key: 'document-extraction', angle: `A DOCUMENT-EXTRACTION operation. Prioritise cleared sources that expose PDFs or attachments: extract structured fields from documents and reconcile them against the structured metadata, with every field traceable to a page or span.` },
]

const conceptChains = await pipeline(
  CONCEPT_ANGLES,

  (angle) => agent(`${PREFLIGHT}

ROLE: Demand and concept agent (round 2, angle: ${angle.key}).

Build ONE portfolio concept using ONLY the cleared sources listed below. This is the
inversion that defines round 2: you may not propose a source that is not on this list.

ANGLE: ${angle.angle}

Complete every element of the README relevance and uniqueness gate: target buyer,
operational decision, demand evidence, source profile, technical proof, portfolio gap,
novelty statement, reusable contribution.

provabilityStatement is MANDATORY and is where round 1 died. State exactly:
- how ground truth is established (what is manually reviewed, how many records, by what procedure)
- what the DENOMINATOR is for every rate metric you intend to claim
- what would falsify each claim
If you cannot answer these on the available sources, choose a different cleared source or a
different claim. A concept whose headline metric cannot be falsified is not buildable here.

Ground demand in research/UPWORK_DEMAND_MATRIX.md — read it and cite real sourceUrls
from it in demandRefs.

verticalProofScope must be the SMALLEST end-to-end slice: collection through verified delivery.

CLEARED SOURCES (the only permitted pool):
${CLEARED_BLOCK}

Do not write files.`, {
    label: `concept:${angle.key}`,
    phase: 'Concepts',
    model: 'sonnet',
    effort: 'high',
    schema: CANDIDATE_SCHEMA,
  }),

  (concept, angle) => {
    if (!concept) throw new Error(`concept ${angle.key} failed`)
    return agent(`${PREFLIGHT}

ROLE: Demand and concept agent (scoring).

Score this concept against the seven Phase 1 criteria, 1-5 each:
1. similarity to paid Upwork work
2. availability of lawful, public, stable-enough sources
3. opportunity to demonstrate difficult extraction and data-quality work
4. usefulness of the resulting dataset
5. ability to show measurable results without fabricated claims
6. time to a convincing first release
7. potential to become a reusable service rather than a disposable demo

Use the full 1-5 range; if everything scores 4-5 the scorecard is worthless.

Round-2-specific scoring rules, derived from why round 1 failed:
- Criterion 4 (dataset usefulness): score 2 or below if the data is synthetic, randomly
  generated, or has no commercial meaning.
- Criterion 5 (measurable without fabrication): score 2 or below if any headline metric
  lacks a real denominator or cannot be falsified. Judge the provabilityStatement harshly.
- Criterion 2: the sources are pre-cleared, so score this on STABILITY and rate-limit
  headroom, not on legality.

CONCEPT:
${JSON.stringify(concept, null, 1)}`, {
      label: `score:${angle.key}`,
      phase: 'Concepts',
      model: 'sonnet',
      effort: 'low',
      schema: SCORE_SCHEMA,
    })
  },
)

const scored = CONCEPT_ANGLES
  .map((a, i) => ({ angle: a, score: conceptChains[i] }))
  .filter((c) => c.score)

if (scored.length === 0) {
  return { stopped: 'ALL_CONCEPTS_FAILED', clearedSources: cleared.length, action: 'No concept survived develop -> score on the cleared source pool. Inspect the journal.' }
}
scored.sort((a, b) => (b.score.total || 0) - (a.score.total || 0))
const leader = scored[0]
log(`Leader: ${leader.angle.key} (${leader.score.total}/35). Running gate and adversarial lenses...`)

// ---------------------------------------------------------------------------
// Phase 4 - Gate. Same rigour as round 1, plus a provability lens sharpened by
// what round 1 taught us.
// ---------------------------------------------------------------------------
phase('Gate')

const LENSES = [
  { key: 'novelty', ask: `Is this a themed variation of an existing portfolio concept, or of a commercial product? The README disqualifies changing only the website, theme, keyword set, or industry label. Attack the novelty claim.` },
  { key: 'compliance', ask: `The sources were pre-cleared, so attack the clearance itself. Independently re-check the operative licence quote and hunt for any terms sentence prohibiting automated collection that the clearance agent missed. Round 1's leader was killed by exactly such a sentence found late. Also attack whether the OPERATION as scoped stays inside the licence — republication of derived data, attribution, retention.` },
  { key: 'provability', ask: `Attack the provabilityStatement directly. Does every rate metric have a real denominator? Is ground truth established from an independent record, or does the pipeline grade itself against its own snapshots? Round 1's leader died because the source retained no history, making change-detection recall unfalsifiable. Verify the claimed retainsHistory is actually true by checking the source. Refute if any headline claim is unfalsifiable.` },
]

const [gate, refs] = await Promise.all([
  agent(`${PREFLIGHT}

ROLE: Portfolio orchestrator (relevance and uniqueness gate).

Apply the README gate to the leading round-2 candidate. It passes ONLY if it adds at least
one net-new technical capability AND differs meaningfully in at least TWO of the seven
dimensions. Verify claimed dimensions against the actual prior-concept list rather than
accepting the candidate's own claims.

Also check the tracking log's candidate/duplication register: it names specific things that
would make each concept family distinct. Verify the candidate actually does those things —
round 1's leader failed precisely because 2 of 5 register-named requirements were absent.

CANDIDATE:
${JSON.stringify(leader.score, null, 1)}
angle: ${leader.angle.angle}

CLEARED SOURCES:
${CLEARED_BLOCK}`, {
    label: 'uniqueness-gate-r2',
    phase: 'Gate',
    model: 'opus',
    effort: 'high',
    schema: GATE_SCHEMA,
  }),

  parallel(LENSES.map((l) => () =>
    agent(`${PREFLIGHT}

ROLE: Adversarial reviewer (lens: ${l.key}).

REFUTE this candidate. ${l.ask}

Default to refuted=true when genuinely uncertain. Use WebFetch to verify claims about
sources rather than reasoning from the description — load it via ToolSearch
("select:WebSearch,WebFetch"). Round 1's most valuable findings came from actually
fetching terms pages, not from analysis.

CANDIDATE: ${leader.angle.key}
${JSON.stringify(leader.score, null, 1)}

CLEARED SOURCES:
${CLEARED_BLOCK}`, {
      label: `refute-r2:${l.key}`,
      phase: 'Gate',
      model: 'opus',
      effort: 'high',
      schema: REFUTE_SCHEMA,
    })
  )),
])

const votes = refs.filter(Boolean)
const refuted = votes.filter((v) => v.refuted).length
const passes = !!(gate && gate.passes) && refuted < 2
log(`Gate: ${gate && gate.passes ? 'PASS' : 'FAIL'}. Refutations: ${refuted}/${votes.length}.`)

let recommended = leader
let promotionNote = null
if (!passes && scored.length > 1) {
  recommended = scored[1]
  promotionNote = `Round-2 leader "${leader.angle.key}" failed the gate (passes=${gate && gate.passes}, ${refuted}/${votes.length} lenses refuted). Runner-up "${recommended.angle.key}" is recommended but has NOT itself cleared the gate.`
  log(`Promoting runner-up: ${recommended.angle.key}`)
}

// ---------------------------------------------------------------------------
// Phase 5 - Handoff.
// ---------------------------------------------------------------------------
phase('Handoff')

const payload = {
  today: TODAY, iteration: ITER, round: 2,
  clearedSources: cleared, rejectedSources: rejected.map((r) => ({ url: r.url, disqualifiers: r.disqualifiers })),
  scored: scored.map((s) => ({ key: s.angle.key, score: s.score })),
  gate, refutations: votes, recommendedKey: recommended.angle.key, promotionNote,
  gatePassed: passes,
}

const [ledger, scorecard] = await parallel([
  () => agent(`${PREFLIGHT}

ROLE: Source and compliance agent (scribe).

Write ${REPO}/design/SOURCE_AND_COMPLIANCE_LEDGER.md (create design/ if needed).

This is the PHASE_01 workstream 3 deliverable, now backed by real clearance work.

Structure:
- "# Source and Compliance Ledger" with date ${TODAY}, iteration ${ITER}.
- "## Method" — sources were cleared BEFORE concepts were proposed (round 2 inversion),
  each independently re-verified by a second agent whose task was to disqualify it.
- "## Cleared sources" — one subsection per cleared source: owner, URL, licence name and
  link, the OPERATIVE QUOTE verbatim, access path, API/bulk availability, rate guidance,
  retains-history, exposes-documents, personal-data risk, fallback if unavailable, and the
  exact list of URLs fetched during clearance.
- "## Disqualified sources" — every rejected source WITH its disqualifiers. Per the README,
  rejected options are retained to prevent rediscovery.
- "## Round 1 disqualifications carried forward" — record the SAM.gov automated-collection
  prohibition, the Google Places caching restriction, and the synthetic-sandbox finding, so
  no future iteration rediscovers them.
- "## Refusals" — what this project deliberately will not collect or automate.

Quote licence text exactly. Do not paraphrase a grant of rights.

DATA:
${JSON.stringify(payload, null, 1)}`, {
    label: 'write:compliance-ledger',
    phase: 'Handoff',
    model: 'sonnet',
    schema: WRITE_SCHEMA,
  }),

  () => agent(`${PREFLIGHT}

ROLE: Demand and concept agent (scribe).

REWRITE ${REPO}/research/CANDIDATE_SCORECARD.md to cover BOTH rounds. Read the existing
file first — round 1's content must be PRESERVED as a "## Round 1" section, including the
failed leader and all three adversarial verdicts. The README forbids erasing rejected
concepts; round 1 is the evidence explaining why round 2 exists.

Then add:
- "## Round 1 outcome and lesson" — all three candidates hit source restrictions found only
  at the compliance/adversarial stage, because concepts were invented before sources were
  cleared. State the specific killers (SAM.gov ToU prohibition on automated collection,
  the latest-version-only API destroying change-detection denominators, Google Places
  caching bar, synthetic-sandbox data having no commercial meaning).
- "## Round 2 method — license-first" — sources cleared first, concepts built only onto them.
- "## Round 2 cleared source pool" — a table, with licence and operative quote.
- "## Round 2 candidates" — scores table across the seven criteria, per-criterion rationale,
  weakest link, and each candidate's provabilityStatement.
- "## Round 2 gate and adversarial review" — verdicts verbatim, not softened.
- "## Recommendation" — the recommended concept and why; if a promotion note exists, state
  plainly that the leader failed and was displaced.
- "## Approval request" — the Phase 1 approval-gate items awaiting human decision.

Present no metric as measured — no run has occurred.

DATA:
${JSON.stringify(payload, null, 1)}`, {
    label: 'write:scorecard-r2',
    phase: 'Handoff',
    model: 'sonnet',
    effort: 'high',
    schema: WRITE_SCHEMA,
  }),
])

const brief = await agent(`${PREFLIGHT}

ROLE: Portfolio orchestrator (iteration brief, round 2).

REWRITE ${REPO}/iterations/${ITER_LC}/ITERATION_BRIEF.md for the round-2 recommendation.
Read the existing file first and preserve its round-1 history in a "## Round 1 history"
section — the abandoned direction explains the current one and may not be erased.

The brief is the approval-gate document. Include, per the README per-iteration template:
Status (AWAITING_APPROVAL), target buyer, operational decision enabled, demand evidence
(link research/UPWORK_DEMAND_MATRIX.md), portfolio gap, novelty versus completed and active
projects, net-new technical capability, shared capabilities reused, proposed scope, explicit
non-goals, assigned roles and work claims, dependencies and blockers.

Add these sections:
- "## Cleared sources" — the sources this build may use, with licence and operative quote,
  linking design/SOURCE_AND_COMPLIANCE_LEDGER.md. State that the build may use NO other source.
- "## Provability" — the candidate's provabilityStatement: ground-truth method, the
  denominator for each rate metric, and what would falsify each claim. This section exists
  because round 1's leader was killed by unfalsifiable metrics.
- "## Proposed vertical proof" — the smallest end-to-end slice.
- "## What approval authorizes" / "## What approval does NOT authorize" — the latter
  restating the PHASE_01 boundary: no authentication bypass, no large-scale infrastructure,
  no paid data acquisition, no sensitive personal information, absent a new explicit decision.
- "## Open questions for the approver" — only genuine decisions.
${passes ? '' : '- "## Gate status" — state prominently that the recommended concept has NOT cleared the uniqueness gate and that approval must include re-running it.'}

Status stays AWAITING_APPROVAL. You may NOT write APPROVED.
Unmeasured values stay "TBD".

DATA:
${JSON.stringify(payload, null, 1)}`, {
  label: 'write:brief-r2',
  phase: 'Handoff',
  model: 'sonnet',
  effort: 'high',
  schema: WRITE_SCHEMA,
})

const logUpdate = await agent(`${PREFLIGHT}

ROLE: Portfolio orchestrator (tracking-log update, round 2).

Update ${REPO}/PORTFOLIO_TRACKING_LOG.md surgically. PRESERVE ALL EXISTING CONTENT,
including the round-1 entry and all rejected concepts.

1. Portfolio catalog — update the ${ITER} row for the round-2 recommendation. Status stays
   AWAITING_APPROVAL. Notes must state the round-2 gate outcome honestly${passes ? '' : ', including that the recommended concept has not itself cleared the gate'}.
2. Candidate and duplication register — ADD rows for the three round-2 concepts with their
   states, and update the three round-1 rows to REJECTED with their real reasons (SAM.gov
   ToU prohibition and unfalsifiable change metrics; Google Places caching bar; synthetic
   data with no commercial meaning). Do not delete the round-1 rows.
3. Rejected or archived concepts — replace the "None recorded" placeholder with the round-1
   rejections and the disqualified sources, each with its reason and a "may be reconsidered
   when" condition.
4. Shared Shipping Pipeline capability ledger — set "Source/compliance ledger" to VERIFIED
   only if design/SOURCE_AND_COMPLIANCE_LEDGER.md now exists with fetched licence evidence,
   citing it. Leave other capabilities alone.
5. Iteration decision and handoff log — APPEND "### ${TODAY} - ${ITER} round 2 license-first
   candidate round" recording: why round 1's approach failed, the method inversion, how many
   sources were swept/shortlisted/cleared/disqualified, the candidates and scores, the gate
   and adversarial outcome, and the next decision (human approval). Record only real history;
   the README forbids manufacturing counts or productivity claims.

DATA:
${JSON.stringify(payload, null, 1)}
ARTIFACTS: ${JSON.stringify({ ledger, scorecard, brief }, null, 1)}`, {
  label: 'write:tracking-log-r2',
  phase: 'Handoff',
  model: 'sonnet',
  effort: 'high',
  schema: WRITE_SCHEMA,
})

return {
  run: '1b',
  stoppedAt: 'AWAITING_APPROVAL',
  iteration: ITER,
  method: 'license-first',
  sources: {
    swept: pool.length,
    withFetchedLicence: fetched.length,
    shortlisted: shortlistUrls.length,
    cleared: cleared.length,
    disqualified: rejected.length,
    retainHistory: withHistory.length,
    exposeDocuments: withDocs.length,
  },
  clearedSources: cleared.map((c) => ({ owner: c.owner, url: c.url, licence: c.licenseName, retainsHistory: c.retainsHistory, exposesDocuments: c.exposesDocuments })),
  candidates: scored.map((s) => ({ key: s.angle.key, total: s.score.total, weakestLink: s.score.weakestLink })),
  recommended: recommended.angle.key,
  scoreTotal: recommended.score.total,
  gatePassed: passes,
  adversarialRefutations: `${refuted}/${votes.length}`,
  promotionNote,
  filesWritten: [ledger, scorecard, brief, logUpdate].filter(Boolean).flatMap((r) => r.filesWritten || []),
  nextStep: passes
    ? `Review iterations/${ITER_LC}/ITERATION_BRIEF.md. If approved, set ${ITER} to APPROVED in PORTFOLIO_TRACKING_LOG.md and run ws-build.js.`
    : `Round-2 leader also failed the gate. Review the scorecard before approving anything — the candidate pool may need a different angle rather than another round.`,
}
