# WS-002 concept recommendation

## Decision boundary

- **Stage:** AWAITING_APPROVAL
- **Authorized work so far:** planning and source/demand verification only
- **Build authorization:** none
- **Publication authorization:** none; WS-001 approval does not transfer
- **Delegation used:** 0 of 4 available turns

This recommendation follows the bounded Shipping Pipeline and the [reviewer evidence standard](../../docs/shipping-pipeline/REVIEWER_EVIDENCE_STANDARD.md). The selected concept must end with its own runnable demonstration, project-specific visual PDF, reproducible evidence, Manifest and artifact-linked release checklist. Those requirements are planned now, but do not authorize implementation or publication.

## Evidence quality

No client posting was supplied with this iteration request. Current demand evidence therefore consists of public Upwork postings and Upwork category pages, not a client interview or a logged-in personalized job feed.

The strongest current signals are:

- [E-commerce Product Automation System](https://www.upwork.com/freelance-jobs/apply/Senior-Full-Stack-Developer-Needed-commerce-Product-Automation-System_~022089095685989660503/) - posted August 16, 2026; asks for identifier/fuzzy product matching, confidence, manual review and explicit approval before write-back.
- [Product Data Cleanup and Standardization](https://www.upwork.com/freelance-jobs/apply/Product-Data-Cleanup-Standardization-CRM-Entry-200-SKUs_~022089101146145792981/) - posted August 16, 2026; asks for SKU normalization, duplicate/missing-data checks and an issues queue.
- [Senior Python Backend Engineer - PDF/Data Extraction](https://www.upwork.com/freelance-jobs/apply/Senior-Python-Backend-Engineer-PDF-Data-Extraction-Supabase_~022091051177676672807/) - current in late August 2026; asks for deterministic document parsers, structured extraction, normalization, provenance and review states.
- [Power BI Dashboard from CSV Data](https://www.upwork.com/freelance-jobs/apply/Power-Dashboard-Specialist-Build-Clean-Interactive-Reports-from-CSV-Data_~022094968596444905810/) - posted September 2, 2026; asks for data modeling, interactive filtering and a reviewer-ready handoff.
- Upwork's [web-scraper hiring guide](https://www.upwork.com/hire/web-scrapers/) describes extraction, cleaning, validation, CSV/JSON delivery and maintainable pipelines as common buyer needs.

These signals support the capabilities below. They do not prove demand for the exact public datasets or public-demo framing.

## Three bounded concepts

| Candidate | Buyer and operational decision | Permitted source path | Net-new proof versus WS-001 | Main weakness |
|---|---|---|---|---|
| **A. Recall-to-Catalog Impact Review** | E-commerce or distributor catalog operations staff deciding which SKUs need human recall verification | openFDA drug enforcement API/bulk data under CC0, plus a synthetic retailer catalog fixture | Explainable product/entity matching, ambiguity routing and catalog-side impact review rather than notice change detection | openFDA forbids medical-care reliance, public-alert use and recall-lifecycle claims; concept-specific demand is indirect |
| **B. Tender Document Evidence Reconciler** | Bid operations or procurement-data staff deciding whether structured tender fields agree with source documents | TED anonymous Search API/XML bulk and freely reusable procurement notices; exact document subset and current terms must be revalidated | Deterministic PDF extraction, page-level provenance and document-vs-record conflict detection | Repeats the procurement vertical immediately after WS-001 and document variability may inflate the proof |
| **C. 311 Service Operations Explorer** | Municipal service contractor or operations analyst deciding where workload and aging need review | Toronto Open Data 311 bulk/API data under the Open Government Licence - Toronto | Geospatial/time-series aggregation, data-quality repair and an interactive operations dashboard | Similar public 311 dashboards already exist; buyer evidence is generic dashboard demand rather than a verified municipal request |

## Recommendation: A. Recall-to-Catalog Impact Review

### Target buyer and problem

Small e-commerce, wholesale or distribution teams can receive a regulator recall record whose product description, firm, lot/code text and identifiers do not line up cleanly with their internal catalog. Staff need a short explainable queue showing likely catalog impacts, definite non-matches and ambiguous records that require verification.

### Operational decision

Decide which catalog rows require a human to open the official source record and verify impact. The tool does not declare a product safe, issue a public alert, infer current recall status or make a medical decision.

### Central testable claim

A provenance-preserving matcher can compare a bounded synthetic catalog with selected openFDA enforcement records and reproduce a hand-labeled set of match, no-match and review-needed decisions using explicit identifier, manufacturer, product-text and lot/code evidence.

### Source and compliance boundary

The [openFDA drug enforcement API](https://open.fda.gov/apis/drug/enforcement/) exposes publicly releasable recall records from 2004 onward and says it is updated weekly. The [openFDA licence page](https://open.fda.gov/license/) states that the data is generally public-domain/CC0 and available for commercial reuse. The proof must also preserve the source's warnings:

- do not use the data for medical-care decisions;
- do not use it to issue public alerts or claim to track a recall lifecycle;
- do not treat the published `status` as a current lifecycle state;
- exclude GMDN content from any commercial categorization or AI-training use unless separately licensed;
- use bounded recorded fixtures by default and a conservative documented API request only if needed.

### Difference from released WS-001

WS-001 compares consecutive procurement records over declared fields and applies qualification rules. WS-002 would instead match records across two schemas where identifiers and descriptive fields may be incomplete, score evidence without hiding uncertainty, and expose a catalog-centric manual-review workflow. It changes the buyer, industry, source, matching problem, proof method and operator decision. It reuses provenance/export components, not WS-001 results or claims.

### Smallest vertical proof

1. Ingest a synthetic catalog of roughly 12-20 products and a bounded recorded set of official openFDA enforcement records.
2. Normalize identifiers, manufacturer names, product descriptions and lot/code tokens without inventing missing values.
3. Apply deterministic match evidence in a declared order: exact identifiers, exact normalized manufacturer plus strong product evidence, then bounded fuzzy evidence.
4. Emit `match`, `no_match` and `review_needed` rows with field-level reasons, source URL, retrieval timestamp and content fingerprint.
5. Compare output with a hand-labeled fixture that includes definite matches, definite non-matches and ambiguous cases.
6. Export the review queue and run report.

The claim fails if the matcher cannot reproduce the labeled fixture without unsafe thresholds, hidden manual repair or self-referential labels.

### Reviewer-operated scenario and edge case

The reviewer changes one catalog identifier or manufacturer spelling and reruns the matcher. The result must visibly change with an explanation. An ambiguous product description with no reliable identifier must route to `review_needed`, never to a confident match.

### Final evidence plan

- **Runnable demo:** edit the small catalog fixture, run real matching code, inspect evidence, open source provenance and export the queue.
- **PDF page 1:** buyer problem, working review queue and screenshot.
- **PDF page 2:** the genuine obstacle - incomplete/inconsistent product identity - plus the deterministic evidence ladder and ambiguity boundary.
- **PDF page 3:** labeled-fixture results, tests, limitations and a short try-it path.
- **Traceability:** sanitized inputs, labeled oracle, actual outputs, test/run records, Manifest and `evidence/RELEASE_CHECKLIST.md` tied to one reviewed version.

## Consolidated review

```json
{
  "decision": "proceed",
  "fatal": [],
  "repairable": [
    "Verify the exact enforcement-record fields and select records with a defensible independent labeling method before approving the proof fixture.",
    "Define thresholds from the labeled fixture and keep the ambiguous band explicit rather than tuning until every example passes.",
    "Recheck openFDA terms, API guidance and any selected-field exemptions immediately before acquisition."
  ],
  "limitations": [
    "No client posting was supplied; current Upwork evidence supports product matching and data quality generally, not this exact recall-review product.",
    "The bounded proof will not establish production recall coverage, real-time operation, medical correctness, current recall status or business impact.",
    "A synthetic catalog proves the workflow and evaluation method, not integration with a retailer's private catalog."
  ],
  "required_vertical_proof": [
    "Independent labeled match/no-match/review fixture",
    "Explainable changed-input result",
    "Ambiguous record safely routed to review",
    "Provenance and deterministic export",
    "No prohibited alert, lifecycle or medical claim"
  ],
  "claims_to_avoid": [
    "complete recall coverage",
    "current recall status",
    "medical or safety determination",
    "public alerting",
    "production accuracy, scale or savings"
  ]
}
```

## Approval request

Approve **Recall-to-Catalog Impact Review** only for the bounded vertical proof above. Approval would authorize fixture/source verification and proof implementation, but not expansion, hosting, publication, paid services or live operational use.
