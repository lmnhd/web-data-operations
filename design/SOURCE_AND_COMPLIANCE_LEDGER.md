# Source and Compliance Ledger

**Date:** 2026-09-02
**Iteration:** WS-001
**Round:** 2 (sources cleared before concepts were proposed)
**Prepared by:** Source and compliance agent (scribe)

This is the Phase 1 workstream-3 deliverable (`design/SOURCE_AND_COMPLIANCE_LEDGER.md` per `PHASE_01_DISCOVERY_AND_EVIDENCE_PLAN.md`) and the required-changes item #4 recorded against the Round 1 leader in `research/CANDIDATE_SCORECARD.md` ("Record the compliance findings in repository files before approval — none currently exist on disk"). It is now backed by real clearance work rather than narrative claims in agent messages.

**Status flag, stated up front and not smoothed over:** the Round 2 leader candidate built on the cleared sources below (`uk-public-buyer-cross-source-resolution`) **failed the relevance/uniqueness gate** (`passes: false`) and was **refuted on all three adversarial lenses** (novelty, compliance, provability) in the same evaluation round this ledger reports on. The runner-up (`change-monitoring`, UK procurement amendment monitoring) is recommended but has **not itself cleared the gate or the adversarial lenses**. This ledger records source clearance only — it does not constitute concept approval. See `PORTFOLIO_TRACKING_LOG.md` for the current iteration status.

---

## Method

Round 1 produced three candidate concepts and checked their source legality only after the concepts were designed. All three hit source restrictions discovered only at the compliance and adversarial-review stages — the source's actual terms were never fetched until a concept had already been built around an assumption about what the source would allow.

Round 2 inverts that order. A concept may only be proposed on a source whose reuse terms have **already been verified by fetching the actual license text, the actual robots.txt, and the actual terms-of-use page** — not inferred from the source's reputation, category, or a vendor's marketing copy. Each candidate source below was ccleared by an initial review, then **independently re-verified by a second agent whose task was specifically to try to disqualify it** (the same adversarial posture applied to concepts, applied one layer earlier, to sources). A source is recorded as cleared only when both passes agree it clears; every fetch performed during clearance is logged per source so the finding can be reproduced rather than taken on faith.

This method does not guarantee the resulting concept clears the relevance/uniqueness gate or survives adversarial review — see the Status flag above. It guarantees only that no concept in this round was proposed on a source whose reuse terms were unverified at proposal time, which was the specific, named Round 1 defect.

---

## Cleared sources

Nine sources were independently cleared this round. For each: owner, URL, licence name and link, the operative quote verbatim, access path, API/bulk availability, rate guidance, retains-history, exposes-documents, personal-data risk, fallback if unavailable, and the exact list of URLs fetched during clearance.

### 1. Open Government Licence — Canada (Government of Canada open data)

- **URL:** https://open.canada.ca/en/open-government-licence-canada
- **Owner:** Government of Canada — His Majesty the King in right of Canada (Treasury Board of Canada Secretariat operates the portal; individual datasets are published by the responsible federal institution).
- **Licence name and link:** Open Government Licence – Canada, Version 2.0 — https://open.canada.ca/en/open-government-licence-canada
- **Operative quote (verbatim):** "The Information Provider grants you a worldwide, royalty-free, perpetual, non-exclusive licence to use the Information, including for commercial purposes" and "Copy, modify, publish, translate, adapt, distribute or otherwise use the Information in any medium, mode or format for any lawful purpose." Sole condition: "Acknowledge the source of the Information by including any attribution statement specified by the Information Provider(s) and, where possible, provide a link to this licence." Personal Information as defined in section 3 of the Privacy Act is explicitly excluded from the licence's scope.
- **Access path:** Official CKAN Action API at `open.canada.ca/data/api/3/action` (GET-only, no authentication for public datasets), plus direct CSV/JSON/XLSX bulk downloads per dataset.
- **API/bulk availability:** Yes, both — see above. No documented numeric rate limit was found on any fetched page; recorded as **TBD**, not assumed unlimited.
- **Rate guidance:** TBD (no numeric limit published in the pages fetched).
- **Retains history:** False / TBD. No dataset-level version/revision history was observed in the portal UI; a change-detection design would need to take its own dated snapshots or separately verify CKAN's activity-stream/revision endpoints rather than assume the portal retains history.
- **Exposes documents:** No.
- **Personal-data risk:** Low. The OGL 2.0 text itself excludes Privacy Act "Personal Information" from the grant. Datasets reviewed (Grants and Contributions; Travel, Hospitality and Conferences) concern institutions and officials in an institutional/legally-mandated-disclosure capacity, not incidental scraping of private individuals. Grant-recipient names are an intentional, legally mandated feature of transfer-payment transparency, not a general-purpose people-search dataset — treat accordingly.
- **Fallback if unavailable:** Direct bulk CSV/JSON/XLSX download per dataset does not depend on the CKAN API being reachable.
- **Fetches performed during clearance:**
  - https://open.canada.ca/robots.txt
  - https://open.canada.ca/en/open-government-licence-canada (fetched twice)
  - https://open.canada.ca/en/terms-and-conditions (404 — does not exist)
  - https://open.canada.ca/en
  - https://www.canada.ca/en/transparency/terms.html (fetched twice)
  - https://open.canada.ca/en/using-open-data
  - https://open.canada.ca/en/access-our-application-programming-interface-api
  - https://open.canada.ca/data/en/dataset (redirected to search.open.canada.ca/en/opendata)
  - https://open.canada.ca/data/en/dataset/4ae27978-0931-49ab-9c17-0b119c0ba92f
  - https://open.canada.ca/data/en/dataset/432527ab-7aac-45b5-81d6-7597107a7013
- **robots.txt finding:** 58 Disallow entries, all confined to CMS/admin/search-UI plumbing (`/admin/`, `/user/login`, `/comment/reply/`, sort-parameter URLs). No Disallow on `/data/` or `/data/api/`. Crawl-delay: 20 (site-wide).
- **Terms finding:** No sentence in the fetched governing terms (`www.canada.ca/en/transparency/terms.html`, fetched twice) prohibits automated data gathering, scraping, bots, or crawlers — the exact category of clause that killed SAM.gov in Round 1, verified absent here.

### 2. Open Government Licence — Toronto (City of Toronto open data)

- **URL:** https://open.toronto.ca/open-data-licence/
- **Owner:** City of Toronto (portal operated as open.toronto.ca).
- **Licence name and link:** Open Government Licence – Toronto (based on OGL – Ontario v1.0) — https://open.toronto.ca/open-data-licence/
- **Operative quote (verbatim):** "The Information Provider grants you a worldwide, royalty-free, perpetual, non-exclusive licence to use the Information, including for commercial purposes, subject to the terms below. You can copy, modify, publish, translate, adapt, distribute or otherwise use the Information in any medium, mode or format for any lawful purpose."
- **Access path:** CKAN-based API (documented endpoints such as `datastore_search`, `download_resource`; custom Toronto CKAN extension) plus a maintained R client package (`opendatatoronto`).
- **API/bulk availability:** Yes. No documented rate-limit guidance was located on the fetched portal docs hub — recorded **TBD**.
- **Rate guidance:** TBD.
- **Retains history:** True.
- **Exposes documents:** No.
- **Personal-data risk:** The licence explicitly excludes "Personal Information" (by cross-reference to Ontario MFIPPA s.2(1)) and separately excludes information not accessible under MFIPPA/PHIPA. One dataset noted in search results (Business Licences, not yet fetched directly) may include sole-proprietor names/phone numbers alongside business identity — a per-dataset due-diligence item, not a source-level disqualifier.
- **Fallback if unavailable:** Direct dataset CSV/JSON downloads via the portal, independent of the API.
- **Fetches performed during clearance:**
  - https://open.toronto.ca/robots.txt
  - https://open.toronto.ca/open-data-license/ (404 — wrong URL spelling)
  - https://open.toronto.ca/open-data-licence/ (fetched twice, full text)
  - https://open.toronto.ca/docs/frequently-asked-questions/
  - https://www.toronto.ca/city-government/data-research-maps/open-data/open-data-licence/
  - https://open.toronto.ca/dataset/4def3f65-2a65-4a4f-83c4-b2a4aed72d46/
  - https://open.toronto.ca/docs/
- **robots.txt finding:** Disallow only `/wp-admin/`; `/wp-admin/admin-ajax.php` explicitly Allowed. No restriction on `/dataset/`, `/docs/`, or `/api/`.
- **Terms finding:** No separate ToU distinct from the licence was found; the licence text itself (fetched twice from two mirrored URLs) contains no automated-collection, scraping, bot, or bulk-download prohibition.
- **Open items carried forward (not disqualifying):** Dataset-level personal-data check needed on Business Licences specifically before use; no numeric rate limit documented; one spot-checked dataset page was Retired with no resources populated, confirming not all datasets on the portal are equally usable — any concept must verify a specific active dataset directly.

### 3. data.europa.eu (EU Open Data Portal / metadata catalog)

- **URL:** https://data.europa.eu/en/legal-notice
- **Owner:** Publications Office of the European Union.
- **Licence name and link:** CC0 1.0 Universal (catalog metadata) + CC BY 4.0 (editorial content) — https://data.europa.eu/en/legal-notice. **Underlying dataset resources each carry their own source-assigned licence, not uniformly CC0** — see scope constraint below.
- **Operative quote (verbatim):** "the European Union has waived all copyright and related or neighbouring rights to metadata of the open data portal via Creative Commons CC0 1.0 Universal Public Domain Dedication ... Unless otherwise noted (e.g. in individual copyright notices), the reuse of the editorial content on this website owned by the EU is authorized under the Creative Commons Attribution 4.0 International (CC BY 4.0) licence ... Most of the resources published display a specific reference to the licence under which the owner has chosen to release them."
- **Access path:** Search/CKAN-style API (`data.europa.eu/api/hub/search/`), SPARQL endpoint (`data.europa.eu/sparql`, `/data/sparql`, full RDF triple store), Registry API.
- **API/bulk availability:** Yes. Read-only Search API requires no authentication; write operations require an OpenID Connect Party Token. Documented pagination guidance: up to 50,000 results per query (10,000 recommended to avoid side effects), incrementing offset until results are empty.
- **Rate guidance:** No numeric rate limit (requests/second or /day) published — **TBD**; a build must self-impose conservative throttling.
- **Retains history:** True.
- **Exposes documents:** True.
- **Personal-data risk:** Low but not zero. The Legal Notice's Third-Party Content section states the portal "publishes metadata from external sources, which may include personal data" and directs users to the original sources' privacy policies. Any concept must screen selected datasets to exclude those that are themselves registries of identifiable individuals.
- **Fallback if unavailable:** TED CSV subset at `data.europa.eu/data/datasets/ted-csv`; SPARQL endpoint as an alternate query path to the Search API.
- **Fetches performed during clearance:**
  - https://data.europa.eu/robots.txt
  - https://data.europa.eu/en/legal-notice (fetched twice: summary and full-text verbatim)
  - https://dataeuropa.gitlab.io/data-provider-manual/api-documentation/
  - https://data.europa.eu/en/faq
- **robots.txt finding:** Disallows only administrative/functional paths (`/admin/`, `/comment/reply/`, `/user/register|password|login|logout`, search/query-string patterns). No Disallow on dataset landing pages, the SPARQL endpoint, or the general API hub for a generic crawler. No Crawl-delay directive.
- **Terms finding:** No sentence in the Legal Notice prohibits automated data gathering, scraping, bots, or crawlers. The FAQ affirmatively states: "Integration on any external application with the portal can only happen at the dataset level by using the existing CKAN-API, via which you may 'extract/query' datasets" — naming programmatic extraction as the sanctioned integration path.
- **Scope constraint (not a disqualifier, but binding on any concept):** data.europa.eu is a metadata catalog harvesting descriptions from national/EU source portals. CC0 covers catalog metadata (titles, descriptions, tags, structure), not automatically the underlying dataset resources/files, which carry per-source licences (including non-commercial ones, per the FAQ). Any concept ingesting actual dataset content, not just catalog metadata, must verify the per-dataset licence field first.

### 4. Find a Tender (UK Crown Commercial Service / Cabinet Office)

- **URL:** https://www.find-tender.service.gov.uk/Developer/Documentation
- **Owner:** Crown Commercial Service / Cabinet Office (Crown copyright).
- **Licence name and link:** Open Government Licence v3.0 (UK) — http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/
- **Operative quote (verbatim):** "a worldwide, royalty-free, perpetual, non-exclusive licence to use the Information subject to the conditions below" including the right to "copy, publish, distribute and transmit the Information," "adapt the Information," and "exploit the Information commercially and non-commercially... by including it in your own product or application," conditioned only on attribution. Find a Tender's own terms page confirms: "Most content on Find a Tender is subject to Crown copyright protection and is published under the Open Government Licence."
- **Access path:** Public, unauthenticated, read-only REST API returning OCDS-formatted JSON — `GET /api/{version}/ocdsReleasePackages` and `GET /api/{version}/ocdsRecordPackages`, filterable by `updatedFrom`/`updatedTo`, `ocid`, notice ID, and procurement stage; cursor pagination (limit 1–100, default 100). Also a documented daily bulk XML ZIP download via data.gov.uk.
- **API/bulk availability:** Yes, both — see above. No account/key needed for retrieval (a `CDP-Api-Key` is required only for the separate notice-**submission** API used by licensed eSenders, not for read/collection).
- **Rate guidance:** Graceful rate limiting via HTTP 429 + `Retry-After` header; **no documented numeric requests-per-day quota found — TBD**, should be confirmed empirically at build time.
- **Retains history:** True. The `ocdsRecordPackages` endpoint retains the full `releases` array per procurement process (confirmed via its own documentation, including a live two-release sample tagged "planning" and "tender" for one ocid) — not just a latest-state snapshot.
- **Exposes documents:** True. Notices commonly link to attached procurement documents/PDFs via the platform's own notice-display mechanism (one specific example PDF URL returned 403/404 as a stale link — the mechanism itself is documented independently and should be re-verified at build time with a live example).
- **Personal-data risk:** OCDS notices include a Section I `contact` field with a named individual, email, and phone for the contracting authority — a government-published official/business point of contact required by the notice format itself, analogous to a published business card. Treat as organizational-role contact data in any data contract; consider redaction in public sanitized examples.
- **Fallback if unavailable:** Daily/monthly bulk XML ZIP download via data.gov.uk, independent of the live API.
- **Fetches performed during clearance:**
  - https://www.find-tender.service.gov.uk/robots.txt (WebFetch, then raw curl — both 404)
  - https://www.find-tender.service.gov.uk/Developer/Documentation (fetched twice)
  - https://www.find-tender.service.gov.uk/Home/TermsAndConditions (fetched twice)
  - http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/
  - https://www.find-tender.service.gov.uk/apidocumentation
  - https://www.find-tender.service.gov.uk/apidocumentation/1.0/GET-ocdsReleasePackages
  - https://www.find-tender.service.gov.uk/apidocumentation/1.0/GET-ocdsRecordPackages
  - https://www-tpp.find-tender.service.gov.uk/Notice/002194-2021/PDF (403, stale example link)
  - https://www.find-tender.service.gov.uk/Notices/OCDS/Search (404, stale/wrong path)
- **robots.txt finding:** Returns HTTP 404 (confirmed by raw curl showing the site's own rendered "Page not found" page) — no robots.txt file exists on the domain; therefore no Disallow directives apply anywhere.
- **Terms finding:** The "Acceptable Use" section of the Terms and Conditions prohibits only disruptive/abusive automation — "monitoring or crawling of a System that impairs or disrupts the System being monitored or crawled," "using manual or electronic means to avoid any use limitations placed on a System, such as access and storage restrictions," denial-of-service, forged headers, malware, IP infringement, illegal/fraudulent activity. **No SAM.gov-style blanket ban on "automated data gathering" or "web scraping tools" as such.** Users consent to Cabinet Office "recording details of any service access requests/downloads and the associated meta-data" (an access-logging notice, not a prohibition).

### 5. Contracts Finder (UK Crown Commercial Service / Cabinet Office)

- **URL:** https://www.contractsfinder.service.gov.uk/Search
- **Owner:** Crown Commercial Service (Cabinet Office) / Crown copyright.
- **Licence name and link:** Open Government Licence v3.0 (UK) — same instrument as Find a Tender, above.
- **Operative quote (verbatim):** "You are granted a worldwide, royalty-free, perpetual, non-exclusive licence to use the Information" including the right to "copy, publish, distribute and transmit the Information," "adapt the Information," and "exploit the Information commercially and non-commercially" — subject to attribution and exclusions for personal data and third-party rights.
- **Access path:** OCDS Search API (`GET Published/Notices/OCDS/Search`) with `publishedFrom`/`publishedTo` date filters, stage filters, cursor pagination (limit 1–100); day-granularity bulk CSV harvester (`GET Harvester/Notices/Data/CSV/{year}/{month}/{day}`).
- **API/bulk availability:** Yes, both. No authentication documented for read access on either endpoint.
- **Rate guidance:** Enforced via HTTP 403 with guidance to wait 5 minutes before retrying; **exact requests-per-minute threshold not stated — TBD**.
- **Retains history:** False. The API returns only current-state rows (update-in-place); no field-level change history is exposed. A change-detection concept built on this source must build and own its own snapshot archive — there is no vendor-provided historical ground truth.
- **Exposes documents:** True.
- **Personal-data risk:** Bounded but real. Notices are primarily organisational (buyer/supplier org names, addresses, CPV codes, values, dates), but individual notices and attached documents can contain identifiable personal data (individual names, phone numbers, emails tied to a natural person — e.g. sole-trader suppliers, named signatories). OGL v3.0 explicitly excludes personal data from its grant. A cleared concept must scope collection/display to organisation- and contract-level fields.
- **Fallback if unavailable:** Historical bulk dataset referenced via the UK government's CKAN data portal (`ckan.publishing.service.gov.uk`), organized by month/year (not independently fetched/verified this session).
- **Fetches performed during clearance:**
  - https://www.contractsfinder.service.gov.uk/robots.txt (HTTP 404, verified via curl -i)
  - https://www.find-tender.service.gov.uk/robots.txt (HTTP 404, verified via curl -i)
  - https://www.contractsfinder.service.gov.uk/Home/TermsAndConditions (fetched twice)
  - https://www.contractsfinder.service.gov.uk (footer/nav link discovery)
  - https://www.contractsfinder.service.gov.uk/apidocumentation
  - https://www.contractsfinder.service.gov.uk/apidocumentation/Notices/1/GET-Published-Notice-OCDS-Search
  - https://www.contractsfinder.service.gov.uk/apidocumentation/Notices/1/GET-Harvester-Notices-Data-CSV
  - https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/
- **robots.txt finding:** Does not exist (HTTP 404, verified via status-code check) — no Disallow directives.
- **Terms finding:** The same "Acceptable Use" section governs both Contracts Finder and Find a Tender (confirmed by the page's own opening line: "This page ... explains the Contracts Finder and Find a Tender service's terms and conditions. You must agree to these to use the Contracts Finder and Find a Tender services."). Prohibits disruptive/abusive automated access (crawling that "impairs or disrupts," "using manual or electronic means to avoid any use limitations placed on a System, such as access and storage restrictions," denial-of-service) — not automated collection per se. **Also states: "Provision of access to the Service is subject to business need"** (discretionary, revocable access) and that use of the service consents to CCS logging access/download metadata. See "Open compliance items" below — this clause interacts with the undocumented rate ceiling in a way that later adversarial review flagged as a real constraint on any polling design, not a blanket prohibition.

### 6. CanadaBuys tender notices (Public Services and Procurement Canada)

- **URL:** https://open.canada.ca/data/en/dataset/6abd20d4-7a1c-4b38-baa2-9525d0bb2fd2
- **Owner:** Public Services and Procurement Canada (dataset maintainer, per the open.canada.ca dataset page).
- **Licence name and link:** Open Government Licence – Canada (same instrument as entry 1, applies to this dataset per its catalog page) — https://open.canada.ca/en/open-government-licence-canada
- **Operative quote (verbatim):** "The Information Provider grants you a worldwide, royalty-free, perpetual, non-exclusive licence to use the Information, including for commercial purposes, subject to the terms below" combined with "Copy, modify, publish, translate, adapt, distribute or otherwise use the Information in any medium, mode or format for any lawful purpose."
- **Access path:** **Bulk CSV download only, not a REST/JSON API** — `https://canadabuys.canada.ca/opendata/pub/*.csv`: New Tender Notices (refreshed every 2h, 6:15am–10:15pm UTC-0500 daily), Open Tender Notices and per-fiscal-year files 2022–2027 (refreshed daily), Legacy Tender Notices 2009–2022, and a cumulative "Complete" file from 2022-08-08 onward. A companion XML data dictionary is published separately.
- **API/bulk availability:** Bulk CSV only (see above); no documented per-request rate limit needed since it is static file download.
- **Rate guidance:** N/A (static file download); respect the documented refresh cadence rather than polling faster than the source updates.
- **Retains history:** True (fiscal-year and legacy cumulative files provide dated historical coverage back to 2009).
- **Exposes documents:** No.
- **Personal-data risk:** Low / not fully confirmed absent by full schema. Fields identified (bilingual titles, closing dates, procurement category, tender/award status, reference/solicitation numbers, currency) show no personal data. Any contact field, if present, would be a government contracting-officer business contact — not confirmed absent from the raw CSV header, which should be spot-checked before build.
- **Fallback if unavailable:** N/A — this source's only access path is already the fallback-grade bulk file; no live API dependency exists.
- **Fetches performed during clearance:**
  - https://open.canada.ca/robots.txt
  - https://open.canada.ca/data/en/dataset/6abd20d4-7a1c-4b38-baa2-9525d0bb2fd2 (fetched twice)
  - https://open.canada.ca/en/open-government-licence-canada
  - https://canadabuys.canada.ca/en/tender-opportunities
  - https://www.canada.ca/en/transparency/terms.html
  - https://open.canada.ca/en/frequently-asked-questions
  - https://canadabuys.canada.ca/robots.txt
  - https://donnees-data.tpsgc-pwgsc.gc.ca/ba2/ac-cb/soutien-support-eng.html
- **robots.txt finding — IMPORTANT SCOPE CONSTRAINT:** `canadabuys.canada.ca/robots.txt` explicitly **disallows** the human-facing tender-browsing HTML interface: `/en/tender-opportunities/*` and `/fr/occasions-de-marche/*`, plus a catch-all `Disallow: /` for unnamed user agents. **Any concept that scrapes individual tender-notice detail pages by URL would violate robots.txt and must be avoided.** The bulk CSV path `/opendata/pub/*.csv` is **not** matched by any Disallow rule and is the sanctioned access method.
- **Terms finding:** No automated-collection prohibition found in the OGL-Canada text, the general Canada.ca Terms and Conditions, or the Open Government FAQ.

### 7. TED / data.ted.europa.eu (EU Publications Office — public procurement)

- **URL:** https://data.ted.europa.eu/
- **Owner:** Publications Office of the European Union (TED / SIMAP system).
- **Licence name and link:** CC BY 4.0 for editorial/website content; a broader reuse grant for the procurement notice data itself under the European Commission's 2011 reuse-of-documents Decision; CC0 1.0 for SIMAP system metadata. Legal notice: https://ted.europa.eu/en/legal-notice
- **Operative quote (verbatim):** "Copyright notice — © European Union, 1998-2026 — The European Commission's reuse policy is implemented by the Commission Decision of 12 December 2011 on the reuse of Commission documents. Unless otherwise noted, the procurement notices published in the Supplement to the Official Journal of the European Union can be freely reused, for commercial or non-commercial purposes. The copyright over the editorial content of the SIMAP websites ... is licensed under the Creative Commons Attribution 4.0 International (CC BY 4.0) license ... The SIMAP's system metadata is dedicated to the public domain in accordance with the Creative Commons Universal Public Domain Dedication deed (CC0 1.0)." Fair usage policy (verbatim, from the developers-corner page): "Visualize or download notices from a single IP / Limits: 600 visualizations or downloads in less than 6 minutes" and "HTTP requests / Limits: 700 requests in the last minute."
- **Access path:** XML bulk download (daily and monthly packages, no sign-in required); TED Search API (anonymous access; `api.ted.europa.eu/v3/notices/search`); TED CSV subset via data.europa.eu; RSS feeds; data.ted.europa.eu itself is a SPARQL/RDF knowledge-graph query service (JSON/CSV/TSV/XML/RDF export).
- **API/bulk availability:** Yes, multiple documented paths — see above.
- **Rate guidance:** 600 visualizations/downloads per IP per 6 minutes; 700 HTTP requests per minute — documented explicitly, quoted above. Note: this numeric policy was found on the sibling host `ted.europa.eu`, not confirmed verbatim on `data.ted.europa.eu` specifically; treated as the governing guidance for the whole open-data program pending confirmation, with an added safety margin recommended.
- **Retains history:** True.
- **Exposes documents:** True.
- **Personal-data risk:** Low, not zero. Named individuals appearing in notices are procurement/contracting officials in an official institutional capacity, not private individuals. TED's own user-account personal data (registered reuser profiles) is governed separately and states no automated decision-making/profiling is applied to that account data.
- **Fallback if unavailable:** Daily/monthly XML bulk packages do not depend on the Search API or SPARQL endpoint being reachable.
- **Fetches performed during clearance:**
  - https://data.ted.europa.eu/robots.txt (curl, HTTP 404 — GitHub Pages default 404; confirms no robots.txt file on this subdomain)
  - https://data.ted.europa.eu/ (curl 200, WebFetch summary)
  - https://ted.europa.eu/robots.txt (curl 200, full text)
  - https://ted.europa.eu/en/legal-notice (curl 200, 212KB fetched)
  - https://ted.europa.eu/en/help/data-reuse (curl 200, 170KB fetched)
  - https://ted.europa.eu/en/simap/developers-corner-for-reusers (curl 200, 180KB fetched — contains the fair-usage table)
  - https://ted.europa.eu/en/simap/developers-corner-for-reusers-fair-usage-policy-TED (curl 404 — stale search-snippet URL, superseded by the page above)
  - https://ted.europa.eu/api/documentation/index.html (curl 200, thin SPA shell — confirms the URL resolves, full content not JS-renderable)
  - https://docs.ted.europa.eu/ and /home/index.html (curl 200/redirect)
  - https://docs.ted.europa.eu/api/latest/index.html (curl 200, 41KB)
  - https://data.europa.eu/data/datasets/ted-csv?locale=en (curl 200, thin SPA shell)
- **robots.txt finding:** `ted.europa.eu/robots.txt` disallows only private/dashboard/login pages, Liferay internal-use paths, and dynamic search query strings, while explicitly **Allow**-ing `/*/simap/xml-bulk-download` and the SPA index paths. `data.ted.europa.eu/robots.txt` returns 404 (GitHub Pages hosting; no file exists at all on this subdomain, confirmed via `Server: GitHub.com` response header) — no restriction present by definition.
- **Terms finding:** No prohibition on automated data gathering, scraping, bots, or crawlers found on the legal notice, data-reuse page, or developers-corner page. These pages instead affirmatively document machine-access paths and state the Search API "can be accessed anonymously."

### 8. NYC Open Data — Recent Contract Awards (DCAS/OCP via NYC Open Data / Socrata)

- **URL:** https://data.cityofnewyork.us/City-Government/Recent-Contract-Awards/qyyg-4tf5
- **Owner:** NYC Department of Citywide Administrative Services (DCAS), Office of Citywide Procurement — published via the Socrata/Tyler Technologies-hosted NYC Open Data portal.
- **Licence name and link:** Public Domain, per dataset metadata (`license` field returned by `https://data.cityofnewyork.us/api/views/qyyg-4tf5.json`).
- **Operative quote (verbatim):** Dataset metadata API: `License: "Public Domain"`. NYC Open Data overview page (per fetched-page synthesis): "There are no restrictions on the use of Open Data." NYC.gov Terms of Use's only IP-type clause — "All other design, information, text, graphics, images, pages, interfaces, links, software, and other items and materials contained in or displayed on NYC.gov ... are the property of the City of New York. All rights are reserved." — is a general site-content/design reservation, not a scraping prohibition, and is assessed as inapplicable to the open datasets themselves.
- **Access path:** Socrata SODA API — `https://data.cityofnewyork.us/resource/qyyg-4tf5.json` (confirmed live by direct fetch, returned real JSON contract-award records). CSV/XML/RDF bulk export also available via `/api/views/qyyg-4tf5/rows.csv?accessType=DOWNLOAD`.
- **API/bulk availability:** Yes, both. No authentication required for read access; a free self-serve app token is optional.
- **Rate guidance:** Unauthenticated requests throttled per-IP (commonly cited ~10 req/sec shared pool, from secondary/community sources, not a directly fetched authoritative page). With a free app token, Socrata states "we do not throttle API requests that are using an application token, unless those requests are determined to be abusive or malicious," with a commonly cited soft allowance around 1,000 req/rolling hour. **Treat exact throttle numbers as TBD** — `dev.socrata.com/docs/rate-limits.html` returned 404 when fetched directly.
- **Retains history:** False. The API returns only current-state rows (update-in-place); no field-level change history is exposed. Any change-detection concept must build and own its own snapshot archive.
- **Exposes documents:** False (as sampled). The schema lists a `DocumentLinks` column, but 5 sampled records (including 2 with populated narrative text) contained no populated URLs/PDF links in any fetched field — this weakens, but does not disqualify, any concept design assuming document reconciliation as a difficulty driver on this dataset; would need re-verification across a larger sample.
- **Personal-data risk:** Low. Sampled `contact_name`/`contact_phone`/`email` fields (7–10 rows fetched directly) are populated exclusively with NYC government agency procurement staff (nyc.gov email domains, agency-line phone numbers) acting in official capacity — not private individuals. `vendor_name`/`vendor_address` fields identify contracted businesses, standard public-record business-entity data.
- **Fallback if unavailable:** CSV/XML/RDF direct export, independent of the SODA API.
- **Fetches performed during clearance:**
  - https://data.cityofnewyork.us/robots.txt
  - https://data.cityofnewyork.us/City-Government/Recent-Contract-Awards/qyyg-4tf5
  - https://data.cityofnewyork.us/api/views/qyyg-4tf5.json
  - https://opendata.cityofnewyork.us/overview/
  - https://www1.nyc.gov/home/terms-of-use.page (301 redirect)
  - https://www.nyc.gov/home/terms-of-use.page
  - https://dev.socrata.com/foundry/data.cityofnewyork.us/qyyg-4tf5
  - https://dev.socrata.com/docs/rate-limits.html (404)
  - https://dev.socrata.com/docs/app-tokens
  - https://data.cityofnewyork.us/resource/qyyg-4tf5.json?$limit=5 (and two further filtered sample queries)
  - https://data.cityofnewyork.us/City-Government/Recent-Contract-Awards/qyyg-4tf5/about_data
  - https://opendata.cityofnewyork.us/open-data-law/
- **robots.txt finding:** Disallow lines cover only browse/search-query-parameter URLs, legacy OData endpoints (`/OData.svc/`, `/api/odata/`), `/api/collocate*`, `/browse/embed`, `/login`, `/tiles/`. Crawl-delay: 1 second. No Disallow on `/City-Government/`, `/resource/`, or `/api/views/` — the paths this dataset needs are unrestricted.
- **Terms finding:** No sentence in the NYC Open Data overview, NYC.gov Terms of Use, or NYC Open Data law page prohibits automated data gathering, scraping, bots, crawlers, or bulk download.

### 9. openFDA (U.S. Food and Drug Administration)

- **URL:** https://open.fda.gov/license/
- **Owner:** U.S. Food and Drug Administration (openFDA program, HHS).
- **Licence name and link:** CC0 1.0 Universal (Public Domain Dedication) — https://open.fda.gov/license/
- **Operative quote (verbatim):** "the content, data, documentation, code, and related materials on openFDA is public domain and made available with a Creative Commons CC0 1.0 Universal dedication." / "You can copy, modify, distribute and perform the work, even for commercial purposes, all without asking permission."
- **Access path:** Official REST API (`api.fda.gov`, JSON) and official bulk download service (`download.open.fda.gov`, zipped JSON per endpoint, machine-readable manifest for automated retrieval).
- **API/bulk availability:** Yes, both. Confirmed working with no API key (test query `api.fda.gov/drug/event.json?limit=1` returned HTTP 200).
- **Rate guidance:** Documented and specific. Without a key: 240 req/min, 1,000 req/day per IP. With a free API key: 240 req/min, 120,000 req/day per key.
- **Retains history:** True (data updated on documented release cycles, e.g. FAERS quarterly), though explicit confirmation that superseded individual records are archived/versioned was not found — a genuine nuance to verify against the specific endpoint chosen.
- **Exposes documents:** No — openFDA serves structured JSON, not document files.
- **Personal-data risk:** Low. The flagship adverse-event dataset (FAERS) is de-identified before public release — patient names/addresses stripped, verbatim case narratives withheld specifically to protect patient confidentiality. Other datasets (recalls, labels, device/drug approvals) concern regulated products and manufacturers, not private individuals. One narrow carve-out: GMDN nomenclature content embedded in device data requires a separate licence from The GMDN Agency for commercial-categorization/AI-training reuse of that specific field only — noted, not a source-level disqualifier.
- **Fallback if unavailable:** `download.open.fda.gov` bulk files, independent of the live query API.
- **Fetches performed during clearance:**
  - https://open.fda.gov/robots.txt (WebFetch: 403; curl with browser UA: 403; curl default UA: 403 — confirmed AccessDenied infra error, not a Disallow rule, since every neighboring path on the domain returns 200)
  - https://api.fda.gov/robots.txt (curl: 404, file does not exist)
  - https://open.fda.gov/ (curl 200)
  - https://open.fda.gov/license/ (WebFetch + curl 200)
  - https://api.fda.gov/drug/event.json?limit=1 (curl, no key: 200)
  - https://open.fda.gov/terms/ (WebFetch 200)
  - https://open.fda.gov/apis/authentication/ (WebFetch 200)
  - https://open.fda.gov/downloads/ (403 — wrong/stale path)
  - https://open.fda.gov/data/drugadverseevents/ (403 — wrong/stale path)
  - https://open.fda.gov/apis/drug/event/ (WebFetch 200)
  - https://open.fda.gov/apis/drug/event/#data-coverage-and-limitations (WebFetch 200, checked specifically for privacy/de-identification language — none found on this sub-anchor)
- **robots.txt finding:** `open.fda.gov/robots.txt` returns HTTP 403 AccessDenied (S3/CloudFront infrastructure error, not an authored Disallow rule — every neighboring path returns 200). `api.fda.gov/robots.txt` returns 404 (file does not exist). No active Disallow rule blocks any needed path.
- **Terms finding:** No sentence in the Terms of Service prohibits automated collection, scraping, bots, or crawlers. Only standard rate-limit/anti-circumvention language ("Your use of openFDA may be subject to certain limitations on access, calls, or use..."; "If FDA reasonably believes that you have attempted to exceed or circumvent these limits, your ability to use openFDA may be temporarily or permanently restricted") — unsurprising given that openFDA is itself an API/bulk-download service by design.

---

## Disqualified sources

Per README, rejected options are retained here to prevent rediscovery.

### The National Archives (UK) — Discovery catalogue / OGL v3.0

- **URL considered:** https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/
- **Disqualifiers:**
  1. Discovery API Terms and Conditions (fetched, quoted verbatim): "Please do not cache or store any content returned by the API" — directly forecloses any change-detection, snapshot-history, or persistent-dataset design. This is the same structural defect that disqualified the Google Places API source in Round 1.
  2. The "Policy on use of website and catalogue data" page (fetched) redirects bulk/entire-catalogue collection to a direct-contact request process rather than endorsing crawling for that purpose: "If you are crawling our site to obtain a copy of our entire catalogue, or a large series, please contact us."
  3. robots.txt on both `nationalarchives.gov.uk` (fetched) and `discovery.nationalarchives.gov.uk` (fetched via curl) disallow the specific catalogue/search/discovery/results paths (`/catalogue/`, `/discovery/`, `/search/` on the main domain; `/results`, `/SearchUI`, `/browse/` on the Discovery subdomain) needed for search-driven enumeration, even though individual record pages are largely unblocked.
  4. OGL v3 (fetched) explicitly excludes personal data, and the underlying Discovery catalogue is confirmed (via the National Archives' own published guidance) to contain records about identifiable living individuals, some closed for up to 100 years under DPA 2018/UK GDPR — a real risk surface.
  5. Rate limits (3,000 requests/5 min site-wide; 3,000 calls/day at ≤1 req/sec for the API, both fetched) are real but not disqualifying by themselves — flagged as a design constraint only.

### resources.data.gov — "Open Licenses" guidance page

- **URL considered:** https://resources.data.gov/open-licenses/
- **Disqualifiers:**
  1. Primary/fatal: the proposed URL is a policy-guidance/documentation page, not a data source — it contains no records any collection or monitoring concept could be built on.
  2. The page is not a licence grant to a dataset; it is an explanatory definition of what qualifies as an "open licence" under the OPEN Government Data Act, addressed to federal agencies publishing their own datasets elsewhere.
  3. The site self-describes as "the central repository for Federal Enterprise Data resources including tools, case studies, playbooks, and guidance" — confirming it is documentation infrastructure, not a dataset catalog.
  4. No underlying dataset means `retainsHistory`, `exposesDocuments`, `apiOrBulkAvailable`, and rate-limit questions are all effectively moot for this URL as proposed.

---

## Round 1 disqualifications carried forward

Recorded here so no future iteration rediscovers them.

### SAM.gov (GSA — federal contract opportunities)

- Terms of Use state verbatim: **"Automated data gathering, web scraping tools are prohibited"** and, if detected, will result in the associated account(s) being denied access to SAM.gov via Login.gov.
- The API carve-out is narrower than it first appears: "You are allowed to use the Contract Opportunities and Entity Management APIs for internal, U.S. Government business purposes" — a public portfolio artifact that republishes collected data satisfies neither "internal" nor "U.S. Government business purpose."
- Amendment/revision-history data requires a federal system account with Contracting Officer/Specialist/Administrator role, IP allowlisting, and (for secure attachment download) Create/Edit/Delete Draft Attachment write permissions — access no portfolio project can legitimately hold.
- The public Get Opportunities API returns only the **latest version** of a notice; amendments overwrite in place or receive a new noticeId inconsistently, so amendment recall has **no denominator** and is structurally unfalsifiable (confirmed independently in Round 2's own provability refutation of the UK cross-source-resolution candidate, which found the identical failure mode reproduced on a different source pair).
- Non-federal, no-role API quota is 10 requests/day — cannot sustain the polling any monitoring design requires.

### Google Places API

- Terms bar caching/storing name, address, phone, hours, and status beyond `place_id` and lat/lng — incompatible with any change-detection design built on a cached snapshot diff.

### Google Business Profile API

- Confirmed unusable for arbitrary third-party businesses (only usable for locations the API caller manages/owns).

### webscraper.io and scrapingcourse.com

- robots.txt `Disallow` verified by direct fetch.

### Synthetic sandboxes (books.toscrape.com, sandbox.oxylabs.io)

- Lawful to scrape, but the data is explicitly random/meaningless (vendor disclaimers state "no real meaning"), so no commercially credible dataset can result. Retained in Round 2's own portfolio register as the acknowledged weakest link of the `product-and-price-intelligence` runner-up-of-the-runner-up candidate.

---

## Refusals

What this project deliberately will not collect or automate, independent of which concept is ultimately approved:

- **No bypass of authentication, CAPTCHAs, or access controls**, on any source, regardless of how the underlying data might otherwise be characterized as "public."
- **No use of the SAM.gov Opportunity Management API** or any federal-role-gated endpoint — the project holds no legitimate Contracting Officer/Specialist/Administrator role, and obtaining one solely to raise an API quota would itself be access-control circumvention in substance.
- **No caching or storage of Google Places API display fields** (name, address, phone, hours, status) beyond `place_id` and lat/lng, per that API's terms.
- **No scraping of canadabuys.canada.ca's human-facing tender-browsing HTML pages** (`/en/tender-opportunities/*`, `/fr/occasions-de-marche/*`) — robots.txt-disallowed; the bulk CSV path is the sanctioned substitute.
- **No republication of Netrows API data** — its terms forbid redistribution of raw data (Round 1 finding, carried forward for the business-location-monitoring fallback candidate).
- **No treatment of any grant-recipient, contractor, or notice-contact name field as a general-purpose people-search or enrichment dataset**, even on sources (OGL-Canada, OGL-Toronto, OGL-UK) whose licences affirmatively permit reuse of the surrounding institutional data — personal data is structurally excluded from every OGL-family licence reviewed, and named individuals appearing in procurement/grant records (contracting officers, sole-trader suppliers, grant recipients) are recorded here as a bounded, disclosed risk to be scoped around in any data contract, not a feature to build on.
- **No claim that any of the nine cleared sources above constitutes a cleared *concept*.** Source clearance under this ledger establishes only that the source's reuse terms were fetched and verified before a concept was proposed on it — it does not establish that a resulting concept passes the relevance/uniqueness gate or survives adversarial review. As recorded in the Status flag at the top of this document, the Round 2 leader candidate built on sources 4 and 5 above **failed the gate and was refuted on all three adversarial lenses** (novelty: the matching problem is the already-registered cross-source-identity problem with the industry label changed, and the disjoint-namespace premise is a closing transitional artifact of the Procurement Act 2023 migration, not an intrinsic difficulty; compliance: the operative Terms and Conditions page was never fetched during the original clearance pass and its "avoiding system restrictions" clause collides with the undocumented rate ceiling, and OGL's personal-data exclusion does not cover the contact fields the concept's own matching method depends on; provability: buyer-party identifier schemes are empirically disjoint between the two sources with zero measured overlap, so no independent ground truth exists for cross-source identity and the concept's benchmark grades itself against its own inputs). No future iteration should treat "the source is cleared" as equivalent to "the concept is approved."
- **No fabrication of rate limits.** Every source above with an undocumented numeric rate ceiling (data.europa.eu, Find a Tender, Contracts Finder, open.canada.ca, open.toronto.ca, data.cityofnewyork.us's exact throttle) is recorded literally as TBD in this ledger rather than estimated or assumed permissive.
