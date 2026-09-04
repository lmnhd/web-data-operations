# Iteration Brief - WS-001

- **Status:** AWAITING_APPROVAL
- **Round:** 2
- **Prepared by:** Portfolio orchestrator (agent role)
- **Prepared (UTC):** 2026-09-02
- **Iteration ID:** WS-001
- **Branch:** main (no iteration branch cut yet; `iteration/ws-001-<project-slug>` to be created on approval per `SOURCE_CONTROL_AND_PUBLIC_ARCHIVE.md`)

> This brief is the approval-gate document required by README.md ("Global tracking log - mandatory preflight" and "Relevance and uniqueness gate"). It records the Round 2 candidate-selection outcome for WS-001: a Round 2 leader that failed the uniqueness gate and all three adversarial lenses, and a Round 2 runner-up recommended in its place. **UPDATE (2026-09-03): the runner-up, `uk-procurement-amendment-monitor`, has now been run through the gate and all three adversarial lenses and also FAILED — see "Gate outcome — uk-procurement-amendment-monitor" and "Where this leaves WS-001" below, appended at the end of this document.** Only the human orchestrator may change Status to APPROVED. Round 1's full history is preserved unmodified in "Round 1 history" rather than erased; the "Gate status" section below is now historical (it describes the gate as not-yet-run) and is preserved rather than rewritten — its outcome is recorded in the appended sections.

---

## Preflight record

Read before drafting, per README "Global tracking log - mandatory preflight": `README.md`, `PORTFOLIO_TRACKING_LOG.md`, `SOURCE_CONTROL_AND_PUBLIC_ARCHIVE.md`, `PHASE_01_DISCOVERY_AND_EVIDENCE_PLAN.md`, `research/UPWORK_DEMAND_MATRIX.md`, `research/CANDIDATE_SCORECARD.md` (both Round 1 and Round 2 sections), and `design/SOURCE_AND_COMPLIANCE_LEDGER.md`.

- Repository: `c:/Users/cclem/Dropbox/Source/Halimede_Concepts/Upwork/Web_Scraping_Data_Operations`, branch `main`.
- Tracking log catalog contains WS-000 (Multi-agent Shipping Pipeline foundation, BUILDING - process/tracking layer, not a data project) and WS-001 (AWAITING_APPROVAL). The rejected/archived table is empty; the candidate/duplication register carries three UNDER_REVIEW/DEFERRED/RECOMMENDED rows, none APPROVED. There is no completed portfolio project to duplicate.
- `design/SOURCE_AND_COMPLIANCE_LEDGER.md` now exists (created this round, 331 lines) recording nine independently cleared sources with fetched licence text and quoted operative sentences, plus disqualified sources and refusals. Its own status flag states explicitly: source clearance is not concept approval.
- `research/CANDIDATE_SCORECARD.md` now contains two rounds. Round 1's three candidates all hit source restrictions discovered only at compliance/adversarial review, after the concepts were already designed. Round 2 inverted that order: sources were cleared first (fetched licence/robots/terms text), and concepts were proposed only on top of the cleared pool. Round 2's leader nonetheless failed the gate and all three adversarial lenses on grounds independent of source legality.

## Round 1 history

Preserved here per the repository rule against erasing rejected concepts or superseded decisions ("the abandoned direction explains the current one"). Full detail lives in `research/CANDIDATE_SCORECARD.md`'s "Round 1" and "Round 1 outcome and lesson" sections; this is the summary needed to understand why Round 2 exists.

**What happened.** Three candidates were scored in Round 1 without first verifying their sources' actual reuse terms: public opportunity intelligence (SAM.gov monitoring, 25/35 — leader), product and price intelligence (23/35 — runner-up), business-location monitoring (21/35). The leader was carried into the gate and adversarial-review stage before its source's terms were checked closely. It **failed the uniqueness gate** (2 of 5 register-named distinctness requirements — provenance, structured qualification — missing) and was **refuted on 2 of 3 adversarial lenses**:

- **Compliance — refuted.** The concept's sole surviving differentiator (document-vs-metadata PDF reconciliation of amendments) depended on SAM.gov's Opportunity Management API, which requires a federal government system account with Contracting Officer/Specialist/Administrator role and IP allowlisting — access this project does not qualify for. SAM.gov's Terms of Use state verbatim: *"Automated data gathering, web scraping tools are prohibited and, if detected, will result in the associated account(s) being denied access to SAM.gov via Login.gov."* The public API's carve-out is scoped to "internal, U.S. Government business purposes," and its non-federal no-role quota (10 requests/day) cannot sustain the polling the concept required.
- **Provability — refuted.** SAM.gov's public Get Opportunities API returns only the latest version of each notice; amendment/revision history exists only behind the same restricted API the compliance lens already excluded. There is no independent ground truth against which amendment-detection recall could be measured, and the concept's own criterion-5 rationale ("checkable against SAM.gov's UI links") was found factually unsupported — the UI link renders only current state.
- **Novelty — not refuted** on its own, but the runner-up promotion made this moot.

The promoted Round 1 runner-up, product and price intelligence, was never itself run through the gate or adversarial lenses (its own recorded weakest link: the only fully compliant sources found were two synthetic sandbox sites, books.toscrape.com and sandbox.oxylabs.io, with explicit "no real meaning" / randomly-assigned-data disclaimers — two natural real-catalog alternatives, webscraper.io and scrapingcourse.com, were checked and rejected on verified `robots.txt` `Disallow` conflicts).

**The lesson that produced Round 2.** All three Round 1 killers — SAM.gov's verbatim scraping prohibition, the Google Places API caching ban, and the synthetic-sandbox "no real meaning" limitation — were sitting in pages that could have been fetched *before* the concepts were scored, not discovered by bad luck. The pattern in every case was: **concept invented first, source checked afterward.** Round 2 inverted that sequence. See "Cleared sources" below.

## How this iteration reached its Round 2 recommendation

A dedicated source-and-compliance pass fetched (not inferred) four things per candidate source before any concept was allowed to be proposed on it: the actual licence text, the actual Terms of Use, `robots.txt`, and whether an official API or bulk-download mechanism exists. Nine sources cleared this test independently (see "Cleared sources"). Three new candidates were then scored, each built only on the cleared pool:

| Candidate | Score /35 |
|---|---:|
| `uk-public-buyer-cross-source-resolution` (Find a Tender + Contracts Finder entity resolution) | 28 (leader) |
| `uk-procurement-amendment-monitor` (Find a Tender change/amendment monitoring) | 27 (runner-up) |
| `uk-tender-document-reconciler` (Find a Tender PDF-vs-OCDS reconciliation) | 25 |

**The Round 2 leader failed, on grounds independent of source legality this time — the sources themselves remained cleared.**

- **Uniqueness gate: FAILS.** Checked against the `PORTFOLIO_TRACKING_LOG.md` register row "Public opportunity intelligence" (the same family as the Round 1 leader), the concept covered only 1 of 5 named distinctness requirements (provenance) — *fewer* than Round 1's leader, which covered 3 of 5 and still failed. It also silently reproduced 2 of 4 distinctness requirements already claimed by the register's separate Business-location-monitoring row, without disclosing the collision.
- **Novelty lens: REFUTED.** The concept's matching problem (cross-source identity resolution, no shared key) is the same structural mechanic already assigned to the Business-location-monitoring register row, with only the website and industry label changed — precisely what README line 167 disqualifies. Worse, fetched primary UK government guidance (GOV.UK PPN 019) states verbatim that dual publication on Contracts Finder is being retired ("there should be no ongoing requirement to publish opportunity notices on Contracts Finder after 25 February 2025"), meaning the "no shared key" problem is a closing transitional artifact of a migration, not an intrinsic engineering problem — and free commercial Apify actors already ship the same deduplication as a default-on flag.
- **Compliance lens: REFUTED.** The clearance had not fetched the operative Contracts Finder/Find a Tender Terms and Conditions page, which bars "using manual or electronic means to avoid any use limitations placed on a System" — directly implicated by the concept's own plan to discover an undocumented rate ceiling by probing until it trips. Independently and more decisively: OGL v3.0 explicitly excludes "personal data" from its licence grant, and live payloads fetched during review showed the concept's entity-resolution method (name/address/contact matching) is unavoidably built on personal data — named officer contacts with direct-dial numbers, and sole-trader supplier contacts at personal Gmail addresses and personal mobile numbers.
- **Provability lens: REFUTED.** Measured from live API payloads (100 releases per source, two windows), the two sources' buyer-identifier schemes have an **empty intersection** — zero shared (scheme, id) pairs. The concept's claim that OCID was "deliberately withheld from the matcher to avoid a leaked oracle" presumes an oracle that does not exist (OCID namespaces are disjoint by construction). With no coded cross-source identifier, the only surviving match signal is the buyer name string — the same signal the matcher and the human labeler would both use, making precision/recall self-referential. This reproduces Round 1's unfalsifiable-metric failure in a new source pair.

Because the leader failed the gate and all three adversarial lenses, this brief does not recommend `uk-public-buyer-cross-source-resolution`. The finding is retained in `research/CANDIDATE_SCORECARD.md` and mirrored into `PORTFOLIO_TRACKING_LOG.md` so it is not silently rediscovered.

**Round 2 runner-up recommendation: `uk-procurement-amendment-monitor` (27/35)**, referred to below as **change-monitoring**. This concept was scored in the same Round 2 pass but has **not yet been run through the uniqueness gate or the three adversarial lenses**. See "Gate status" below — this is the central caveat of this brief.

---

## Target buyer

TBD in precise wording pending the gate run named below. Provisionally, based on demand evidence: small contractors, consultants, and bid-pursuit/BD teams who need to track live UK central-government procurement opportunities for material changes (amendments, deadline shifts, status changes) without manually re-checking each tracked tender. This mirrors the demand pattern evidenced for SAM.gov-style contract monitors and GovWin IQ (`research/UPWORK_DEMAND_MATRIX.md` row 31, row 36) transplanted to a UK source that, unlike SAM.gov, cleared the Round 2 licence/robots/terms check for change-monitoring use (see "Cleared sources").

## Operational decision enabled

TBD in precise wording pending the gate run. Provisionally: an amendment or deadline change on a tracked UK central-government tender should surface as a reviewable, dated alert an operator can act on (respond before a shortened deadline, re-assess bid viability after a scope change) without polling Find a Tender manually.

## Demand evidence

Linked: [`research/UPWORK_DEMAND_MATRIX.md`](../../research/UPWORK_DEMAND_MATRIX.md).

Specific supporting rows (2026-09-02 access date):

- Row 31 — SAM.gov Government Contract Monitor (Apify actor, DIRECT_POSTING tier): packaged recurring monitoring product for federal procurement, "recommended because federal opportunities often have tight response windows" — the same buyer need (deadline/change monitoring on public procurement) this concept targets, on a different, UK, source.
- Row 36 — GovWin IQ (AGGREGATE_REPORT tier): analyst-curated B2G opportunity intelligence platform, continuously collecting government data; corroborates recurring change-monitoring as a commercially validated pattern in this category.
- Matrix synthesis: "Recurring monitoring/change-detection is commercially validated at the product level, separate from one-off Upwork gigs" (matrix line 45).

Demand gap carried forward honestly, not estimated over: no UK-specific (Find a Tender / Contracts Finder) monitoring posting was located in this pass — the demand evidence for this exact buyer problem is US-federal-procurement-shaped (SAM.gov, GovWin IQ), transplanted to a UK source by inference, not directly evidenced for the UK market. This is a genuine open question, not resolved by this brief — see "Open questions for the approver."

## Portfolio gap addressed

TBD in precise wording pending gate re-run and Manifest drafting. Provisionally: WS-000 has no data project; there is no released or active portfolio entry demonstrating recurring change/amendment monitoring against a government procurement API with an independently-verifiable (non-self-referential) ground-truth denominator — the exact capability that sank the Round 1 SAM.gov leader on provability grounds.

## Novelty versus completed and active projects

Against WS-000 (the only non-candidate catalog entry), novelty is trivially satisfied — WS-000 has no buyer data problem, sources, extraction, normalization, or delivery destination of its own to compare against.

Against the Round 2 sibling candidates, `research/CANDIDATE_SCORECARD.md` records this concept as covering a distinct normalization/matching problem (incremental polling against a high-water mark plus OCID-based timeline grouping, i.e. **temporal versioning within one source**) compared with `uk-public-buyer-cross-source-resolution`'s cross-source identity resolution and `uk-tender-document-reconciler`'s document-vs-metadata reconciliation.

**This has NOT been independently checked against the `PORTFOLIO_TRACKING_LOG.md` candidate/duplication register the way the Round 2 leader was.** That register's "Public opportunity intelligence" row is the governing row for any UK-procurement-monitoring concept (same buyer problem, same source family as SAM.gov) and names five distinctness requirements: provenance, structured qualification, solicitation documents, amendments, deadline change tracking. The concept as scored covers amendments and deadline change tracking; provenance, structured qualification, and solicitation documents have not been confirmed in scope. This gap is not resolved here — see "Gate status."

## Net-new technical capability

TBD — to be confirmed by the gate re-run. Candidate capability from the Round 2 scoring pass: incremental change/amendment detection on live UK central-government procurement notices, using cursor pagination against a high-water mark (`updatedFrom`/`updatedTo`), OCID-based timeline grouping across an entity's release history, and tag-based event classification (`tenderUpdate`, `awardUpdate`, `tenderCancellation`, etc.), benchmarked against a denominator drawn from an **independent** query of the same API over a fixed date-range window — decoupled from the pipeline's own capture log — plus a manual-review reconciliation pass against raw payload. This provability design is materially different from, and was not broken by the same finding as, the refuted leader's approach: it does not depend on a cross-source join key, so the leader's fatal "empty intersection" finding does not apply to it. It has not itself been tested against a refutation lens.

## Shared capabilities reused

Per the tracking log's Shared Shipping Pipeline capability ledger, WS-001 is the introducing iteration for: source/compliance ledger (now `IN_PROGRESS`, ledger exists but not yet `VERIFIED` because no concept built on it has cleared the gate), immutable raw capture and provenance, normalization and validation stages, reason-coded review outputs, checkpoint/retry/resume behavior, reproducible exports and run report, benchmark and claim verification, and the reviewer-facing Project Manifest. All remain `PLANNED` or `IN_PROGRESS`, none `VERIFIED` — nothing is being duplicated by proceeding.

## Proposed scope

TBD in final detail pending the gate re-run. Provisional scope, not yet approved for build:

- Collect UK central-government procurement notices from the Find a Tender OCDS API (`ocdsReleasePackages`) for a bounded seed set of ocids (~100-200), polling incrementally against `updatedFrom`/`updatedTo`.
- Group releases by OCID into a per-entity timeline; classify each new release by its OCDS tag (planning/tender/tenderUpdate/award/awardUpdate/tenderCancellation, etc.).
- Detect and surface amendments and deadline changes as reason-coded, reviewable alerts (change confirmed / no change / review-needed), never silent overwrites.
- Maintain field-level provenance (source URL, retrieval timestamp, content fingerprint, OCDS release ID) on every captured field — **not yet confirmed in scope; required if the register-collision finding above is to be resolved.**
- Benchmark recall/precision/latency against a denominator independently queried from the same API over a fixed date-range window, decoupled from the pipeline's own capture log, reconciled against raw payload for a bounded ocid sample by manual review.
- Produce a reproducible run report and CSV/JSON export; explicitly exclude persisting or matching on named-individual contact fields (see "Cleared sources" personal-data notes).

## Explicit non-goals

- No authentication bypass, CAPTCHA evasion, or defeat of any access control, on any source.
- No persisting, matching, or publishing named-individual contact fields (buyer/supplier contact name, personal email, personal phone) — the Round 2 leader was refuted in part because OGL v3.0 excludes "personal data" from its grant and the UK procurement sources carry real personal contact fields (officer names/direct-dial numbers; sole-trader personal Gmail addresses and mobiles). Contact fields, if collected at all, are treated as organisational-role data only, per the ledger's personal-data-risk notes.
- No cross-source entity resolution between Find a Tender and Contracts Finder buyer identities — that mechanic was independently refuted (empty scheme intersection, no shared key) and must not be silently reintroduced under this brief's approval.
- No "avoiding a use limitation" behavior: no probing an undocumented rate ceiling to discover it by triggering 403/429 responses repeatedly, and no retry/backoff pattern designed specifically to keep collecting past a rate-limit signal. Any rate-limit ceiling stays literally TBD until confirmed by the source owner or by a single, disclosed, conservative empirical observation — not an adversarial probe.
- No claim that population-level amendment rate, recall, or coverage is known — only the fixed-window, reconciled-sample metrics defined in "Provability" below.
- No fabricated demand, benchmark, or coverage figures; every metric stays literally `TBD` until produced by a recorded run.
- No large-scale infrastructure, paid data acquisition, or personal-data collection without a new explicit decision (restated fully below).

## Assigned roles and work claims

| Role/agent | Claimed task | Status |
|---|---|---|
| Portfolio orchestrator | Coordinate WS-001 Round 2 candidate selection, rewrite this brief, own the approval gate | Active (this brief) |
| Demand and concept agent | Produced Round 2 candidate scoring in `research/CANDIDATE_SCORECARD.md` | Complete for this pass |
| Source and compliance agent | Cleared 9 sources with fetched licence/robots/terms text in `design/SOURCE_AND_COMPLIANCE_LEDGER.md`; **has not yet re-verified `change-monitoring`'s specific rate-limit/ToS claims against the operative Contracts Finder/Find a Tender Terms and Conditions page** (the same gap that contributed to the leader's compliance refutation) | Partially complete — gap flagged |
| Gate/adversarial-review agent(s) | Ran gate + 3 lenses against the Round 2 leader (`uk-public-buyer-cross-source-resolution`); **has not yet run the same pass against `change-monitoring`** | Not started for recommended concept |
| Data and architecture agent | Not yet engaged for this iteration | Not started |
| Build agents | Not yet engaged; no build authorized by this brief | Not started |
| Verification and evidence agent | Not yet engaged | Not started |
| Release and portfolio agent | Not yet engaged | Not started |

No file changes beyond this brief and (if the orchestrator directs it) the tracking-log entry are authorized by this document.

## Dependencies and blockers

- **Blocking:** `change-monitoring` has not been run through the uniqueness gate or the three adversarial refutation lenses that the Round 2 leader underwent. This brief recommends it as the strongest remaining evidence-scored candidate, not as a gate-passed concept. See "Gate status."
- **Blocking:** the concept's own recorded weakest link is that its write-up never itself fetched or quoted licence/ToS text for Find a Tender specifically (though that text exists, verified, in `design/SOURCE_AND_COMPLIANCE_LEDGER.md`) — and the compliance refutation of the sibling leader found the *operative* Terms and Conditions page (`contractsfinder.service.gov.uk/Home/TermsAndConditions`, which governs both Find a Tender and Contracts Finder) had not been fetched at all during clearance. This gap must be closed — by fetching that exact page against this concept's specific design — before a gate run can be trusted.
- **Blocking:** the numeric rate-limit ceiling for the Find a Tender API remains completely undocumented (`TBD`). The compliance refutation of the sibling leader found that discovering this ceiling by probing until it triggers a 429 is itself a Terms-and-Conditions violation ("using manual or electronic means to avoid any use limitations"). Any build must use a conservative, disclosed, non-adversarial polling cadence and record the ceiling as TBD rather than discover it by force.
- **Not blocking, but tracked:** the UK-specific demand evidence gap noted above (no UK Find a Tender / Contracts Finder monitoring posting located; the buyer pattern is inferred from US SAM.gov / GovWin IQ evidence).
- No branch/file collisions found; tracking log's active-work-claims table shows only the orchestrator's own Phase 1 coordination task.

---

## Cleared sources

Full detail, fetch lists, and reproducible operative quotes: [`design/SOURCE_AND_COMPLIANCE_LEDGER.md`](../../design/SOURCE_AND_COMPLIANCE_LEDGER.md). **The build may use no other source than the ones cleared in that ledger.** Any source not listed there — including any not-yet-fetched page, however similar it looks to a cleared one — is out of scope until it is independently cleared by the same fetch-and-quote method and added to the ledger.

The source relevant to `change-monitoring` specifically:

| Source | Owner | Licence | Operative quote (fetched, verbatim) | Access | Retains history | Personal-data risk |
|---|---|---|---|---|---|---|
| [find-tender.service.gov.uk](https://www.find-tender.service.gov.uk) | UK Cabinet Office / Crown Commercial Service | Open Government Licence v3.0 | "a worldwide, royalty-free, perpetual, non-exclusive licence to... exploit the Information commercially and non-commercially." | Public OCDS REST API (`ocdsReleasePackages`, `ocdsRecordPackages`), unauthenticated reads; daily bulk XML ZIP | **True** — `ocdsRecordPackages` retains the full releases array per procurement process, not latest-state-only. This is the specific property that gives `change-monitoring` a real denominator, unlike the SAM.gov source that sank the Round 1 leader. | Named contracting-authority contact (business role) in Section I of each notice — **must be excluded from persistence/matching per this brief's non-goals**, not merely because it is inconvenient but because OGL v3.0 excludes "personal data" from its grant. |

**Caveat carried forward from the Round 2 gate/adversarial findings, not smoothed over:** the compliance refutation of the sibling leader found that the *operative Terms and Conditions* page governing both Find a Tender and Contracts Finder (`https://www.contractsfinder.service.gov.uk/Home/TermsAndConditions`) was not among the pages fetched during the original Find a Tender clearance in the ledger. That page bars "using manual or electronic means to avoid any use limitations placed on a System, such as access and storage restrictions" — directly relevant to how this concept's polling cadence and rate-limit handling must be designed. This page must be fetched and its findings folded into the ledger before build, even though the concept's design (independent-denominator benchmarking, no cross-source matching, no adversarial rate-limit probing) appears structurally compatible with what is currently known of that clause.

## Provability

This section exists because the Round 1 leader was killed by an unfalsifiable metric (SAM.gov: no independent record of amendments), and the Round 2 leader was killed by the same failure mode wearing a different source (Find a Tender + Contracts Finder: no shared cross-source identity key, so precision/recall were self-referential). `change-monitoring`'s design was scored specifically because it avoids both failure modes — but this has not been independently verified by an adversarial pass. Recorded here exactly as scored, so the gate re-run can test it rather than take it on faith:

- **Ground-truth method:** recall, precision, and latency are measured against a denominator drawn from an **independent** query of the same Find a Tender API, filtered by the same `updatedFrom`/`updatedTo` date-range window used for the benchmark period, but issued and captured **separately from** the pipeline's own incremental capture log — i.e., a second, independently-run query against the same live source, not a second source and not the pipeline grading its own prior output. This is a materially weaker independence guarantee than a true third-party ground truth (both the pipeline and the "independent" check ultimately read the same underlying API state), and that limitation should be stated plainly in any Manifest, not implied away.
- **Denominator per rate metric:**
  - *Recall* (did the pipeline catch every amendment/change event in the window?): denominator = count of tenderUpdate/awardUpdate/tenderCancellation/etc.-tagged releases returned by the independent date-range query for the same ocid set and window; numerator = count of those same releases the pipeline's incremental capture actually recorded.
  - *Precision* (are the pipeline's reported "change" alerts real?): denominator = count of alerts the pipeline raised in the window; numerator = count confirmed correct by manual review against the raw OCDS payload.
  - *Latency* (how long between a change posting and the pipeline detecting it): measured only for changes where the independent query's own timestamp can serve as the posted-time reference; not claimed for changes without such a timestamp.
  - *Population-level amendment rate* (how often UK central-government tenders get amended, in general): explicitly **not claimed** — the benchmark covers only the bounded seed set (~100-200 ocids) over the fixed window, and this scope limit must be stated, not implied away, in any published claim.
- **What would falsify each claim:** a recall claim is falsified if the independent date-range query surfaces a tagged update release for a tracked ocid that the pipeline's own capture log does not contain. A precision claim is falsified if manual review of the raw payload for an alerted change finds no actual field-level difference from the prior captured state (a false positive). A latency claim is falsified if the independently-queried posted timestamp precedes the pipeline's detection timestamp by more than the stated tolerance for a reviewed sample item. The whole provability design is falsified at the source level if a future fetch of the Find a Tender API shows `ocdsRecordPackages` does **not** in fact retain a full releases array (contradicting the ledger's `retainsHistory: true` finding) — that finding should be re-confirmed, not assumed permanent, before build.

## Proposed vertical proof

The smallest end-to-end slice — collection through verified delivery:

1. **Source:** Find a Tender OCDS API (`ocdsReleasePackages`), the single cleared source in scope for this concept — no Contracts Finder, no cross-source matching.
2. **Seed set:** a bounded set of ocids (~100-200), selected by a fixed, disclosed criterion (e.g., a date-range slice of recent tender notices), not cherry-picked for favorable results.
3. **Collect:** incremental polling against a high-water mark (`updatedFrom`/`updatedTo`), over a real calendar-week window, at a conservative, disclosed, non-adversarial cadence (no probing to find the undocumented rate ceiling).
4. **Provenance:** every captured release carries source URL, retrieval timestamp, content fingerprint, and OCDS release ID.
5. **Group and classify:** group releases by OCID into a per-entity timeline; classify each new release by its OCDS tag.
6. **Detect and report:** produce a reason-coded change report (amendment confirmed / deadline changed / no change / review-needed) plus a reproducible run report (attempted/collected/rejected/retried counts, elapsed time).
7. **Benchmark:** run the independent date-range query described in "Provability" over the same window and ocid set; compute recall/precision against it; manually reconcile a bounded sample against raw payload.
8. **Deliver:** CSV/JSON export of the captured timeline, the change report, and the benchmark result, with named-individual contact fields excluded per the non-goals above.

This slice deliberately excludes cross-source matching, document/attachment reconciliation, structured eligibility qualification, and any second source — those are later-iteration expansions (or, per the gate finding on the register-collision risk, may need to be added to this same concept before it can clear the gate — see "Gate status").

---

## What approval authorizes

Approving this brief (Status change to APPROVED, by the human orchestrator only) authorizes:

- Running the relevance-and-uniqueness gate and the novelty/compliance/provability refutation lenses against **`uk-procurement-amendment-monitor` (change-monitoring)** specifically, using the same rigor already applied to the twice-refuted leaders in Rounds 1 and 2 — **this is mandatory, not optional, before any build begins.**
- Fetching and folding into `design/SOURCE_AND_COMPLIANCE_LEDGER.md` the operative Contracts Finder/Find a Tender Terms and Conditions page (`https://www.contractsfinder.service.gov.uk/Home/TermsAndConditions`), which the compliance refutation of the sibling leader found was missing from the original clearance.
- Producing the remaining Phase 1 workstream deliverables scoped to `change-monitoring`, **conditional on it clearing the gate re-run**: `design/DATA_CONTRACT.md`, `design/PROOF_AND_BENCHMARK_SPEC.md`, `design/ARCHITECTURE_BRIEF.md`, `portfolio/THREE_PAGE_STORYBOARD.md`.
- Building the proposed vertical proof described above **only after** `change-monitoring` has independently passed its own uniqueness gate and adversarial review — this brief does not pre-clear that gate.
- Creating the iteration branch `iteration/ws-001-<project-slug>` per `SOURCE_CONTROL_AND_PUBLIC_ARCHIVE.md` once a project slug is set and the gate has passed.

## What approval does NOT authorize

Restating the PHASE_01 approval-gate boundary verbatim in substance: **Phase 2 must not expand into authentication bypass, large-scale infrastructure, paid data acquisition, or collection of sensitive personal information without a new explicit decision.**

Concretely, this brief does not authorize:

- Bypassing authentication, defeating CAPTCHAs, or evading any access control on any source, including Find a Tender.
- Probing an undocumented rate ceiling by deliberately triggering repeated 403/429 responses to discover it, or building retry/backoff logic specifically designed to keep collecting past a rate-limit signal — the Round 2 compliance refutation identified this pattern as "using manual or electronic means to avoid any use limitations," a Terms-and-Conditions violation.
- Persisting, matching, or publishing named-individual contact fields from any UK procurement source (officer names, direct-dial numbers, personal email addresses, personal mobile numbers) — OGL v3.0 excludes personal data from its grant, and this was an independently fatal finding against the Round 2 leader.
- Reintroducing cross-source entity resolution between Find a Tender and Contracts Finder buyer identities under this brief's approval — that mechanic was independently refuted this round (empty scheme intersection measured from live payloads) and stays refuted unless a future iteration finds a genuine shared key.
- Standing up large-scale scraping infrastructure (distributed crawling, proxy rotation at scale, dedicated hosting) beyond what a single bounded vertical-proof seed set requires.
- Any paid data acquisition (paid APIs, paid datasets, paid proxy/anti-bot-bypass services) without a new explicit decision recorded in the tracking log.
- Collecting sensitive personal information of any kind.
- Treating `uk-public-buyer-cross-source-resolution` or the Round 1 SAM.gov concept as re-approved by implication — both remain failed/deferred pending the specific fixes recorded in `research/CANDIDATE_SCORECARD.md`; reviving either requires a new gate pass, not silent reuse of this approval.
- Moving WS-001 to `APPROVED` status without first re-running the gate and all three adversarial lenses against `change-monitoring` — see "Gate status" immediately below.

---

## Gate status

**The recommended concept, `uk-procurement-amendment-monitor` (change-monitoring), has NOT cleared the relevance-and-uniqueness gate.** It has not been run through that gate at all, nor through the novelty, compliance, or provability adversarial lenses. It is the highest-scoring candidate that has *not yet been refuted*, not a candidate that has been *tested and survived*. Two prior leaders in this same iteration — the Round 1 SAM.gov concept and the Round 2 `uk-public-buyer-cross-source-resolution` concept — both scored higher than their respective runner-ups and both failed decisively once actually tested. There is no basis to assume `change-monitoring` will behave differently merely because it scored well or because its provability design was constructed to avoid the specific failure modes that sank the other two.

**Approval of this brief must include re-running the gate against `change-monitoring` before any build work begins**, specifically checking it against:

1. The `PORTFOLIO_TRACKING_LOG.md` "Public opportunity intelligence" register row (provenance, structured qualification, solicitation documents, amendments, deadline change tracking) — the concept currently covers 2 of 5 as scored (amendments, deadline change tracking); provenance is claimed in this brief's proposed scope but not yet confirmed by an adversarial pass, and structured qualification and solicitation documents are out of scope entirely.
2. The novelty lens, specifically for whether "amendment/deadline monitoring on a single source via incremental polling" is meaningfully distinct from existing SAM.gov-style monitor products (the demand evidence itself cites one, row 31) rather than the same product pattern on a different government website — the exact concern the novelty lens raised (and did not fully resolve) against the Round 1 SAM.gov leader before it was displaced on other grounds.
3. The compliance lens, specifically re-fetching the Contracts Finder/Find a Tender Terms and Conditions page identified as missing from the original clearance, and confirming this concept's specific polling design does not fall under "using manual or electronic means to avoid any use limitations."
4. The provability lens, specifically stress-testing whether the "independent" date-range query described above is actually independent enough to serve as ground truth, given that it reads the same underlying live API state as the pipeline's own capture — this is a real, disclosed weakness in the design as scored, not a resolved question.

Until that gate run is complete and recorded, WS-001 remains `AWAITING_APPROVAL` in substance even if a human approves this brief — approval authorizes the gate run, not the build.

---

## Open questions for the approver

Only genuine decisions requiring human judgment, not busywork:

1. **Accept the runner-up promotion and its unresolved gate status?** The Round 2 leader (`uk-public-buyer-cross-source-resolution`) failed the uniqueness gate and all three adversarial lenses. This brief recommends promoting `uk-procurement-amendment-monitor`, the next-highest-scored Round 2 candidate (27/35 vs. 28/35), on the same provisional basis as the Round 1 runner-up promotion — with the explicit understanding that this candidate has not itself been tested and two prior leaders in this iteration both failed once tested. Does the approver accept this promotion-pending-gate-run, or prefer the orchestrator attempt required fixes on either failed leader (SAM.gov or the cross-source-resolution concept) before re-scoring, or direct a Round 3 source/concept search instead?
2. **Accept UK-inferred demand evidence?** The demand evidence directly supporting change-monitoring is US-federal-procurement-shaped (SAM.gov Contract Monitor, GovWin IQ) and transplanted to a UK source by inference — no UK-specific Find a Tender/Contracts Finder monitoring posting was located. Is this an acceptable evidentiary basis for a foundational, capability-introducing WS-001 project, or should the approver direct further UK-specific demand research before the gate run proceeds?
3. **Business-location monitoring as a fallback?** That candidate scored lowest in Round 1 (21/35) and was never gated. It remains UNDER_REVIEW in the register as an ungated fallback. Should it be considered further for WS-001 if `change-monitoring` also fails its gate run, or formally set aside for a later iteration?
4. **Scope of "provenance" if added to close the register-collision gap.** This brief's proposed scope tentatively adds field-level provenance to address the register's "Public opportunity intelligence" distinctness requirement. Should provenance be treated as in-scope for the vertical proof from the start (larger initial build), or added only if the gate run specifically flags its absence as blocking (smaller initial build, provenance as a fast-follow)?

---

## Gate outcome — uk-procurement-amendment-monitor

**Recorded 2026-09-03.** The gate run demanded by "Gate status" above has now occurred. **Result: FAILS (`passes: false`).** Score was 27/35. All three adversarial lenses returned `refuted: true` (3/3). Both binding caveats were tested; one is satisfied, one is not (`caveatsSatisfied: false`).

### Relevance-and-uniqueness gate

- **Test 1 — net-new technical capability: PASSES.** Verified against the actual catalog (WS-000 is process infrastructure with no data capability of its own) and the Shared Shipping Pipeline capability ledger (no change-detection, temporal-versioning, provenance, or benchmark capability recorded above `PLANNED`). FETCHED confirmation that `ocdsRecordPackages` returns a multi-release array per ocid means the denominator that never existed for SAM.gov does physically exist here.
- **Test 2 — two-of-seven dimensions: PASSES**, and on substance rather than vacuously: monitoring/change-detection behavior, the matching problem (OCID process identifier vs. cross-source identity), and benchmark evidence (independent re-query vs. two refuted self-referential designs) all differ from the rejected concepts on real grounds.
- **Test 3 — candidate/duplication register: FAILS, and decisive.** Checked strictly against the governing register row, "Public opportunity intelligence" (Round 1, SAM.gov — same buyer, same source family, same lead-discovery overlap warning):
  - **MET (3 of 5):** Amendments (core mechanic — OCID timeline grouping plus tag-based classification of tenderUpdate/awardUpdate/tenderCancellation releases, resting on a FETCHED-confirmed full releases array per ocid). Deadline change tracking (committed in verticalProofScope with a named falsification condition). Provenance (four specific fields — source URL, retrieval timestamp, content fingerprint, OCDS release ID — carried on every captured release; this is the requirement whose absence contributed to the Round 1 leader's failure, and it is now a build item here, not an aspiration).
  - **MISSING (2 of 5), and decisive:**
    - **Structured qualification** — nothing in the candidate performs deterministic eligibility assessment (CPV code, lot, value threshold, buyer type, place of performance) yielding accepted/rejected/review-needed states about bid fit. The candidate's "change confirmed / no change / review-needed" reason codes classify CHANGE EVENTS, not opportunity eligibility — these are different objects and the gate explicitly declined to blur them together. Absent in the Round 1 leader, absent in the Round 2 leader, absent here — three candidates in a row.
    - **Solicitation documents** — excluded by deliberate design (the capability was split off to the sibling `uk-tender-document-reconciler`), despite Find a Tender being recorded `exposesDocuments: true` in the ledger. A scoping choice, not a source constraint.
  - Coverage is 3 of 5 — numerically **identical** to the Round 1 leader's 3 of 5, which the register already records as a gate failure at that exact count. Better than the Round 2 leader's 1 of 5, but not a pass.
- **Duplication risk: MEDIUM, with one undisclosed collision.** Against the Round 1 register row the candidate ties a documented failure. Separately and not disclosed by the candidate's own noveltyStatement: it reproduces "scheduled monitoring" from the Business-location-monitoring row's four named distinctness requirements (loosely analogous field-level change detection), though it does NOT reproduce that row's two load-bearing mechanics (cross-source entity resolution and conflict review are explicit non-goals) — a materially smaller collision than the Round 2 leader's 2 of 4, but still undisclosed. The candidate's noveltyStatement differentiates only against its two Round 2 siblings and never mentions the Business-location-monitoring row at all.

### Binding caveat 1 — organisation-level identifiers only

**SATISFIED**, and affirmatively rather than by silence. The candidate states a field-level data contract excluding named-individual contact fields per the OGL personal-data exclusion, and its matching mechanic (group by OCID, diff by OCDS tag) never reads `contactPoint` at all — organisation identifiers (GB-PPON, GB-COH) are independently sufficient. The round-2 compliance refutation (which depended on name/address/contact matching) does not reach this design. One qualification carried forward from the novelty lens for future attention: a live tenderUpdate payload was found to carry a named NHS officer's work email inside an amendment's free-text `oldValue.text` prose blob — i.e., inside the unstructured change body the concept must store and diff to function, not inside a structured contact field a schema can exclude. This is not a caveat-1 failure as scored (the field-level contract covers structured fields), but it is a gap a build must close (see scopeConditions below).

### Binding caveat 2 — no rate-limit probing

**NOT SATISFIED.** The candidate's own provabilityStatement defers all rate-limit numbers "pending fetched verification of the operative Terms and Conditions page." That verification has now been performed and the escape hatch is empirically closed:
- `https://www.contractsfinder.service.gov.uk/Home/TermsAndConditions` — FETCHED. Carries the prohibition ("Using manual or electronic means to avoid any use limitations placed on a System, such as access and storage restrictions") and a previously-unnoticed "Interception" clause ("Monitoring of data or traffic, other than for approved business use, on Find a Tender without permission"), but publishes **no numeric rate ceiling of any kind**.
- `https://www.find-tender.service.gov.uk/apidocumentation` and `/apidocumentation/api-how-to-guide` — FETCHED. No rate limit, quota, or fair-use polling frequency is published anywhere on the public read path; the how-to guide documents only the licensed submission API (SIRSI account, API licence, CDP API key), not the read path this concept uses. The only published rate behavior is reactive (`429` + `Retry-After`, no threshold stated).

So no published ceiling exists to derive a number from, and the candidate's own stated plan to obtain one from that page cannot succeed. Compounding this, the candidate's own recorded scoring basis (`research/CANDIDATE_SCORECARD.md` criterion 2, and `design/SOURCE_AND_COMPLIANCE_LEDGER.md` line 111) describes the ceiling as "only empirically discoverable at build time" / "should be confirmed empirically at build time" — language that names the barred probing pattern. This brief's own non-goals already forbid it, but the candidate as submitted does not carry that constraint in its own design, and its scoring rationale contradicts it.

### Adversarial lenses (3/3 refuted)

- **Novelty — REFUTED**, on two independent grounds. (1) Register collision: the candidate is register row "Public opportunity intelligence"'s amendments + deadline-change-tracking + provenance (3 of 5), minus the two requirements whose absence already failed the Round 1 leader, with the source swapped SAM.gov → Find a Tender and the industry label (government procurement) held constant — the same error pattern that sank the Round 2 leader. Round 1's own novelty lens had left a standing pre-registered condition that descoping the PDF/document sub-feature would collapse this family into "another SAM.gov watcher" and should be re-refuted — this candidate arrives with that collapse already executed (documents are explicitly out of scope, split to the sibling). (2) Measured, not reasoned: 300 live releases fetched across three days show Find a Tender already publishes the change events the concept claims to "detect" — change-typed tags, populated `amendments` arrays with `oldValue`/`newValue` pairs, and all 8 sampled `unstructuredChanges` entries carrying both old and new values plus a `where.section` pointer. One deadline change arrived as published prose naming the new date directly. This inverts the concept's own stated novelty premise (built against SAM.gov's destroyed version history); the source here already did the versioning, so "OCID timeline grouping" and "tag classification" reduce to a GROUP BY and a field read. Only 17 of 275 distinct ocids had more than one release in-window.
- **Compliance — REFUTED**, on the rate-ceiling caveat (caveat 2 above). Personal-data caveat 1 was found survivable (see above) — the refutation rests on the rate-limit point alone, which is fatal because the concept's own remedy (fetch the T&Cs page to learn the ceiling) was tested and returned nothing, and the only lawful route (published guidance) is closed. The compliant path (data.gov.uk daily bulk XML ZIPs, verified as per-day files bundled into monthly datasets) and the valuable path (sub-day amendment/deadline-shift alerting) are structurally disjoint.
- **Provability — REFUTED**, on the denominator. The claimed recall denominator ("count of amendment/change-tagged releases") is a tag count, not a semantic-change count. Measured: one ocid (`ocds-h6vhtk-06d396`) returned 7 releases, 6 tagged `tenderUpdate`, with `tender.tenderPeriod.endDate` **identical** across all seven. Releases are full snapshots, not deltas; no `amendments` array, no rationale field, and the `versionedRelease` object (the one structure that would localise field-level change) is present on some records and absent on others. The concept's own stated precision falsifier ("falsified if manual review finds no actual field-level difference from prior state") is already tripped by this measurement. The underlying oracle mechanism itself (OCID-based `ocdsRecordPackages` history, cursor pagination, repeat-call stability) was tested and found genuinely sound — this is a narrower, metric-definition failure, not a repeat of Round 1/2's structural failures.

### registerRequirementsMissing (verbatim from the gate)

1. **Structured qualification** — missing, and decisive. No deterministic eligibility assessment (CPV code, lot, value threshold, buyer type, place of performance) yielding accepted/rejected/review-needed states about bid fit. The candidate's change-event reason codes ("change confirmed / no change / review-needed") classify change events, not opportunity eligibility. Absent in the Round 1 leader, absent in the Round 2 leader, absent here — three candidates in a row.
2. **Solicitation documents** — missing, and deliberately so. Excluded by design; the capability sits with the ungated sibling `uk-tender-document-reconciler`. Find a Tender is recorded `exposesDocuments: true`, so this is a scoping choice, not a source constraint.

### scopeConditions the lenses proposed (a revised version would need these to be survivable)

**From the gate / required changes:**
- Add structured qualification as an in-scope, scored capability (deterministic eligibility assessment on CPV/classification code, lot, value threshold, buyer type, place of performance), kept distinct from the change-event reason codes.
- Add solicitation documents to scope, or record an explicit orchestrator decision that the concept ships without them and state what substitutes for that register requirement.
- Disclose and resolve the Business-location-monitoring register collision explicitly in the noveltyStatement (state "scheduled monitoring" is reproduced, cross-source resolution and conflict review are not, and why the remaining overlap does not strip that row of its distinctness).
- Replace the deferred rate-limit language with a committed numeric fixed-interval cadence, since the T&Cs page carries no quota to defer to.
- Retract the "empirically discoverable at build time" language from the candidate's own scoring basis (scorecard and ledger); state affirmatively that 429 + Retry-After will be honored as a stop signal, never a discovery loop, and that no backoff-and-rotate will be used to sustain a refused rate.
- Re-run the gate after the changes; a high score and a sounder provability design are not substitutes for a passed register test.

**From the novelty lens:**
- Re-scope the headline capability away from "change detection" (which the source already publishes as tags and amendment arrays) toward work the publisher does NOT do — e.g., normalizing the free-text `unstructuredChanges` prose into typed, machine-comparable change records, or reconciling publisher-asserted amendment metadata against actual field-level deltas to detect unflagged silent changes.
- Drop or heavily qualify the framing that this "avoids the unmeasurable-recall failure mode" of the Round 1 leader — Find a Tender does not have that reconstruction problem; the source already retains history and self-labels changes.
- Re-measure the amendment population before committing to a bounded seed set (measured: only 17 of 275 ocids had >1 release in a 3-day window) — a week-long ~100-200 ocid seed set may yield a single-digit number of change events, too thin for a recall/precision claim.
- Refer the personal-data-in-free-text finding (named NHS officer email inside an `oldValue.text` prose blob) to the compliance lens before any build; the current field-level contract covers structured fields only.

**From the compliance lens:**
- Caveat 1 (personal data) is satisfiable and was not the reason for refutation — implement as an ALLOWLIST (enumerate permitted fields, never a denylist), drop `contactPoint` at parse time before persistence, and exclude free-text fields (`tender.description`, `awards[].description`) from published output since personal data leaks into prose that no field-level rule catches.
- Replace live polling with the data.gov.uk daily bulk XML ZIPs as the PRIMARY source, not a fallback — removes the undocumented-ceiling problem entirely, but requires the "respond before a shortened deadline" buyer promise to be rewritten honestly (latency degrades from sub-day to next-day) or dropped. Confirm OGL v3.0 applies to the bulk files specifically (the dataset page's licence field currently reads "Not set").
- If live polling is retained, obtain WRITTEN permission for the monitoring use (the "Interception" clause bars monitoring "without permission") and cite it in a repository file before building.
- Set the poll interval from a disclosed conservative constant, fix it in config, never adapt it upward; treat any 429 as a hard stop, never a backoff-and-resume signal; never rotate IPs, user agents, or sessions.
- Re-scope the headline metric away from LATENCY (which structurally requires the forbidden probing) toward COMPLETENESS/correctness, which the bulk files can prove without rate-sensitive polling.
- Document the concept's bid-pursuit business need explicitly; the T&Cs state access is "subject to business need" and revocable at any time without notice.

**From the provability lens:**
- Replace the tag-count denominator with a diff-derived denominator: for the seed ocid set and fixed window, compare consecutive full snapshots field-by-field over a pre-declared, publicly disclosed field set, and count only releases where a declared field actually changed. Tag-based counts may be reported only as a labelled superset, never as the recall denominator.
- Re-scope the buyer-facing headline metric to "material-change detection" over a declared field set, not "amendment monitoring" in the abstract.
- Publish the measured tenderUpdate-to-material-change ratio as a first-class finding (this run's sample: 6 tenderUpdate releases on one ocid, 0 change in `tenderPeriod.endDate`) — itself a credible, honest portfolio result.
- Do not depend on `versionedRelease` (present on some records, absent on others); compute field-level change from full snapshots, using `versionedRelease` only as a corroborating cross-check when present.
- State plainly that both the pipeline and the "independent" query read the same underlying API — this is a reproducibility oracle, not third-party ground truth.
- Keep the rate ceiling literally TBD; use conservative fixed-interval polling well below any plausible limit; honour 429 + Retry-After; never probe upward, never backoff-and-rotate.
- Enforce the organisation-level-identifier-only contract at ingest, not export — releases are full snapshots repeating all fields every time, so contact fields recur in every captured release and must be dropped before persistence.

## Where this leaves WS-001

All three Round 2 candidates and both prior round leaders have now been examined. None has cleared the relevance-and-uniqueness gate, and none has survived adversarial review:

- **Round 1 leader — Public opportunity intelligence (SAM.gov):** FAILED the gate (2 of 5 register requirements missing) and REFUTED on compliance (automated collection prohibited by SAM.gov's own Terms of Use; amendment history requires federal-role authentication this project does not have) and provability (public API returns latest-version-only, no denominator for amendment recall).
- **Round 2 leader — `uk-public-buyer-cross-source-resolution`:** FAILED the gate (1 of 5 register requirements met) and REFUTED 3/3 — novelty (reproduced the Business-location-monitoring row's cross-source entity-resolution mechanic under a swapped industry label), compliance (matching method unavoidably built on personal data; missed the operative T&Cs page), provability (measured empty intersection of buyer-identifier schemes across both sources — no oracle to withhold).
- **Round 2 runner-up — `uk-procurement-amendment-monitor` (this gate run):** FAILED the gate (3 of 5 register requirements met, tying the Round 1 leader's failing count) and REFUTED 3/3 — novelty (register collision plus a measured finding that the source already publishes the change events the concept claims to detect), compliance (the rate-ceiling caveat's only lawful escape hatch is empirically closed — no published quota exists anywhere on the operative pages), provability (the recall denominator is a tag count that measurably does not track semantic change).
- **Round 2 third candidate — `uk-tender-document-reconciler`:** never promoted, never gated, still `UNDER_REVIEW`, retained as an ungated fallback.
- **Round 1 other candidates — Product and price intelligence, Business-location monitoring:** REJECTED on source-legality grounds (synthetic-data-only sources; Google Places caching prohibition) before or without a full gate/lens run.

Two consecutive rounds have each produced a highest-scored leader that failed once actually tested, and a runner-up promoted in its place that also failed once tested. The scoring rubric has not yet identified a candidate that survives the gate and all three adversarial lenses. This is not evidence that UK procurement data is unusable — cleared sources remain cleared, and this run's own lenses found real, repairable design fixes (structured qualification, a diff-derived denominator, a bulk-file compliance path) rather than a source-legality dead end. But the pattern across two rounds — score high, fail when tested — means another automated scoring-and-promotion cycle from the same candidate pool is unlikely to produce a different outcome on its own.

**The next step is a human decision on direction, not another automated round.** Concretely, the options on the table are:

1. Repair `uk-procurement-amendment-monitor` per the scopeConditions above (add structured qualification, fix the rate-ceiling caveat via the bulk-XML path or written permission, replace the denominator, disclose the register collision) and re-run the gate.
2. Repair the Round 2 leader (`uk-public-buyer-cross-source-resolution`) per its own recorded required changes (organisation-level-identifier-only matching, structured qualification, disclosed register collision resolution).
3. Gate the untested Round 2 third candidate (`uk-tender-document-reconciler`) as-is, or repaired.
4. Pursue a different source/concept pairing from the cleared-source pool in `design/SOURCE_AND_COMPLIANCE_LEDGER.md`, or clear new sources.
5. Reconsider Round 1's lowest-scored, never-gated fallback (Business-location monitoring) if a business-location source is found whose licence affirmatively permits caching the operating-detail fields needed for change detection.

Status remains `AWAITING_APPROVAL`. No concept in WS-001 is `APPROVED`. No build work is authorized.
