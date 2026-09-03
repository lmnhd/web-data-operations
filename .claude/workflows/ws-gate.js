export const meta = {
  name: 'ws-gate',
  description: 'WS Shipping Pipeline Run 1c: run the relevance/uniqueness gate and three adversarial lenses on a named candidate, then record APPROVED or the refutation',
  phases: [
    { title: 'Load', detail: 'Read the candidate, cleared sources, and prior rejections', model: 'haiku' },
    { title: 'Gate', detail: 'Uniqueness gate plus novelty, compliance and provability lenses', model: 'opus' },
    { title: 'Record', detail: 'Update the brief and tracking log with the verdict', model: 'sonnet' },
  ],
}

const REPO = String((args && args.repo) || 'c:/Users/cclem/Dropbox/Source/Halimede_Concepts/Upwork/Web_Scraping_Data_Operations')
const TODAY = String((args && args.today) || '2026-09-03')
const ITER = String((args && args.iteration) || 'WS-001')
const ITER_LC = ITER.toLowerCase()
const SLUG = String((args && args.candidate) || 'uk-procurement-amendment-monitor')

// Caveats carried in from the round-2 adversarial findings. These are binding on
// the candidate: if it cannot satisfy them, the gate must fail it.
const CAVEATS = `
BINDING CAVEATS from round-2 adversarial findings. The candidate must satisfy BOTH:

1. ORGANISATION-LEVEL IDENTIFIERS ONLY. OGL v3.0's grant EXCLUDES personal data, and the
   round-2 compliance lens found named officer contacts and sole-trader personal emails and
   mobile numbers in live Find a Tender / Contracts Finder payloads. The concept may match,
   store, or publish organisation-level identifiers (GB-PPON, GB-COH) and organisation names
   only. Any design touching personal contact fields fails this gate.

2. NO RATE-LIMIT PROBING. The operative Contracts Finder / Find a Tender Terms and
   Conditions page (https://www.contractsfinder.service.gov.uk/Home/TermsAndConditions)
   bars "Using manual or electronic means to avoid any use limitations placed on a System,
   such as access and storage restrictions." The rate ceiling must be established from
   PUBLISHED guidance or by conservative fixed-interval polling well below any plausible
   limit — never by probing upward until a 403/429 trips, and never by backoff-and-rotate
   to sustain a rate the service refused.
`

const PRIOR_REJECTIONS = `
ALREADY REJECTED — do not re-propose, and check the candidate does not reintroduce these:
- SAM.gov: ToU prohibits automated collection; public API returns latest version only, so
  amendment recall has no denominator (round 1 leader, refuted on compliance + provability).
- Google Places / Business Profile: terms bar caching the operating-detail fields.
- Synthetic sandboxes: data explicitly random/meaningless, no commercial credibility.
- uk-public-buyer-cross-source-resolution (round 2 leader, refuted 3/3): reproduced the
  business-location-monitoring register row's cross-source identity mechanic under a new
  industry label; its "no shared key" premise is a closing transitional artifact of a UK
  identifier migration (PPN 019 retires Contracts Finder dual publication); buyer-identifier
  schemes measured to have an EMPTY intersection across the two sources.
- The National Archives Discovery API: "do not cache or store any content returned by the API".
`

const PREFLIGHT = `
You are an agent in the Web Scraping & Data Operations multi-agent Shipping Pipeline.
Repository root: ${REPO}
Active iteration: ${ITER}. Today's UTC date: ${TODAY}.

MANDATORY PREFLIGHT (README.md "Global tracking log - mandatory preflight"):
Before writing anything, read in the repo root:
  README.md, PORTFOLIO_TRACKING_LOG.md, SOURCE_CONTROL_AND_PUBLIC_ARCHIVE.md,
  PHASE_01_DISCOVERY_AND_EVIDENCE_PLAN.md, research/CANDIDATE_SCORECARD.md,
  design/SOURCE_AND_COMPLIANCE_LEDGER.md, iterations/${ITER_LC}/ITERATION_BRIEF.md
These outrank your own instincts about how to do the work.

CONTEXT: Two candidate rounds have run. Round 1's leader and round 2's leader were BOTH
refuted and rejected. This run gates the round-2 RUNNER-UP, "${SLUG}", which scored 27/35
and was never itself put through the gate or the adversarial lenses.
${PRIOR_REJECTIONS}
${CAVEATS}

NON-NEGOTIABLE RULES:
- Never fabricate demand data, licences, terms, URLs, dates, or metrics.
- Anything not yet measured stays literally "TBD".
- A claim about a source is worthless unless you FETCHED it. State FETCHED or INFERRING and
  quote the operative sentence. Round 1 and round 2 were both decided by fetched evidence.
- Never approve work that bypasses authentication, defeats CAPTCHAs, evades access controls,
  or collects restricted personal data.
- Preserve existing file content. Never delete rejected concepts or superseded decisions.
- Do not run git commit, git push, git tag, or gh.
- Your final message IS your return value. Return data, not conversational filler.
`

const LOAD_SCHEMA = {
  type: 'object',
  required: ['found', 'candidate'],
  properties: {
    found: { type: 'boolean' },
    candidate: {
      type: 'object',
      properties: {
        name: { type: 'string' },
        slug: { type: 'string' },
        targetBuyer: { type: 'string' },
        operationalDecision: { type: 'string' },
        sourcesUsed: { type: 'array', items: { type: 'string' } },
        technicalProof: { type: 'string' },
        noveltyStatement: { type: 'string' },
        provabilityStatement: { type: 'string' },
        verticalProofScope: { type: 'string' },
        reusableContribution: { type: 'string' },
        weakestLink: { type: 'string' },
        score: { type: 'number' },
      },
    },
    clearedSources: { type: 'array', items: { type: 'string' } },
    priorConcepts: { type: 'array', items: { type: 'string' } },
    notes: { type: 'string' },
  },
}

const GATE_SCHEMA = {
  type: 'object',
  required: ['passes', 'dimensionsDiffered', 'netNewCapability', 'registerRequirementsMet', 'reasoning'],
  properties: {
    passes: { type: 'boolean' },
    dimensionsDiffered: { type: 'array', items: { type: 'string' } },
    netNewCapability: { type: 'string' },
    registerRequirementsMet: { type: 'array', items: { type: 'string' }, description: 'which register-named distinctness requirements this actually satisfies' },
    registerRequirementsMissing: { type: 'array', items: { type: 'string' } },
    duplicationRisk: { type: 'string' },
    caveatsSatisfied: { type: 'boolean', description: 'does it satisfy BOTH binding caveats?' },
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
    fetchesPerformed: { type: 'array', items: { type: 'string' } },
    scopeConditions: { type: 'array', items: { type: 'string' }, description: 'conditions that would make this survivable, if it is refuted on a fixable point' },
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
// Phase 1 - Load the candidate from the artifacts on disk.
// ---------------------------------------------------------------------------
phase('Load')
log(`Loading candidate "${SLUG}" from the round-2 artifacts...`)

const loaded = await agent(`${PREFLIGHT}

TASK: Load the full specification of candidate "${SLUG}" from the repository.

Read research/CANDIDATE_SCORECARD.md (which covers both rounds) and
iterations/${ITER_LC}/ITERATION_BRIEF.md. Extract this candidate's target buyer,
operational decision, sources used, technical proof, novelty statement, provability
statement, vertical-proof scope, reusable contribution, weakest link, and score.

Also extract from design/SOURCE_AND_COMPLIANCE_LEDGER.md the list of CLEARED source URLs,
and from PORTFOLIO_TRACKING_LOG.md every prior and active concept.

Set found=false if the candidate is not present in the scorecard. Do not write files.`, {
  label: 'load-candidate',
  phase: 'Load',
  model: 'haiku',
  effort: 'low',
  schema: LOAD_SCHEMA,
})

if (!loaded || !loaded.found) {
  return {
    stopped: 'CANDIDATE_NOT_FOUND',
    slug: SLUG,
    action: `Could not locate "${SLUG}" in research/CANDIDATE_SCORECARD.md. Check the slug and re-run.`,
  }
}

const C = loaded.candidate || {}
const CAND_BLOCK = JSON.stringify(C, null, 1)
const CLEARED_BLOCK = JSON.stringify(loaded.clearedSources || [], null, 1)
log(`Loaded "${C.name || SLUG}" (${C.score || '?'}/35). Gating against ${(loaded.clearedSources || []).length} cleared sources.`)

// ---------------------------------------------------------------------------
// Phase 2 - Gate + three adversarial lenses, concurrently.
// ---------------------------------------------------------------------------
phase('Gate')
log('Running uniqueness gate and three adversarial lenses...')

const LENSES = [
  {
    key: 'novelty',
    ask: `Is this a themed variation of an existing portfolio concept, of a sibling candidate, or of a
commercial product? README line 167 disqualifies changing only the website, visual theme,
keyword set, or industry label.

Round 2's leader died on exactly this lens: it reproduced the business-location-monitoring
register row's cross-source identity mechanic under a new industry label. Check whether THIS
candidate reproduces any register-named mechanic the same way.

Also check for commercial prior art shipping the same capability on the same source — but
weigh it correctly: the README scopes the gate to THIS portfolio's completed and active
projects. Commercial prior art is a criterion-7 concern, not automatically a novelty kill.
Do not double-count a penalty already levied in scoring.`,
  },
  {
    key: 'compliance',
    ask: `Attack the compliance story with fetched evidence.

Round 2's leader was killed here by an operative Terms page the clearance agent never
fetched. Fetch the terms for EVERY source this candidate names, including
https://www.find-tender.service.gov.uk/ terms and any linked acceptable-use page, plus
robots.txt. Hunt specifically for any sentence prohibiting automated collection, crawling,
caching, storage, or circumvention of use limitations.

Then test the two BINDING CAVEATS above:
- Does the design as scoped touch PERSONAL data (named officer contacts, sole-trader emails
  or mobiles)? OGL v3.0's grant excludes personal data. If the concept needs those fields,
  refute.
- Does the design require discovering the rate ceiling by probing until it trips, or
  sustaining a rate the service refused? If so, refute.

If the concept is refutable ONLY on a fixable scoping point, still set refuted=true but
list the precise scopeConditions that would make it survivable.`,
  },
  {
    key: 'provability',
    ask: `Attack the provabilityStatement directly. This is the lens that killed BOTH prior leaders.

Round 1: SAM.gov overwrote notices in place, so the pipeline could only grade itself against
its own snapshots — recall had no denominator.
Round 2: the cross-source join key was measured to have an EMPTY intersection, so the
"withheld oracle" had no oracle.

This candidate claims Find a Tender publishes amendments as discrete, independently-fetchable
OCDS releases tagged tenderUpdate / awardUpdate / contractUpdate, retrievable retrospectively
via updatedFrom / updatedTo — giving an external oracle independent of the pipeline's own
capture history.

VERIFY THAT CLAIM EMPIRICALLY. Load WebFetch via ToolSearch and actually call the API:
  https://www.find-tender.service.gov.uk/api/1.0/ocdsReleasePackages?updatedFrom=...&updatedTo=...&limit=...
Confirm with real responses:
- do releases genuinely carry tenderUpdate / awardUpdate / contractUpdate tags?
- does querying a historical window return the SAME releases on repeat calls (a stable oracle),
  or does it reflect only current state?
- can multiple releases for one ocid be retrieved, showing a real revision sequence?
- is there a real DENOMINATOR for an amendment-detection recall metric?

Refute if any headline metric would be unfalsifiable or self-referential. Report the actual
API calls you made in fetchesPerformed.`,
  },
]

const [gate, refs] = await Promise.all([
  agent(`${PREFLIGHT}

ROLE: Portfolio orchestrator (relevance and uniqueness gate).

Apply the README gate to candidate "${SLUG}".

It PASSES only if it adds at least one net-new technical capability AND differs meaningfully
in at least TWO of the seven README dimensions. Verify claimed dimensions against the actual
prior-concept list rather than accepting the candidate's own claims.

Then check the tracking log's candidate/duplication register. It names specific requirements
that make each concept family distinct. Round 1's leader failed because 2 of 5
register-named requirements were absent, and round 2's leader met only 1 of 5. Enumerate
which requirements THIS candidate actually satisfies (registerRequirementsMet) and which it
does not (registerRequirementsMissing). Be strict: a requirement is met only if the candidate
concretely does that thing, not if it could in principle.

Finally set caveatsSatisfied: does the candidate satisfy BOTH binding caveats above
(organisation-level identifiers only; no rate-limit probing)? If it is silent on either,
it does not yet satisfy it — say so in requiredChanges rather than assuming good intent.

CANDIDATE:
${CAND_BLOCK}

CLEARED SOURCES:
${CLEARED_BLOCK}

PRIOR AND ACTIVE CONCEPTS:
${JSON.stringify(loaded.priorConcepts || [], null, 1)}`, {
    label: 'uniqueness-gate',
    phase: 'Gate',
    model: 'opus',
    effort: 'high',
    schema: GATE_SCHEMA,
  }),

  parallel(LENSES.map((l) => () =>
    agent(`${PREFLIGHT}

ROLE: Adversarial reviewer (lens: ${l.key}).

Your job is to REFUTE this candidate, not to appreciate it. ${l.ask}

Default to refuted=true when genuinely uncertain. Use WebFetch/WebSearch to verify claims
about sources rather than reasoning from the description — load them via ToolSearch
("select:WebSearch,WebFetch"). Every decisive finding in rounds 1 and 2 came from actually
fetching a page, never from analysis alone.

Record every URL you fetched in fetchesPerformed.

CANDIDATE:
${CAND_BLOCK}

CLEARED SOURCES:
${CLEARED_BLOCK}`, {
      label: `refute:${l.key}`,
      phase: 'Gate',
      model: 'opus',
      effort: 'high',
      schema: REFUTE_SCHEMA,
    })
  )),
])

const votes = refs.filter(Boolean)
const refuted = votes.filter((v) => v.refuted).length
const lensesLost = votes.filter((v) => v.refuted).length
// Same bar as rounds 1 and 2: gate must pass AND fewer than 2 lenses refute.
const passes = !!(gate && gate.passes) && refuted < 2
const caveatsOk = !!(gate && gate.caveatsSatisfied)

log(`Gate: ${gate && gate.passes ? 'PASS' : 'FAIL'} (caveats ${caveatsOk ? 'satisfied' : 'NOT satisfied'}). Refutations: ${refuted}/${votes.length}.`)

const scopeConditions = votes.flatMap((v) => v.scopeConditions || [])
if (scopeConditions.length > 0) log(`${scopeConditions.length} scope condition(s) proposed by the lenses.`)

// ---------------------------------------------------------------------------
// Phase 3 - Record the verdict. Writes happen either way: a refutation is
// evidence the README requires retaining.
// ---------------------------------------------------------------------------
phase('Record')

const verdict = {
  today: TODAY,
  iteration: ITER,
  candidate: SLUG,
  candidateName: C.name,
  score: C.score,
  gate,
  refutations: votes,
  refutedCount: refuted,
  passes,
  caveatsSatisfied: caveatsOk,
  scopeConditions,
  binding: {
    organisationIdentifiersOnly: 'OGL v3.0 excludes personal data; match and publish organisation-level identifiers (GB-PPON, GB-COH) and organisation names only.',
    noRateLimitProbing: 'Establish the rate ceiling from published guidance or conservative fixed-interval polling; never probe upward until a 403/429 trips, never backoff-and-rotate to sustain a refused rate.',
  },
}

const brief = await agent(`${PREFLIGHT}

ROLE: Portfolio orchestrator (iteration brief update).

Update ${REPO}/iterations/${ITER_LC}/ITERATION_BRIEF.md to record this gate outcome.
Read it first and PRESERVE its existing round-1 and round-2 history sections.

${passes ? `The candidate PASSED. Rewrite the brief so "${SLUG}" is the recommended concept:

- Set the concept, target buyer, operational decision, novelty, net-new capability, scope,
  explicit non-goals, and vertical proof from the candidate specification below.
- Status stays AWAITING_APPROVAL. You may NOT write APPROVED — only the human orchestrator
  crosses that boundary.
- Add "## Gate outcome" recording that the uniqueness gate passed and ${refuted} of
  ${votes.length} adversarial lenses refuted, with each lens's reasoning summarised honestly.
- Add "## Binding scope conditions" containing BOTH caveats verbatim from the data below,
  plus any scopeConditions the lenses proposed. State that these are binding on the build and
  that a build violating them must be stopped.
- Add "## Provability" with the candidate's provability statement and, if the provability
  lens performed live API calls, what those calls actually confirmed.` : `The candidate FAILED (gate passes=${gate && gate.passes}, ${refuted}/${votes.length} lenses refuted).

Do NOT rewrite the brief around it. Instead:
- Keep Status AWAITING_APPROVAL.
- Add or update "## Gate outcome — ${SLUG}" recording the failure, each lens's verdict and
  fatal flaw verbatim, and the gate's registerRequirementsMissing.
- Add "## Where this leaves ${ITER}" stating plainly that all three round-2 candidates and
  both prior leaders have now been examined, which ones were refuted and on what grounds, and
  that the next step is a human decision on direction rather than another automated round.
- List any scopeConditions the lenses proposed that would make a revised version survivable.`}

Unmeasured values stay "TBD". No metric may be presented as measured — no run has occurred.

VERDICT DATA:
${JSON.stringify(verdict, null, 1)}

CANDIDATE SPECIFICATION:
${CAND_BLOCK}`, {
  label: 'write:brief',
  phase: 'Record',
  model: 'sonnet',
  effort: 'high',
  schema: WRITE_SCHEMA,
})

const logUpdate = await agent(`${PREFLIGHT}

ROLE: Portfolio orchestrator (tracking-log update).

Update ${REPO}/PORTFOLIO_TRACKING_LOG.md surgically. PRESERVE ALL EXISTING CONTENT,
including every rejected concept and superseded decision from rounds 1 and 2.

1. Portfolio catalog — update the ${ITER} row for this gate outcome.
   ${passes ? `Concept becomes "${C.name || SLUG}", with its real target buyer and the gate-confirmed net-new capability as Distinct proof. Status stays AWAITING_APPROVAL (the human approval gate is still pending). Notes must state that the uniqueness gate PASSED with ${refuted}/${votes.length} lenses refuting, and that the build is bound by the two scope conditions.` : `Notes must state that "${SLUG}" also failed the gate, with the count of refuting lenses, and that ${ITER} now awaits a human direction decision rather than another automated candidate round.`}

2. Candidate and duplication register — update the "${SLUG}" row with its gate state
   (${passes ? 'RECOMMENDED / gate-cleared' : 'REJECTED'}) and the evidence. Preserve every other row.

${passes ? '' : `3. Rejected or archived concepts — ADD a row for "${SLUG}" with its refutation reasons and a specific "may be reconsidered when" condition drawn from the lenses' scopeConditions.\n`}
${passes ? '3' : '4'}. Iteration decision and handoff log — APPEND a new entry
   "### ${TODAY} - ${ITER} gate outcome for ${SLUG}" recording: which candidate was gated and
   why (it was round 2's untested runner-up), the gate verdict, each adversarial lens's
   verdict and the evidence it fetched, the binding scope conditions, and the next decision.
   Record ONLY real history — the README forbids manufacturing counts or productivity claims.

${passes ? `${'5'}. Shared Shipping Pipeline capability ledger — leave every capability state unchanged. Nothing new has been verified by a RUN; the gate is a decision, not a run.` : ''}

Do not mark anything APPROVED, RELEASED, or VERIFIED that has not actually happened.

VERDICT DATA:
${JSON.stringify(verdict, null, 1)}`, {
  label: 'write:tracking-log',
  phase: 'Record',
  model: 'sonnet',
  effort: 'high',
  schema: WRITE_SCHEMA,
})

return {
  run: '1c',
  iteration: ITER,
  candidate: SLUG,
  candidateName: C.name,
  score: C.score,
  gatePassed: !!(gate && gate.passes),
  caveatsSatisfied: caveatsOk,
  adversarialRefutations: `${refuted}/${votes.length}`,
  overallPass: passes,
  lensVerdicts: votes.map((v) => ({ lens: v.lens, refuted: v.refuted, fatalFlaw: v.fatalFlaw ? String(v.fatalFlaw).slice(0, 400) : null })),
  registerRequirementsMet: (gate && gate.registerRequirementsMet) || [],
  registerRequirementsMissing: (gate && gate.registerRequirementsMissing) || [],
  requiredChanges: (gate && gate.requiredChanges) || [],
  scopeConditions,
  filesWritten: [brief, logUpdate].filter(Boolean).flatMap((r) => r.filesWritten || []),
  nextStep: passes
    ? `Gate cleared. Set ${ITER} to APPROVED in PORTFOLIO_TRACKING_LOG.md, then run ws-build.js with the two binding scope conditions in force.`
    : `"${SLUG}" also failed. All round-2 candidates are now exhausted — this needs a human direction decision, not another automated round.`,
}
