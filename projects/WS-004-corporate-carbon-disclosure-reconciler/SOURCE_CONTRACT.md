# WS-004 Source Contract

## Status

`PROVISIONAL_FOR_BOUNDED_SOURCE_SELECTION` - recorded before acquisition. Implementation remains prohibited until three usable documents, the exact factor file, and the frozen validation plan are recorded and committed.

## Source A: Companies House Free Accounts Data Product

- **Owner:** Companies House, UK Department for Business and Trade.
- **Official landing page:** https://download.companieshouse.gov.uk/en_accountsdata.html
- **Official guidance:** https://www.gov.uk/guidance/companies-house-data-products
- **Access path:** One direct daily ZIP from the official Accounts Data Product. No HTML scraping, login, API key, rate probing, pagination, or Document API call.
- **Published content:** Electronically filed company accounts as iXBRL (`.html`), XBRL (`.xml`), or zipped iXBRL instance documents. Companies House describes the files as free and intended to let users manipulate accounts data for their own needs.
- **Coverage limitation:** The product excludes non-electronic accounts and revised/amending paper accounts. It must not be presented as complete or current for every company.
- **Use statement:** Companies House says it imposes no rules or requirements on use of public-register information while making users responsible for applicable data protection, copyright, and other law and for checking legal requirements before publication.
- **Permitted proof treatment:** Acquire one bounded official daily archive for source selection. Select no more than three usable documents. Retain publicly only company number, filing/source identifier, reporting period, selected company-level energy/emissions facts, necessary iXBRL concept or page provenance, retrieval time, source URL, and SHA-256. Do not commit the bulk archive or full source documents.
- **Excluded fields/content:** Personal names, signatures, author metadata, officer/contact details, addresses, unrelated narrative, financial-account details unrelated to the declared proof, and full filing bodies.
- **Publication treatment:** A future public demo may display derived numerical facts, short labels necessary to identify metrics, hashes, and attribution. It may not redistribute full filings or substantial narrative. Any need for broader excerpts or screenshots requires a new review before publication approval.
- **Acquisition ceiling:** One daily archive, preferably no more than 100 MiB compressed. Stop if it does not yield three usable documents; do not automatically download a second archive.
- **Local handling:** Keep the source archive and extracted search corpus under ignored `tmp/ws004_source/`. Commit only minimized, reviewed fixtures after removing excluded content.

## Source B: UK Government GHG Conversion Factors 2026

- **Owner:** Department for Energy Security and Net Zero.
- **Official page:** https://www.gov.uk/government/publications/greenhouse-gas-reporting-conversion-factors-2026
- **Access path:** Official 2026 flat-file workbook for automatic processing.
- **Version boundary:** The flat file was corrected and republished on 2026-07-31. Record the exact download URL, retrieval time, workbook notices, and SHA-256. Never label it merely “latest.”
- **Licence boundary:** The GOV.UK page is OGL v3.0 except where otherwise stated. Inspect and record the workbook's own notices before retaining any factor subset.
- **Permitted proof treatment:** Commit only the minimal factor rows needed by the six-case oracle, including year, category, activity unit, emissions unit, factor value, source-sheet/row provenance, download URL, update date, and workbook hash.
- **Calculation boundary:** Apply a factor only when activity value, unit, factor category, and factor year are explicit and compatible. Blank, zero-corrected, unknown, or ambiguous rows route to review.

## Privacy and safety

- Process public company-level reporting facts only.
- Do not store credentials or request a Companies House API key.
- Do not infer private activity data, fuel mix, missing factors, or regulatory conclusions.
- Do not identify individuals or expose signatures/contact information.
- Results are evidence-reproducibility classifications, not audit opinions or compliance certifications.

## Stop conditions

Stop before implementation and report the gap if any of these occurs:

1. The official archive exceeds the 100 MiB ceiling or is unavailable.
2. One archive does not contain three text-bearing documents with usable SECR material.
3. Minimized public evidence cannot be separated from excluded personal or copyrighted narrative.
4. The factor workbook's own notices conflict with the planned minimized factor subset.
5. The project-local validation plan is not frozen and committed.
