# WS-004 Bounded Vertical Proof Brief

## Approval and boundary

- **Concept:** Corporate Carbon Disclosure Reconciliation Desk
- **Approval:** Human approved Candidate A and the four-turn delegated-agent ceiling on 2026-09-12.
- **Current authority:** Source-contract verification, selection of no more than three permitted public SECR account documents, validation-plan freeze, and one six-case local vertical proof.
- **Not authorized:** Expanded UI, public hosting, paid services, publication, production use, environmental-performance scoring, regulatory compliance, or audit assurance.
- **Delegation:** No research/build agent is allocated. One fresh-context non-builder validator and one repair recheck remain reserved before any such allocation.

This brief incorporates the [Reviewer Evidence Standard](../../docs/shipping-pipeline/REVIEWER_EVIDENCE_STANDARD.md) and [Independent Validation Protocol](../../docs/shipping-pipeline/INDEPENDENT_VALIDATION.md). Builder review is not independent validation.

## Buyer and decision

An ESG assurance analyst, sustainability reporting team, or accounting reviewer needs to decide whether a disclosed company-level energy/emissions calculation is reproducible from explicit evidence, conflicts with that evidence, or needs human follow-up.

The proof answers only: **is the disclosed arithmetic reproducible from explicit activity, unit, factor category, and factor year?** It does not decide whether a filing complies with law or whether the underlying disclosure is true.

## Source strategy

Use one official Companies House Free Accounts Data Product daily archive, not the key-authenticated Document API. Select at most three electronically filed iXBRL/XBRL account documents that contain usable company-level SECR material. Retain public evidence only as minimized numerical excerpts, source identifiers, retrieval metadata, and hashes under the [source contract](../../projects/WS-004-corporate-carbon-disclosure-reconciler/SOURCE_CONTRACT.md).

Use the Department for Energy Security and Net Zero 2026 conversion-factor flat file only after its workbook notices, update date, and SHA-256 are recorded. No factor may be inferred from an absent category or blank value.

## Declared six-case oracle

| Case | Purpose | Expected decision |
|---|---|---|
| 1 | Explicit activity, supported unit, explicit factor category/year, arithmetic within tolerance | RECONCILED |
| 2 | Second structurally different valid disclosure within tolerance | RECONCILED |
| 3 | Explicit inputs whose disclosed result conflicts with recomputation | MISMATCH |
| 4 | Disclosed emissions total without activity breakdown or factor reference | REVIEW_REQUIRED: INSUFFICIENT_CALCULATION_EVIDENCE |
| 5 | Image-only or otherwise unsupported source representation | REVIEW_REQUIRED: UNSUPPORTED_SOURCE_FORMAT |
| 6 | Unknown/unsupported factor year or category | REVIEW_REQUIRED: UNKNOWN_FACTOR_REFERENCE |

Planned benchmark total: 2 RECONCILED, 1 MISMATCH, 3 REVIEW_REQUIRED. This is a declared oracle, not an observed result.

## Reviewer-operated scenario

Change one activity unit from `MWh` to `kWh` without changing its numeric value. The normalized activity and recomputed emissions must change by exactly 1,000x; the input hash must change; the unchanged engine, factor, and source hashes must remain stable; and the decision must become MISMATCH unless the disclosed output changes consistently.

## Smallest proof implementation

1. Parse only the selected minimized fixture fields: source ID/hash, reporting period, activity value/unit, disclosed emissions value/unit, factor category/year, and page or iXBRL concept provenance.
2. Normalize `kWh`, `MWh`, `kgCO2e`, and `tCO2e` using explicit decimal arithmetic.
3. Resolve a factor only by exact versioned category and unit keys from the pinned official factor subset.
4. Recompute only when every required input is explicit; otherwise fail closed with a reason code.
5. Emit deterministic JSON and CSV with the run ID, source/factor/input hashes, normalized values, variance, tolerance, decision, and provenance.
6. Supply a simple local reviewer runner. No public hosting is part of the proof approval.

## Pre-implementation gates

Before code or fixture implementation:

- record the final three source documents and confirm the permitted minimized evidence treatment;
- inspect the factor workbook notices and pin the exact factor file;
- copy the pre-build plan to project `evidence/VALIDATION_PLAN.json` with exact artifact paths and builder identity;
- commit the source contract, selected-source record, factor record, oracle, and frozen plan.

If three usable source documents cannot be found in one bounded archive, stop and report the evidence gap rather than expanding acquisition automatically.

## Future expansion obligations

Expansion approval would be required for a reviewer web UI, project-specific three-page visual PDF, additional documents, public hosting, Manifest, independent validator dispatch, or publication. Any final project must have its own runnable demo, plain-English visual PDF, problem-solving evidence, Manifest, release checklist, independent PASS, and executable hash gate.
