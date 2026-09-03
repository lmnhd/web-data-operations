# Candidate Scorecard

**Iteration:** WS-001
**Round 1 evaluation date:** 2026-09-02
**Round 2 evaluation date:** 2026-09-02

This scorecard is a Phase 1 deliverable (`research/CANDIDATE_SCORECARD.md` per `PHASE_01_DISCOVERY_AND_EVIDENCE_PLAN.md`, workstream 2). It now covers **two rounds** of candidate evaluation for WS-001. Selection is evidence-based: **prior career history did not decide the winner.** No metric in this document is a measured result — no build, run, or benchmark has occurred for WS-001 in either round. Every quantity below is a *score* (a rubric judgment) or a *count of recorded demand signals*, not a performance, accuracy, or scale claim.

Per the repository rule against erasing rejected concepts or superseded decisions, **Round 1's full scoring, gate result, and adversarial review are preserved below unchanged**, under [Round 1](#round-1). Round 1's three candidates were all subsequently found to hit source-reuse restrictions that were discovered only at the compliance and adversarial-review stages — see [Round 1 outcome and lesson](#round-1-outcome-and-lesson) for the specific findings. Round 2 (below that) inverts the method: sources are cleared first, by fetching actual license/terms/robots text, and concepts are proposed only onto a source already found lawful.

**Reading order for a reviewer new to this file:** [Round 1 outcome and lesson](#round-1-outcome-and-lesson) and [Round 2 method — license-first](#round-2-method--license-first) explain why the document is shaped this way; [Recommendation](#recommendation-1) and [Approval request](#approval-request-1) carry the current decision. The original Round 1 sections below that are historical record, not the active recommendation.

---

## Round 1

## Method

Each candidate is scored 1-5 on the seven Phase 1 criteria (`PHASE_01_DISCOVERY_AND_EVIDENCE_PLAN.md`, workstream 2):

1. Similarity to paid Upwork work
2. Availability of lawful, public, stable-enough sources
3. Opportunity to demonstrate difficult extraction and data-quality work
4. Usefulness of the resulting dataset
5. Ability to show measurable results without fabricated claims
6. Time to a convincing first release
7. Potential to become a reusable service rather than a disposable demo

**Criterion 2 is bound to the compliance verdict.** A candidate whose sources are found `NOT_FEASIBLE` by source-and-compliance review is floored at 1 on criterion 2 regardless of how attractive the source otherwise looks; a `FEASIBLE_WITH_CONSTRAINTS` verdict is scored on the real weight of those constraints rather than defaulted to a fixed value. This binding is why criterion-2 rationale below cites the compliance verdict explicitly for every candidate.

After scoring, every candidate — not only the top scorer — passes through the README "Relevance and uniqueness gate" (`README.md` lines 144-167) and a three-lens adversarial review (novelty, compliance, provability). A high total score does not by itself authorize a concept; it must also survive the gate and the adversarial review below.

Demand-evidence basis: `research/UPWORK_DEMAND_MATRIX.md`, referenced throughout as "the demand matrix." Recorded signal counts from that research pass: **21 total demand signals, 10 at DIRECT_POSTING tier.** Evidence gaps encountered while building that matrix (platform access blocks, unparseable PDFs, missing absolute dates, etc.) are listed under [Demand evidence gaps](#demand-evidence-gaps) at the end of this document so they are not lost.

---

## Scores

| Candidate | 1. Similarity to paid work | 2. Lawful source availability (compliance-bound) | 3. Extraction/data-quality difficulty | 4. Dataset usefulness | 5. Measurable without fabrication | 6. Time to first release | 7. Reusable-service potential | **Total /35** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Public opportunity intelligence (SAM.gov) | 4 | 4 | 3 | 3 | 4 | 4 | 3 | **25** |
| Product and price intelligence | 4 | 3 | 3 | 2 | 4 | 4 | 3 | **23** |
| Business-location monitoring | 4 | 2 | 4 | 3 | 3 | 2 | 3 | **21** |

Ranked by raw total, public opportunity intelligence scores highest. As documented below in [Relevance and uniqueness gate](#relevance-and-uniqueness-gate) and [Adversarial review](#adversarial-review), the raw score is **not** the recommendation basis: that candidate fails the gate and is refuted on two of three adversarial lenses. See [Recommendation](#recommendation).

---

## Per-candidate assessment

### Public opportunity intelligence (SAM.gov)

| Criterion | Score | Rationale |
|---|---:|---|
| 1. Similarity to paid Upwork work | 4 | Automated monitoring of a structured government/business data source with change detection and alerting closely mirrors common paid Upwork briefs (lead-gen monitors, bid-tracking tools, deadline alert systems). Not a generic scraper-for-hire clone, but also not a wholly novel task category. |
| 2. Lawful source availability (compliance-bound) | 4 | Compliance verdict is FEASIBLE_WITH_CONSTRAINTS, not NOT_FEASIBLE, so this does not default to 1. Primary source is a documented, free, official public API (SAM.gov Opportunities API) with published schema and a sanctioned key-issuance flow; robots.txt and terms-of-use were directly fetched and interpreted (terms target unauthorized scraping, not the documented API). Docked one point because exact rate-limit quotas are undocumented publicly and must be confirmed at key issuance, and the restricted internal Opportunities-API (revision history) was correctly excluded as not permitted. |
| 3. Extraction/data-quality difficulty | 3 | Real difficulty exists in amendment-to-parent-notice linkage (must be built via repeated polling + noticeId/solicitationNumber matching since the native amendment API is inaccessible) and in document-vs-structured-metadata PDF reconciliation, identified as the surviving genuine differentiator. However, a close competitor (orbiscribe) already ships typed change-event detection on this exact source, narrowing the claimed extraction novelty to one sub-feature rather than the whole pipeline. |
| 4. Dataset usefulness | 3 | A clean, deduplicated, amendment-linked feed of federal contracting opportunities with deadline-change alerts has clear utility for small contractors/consultants. But corrected demand evidence shows the original claim (GovWin IQ specifically monetizes amendment/deadline alerts) was an overstatement of the cited source — the article only confirms generic "email/keyword alerts" industry-wide, weakening the demand case versus the original framing. |
| 5. Measurable without fabrication | 4 | API-based collection with a documented schema makes measurable claims straightforward (record counts, amendment-detection rate, latency between posted amendment and detected alert, attachment reconciliation success rate) without needing to fabricate anything, since ground truth is checkable against sam.gov's own UI links. **Adversarial review below found this rationale factually wrong — see Provability lens.** |
| 6. Time to first release | 4 | No browser automation needed; a working key-based JSON API with clear pagination and a bounded NAICS/date-range scope means a vertical proof-of-concept (two scheduled runs, real calendar-day gap) is achievable quickly. Main time sink is building and validating the amendment-linkage and PDF-reconciliation logic, not the collection layer itself. |
| 7. Reusable-service potential | 3 | The underlying API access pattern generalizes to a real monitoring service, and the concept is not just an industry-label swap of a prior template. But at least two commercial Apify actors already occupy adjacent territory on the same API, meaning a productized version would need real differentiation (the PDF-vs-metadata reconciliation) to avoid being "another SAM.gov watcher." |

**Total: 25/35**

**Weakest link:** The concept's demand-evidence framing overstated what competitors (GovWin IQ) actually monetize, and a near-identical open competitor product (orbiscribe's Apify actor) already ships typed change-event/deadline monitoring on this same API — so real differentiation narrows to one sub-feature (document-vs-metadata PDF reconciliation for amendments) rather than the headline "amendment/deadline monitoring" claim, and that narrower feature must actually prove out to justify the concept. Adversarial review below finds this sub-feature is itself blocked by an access control and structurally unmeasurable for its headline claim — see [Adversarial review](#adversarial-review).

---

### Product and price intelligence

| Criterion | Score | Rationale |
|---|---:|---|
| 1. Similarity to paid Upwork work | 4 | Price/availability monitoring and change-detection scraping is a very common paid Upwork request category, closely matching real client asks for competitor price trackers and catalog monitors. |
| 2. Lawful source availability (compliance-bound) | 3 | Compliance verdict is FEASIBLE_WITH_CONSTRAINTS (not NOT_FEASIBLE), so this is not forced to 1, but it is held down: the only fully compliant sources are two synthetic scraping-sandbox sites (books.toscrape.com, sandbox.oxylabs.io) with explicit demo/no-real-meaning disclaimers, and two natural, on-brand candidates (webscraper.io test-sites, scrapingcourse.com) were verified and rejected for robots.txt Disallow conflicts. Source pool is lawful but thin and non-commercial. |
| 3. Extraction/data-quality difficulty | 3 | Price-change detection, availability-history tracking, and category/near-duplicate grouping are legitimate data-quality problems; the optional Oxylabs JS-rendered SPA path adds a genuine dynamic-rendering challenge. But books.toscrape.com is plain static HTML with no anti-bot friction, pagination tricks, or auth walls, capping how "difficult" the primary extraction actually is. |
| 4. Dataset usefulness | 2 | Both compliant sources are explicitly synthetic demo catalogs with randomly assigned prices/ratings carrying "no real meaning" — this must be labeled as such in the Manifest per the compliance finding. A dataset built on fictional/random data has limited standalone usefulness beyond demonstrating the pipeline mechanics. |
| 5. Measurable without fabrication | 4 | Price-change and availability-change detection produce cleanly measurable pass/fail outcomes (correct diffs, catch rate on injected changes) without needing to fabricate demand numbers — straightforward to report honestly as pipeline/QA metrics rather than business impact. |
| 6. Time to first release | 4 | Static HTML primary source, no auth/CAPTCHA, small well-understood catalog — a working collector plus a twice-daily change-detection proof is realistic quickly. |
| 7. Reusable-service potential | 3 | The price/availability-monitor pattern (adapter-per-site, diffing engine, alerting) generalizes well architecturally, but the concept as scoped here is tied to two toy sandbox sites with sanctioned-for-scraping disclaimers — turning it into a real reusable service requires re-verifying compliance against actual commercial retail sites, which is deferred, not demonstrated, here. |

**Total: 23/35**

**Weakest link:** The only lawful, verified sources are synthetic scraping-practice sandboxes (books.toscrape.com, sandbox.oxylabs.io) with explicit "no real meaning"/randomly-assigned data disclaimers — two natural real-catalog alternatives were checked and rejected on robots.txt grounds. The resulting dataset and any price-change "signal" will read as a synthetic-data demo rather than evidence of handling a real, commercially meaningful price-intelligence problem, undercutting dataset usefulness and the reusable-service story simultaneously. This limitation is disclosed transparently rather than fabricated around, and it is scoped to a first-release proof-of-mechanism rather than a claim of commercial-market coverage.

---

### Business-location monitoring

| Criterion | Score | Rationale |
|---|---:|---|
| 1. Similarity to paid Upwork work | 4 | Cross-directory business listing accuracy/monitoring (location, hours, phone, status) closely mirrors common paid Upwork jobs (directory audits, listing accuracy checks, local SEO data ops). Not the single most-posted category, but well within recognizable buyer demand. |
| 2. Lawful source availability (compliance-bound) | 2 | Compliance verdict is FEASIBLE_WITH_CONSTRAINTS, not NOT_FEASIBLE, so this is not floored at 1 — but constraints are substantial: Google Places API bars caching/storage of nearly all display fields (name, address, phone, hours, status) except place_id and lat/lng, which undermines the concept's own "incremental diff against cached snapshot" design and forces re-query-per-comparison. GBP API (the source actually named in the demand-evidence article) is confirmed NOT usable for arbitrary third-party businesses. Netrows forbids redistribution of raw data entirely. First-party site ToS (Ace Hardware) is only partially verified — the anti-scraping clause presence is explicitly UNCONFIRMED. Each additional business added to a fixture set requires its own robots.txt/ToS check, so the source picture does not stabilize as a reusable pattern. |
| 3. Extraction/data-quality difficulty | 4 | Genuine hard problems are present: cross-source entity resolution (matching the same business across first-party site, Places API, and a second aggregator), field-level conflict detection, and handling a source that legally forbids the exact caching pattern a naive design would use. That last constraint, once designed around, is itself a nontrivial and demonstrable engineering problem. |
| 4. Dataset usefulness | 3 | An operator-facing conflict/discrepancy report on business location data is plausibly useful for franchise/multi-location operators and marketing agencies, but the compliance findings cut its usefulness: Netrows data can't be redistributed even in a sanitized example dataset, and Places API fields largely can't be retained as historical records — so the "dataset" that can actually be shown publicly is thinner than the concept implies (conclusions/flags only, not much raw field data). |
| 5. Measurable without fabrication | 3 | Feasible to measure precision/recall of conflict detection against a small hand-verified fixture set of real businesses, but exact rate limits for both Places API and Netrows are TBD/gated behind console or paid-account access not yet retrieved, and the caching restriction may force a redesign before any benchmark can be run at all — adds real risk that early measurement gets delayed by discovering further terms constraints mid-build. |
| 6. Time to first release | 2 | Before any collection code is written, the design must be reworked to avoid retaining barred Places API fields, the Ace Hardware ToS gap must be closed, and a real per-business compliance check must be done for every fixture-set business (this doesn't scale to a quick fixture the way a single-source scraper would). GBP API being unusable for the concept's original workflow also means part of the original design premise needs revisiting before build starts. |
| 7. Reusable-service potential | 3 | A cross-source conflict-detection and entity-resolution engine is architecturally reusable across other monitoring verticals, but the specific value proposition here is weakened by the redistribution ban on the richest third-party source (Netrows) and the no-caching rule on Places API, meaning a productized recurring-monitoring service would need to be built around live re-query costs and non-redistributable-data constraints from day one — workable, but a real design tax on the reusable core. |

**Total: 21/35**

**Weakest link:** The candidate's own core technical design (incremental diff against a cached snapshot of location field values) directly conflicts with Google Places API's terms, which bar caching/storing almost all display-relevant fields (name, address, phone, hours, status) beyond place_id and lat/lng; combined with GBP API being confirmed unusable for arbitrary third-party businesses (the source actually cited in the demand-evidence article) and Netrows barring redistribution of its data, the source foundation requires a real redesign before build, not just a "use responsibly" caveat — this is the single most likely thing to stall or shrink the project.

---

## Relevance and uniqueness gate

Per `README.md` "Relevance and uniqueness gate" (lines 144-167), a concept must normally add at least one net-new technical capability **and** differ meaningfully from prior projects in at least two of seven dimensions, and must not merely change the website, theme, keyword set, or industry label.

**Gate was run against the leading candidate, public opportunity intelligence (score 25/35).**

**Result: FAILS.**

- **Net-new technical capability test — PASSES.** Amendment-to-parent-notice linkage on SAM.gov, built by repeated polling and noticeId/solicitationNumber matching (the native amendment/revision-history API being inaccessible), combined with reconciliation of attached solicitation PDFs against structured API metadata, is a genuine capability not held by any prior or active repo concept. The one documented competitor on this same source (an Apify SAM.gov Contract Monitor actor, demand-matrix row 31) is recorded as having "no explicit entity-resolution/matching described." This capability is real and net-new.

- **Two-of-seven-dimensions test — PASSES, but close to vacuous.** Verified against the actual prior-concept list rather than accepted at face value: the tracking log's portfolio catalog contains exactly one non-candidate entry, WS-000 (the Multi-agent Shipping Pipeline foundation, status BUILDING), which is process/tracking infrastructure with no buyer data problem, sources, extraction, normalization, change detection, or delivery destination of its own. The other two entries (business-location monitoring, price intelligence) are UNDER_REVIEW sibling candidates from this same scoring pass, not completed or active projects. There are zero completed projects to differ from; the catalog note for WS-001 reads "Must add the first end-to-end collection and verification evidence." Against WS-000, all seven dimensions differ trivially by default for *any* web-data concept. This test therefore carries little real discriminating weight in this iteration — the binding constraint is the candidate/duplication register test below.

- **Candidate/duplication register test — FAILS. This is the decisive finding.** The `PORTFOLIO_TRACKING_LOG.md` candidate/duplication register names this concept family's overlap risk explicitly: "May overlap with Local Contract Scouter if framed only as lead discovery," and lists five things that would make it distinct: solicitation documents, amendments, provenance, deadline change tracking, structured qualification. Checked against the candidate as scored:
  - Solicitation documents — **covered** (criteria 3 and 7, PDF-vs-metadata reconciliation).
  - Amendments — **covered** (criterion 3, amendment-to-parent linkage via polling and noticeId/solicitationNumber matching).
  - Deadline change tracking — **covered** (criterion 5, latency between posted amendment and detected alert).
  - Provenance — **absent** from all seven scored criteria.
  - Structured qualification — **absent** from all seven scored criteria.

  Two of the five register-named distinctness requirements are unaddressed, and **structured qualification is precisely the requirement that separates this concept from lead discovery** — without it, the concept is a monitored feed of opportunities, which is the exact framing the register warns against.

- **Aggravating factor — first-project burden.** README's "Continuous-shipping sequence" assigns Project 1 the job of establishing the shared collection, provenance, validation, export, and reporting foundation. The candidate's own weakest-link finding concedes that after correcting the GovWin IQ demand overstatement and accounting for the orbiscribe competitor, real differentiation narrows to one unproven sub-feature. Staking the portfolio's foundational project on a single unproven sub-feature, while omitting two register requirements that would have provided independent distinctness, is not an acceptable risk posture for WS-001.

- **Honest-claim check:** no fabrication detected in the candidate as scored. It self-corrects the GovWin IQ demand overstatement, rate-limit quotas are correctly left unconfirmed rather than estimated, and the restricted internal Opportunities API was correctly excluded rather than assumed accessible.

**Verdict: passes = false.** Two of five register-named distinctness requirements (provenance, structured qualification) are missing from the highest-scoring candidate as currently framed. The gate treats this as repairable-in-principle (the required changes are recorded for a future run), not evidence that the underlying source is unusable — but the concept as scored today does not clear the gate and cannot be approved in its current form.

Full required-changes list, as recorded by the gate review, for reference if this concept is revisited:

1. Add structured qualification as an in-scope, scored capability (deterministic set-aside/NAICS/PSC/size-standard/place-of-performance eligibility assessment with reason-coded accepted/rejected/review-needed states).
2. Add provenance as an explicit in-scope capability (source URL, retrieval timestamp, content fingerprint, extraction method, and document-vs-metadata origin marker per field).
3. Re-scope the headline claim away from "amendment/deadline monitoring" toward reconciled, qualified, provenance-tracked opportunity intelligence.
4. Record the compliance findings (SAM.gov verdict, robots.txt/terms fetch dates, competitor findings) in repository files before approval — none currently exist on disk.
5. Add a written competitive-differentiation statement naming known competitors.
6. Carry the unresolved SAM.gov rate-limit quota forward as a literal TBD.
7. Re-run this gate before moving WS-001 to APPROVED.

---

## Adversarial review

Three adversarial lenses were applied to the leading candidate (public opportunity intelligence, score 25/35) to stress-test it beyond the gate above. Refutations are recorded verbatim below and are not softened.

### Novelty lens

**Verdict: refuted = false** (attack fails; candidate survives this lens)

> ATTACK ATTEMPTED: that this is a themed variation — a generic monitor-and-diff scraper wearing a "government procurement" industry label, which README line 167 explicitly disqualifies.
>
> THE ATTACK FAILS. README lines 157-167 set the actual test: at least one net-new technical capability plus meaningful difference in >=2 of seven dimensions, where the disqualifier targets changing "only the website, visual theme, keyword set, or industry label." Against the two active sibling candidates the differences are structural, not cosmetic:
>
> 1. SOURCE AND CONTENT TYPES — the only candidate whose payload pairs structured API metadata with attached binary documents (solicitation PDFs). Location-monitoring is HTML/API business profiles; price-intelligence is product pages.
> 2. NORMALIZATION/MATCHING PROBLEM — amendment-to-parent-notice linkage is TEMPORAL VERSIONING (one entity, N ordered revisions, supersession). Location-monitoring is CROSS-SOURCE IDENTITY (N sources, one entity); price-intelligence is VARIANT RESOLUTION. Three genuinely distinct matching problems, not one problem relabeled.
> 3. MONITORING BEHAVIOR — deadline-change tracking on a legally consequential field differs from price-delta alerting in what a false negative costs.
>
> Three dimensions clears the required two. None of these is a website, theme, keyword, or industry-label swap.
>
> WHY THE STRONGEST COUNTER-EVIDENCE IS OUT OF SCOPE FOR THIS LENS. The scorecard's weakest link — orbiscribe's Apify actor already shipping typed change-event detection on this same API, plus ryanclinton/sam-gov-contract-monitor appearing as a DIRECT_POSTING signal in the demand matrix — is the best card against this candidate, and it was tested hard. It is not a novelty refutation. The README scopes the gate to "all completed and active projects" (line 154) and "prior projects" (line 157) — THIS portfolio's projects. The tracking-log catalog holds only WS-000 (pipeline foundation) and WS-001 (unassigned); the rejected/archived table is empty. There is no prior portfolio project for this to be a themed variation OF. Commercial prior art is a market-differentiation concern, correctly booked under criterion 7 and already scored down to 3 there; importing it here double-counts a levied penalty. It also proves too much — an Apify actor exists for nearly every scraping target, so that standard refutes all three candidates and every future one. Under README criterion 1, two commercial products on this exact source is affirmative "similarity to paid work" evidence, which the portfolio is meant to demonstrate.
>
> NET-NEW CAPABILITY IS REAL, NOT AN ARTIFACT. The surviving differentiator — document-vs-structured-metadata PDF reconciliation with amendment provenance — is thin but sufficient: README asks for "at least ONE net-new technical capability." The capability ledger shows every collection capability at PLANNED, none VERIFIED, so nothing is being duplicated. The difficulty is not manufactured: linkage must be rebuilt via repeated polling and noticeId/solicitationNumber matching because the native revision-history API was correctly excluded as not permitted. That constraint is compliance-driven, not contrived, and reconstructing version lineage from observed snapshots is precisely the provenance work the core positioning names ("preserve provenance... resolve messy records"). Neither sibling candidate would produce it.
>
> VERDICT: refuted=false. Not benefit-of-the-doubt — the themed-variation charge fails cleanly on three structural dimensions, and the strongest attack available is scoped out of this lens by the README's own wording and already priced into criterion 7.

**Fatal flaw recorded on this lens:** None fatal to novelty itself. Two conditions flagged for enforcement: (1) an evidence-integrity gap — the compliance findings this candidate relies on (orbiscribe, restricted internal API) exist only in scoring narrative, not in a persisted repository artifact, and must land in `design/SOURCE_AND_COMPLIANCE_LEDGER.md` before approval; (2) a narrow margin — novelty now rests entirely on the PDF-vs-metadata reconciliation sub-feature, since the headline amendment/deadline-monitoring claim is occupied by an existing competitor; if a build descopes that sub-feature, the concept collapses into "another SAM.gov watcher" and should be re-refuted at the build gate.

### Compliance lens

**Verdict: refuted = true** (attack succeeds; candidate does not survive this lens)

> The concept's sole surviving differentiator — document-vs-metadata PDF reconciliation of amendments — depends on solicitation attachment retrieval, which is access-controlled. The SAM.gov Opportunity Management API that exposes attachments and revision history requires a federal government system account with Contracting Officer/Specialist/Administrator roles, IP allowlisting, and (for secure attachment download) Create/Edit/Delete Draft Attachment write permissions. The concept therefore either cannot deliver its differentiator or must work around an access control to do so. Compounding this, SAM.gov Terms of Use state verbatim that "Automated data gathering, web scraping tools are prohibited," and the API carve-out is scoped to "internal, U.S. Government business purposes" — which a public portfolio project republishing output does not satisfy. Finally, the non-federal no-role API quota is 10 requests/day, which cannot sustain the repeated polling the concept explicitly requires for amendment linkage and deadline-change detection, creating pressure to acquire a role the project does not qualify for.
>
> REFUTATION 1 (FATAL): THE DIFFERENTIATOR IS BEHIND THE ACCESS CONTROL. The scorecard's own weakest-link concedes the concept collapses into the already-registered "Local Contract Scouter" overlap unless it delivers document-vs-metadata PDF reconciliation for amendments — attachment/document processing is not a nice-to-have, it is the entire novelty claim. That capability is access-controlled: verified at the GSA Opportunity Management API documentation, it requires a valid SAM.gov federal government system account with read and write permissions under the Contract Opportunity domain, restricted to Administrator/Contracting Officer/Contracting Specialist roles, a separately requested and approved system account, user authorization headers plus a system-account API key, and IP-registered validation. Secure attachment download requires Create/Edit/Delete Draft Attachment — write permissions on federal solicitation documents that a portfolio project has no legitimate basis to hold. On the public API path, the description field itself requires API authentication and the documentation does not establish that resourceLinks attachments are publicly retrievable; 401/403 responses are defined for this API and controlled resources remain access-controlled even when the parent notice is public. Consequence: the reconciliation feature either does not run, or runs by circumventing an access control — disqualifying under the standing instruction to reject outright any concept that evades access controls. The compliance finding's own exclusion of the revision-history API as "not permitted" is scored as though costless; it is not costless, it removes the differentiator.
>
> REFUTATION 2: TERMS OF USE PROHIBIT THE ACTIVITY BY NAME, AND THE CARVE-OUT DOES NOT COVER THIS USE. SAM.gov's Terms of Use state verbatim: "Automated data gathering, web scraping tools are prohibited and, if detected, will result in the associated account(s) being denied access to SAM.gov via Login.gov." The API carve-out is narrower than the criterion-2 scoring represented: "You are allowed to use the Contract Opportunities and Entity Management APIs for internal, U.S. Government business purposes." A public Upwork portfolio artifact that republishes collected opportunity data is neither internal nor a U.S. Government business purpose. GSA shows it knows how to grant public redistribution rights when intended, by pointing a distinct API (Federal Hierarchy Public API) at that purpose explicitly; no equivalent dissemination grant was found for Contract Opportunities attachment content.
>
> REFUTATION 3: RATE LIMITS MAKE THE CORE MECHANIC NON-VIABLE AND CREATE PRESSURE TO ACQUIRE A ROLE THE PROJECT DOES NOT QUALIFY FOR. Non-federal with no SAM.gov role = 10 requests/day; with role = 1,000/day; federal system account = 10,000/day. Ten calls/day cannot sustain notice discovery plus per-notice description and attachment fetches plus re-polling for change detection, which the concept's own mechanic requires. The incentive this creates — obtaining a SAM.gov role for the purpose of raising a quota rather than because the operator legitimately holds that role — is access-control circumvention in substance.
>
> REFUTATION 4 (secondary, unscored by the scorecard, not load-bearing for the verdict): the personal-data boundary for contracting-officer POC fields is unspecified in the concept as scored, and SAM is a Privacy Act system of records containing PII/CUI; no retention limit or sanitization rule is stated.
>
> EVIDENCE-QUALITY FLAG: robots.txt for sam.gov could not be reproduced as claimed (the fetch returned a generic Drupal robots.txt with no crawl-delay, almost certainly from a redirect, not SAM.gov's own SPA) — assigned zero weight in either direction, but it undercuts the criterion-2 assertion that "robots.txt and terms-of-use were directly fetched and interpreted correctly": the terms-of-use interpretation reported is contradicted by the verbatim carve-out text, and the robots.txt claim could not be reproduced. Criterion 2's score is not supported by evidence that could be reproduced on this pass.
>
> WHAT WOULD REVIVE THE CONCEPT: a materially rescoped version limited to structured metadata only from the public Get Opportunities API (attachments, descriptions, and revision history declared explicit non-goals), a role-backed key obtained through a path the operator genuinely qualifies for with quota documented before build, POC/contact fields excluded or sanitized, and a differentiator that does not depend on document reconciliation. But the tracking log's own recorded warning is that a metadata-only opportunity feed "may overlap with Local Contract Scouter if framed only as lead discovery" — so the compliant version is the version that fails the uniqueness gate. The concept is squeezed between the compliance boundary and the novelty boundary.
>
> VERDICT: REFUTED. Three independent primary-source findings each independently damage the compliance story, and the first is fatal on its own: the feature that makes this concept distinct from an already-registered overlapping concept is the feature that sits behind federal-role authentication requiring write permissions.

### Provability lens

**Verdict: refuted = true** (attack succeeds; candidate does not survive this lens)

> The concept's differentiating capability — amendment and deadline-change tracking — cannot produce measurable recall, because the only lawful source destroys the evidence needed to verify it. GSA's public Get Opportunities API returns ONLY the latest active version of each notice; when a notice is amended the same noticeId receives an updated payload and the prior version is replaced, not retained. Revision history exists solely in the Opportunity Management API, which requires a government email address, a federal system account with Contract Opportunity write permissions, a Contracting Officer/Specialist role, and IP allowlisting — correctly excluded by the compliance finding as not permitted. Consequently a snapshot-diff pipeline can only count changes it happened to catch; it has no denominator and cannot measure missed changes, making the headline metrics ("amendment-detection rate," "detection latency") unfalsifiable in the failure direction and self-referential — graded against the pipeline's own snapshots rather than any independent record.
>
> VERIFIED FINDINGS: (1) the public API returns latest version only, corroborated by independent third-party documentation stating amendments do not appear as separate records and the same noticeId receives an updated payload with the original replaced, not retained; (2) no amendment indicator and no parent-notice link exists in the documented public schema — noticeId/solicitationNumber matching works only for the subset of amendments that receive a new noticeId, and fails entirely for in-place overwrites; (3) revision history is behind the restricted Opportunity Management API, correctly excluded by the compliance finding, and that correct exclusion is precisely what removes the ground truth; (4) THE SCORECARD'S CRITERION-5 RATIONALE IS FACTUALLY WRONG — it scored 4 on "ability to show measurable results without fabricated claims" because "ground truth is checkable against sam.gov's own UI links," but the public uiLink renders only the CURRENT version, and version history is explicitly directed to the Data Services section, not the notice page; a human reviewer opening uiLink sees the same current state the pipeline saw, so Phase 1's mandatory "manually reviewed ground-truth samples" is unconstructible for the differentiating feature; (5) a documented silent-loss case exists with no possible detector — amendments sometimes get a new noticeId and sometimes overwrite in place, and in the overwrite case the previous version is simply gone from both data sources, so the pipeline cannot distinguish "no amendment occurred" from "an amendment occurred and both versions vanished," making any completeness claim about amendment capture a fabrication under this repository's non-negotiable rules; (6) rate limits remain numerically undocumented for public keys, so the Phase 1 metric "elapsed time and request volume under the documented rate policy" has no documented policy to measure against.
>
> WHY THE OBVIOUS RESCOPES ALSO FAIL: rescoping to "detect only new-noticeId amendments, report recall as TBD" is honest but yields a first release whose headline capability carries a permanent unmeasured recall, on a source where an existing open competitor already ships typed change-event detection — not a defensible release. Rescoping to the PDF-vs-metadata reconciliation sub-feature alone is genuinely provable (resourceLinks are fetchable and a human can compare a PDF's stated deadline against the API's structured deadline field, giving real checkable ground truth) — but that is a document-parsing/conflict-resolution exercise, not "opportunity intelligence," and does not justify the amendment/deadline-monitoring framing the concept is built on; passing the concept on the strength of a surviving sub-feature while its headline claim is unmeasurable is exactly the benefit-of-the-doubt pass this review is meant to prevent. Rescoping to "measure detection latency only" fails because latency requires an independent record of when the amendment actually posted, and the only system holding that record is the restricted API the concept correctly refuses to use.
>
> RECOMMENDATION IF THIS SOURCE IS REVISITED: do not carry the criterion-5 rationale ("ground truth is checkable against sam.gov's own UI links") forward into any future brief or Manifest — it is unsupported and would become a fabricated claim in a reviewer-facing document if repeated. If this source is revisited later, the honest path is a concept framed on document-vs-structured-metadata conflict reconciliation, which has real, human-checkable ground truth, NOT on amendment/deadline change monitoring. Record this refutation reason in the rejected/archived register so the amendment-tracking framing is not rediscovered without this evidence.
>
> VERDICT: REFUTED on the provability lens.

**Summary across lenses:** Novelty — not refuted. Compliance — refuted. Provability — refuted. Two of three adversarial lenses find the leading candidate does not survive as scored, independent of and in addition to the gate failure above.

---

## Recommendation

**Recommended concept: Product and price intelligence (23/35).**

The highest scorer, public opportunity intelligence (25/35), **failed the relevance and uniqueness gate** (two of five register-named distinctness requirements — provenance and structured qualification — are missing from the scored concept) **and was refuted on two of three adversarial lenses** (compliance: its sole differentiator sits behind a federal-role access control it cannot legitimately hold; provability: its headline amendment/deadline-tracking claim cannot produce measurable recall because the only lawful source silently discards prior versions). It is displaced from the recommendation on that basis, not on preference. Its full scoring, gate result, and refutations are preserved above rather than deleted, per the repository rule against erasing rejected concepts or superseded decisions.

Product and price intelligence is recommended as the next-best evidence-based option:

- It scores second overall (23/35) on the same seven-criterion rubric, with no criterion below 2.
- Its criterion-2 (lawful source availability) constraints are disclosed transparently rather than discovered as fatal late: the compliant sources are synthetic scraping-practice sandboxes with explicit no-real-meaning disclaimers, and this limitation is already priced into criterion 4 (dataset usefulness, scored 2) rather than hidden.
- Unlike the leading candidate, no access-control conflict or unmeasurable-recall problem has been identified against it in this review pass. It has not yet been run through the same adversarial-lens depth applied to the leading candidate above; the orchestrator should confirm it clears the relevance-and-uniqueness gate and the three adversarial lenses before moving WS-001 to APPROVED, per the standing instruction accompanying this recommendation.
- Its core technical claims (price-change detection, availability-history tracking, near-duplicate/variant grouping) are checkable against the pipeline's own controlled fixture data without the same silent-data-loss problem found in the SAM.gov candidate, because the sandbox sources are static and fully observable rather than a live government system that discards prior state.

This recommendation is provisional pending the orchestrator running the same gate-and-adversarial-review pass against this candidate that was run against the leading one, and pending resolution of the dataset-usefulness weakness (criterion 4, scored 2) — most plausibly by scoping the Manifest's claims explicitly to pipeline-mechanism proof rather than commercial market coverage, consistent with the "no real meaning" disclaimer already attached to the source data.

Business-location monitoring (21/35) remains the lowest-scored candidate; its core technical design directly conflicts with Google Places API's caching restrictions, and it is not recommended at this time. Its full scoring is preserved above.

---

## Approval request

Per `PHASE_01_DISCOVERY_AND_EVIDENCE_PLAN.md`, "Approval gate before implementation," the following five items require human decision before Phase 2 (implementation) may begin. None of these decisions has been made by an agent; they are listed here awaiting human review.

1. **Selected use case and target client** — awaiting decision. This scorecard recommends product and price intelligence over the higher-scoring but gate-failed and doubly-refuted public opportunity intelligence candidate; business-location monitoring is the lowest-scored option. A human approver must confirm or override this recommendation before Phase 2 begins.

2. **Target sources and compliance ledger** — awaiting decision. No `design/SOURCE_AND_COMPLIANCE_LEDGER.md` exists in the repository yet. The compliance findings referenced throughout this scorecard (SAM.gov FEASIBLE_WITH_CONSTRAINTS verdict and its access-control conflict, the price-intelligence synthetic-sandbox source set, the location-monitoring Places-API caching conflict) must be committed to that file before this item can be considered resolved, regardless of which concept is approved.

3. **Data contract and expected exports** — **to be drafted after approval.** This is a Run 2 deliverable (`design/DATA_CONTRACT.md`), dependent on which concept is approved under item 1.

4. **Proof metrics and benchmark method** — **to be drafted after approval.** This is a Run 2 deliverable (`design/PROOF_AND_BENCHMARK_SPEC.md`), dependent on which concept is approved under item 1. No benchmark has been run for any candidate; every quantitative reference in this scorecard is a rubric score or a count of recorded demand signals, never a measured pipeline result.

5. **Phase 2 minimum viable build scope** — awaiting decision. Cannot be scoped until items 1-4 are resolved. Phase 2 must not expand into authentication bypass, large-scale infrastructure, paid data acquisition, or collection of sensitive personal information without a new explicit decision, per the Phase 1 plan.

---

## Demand evidence gaps

Recorded during the demand-evidence research pass (`research/UPWORK_DEMAND_MATRIX.md`) and carried forward here so they are not lost. These describe access limitations encountered while gathering evidence, not measured findings about the candidates themselves.

- Upwork could not be accessed via direct fetch for any individual job-posting URL — every attempt (multiple distinct job URLs, plus the web-scraping category page) returned HTTP 403 Forbidden. This is itself a repeatable observation about Upwork's anti-bot posture toward automated fetchers, but it means no Upwork DIRECT_POSTING evidence with full posting text could be captured this session — only search-result snippets (titles/URLs) exist, insufficient to responsibly extract deliverable/tooling/volume detail, so no Upwork row was recorded as a full signal.
- WeWorkRemotely's programming category page also returned HTTP 403. RemoteOK content was only reached indirectly through search summaries of third-party aggregator pages, not the primary board itself, so no RemoteOK/WeWorkRemotely row met the DIRECT_POSTING bar this session.
- Contra.com search results surfaced only freelancer-directory/hire pages and third-party scraper-tool listings, not actual client-posted job requests, so no genuine Contra job posting could be evidenced.
- PeoplePerHour listing pages returned rich per-row detail but were summarized rather than returned as raw HTML, so exact phrasing/full body text beyond one full-detail page is a compressed paraphrase, not a verbatim transcript.
- No aggregate market-survey report or forum/blog demand-trend discussion was captured — all recorded signals are DIRECT_POSTING tier from this pass.
- Could not confirm current "proof of prior work" expectations across most postings — only one posting explicitly stated portfolio/methodology requirements.
- Exact posting dates for several rows are relative ("19 days ago") as rendered at access time (2026-09-02) rather than absolute calendar dates.
- The Apify/Web Scraping Club 2026 PDF report could not be parsed directly (PDF tooling unavailable in this environment); relied on a summary page instead, which itself noted it omits output-destination/format detail, data-volume metrics, and detailed failure points likely present only in the full PDF.
- The Zyte 2025 Web Scraping Industry Report page returned truncated content on fetch; excluded from signals rather than guessed at.
- No dedicated Upwork-published market-research report with quantified demand trends for web scraping/data extraction was found; only live job-listing pages and third-party marketing pages were located.
- Proxyway's proxy/web-scraping market-research reports were found only as search-result titles/snippets, not fetched and verified directly, so they are omitted rather than reported second-hand.
- No report found in this pass explicitly breaks out "proof or prior-work evidence requested by clients" as its own statistic.
- Volume/frequency figures are reported only as relative/percentage-change statistics in sources found, not absolute volume benchmarks.
- Cleaning/matching-requirement statistics from one signal come from vendor marketing/how-to pages rather than a single dated, citable market report, so that signal is recorded at SECONDARY_COMMENTARY tier with lower confidence.
- Direct Upwork job-posting pages consistently returned HTTP 403 to unauthenticated fetch — itself a recorded anti-bot/auth-wall signal, but it means Upwork-specific demand had to be evidenced via a third-party aggregator and Upwork's own public hiring-guide pages rather than live current postings.
- No genuine government RFP/solicitation specifically requesting third-party web-scraping, monitoring, or data-enrichment services was located and confirmed readable; one candidate PDF could not be parsed as text (binary/compressed stream, and local PDF rendering tooling unavailable), so its content is not included as a signal.
- Update-frequency figures for several data-as-a-service vendors are marketing language ("high frequency," "real-time") rather than disclosed numeric cadence.
- No confirmed volume, pricing, or proof-of-work figures for GovWin IQ were available beyond secondary description; the platform itself was not directly fetched.
- No signals found in this pass involve restricted personal data, authentication bypass, or CAPTCHA evasion requests — searches intentionally avoided and did not surface such requests, consistent with the non-negotiable rule against proposing that kind of work.
- Sample coverage across the three candidates is uneven: procurement/opportunity intelligence and price/product intelligence are well evidenced (DIRECT_POSTING tier for both), while business-location monitoring rests more heavily on aggregate-report/secondary-commentary sources — a live client RFP or job posting specifically requesting multi-location listing-accuracy monitoring was not located in this session.

---

## Round 1 outcome and lesson

All three Round 1 candidates were carried into the gate/adversarial-review stage before their sources' actual reuse terms were checked closely enough. Each one subsequently hit a source restriction that had existed the entire time but was found only when the compliance and adversarial-review lenses were finally applied — not before the concept was scored, written up, and provisionally recommended. The pattern in every case was the same order of operations: **concept invented first, source checked afterward.**

The specific killers, recorded here so they are not rediscovered:

- **SAM.gov Terms of Use prohibit the activity by name.** Verbatim: *"Automated data gathering, web scraping tools are prohibited and, if detected, will result in the associated account(s) being denied access to SAM.gov via Login.gov."* This sentence was not found until the Round 1 compliance-lens adversarial review fetched the ToU directly; the original criterion-2 scoring had asserted "robots.txt and terms-of-use were directly fetched and interpreted (terms target unauthorized scraping, not the documented API)" — a claim the adversarial review found could not be reproduced and was contradicted by the ToU's own text.
- **The public API returns only the latest version of a notice, destroying the amendment-tracking denominator.** SAM.gov's Get Opportunities API overwrites a notice's prior state on amendment rather than retaining it; revision history exists only behind the restricted Opportunity Management API, which requires a federal system account with Contracting Officer/Specialist/Administrator role and IP allowlisting. Without an independent record of what changed and when, amendment-detection recall has no denominator — a snapshot-diff pipeline can only count changes it happened to catch, and cannot distinguish "no amendment occurred" from "an amendment occurred and both versions vanished." This made the leading candidate's headline metric unfalsifiable in the failure direction, not merely uncertain.
- **Google Places API bars caching/storing the exact fields a change-detection design needs.** Terms prohibit retaining name, address, phone, hours, and status beyond `place_id` and lat/lng — the business-location-monitoring candidate's own core mechanic (incremental diff against a cached snapshot) directly violates this, and the Google Business Profile API named in the underlying demand evidence was separately confirmed unusable for arbitrary third-party businesses.
- **Synthetic-sandbox sources produce no commercially credible dataset.** The only fully compliant sources found for the price-intelligence candidate (books.toscrape.com, sandbox.oxylabs.io) carry explicit disclaimers that their prices/ratings are randomly assigned and have no real meaning; two natural real-catalog alternatives (webscraper.io, scrapingcourse.com) were checked and rejected on verified robots.txt `Disallow` conflicts. A dataset built on fictional data cannot support a commercial-usefulness claim, only a pipeline-mechanism demonstration.

**The lesson driving Round 2:** none of these four killers required guesswork to find — each was sitting in a page that could have been fetched before the concept was scored. Round 2 therefore inverts the sequence: clear a source's actual license/terms/robots text first, and only propose a concept once that source is independently marked `cleared: true`.

---

## Round 2 method — license-first

Round 2 was run by a dedicated source-and-compliance pass that, for each candidate source, fetched (not inferred) four things before any concept was allowed to be proposed on it:

1. The actual license or reuse-grant text (not a summary page), quoted verbatim for its operative sentence.
2. The site's Terms of Use / Terms and Conditions, searched specifically for an automated-collection, scraping, bot, or crawler prohibition — the exact sentence type that sank SAM.gov in Round 1.
3. `robots.txt`, fetched directly, checked for `Disallow` rules covering the paths a concept would actually need (dataset/API paths, not just the human browsing UI).
4. Whether an official API or bulk-download mechanism exists, and under what authentication and rate-limit terms.

A source is recorded `cleared: true` only when all four checks come back clean — an affirmative reuse grant, no automated-collection prohibition found, no blocking `robots.txt` rule on the needed paths, and a real access mechanism. Every source below carries its fetch list and the operative quoted sentence so the clearance is independently reproducible, not merely asserted. Sources with gaps (undocumented rate limits, dataset-level personal-data risk, thin document coverage) are recorded honestly as open items in `disqualifiers` rather than smoothed over — a cleared source is not a source with zero remaining questions, it is a source with no reuse-terms question left unanswered.

Concepts were then built **only** on top of this already-cleared pool. This is the structural fix for Round 1's failure: a concept can no longer reach the scoring or gate stage riding on an unverified assumption about its own source's legality.

---

## Round 2 cleared source pool

All sources below were independently fetched and marked `cleared: true` by the source-and-compliance agent. Two additional candidate URLs were checked and **rejected** (recorded after the table) rather than cleared.

| Source | Owner | License | Operative quote (fetched, verbatim) | API / bulk access | Retains history | Exposes documents | Personal-data risk |
|---|---|---|---|---|---|---|---|
| [open.canada.ca](https://open.canada.ca) — Grants & Contributions / Travel & Hospitality (Proactive Disclosure) | Government of Canada / Treasury Board | Open Government Licence – Canada 2.0 | "The Information Provider grants you a worldwide, royalty-free, perpetual, non-exclusive licence to use the Information, including for commercial purposes." | CKAN Action API (`/data/api/3/action`) + direct CSV/JSON/XLSX bulk downloads, unauthenticated GET | false / TBD (no revision history observed in portal UI) | false | Low — Privacy Act "Personal Information" is explicitly excluded from the OGL grant itself |
| [open.canada.ca](https://open.canada.ca) — CanadaBuys tender notices (dataset `6abd20d4-...`) | Public Services and Procurement Canada | Open Government Licence – Canada | "Copy, modify, publish, translate, adapt, distribute or otherwise use the Information in any medium, mode or format for any lawful purpose." | Bulk CSV only (`canadabuys.canada.ca/opendata/pub/*.csv`); the HTML tender-browsing UI (`/en/tender-opportunities/*`) is `robots.txt`-disallowed and must NOT be scraped | true (per-fiscal-year files + cumulative "Complete" file since 2022-08-08) | false | Low / TBD — CSV header row not independently confirmed field-by-field |
| [open.toronto.ca](https://open.toronto.ca) | City of Toronto | Open Government Licence – Toronto (OGL-Ontario v1.0 based) | "The Information Provider grants you a worldwide, royalty-free, perpetual, non-exclusive licence to use the Information, including for commercial purposes." | CKAN API + `opendatatoronto` R package | true | false | Low — licence excludes "Personal Information" by MFIPPA cross-reference; Business Licences dataset flagged for per-dataset re-check |
| [data.europa.eu](https://data.europa.eu) (EU open-data metadata catalog) | Publications Office of the EU | CC0 1.0 (catalog metadata) + CC BY 4.0 (editorial content) | "the European Union has waived all copyright and related or neighbouring rights to metadata of the open data portal via Creative Commons CC0 1.0 Universal Public Domain Dedication." | Search/CKAN-style API + SPARQL endpoint, unauthenticated for reads; pagination up to 50,000/query documented | true | true | Low but not zero — portal harvests third-party metadata that "may include personal data" per its own Legal Notice |
| [find-tender.service.gov.uk](https://www.find-tender.service.gov.uk) | UK Cabinet Office / Crown Commercial Service | Open Government Licence v3.0 | "a worldwide, royalty-free, perpetual, non-exclusive licence to... exploit the Information commercially and non-commercially." | Public OCDS REST API (`ocdsReleasePackages`, `ocdsRecordPackages`), unauthenticated reads; daily bulk XML ZIP | true — `ocdsRecordPackages` retains full releases array, not latest-state-only | true (notices link to attachments) | Named contracting-authority contact (business role, not private individual) in Section I |
| [contractsfinder.service.gov.uk](https://www.contractsfinder.service.gov.uk) | UK Cabinet Office / Crown Commercial Service | Open Government Licence v3.0 | "You are granted a worldwide, royalty-free, perpetual, non-exclusive licence to use the Information... exploit the Information commercially and non-commercially." | OCDS Search API + day-granularity bulk CSV harvester, unauthenticated | false | true | Bounded — organisation/contract-level by design, but individual notices/PDFs can carry named sole-trader or signatory contacts |
| [data.ted.europa.eu](https://data.ted.europa.eu) (EU Tenders Electronic Daily) | Publications Office of the EU | Freely reusable per 2011 Commission reuse Decision; CC BY 4.0 (editorial); CC0 1.0 (system metadata) | "the procurement notices published in the Supplement to the Official Journal of the European Union can be freely reused, for commercial or non-commercial purposes." | Daily/monthly bulk XML packages (no sign-in), anonymous Search API, SPARQL/RDF; documented fair-usage policy (600 downloads/6 min/IP; 700 HTTP requests/min) | true | true | Low — named contacts are institutional procurement officials, not private individuals |
| [data.cityofnewyork.us](https://data.cityofnewyork.us) — Recent Contract Awards (`qyyg-4tf5`) | NYC DCAS / Office of Citywide Procurement | Public Domain (dataset metadata) | Socrata Views API License field: `"Public Domain"`; NYC Open Data overview: "no restrictions on the use of Open Data." | Socrata SODA API, no auth required for reads; CSV/XML/RDF export | false — current-state only, no vendor-provided history | false — `DocumentLinks` field present but empty in sample | Low — sampled contact fields are city-agency staff on `.nyc.gov` addresses, not private individuals |
| [open.fda.gov](https://open.fda.gov) (openFDA) | U.S. FDA / HHS | CC0 1.0 Universal | "the content, data, documentation, code, and related materials on openFDA is public domain... You can copy, modify, distribute and perform the work, even for commercial purposes, all without asking permission." | REST API (`api.fda.gov`), 240 req/min & 1,000 req/day unauthenticated, higher with free key; official bulk-download service with machine-readable manifest | true | false | Low — flagship adverse-event dataset is de-identified before public release |

**Rejected, not cleared** (checked and excluded from the pool, so they are not silently missing):

- `https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/` (as applied to the Discovery catalogue) — the Discovery API's own Terms and Conditions state verbatim **"Please do not cache or store any content returned by the API"**, which forecloses any change-detection or snapshot-history design — the identical structural defect that disqualified Google Places in Round 1. Also flagged: `robots.txt` disallows the specific catalogue/search/discovery paths a scraper would need, and the underlying catalogue contains records about identifiable living individuals, some closed for up to 100 years under the Data Protection Act 2018 / UK GDPR.
- `https://resources.data.gov/open-licenses/` — not a data source at all. It is federal policy/guidance documentation about what qualifies as an "open license," addressed to agencies publishing their own datasets elsewhere. No records exist on this page for any concept to be built on.

---

## Round 2 candidates

Three candidates were scored against the same seven Phase 1 criteria used in Round 1, built only on the cleared pool above.

| Candidate | 1. Similarity to paid work | 2. Lawful source availability | 3. Extraction/data-quality difficulty | 4. Dataset usefulness | 5. Measurable without fabrication | 6. Time to first release | 7. Reusable-service potential | **Total /35** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `uk-public-buyer-cross-source-resolution` (Find a Tender + Contracts Finder entity resolution) | 4 | 4 | 5 | 4 | 4 | 3 | 4 | **28** |
| `uk-procurement-amendment-monitor` (Find a Tender change/amendment monitoring) | 4 | 3 | 4 | 4 | 4 | 4 | 4 | **27** |
| `uk-tender-document-reconciler` (Find a Tender PDF-vs-OCDS reconciliation) | 4 | 3 | 4 | 3 | 4 | 3 | 4 | **25** |

Ranked by raw total, `uk-public-buyer-cross-source-resolution` scores highest. As with Round 1, **the raw score is not the recommendation basis** — see [Round 2 gate and adversarial review](#round-2-gate-and-adversarial-review) below, where this leader is displaced.

### `uk-public-buyer-cross-source-resolution` (Round 2 leader — 28/35)

| Criterion | Score | Rationale |
|---|---:|---|
| 1. Similarity to paid Upwork work | 4 | Cross-source data reconciliation, entity matching, and dedup/CRM-hygiene tasks are common paid Upwork gigs. Public-sector procurement specifically is a smaller niche than generic scraping, so strong but not a 5. |
| 2. Lawful source availability | 4 | Both Find a Tender and Contracts Finder are official UK government OCDS APIs, documented, unauthenticated read access, actively maintained government infrastructure. Not a 5 because OCDS schema/field completeness (e.g. inconsistent presence of `GB-COH`) is admittedly uneven. |
| 3. Extraction/data-quality difficulty | 5 | Genuine hard problem: disjoint ID namespaces, no shared key, field-level conflict resolution, blocking, confidence scoring, human review queue with full provenance. |
| 4. Dataset usefulness | 4 | Real government contracting data with real commercial meaning. Capped below 5 because the vertical proof is a single short week-long window with a bounded blocked candidate set. |
| 5. Measurable without fabrication | 4 | Explicit denominators, a named blocking-recall gap reported separately, explicit refusal to claim population-level recall, OCID deliberately withheld from the matcher to avoid a leaked oracle. **The adversarial review below found the premise of this design factually broken — see [provability lens](#round-2-gate-and-adversarial-review).** |
| 6. Time to a convincing first release | 3 | Requires building collection, extraction, blocking, scoring, AND a full manual review queue/UI before any credible numbers exist. |
| 7. Reusable-service potential | 4 | The blocking + confidence scoring + review queue + benchmark pattern is generalizable across future iterations beyond this specific source pair. |

**Total: 28/35.** **Weakest link:** time to a convincing first release (3/5) — collection, extraction, blocking, confidence scoring, and a manual review queue are all required before any credible precision/recall number exists.

**Provability statement (as scored):** "The concept deliberately withholds OCID from the matcher to avoid a leaked oracle, reports the blocking-recall gap separately from the headline number, and refuses to claim population-level recall — precision/recall are computed only over labeled pairs in the reviewed blocked set." (This statement is directly contradicted by measured evidence in the adversarial review below.)

### `uk-procurement-amendment-monitor` (27/35)

| Criterion | Score | Rationale |
|---|---:|---|
| 1. Similarity to paid Upwork work | 4 | Directly mirrors demand-matrix signals for tender/contract monitoring, change alerting, and an operator dashboard. UK-specific monitoring is a narrower niche than the broader US-focused demand signals cited. |
| 2. Lawful source availability | 3 | Live working API calls verified (pagination, `updatedFrom`/`updatedTo`, tag arrays), but the rate-limit ceiling is undocumented and only empirically discoverable at build time; no license/ToS text was directly quoted for this specific concept write-up despite the cleared-source record existing for Find a Tender. |
| 3. Extraction/data-quality difficulty | 4 | Cursor pagination, incremental polling against a high-water mark, OCID-based timeline grouping, tag-based event classification, and a manual-review reconciliation step against raw payload — real substance, though structured JSON API consumption rather than messier extraction. |
| 4. Dataset usefulness | 4 | Real, live UK central-government procurement amendment data with commercial meaning. Capped below 5 by a bounded seed set (~100-200 ocids) and exclusion of document/attachment content. |
| 5. Measurable without fabrication | 4 | Defines a real, non-self-referential denominator (independently queried via the same API's date-range filter, decoupled from the pipeline's own capture log), plus a manual-review reconciliation step and falsifiability criteria for recall, precision, and latency. |
| 6. Time to a convincing first release | 4 | Well-bounded vertical-proof scope; API mechanics already confirmed working live, which meaningfully de-risks build time. |
| 7. Reusable-service potential | 4 | The change-detection/denominator pattern is explicitly designed to generalize to other `retainsHistory: true` OCDS-compatible sources (TED, CanadaBuys). |

**Total: 27/35.** **Weakest link:** the concept write-up never itself fetched or quoted license/ToS text for Find a Tender (despite that text existing in the cleared-source record) and leaves the API rate-limit ceiling completely undocumented/TBD — meaning the two pillars Round 1 failed on are the same two things not yet nailed down with fetched evidence in this concept's own writeup, only inferred from the adjacent cleared-source record.

**Provability statement (as scored):** "Recall, precision, and latency are measured against a denominator drawn from an independent query of the same API over a fixed date-range window, decoupled from the pipeline's own capture log, plus a manual-review reconciliation pass against raw payload for a bounded ocid sample; population-level amendment rate is explicitly left TBD rather than estimated."

### `uk-tender-document-reconciler` (25/35)

| Criterion | Score | Rationale |
|---|---:|---|
| 1. Similarity to paid Upwork work | 4 | B2G procurement/tender monitoring and document parsing against a public register closely mirrors GovWin IQ/SAM.gov Contract Monitor style gigs. |
| 2. Lawful source availability | 3 | Find a Tender is stable under OGL v3.0 with no `robots.txt` block, but the viable slice depends on a thin, empirically ~6-10% minority of notices carrying genuine PDF attachments; that filtered subset's day-to-day stability is unverified beyond one session's sample. |
| 3. Extraction/data-quality difficulty | 4 | Genuine multi-page PDF parsing with page/byte-offset provenance plus a two-source (PDF vs OCDS JSON) reconciliation state machine, though the first proof slice is scoped to a single field (deadline). |
| 4. Dataset usefulness | 3 | Real, non-synthetic commercial data, but explicitly scoped to a small filtered fixture set with only deadline reconciled; coverage intentionally narrow (~10% of notices). |
| 5. Measurable without fabrication | 4 | Real denominator (fixture notices manually reviewed), a falsification condition (verdict mismatch beyond stated tolerance), separated from an independently reproducible coverage ratio — though sample so far is only 2 notices/6 documents. |
| 6. Time to a convincing first release | 3 | Well-scoped slice helps speed, but requires building PDF fetch+extraction with page-locator provenance, an OCDS reconciliation state machine, and a manual-review harness. |
| 7. Reusable-service potential | 4 | The reconciliation pipeline stage (fetch->extract->lookup->verdict->benchmark) is explicitly designed for reuse on other document-bearing sources (Contracts Finder, data.europa.eu), and fills a genuine portfolio gap — no document-touching capability exists yet. |

**Total: 25/35.** **Weakest link:** source stability/headroom for the PDF-bearing subset — only two notices' PDFs have actually been fetched and confirmed, and the ~6-10% PDF-bearing minority ratio rests on a single 100-release sample over a two-month window.

**Provability statement (as scored):** "Verdicts (deadline match / mismatch) are computed against a manually reviewed fixture set of notices, with a stated tolerance and an explicit failure condition (verdict mismatch beyond tolerance); coverage ratio (fraction of notices with reconcilable PDFs) is reported separately as a reproducible measurement, not folded into the accuracy headline."

---

## Round 2 gate and adversarial review

The relevance-and-uniqueness gate and all three adversarial lenses were run against the Round 2 leader, `uk-public-buyer-cross-source-resolution` (28/35). Verdicts are recorded verbatim below, not softened.

### Gate result: FAILS (passes = false)

> **Net-new technical capability test — PASSES.** Cross-source entity resolution across two disjoint government ID namespaces with no shared key: candidate blocking, field-level conflict resolution with confidence scoring, a provenance-carrying human review queue, and a benchmark that deliberately withholds the OCID linkage from the matcher so it cannot act as a leaked oracle. Verified net-new against the actual prior-concept list: the tracking log's portfolio catalog holds exactly one non-candidate entry (WS-000, a process/tracking layer with no sources, extraction, matching or delivery of its own), the Shared Shipping Pipeline capability ledger contains no entity-resolution capability in any state, and no completed or active project holds this.
>
> **Two-of-seven-dimensions test — PASSES, but near-vacuously**, for the same reason as Round 1: there are zero completed portfolio projects to differ from.
>
> **Candidate/duplication register test — FAILS. This is the decisive finding.** The candidate's subject matter is UK government procurement notices, its buyer is bid-pursuit/BD on public-sector procurement, and its own criterion-1 rationale names "procurement-intelligence scraping" — the same `PORTFOLIO_TRACKING_LOG.md` register row, **Public opportunity intelligence** (state DEFERRED), whose leader failed the Round 1 gate. Checked against that row's five named distinctness requirements:
> - Provenance — **covered** ("human review queue with full provenance", field-level conflict resolution).
> - Structured qualification — **absent.** No criterion performs deterministic eligibility assessment (CPV code, lot, value threshold, buyer type, place of performance) producing reason-coded accepted/rejected/review-needed states.
> - Solicitation documents — **absent.** Both cleared UK sources are recorded `exposesDocuments: true`; documents were simply not taken into scope.
> - Amendments — **absent.** No version or revision handling; Contracts Finder is recorded `retainsHistory: false` and the proof is a single cross-sectional window.
> - Deadline change tracking — **absent.** No change-detection behavior of any kind; a static one-window reconciliation.
>
> Coverage: 1 of 5. Round 1's leader covered 3 of 5 and FAILED. This candidate covers strictly fewer register-named requirements than the concept the register already rejected in the same family.
>
> **Second, unacknowledged duplication:** the candidate's angle reproduces the "What would make it distinct" column of the register's **Business-location monitoring** row almost verbatim ("Cross-source entity resolution, operating-detail changes, conflict review, scheduled monitoring") — covering 2 of 4 and omitting operating-detail changes and scheduled monitoring, silently stripping a registered sibling concept of half its distinctness without a recorded decision.
>
> **Process debt carried forward:** Round 1 required change #4 ("Record the compliance findings in repository files before approval") is still unmet — `design/SOURCE_AND_COMPLIANCE_LEDGER.md` does not exist, and the verified licence/robots evidence for the cleared source pool lives only outside version control.

**Required changes recorded by the gate** (for any future revival): add structured qualification as a scored capability; restore at least one more register-named requirement (solicitation documents is the cheapest, since both sources are `exposesDocuments: true`); resolve the collision with the Business-location monitoring register row explicitly; re-scope the headline claim from a technique ("cross-source entity resolution") to a buyer-facing outcome; write `design/SOURCE_AND_COMPLIANCE_LEDGER.md` before any approval; preserve the provability design's withheld-oracle discipline through any rescope; re-run the gate after changes — a high rubric total or a genuinely cleared source pool are not substitutes for a passed register test.

### Novelty lens — refuted = true

> The concept adopts, unchanged, the CROSS-SOURCE IDENTITY matching problem (N sources, one entity) that `PORTFOLIO_TRACKING_LOG.md` already assigns as the named distinctness requirement of the sibling business-location-monitoring candidate, altering only the website (Places/Netrows -> Find a Tender/Contracts Finder) and the industry label (local business -> UK public buyer) — precisely the substitution README line 167 disqualifies.
>
> Compounding this, the matching difficulty it demonstrates is a **closing transitional artifact**, not an intrinsic problem, verified against fetched primary government text: GOV.UK PPN 019 guidance states verbatim *"the Procurement Act 2023 does not require publication of notices on Contracts Finder"* and *"there should be no ongoing requirement to publish opportunity notices on Contracts Finder after 25 February 2025."* GOV.UK Central Digital Platform guidance states the new PPON identifier *"will appear in every notice and is the way that information about that organisation is joined together digitally"* — the exact shared key the concept claims does not exist. Live API sampling confirmed GB-PPON now covers 51-73% of Find a Tender buyer parties and 0% of Contracts Finder's frozen legacy records, so the concept's own bounded one-week proof window sits inside a shrinking tail of a problem the source owner is retiring by statute.
>
> Also found (supporting, not primary): free commercial tooling already ships this exact capability as a default-on flag — one Apify actor advertises "Automatic deduplication — same tender on both platforms is returned once," another ships a `dedupeByOcid` parameter "enabled by default."

### Compliance lens — refuted = true

> The clearance never fetched the operative terms page. `https://www.contractsfinder.service.gov.uk/Home/TermsAndConditions` (HTTP 200) governs both sites and carries a full "Acceptable Use" section the clearance record did not cite. Its binding sentences bar "Monitoring or Crawling... that impairs or disrupts the System" and, more decisively, **"Using manual or electronic means to avoid any use limitations placed on a System, such as access and storage restrictions."** The clearance record itself documents that both APIs enforce undocumented rate limits (Contracts Finder via HTTP 403 + "wait 5 minutes", Find a Tender via 429 + Retry-After) with the numeric threshold marked TBD, and proposes discovering the ceiling by probing until it trips — precisely the "electronic means to avoid a use limitation" the clause describes.
>
> Independently fatal: OGL v3.0 exempts "personal data in the Information" from its licence grant, and this concept's entire method is name/address/contact similarity matching. Live data fetched during review confirms personal data is pervasive and unavoidable in the fields the matcher needs: Contracts Finder returned named officer contacts with direct-dial numbers; Find a Tender returned supplier contacts at personal Gmail addresses (sole traders, where the business identity IS the natural person) and a personal UK mobile number. Blocking, confidence scoring, a persistent human review queue, and a published sanitized example dataset all constitute storage and republication of identifiable personal data outside the OGL grant, with no lawful basis, retention limit, or DPIA in scope — the identical defect the scorecard already recorded against the Round 1 leader's contracting-officer POC fields, relocated to a new source rather than cured.

### Provability lens — refuted = true

> **The cross-source join key does not exist**, so ground truth cannot be independent of the matcher. Measured from live payloads (100 Find a Tender releases; two independent 100-release Contracts Finder windows): Find a Tender buyer-party identifier schemes are `GB-PPON` (majority), `GB-COH`, `GB-NHS`, `GB-CHC`, none (~25%); Contracts Finder buyer-party identifier schemes are `GB-SRS`, `GB-LAE`, `GB-GOR`, and **no coded identifier at all for the majority (55/100)**. Measured scheme intersection between the two sources: **empty set**. Measured shared (scheme, id) buyer pairs: **0**.
>
> The concept's central provability claim — that OCID is "deliberately withheld from the matcher to avoid a leaked oracle" — presumes an oracle exists to withhold. It does not: OCID namespaces are disjoint by construction (`ocds-h6vhtk-*` vs `ocds-b5fd17-*`; measured OCID intersection 0), so OCID was never a cross-source identity oracle. With no coded identifier on the majority of the Contracts Finder side, the only surviving match signal is the buyer NAME STRING — which is also the matcher's primary input feature. The operator's manual labels are therefore produced by reading the same strings the matcher consumes: precision/recall become self-referential, the pipeline grading itself. **This is Round 1's unfalsifiable-headline-metric failure reproduced in a new source pair, not avoided by it.**
>
> The claimed denominator ("labeled pairs in the reviewed blocked set") is a denominator for blocking-set precision only — there is no denominator for TRUE cross-source buyer pairs in the population, so recall is not merely "deliberately not claimed," it is structurally unmeasurable with these two sources.

**Summary across lenses:** Gate — fails. Novelty — refuted. Compliance — refuted. Provability — refuted. All three adversarial lenses and the gate agree: the Round 2 leader does not survive as scored, for reasons independent of source legality (which, notably, was NOT what failed this time — the sources themselves remain cleared).

---

## Recommendation

**Recommended concept (provisional): `uk-procurement-amendment-monitor` (27/35).**

The Round 2 leader, `uk-public-buyer-cross-source-resolution` (28/35), **failed the relevance-and-uniqueness gate** (1 of 5 register-named distinctness requirements met, fewer than Round 1's leader, which failed on 3 of 5) **and was refuted on all three adversarial lenses** — novelty (the matching problem is a closing transitional artifact, already the register's Business-location-monitoring distinctness mechanic wearing a new industry label), compliance (the personal-data-exempt OGL licence cannot cover the name/contact matching the method requires, and the site's Acceptable Use clause bars circumventing undocumented rate limits), and provability (the two sources' buyer-identifier namespaces have a measured empty intersection, so the claimed withheld-oracle benchmark design has no oracle to withhold — precision/recall would be self-referential). **The leader failed and was displaced, exactly as happened in Round 1 with a different candidate.** Its full scoring, gate result, and refutations are preserved above rather than deleted.

`uk-procurement-amendment-monitor` is recommended as the next-best evidence-based option:

- It scores second overall in Round 2 (27/35), with no criterion below 3.
- It is built on the same cleared, license-verified Find a Tender source (OGL v3.0, quoted operative sentence, unauthenticated OCDS API confirmed working live), so it does not reopen the licensing question that Round 2 exists to have already answered.
- Its provability design defines an independent, non-self-referential denominator: recall/precision/latency are measured against a denominator drawn from an independent query of the same API over a fixed date-range window, decoupled from the pipeline's own capture log — this is a materially different design from the refuted leader's broken withheld-oracle mechanism, because it does not depend on a cross-source join key that turned out not to exist.
- Its weakest link is process, not structural: the concept write-up itself never fetched/quoted the Find a Tender license/ToS text (though that text exists, verified, in the cleared-source record above) and the API's numeric rate-limit ceiling remains undocumented/TBD.

**This recommendation is provisional and has NOT itself cleared the gate or the three adversarial lenses.** Per the orchestrator's own promotion note, runner-up promotion authorizes running that gate and review — it does not substitute for it. Before this concept can move WS-001 to `APPROVED`, the same gate-and-adversarial-review pass applied to the Round 2 leader above must be run against `uk-procurement-amendment-monitor`, specifically checking it against the same **Public opportunity intelligence** register row (structured qualification, solicitation documents, amendments, deadline tracking, provenance) that sank both the Round 1 leader and the Round 2 leader — a UK amendment monitor sits in the same register family and must not be assumed to clear it merely because its provability design is sounder.

`uk-tender-document-reconciler` (25/35) remains the lowest-scored Round 2 candidate and is not recommended at this time; its full scoring is preserved above as a fallback, and it shares the same unresolved register-collision risk as the other two.

---

## Approval request

Per `PHASE_01_DISCOVERY_AND_EVIDENCE_PLAN.md`, "Approval gate before implementation," the following five items still require human decision before Phase 2 (implementation) may begin. None of these decisions has been made by an agent in either round; they are listed here awaiting human review.

1. **Selected use case and target client** — awaiting decision. Round 2 recommends `uk-procurement-amendment-monitor` (UK public-sector procurement change/amendment monitoring) over the higher-scoring but gate-failed and triply-refuted `uk-public-buyer-cross-source-resolution`. `uk-tender-document-reconciler` is the lowest-scored Round 2 option. A human approver must confirm or override this recommendation, and must be aware that the recommended concept has **not yet itself been run through the gate or adversarial lenses.**
2. **Target sources and compliance ledger** — awaiting decision. No `design/SOURCE_AND_COMPLIANCE_LEDGER.md` exists in the repository yet, in either round. The Round 2 cleared-source pool above (Find a Tender, Contracts Finder, TED, data.europa.eu, open.canada.ca, open.toronto.ca, NYC Open Data, openFDA), with fetched license text and quoted operative sentences, must be committed to that file before this item can be considered resolved, regardless of which concept is approved.
3. **Data contract and expected exports** — to be drafted after approval. This is a Run 2 deliverable (`design/DATA_CONTRACT.md`), dependent on which concept is approved under item 1.
4. **Proof metrics and benchmark method** — to be drafted after approval. This is a Run 2 deliverable (`design/PROOF_AND_BENCHMARK_SPEC.md`), dependent on which concept is approved under item 1. No benchmark has been run for any candidate in either round; every quantitative reference in this scorecard is a rubric score, a count of recorded demand signals, or a count of measured API-payload facts gathered during compliance/adversarial review — never a measured pipeline result.
5. **Phase 2 minimum viable build scope** — awaiting decision. Cannot be scoped until items 1-4 are resolved, and cannot be scoped for `uk-procurement-amendment-monitor` specifically until it clears its own gate/adversarial run. Phase 2 must not expand into authentication bypass, large-scale infrastructure, paid data acquisition, or collection of sensitive personal information without a new explicit decision, per the Phase 1 plan. Given that the Round 2 leader was refuted specifically for a personal-data/licence-exemption collision, any approved scope must explicitly exclude persisting or matching on named-individual contact fields regardless of which concept is ultimately approved.
