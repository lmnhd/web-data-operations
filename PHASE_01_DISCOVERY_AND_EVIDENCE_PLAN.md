# Phase 1 - Discovery and Evidence Plan

## Phase objective

Select and specify one portfolio project that demonstrates an intermediate-level web-data operation from collection through verified delivery. Phase 1 does not begin with crawler code. It establishes the use case, permissions, data contract, failure model, proof metrics, and portfolio story that the implementation must satisfy.

## Working hypothesis

The strongest project will be a **multi-source monitoring and enrichment pipeline** rather than a single-site scraper. It should combine several realistic data problems without becoming a contrived feature showcase:

- paginated and detail-page collection;
- at least one JavaScript-rendered source or browser-assisted step;
- structured HTML plus a document source such as PDF;
- incremental updates and change detection;
- normalization and entity resolution across sources;
- source citations and collection timestamps at the field or record level;
- validation, deduplication, review queues, and reason-coded exclusions;
- rate limits, retries, checkpoints, resumability, and observable failures;
- useful CSV/Excel and JSON output, with a small operator-facing report or dashboard.

This is a hypothesis to validate against current Upwork demand and feasible public sources. It is not yet an approved build specification.

## Phase 1 workstreams

### 1. Demand evidence

Review a representative sample of current intermediate Upwork postings and classify the actual deliverables clients request.

Capture:

- source types and access constraints;
- requested tools and languages;
- one-time extraction versus recurring monitoring;
- expected volume and update frequency;
- output destinations;
- anti-bot or authentication expectations;
- data-cleaning, enrichment, and matching requirements;
- proof or prior-work evidence requested by clients;
- common failure points and signs of risky or prohibited work.

Deliverable: `research/UPWORK_DEMAND_MATRIX.md` with links, dates, categories, and a short synthesis. Do not copy client data or reproduce private job material beyond what is necessary for analysis.

### 2. Candidate use cases

Develop three candidate projects and score each against:

- similarity to paid Upwork work;
- availability of lawful, public, stable-enough sources;
- opportunity to demonstrate difficult extraction and data-quality work;
- usefulness of the resulting dataset;
- ability to show measurable results without fabricated claims;
- time to a convincing first release;
- potential to become a reusable service rather than a disposable demo.

Initial candidates to investigate:

1. **Public opportunity intelligence:** collect and reconcile government or institutional solicitations, amendments, deadlines, contacts, and attached documents.
2. **Business-location monitoring:** track multi-location business details, services, hours, reviews/signals, and material changes across permitted public sources.
3. **Product and price intelligence:** monitor a carefully bounded group of public product pages for price, availability, specifications, and changes.

Deliverable: `research/CANDIDATE_SCORECARD.md` and one recommended concept. Selection must be evidence-based; prior career history should not decide the winner.

### 3. Collection and compliance boundaries

For every proposed source, record:

- public URL and owner;
- data fields needed;
- whether an official API, feed, export, or downloadable document exists;
- robots.txt and relevant published access terms;
- authentication, paywall, personal-data, or account restrictions;
- reasonable request frequency and caching policy;
- attribution or retention requirements;
- allowed fallback if collection becomes unavailable.

Prefer an official API or download when it provides the required data. Browser automation should demonstrate a legitimate technical need, not bypass access controls. The project must not evade CAPTCHAs, defeat authentication, collect restricted personal data, or disguise prohibited traffic.

Deliverable: `design/SOURCE_AND_COMPLIANCE_LEDGER.md`.

### 4. Data contract and truth model

Define the record schema before implementation, including:

- canonical identifier and entity-matching keys;
- raw, normalized, and derived fields;
- required versus optional fields;
- source URL, retrieval time, content fingerprint, and extraction method;
- field confidence and conflict-handling rules;
- duplicate and version semantics;
- accepted, rejected, and manual-review states;
- export formats and deterministic sorting.

Keep raw evidence separate from normalized and inferred values. Never silently replace a source fact with an AI-generated guess.

Deliverable: `design/DATA_CONTRACT.md` with sanitized example records.

### 5. Reliability and proof specification

Define how the finished system will be tested and what its portfolio claims may say.

Baseline metrics to design for, then measure from real runs:

- pages/items attempted, collected, rejected, and retried;
- successful request and parse rates;
- required-field completeness;
- duplicate rate before and after resolution;
- number and type of source conflicts;
- incremental-run change counts;
- checkpoint/resume behavior after an injected failure;
- validation and regression-test results;
- elapsed time and request volume under the documented rate policy.

The benchmark dataset must contain manually reviewed ground-truth samples so that extraction and matching quality can be assessed honestly. Metrics remain labeled `TBD` until a reproducible benchmark run exists.

Deliverable: `design/PROOF_AND_BENCHMARK_SPEC.md`.

### 6. Architecture and operator experience

Specify a modular pipeline with clear responsibility boundaries:

```text
Source registry
  -> compliant fetchers
  -> immutable raw capture
  -> parsers
  -> normalized records
  -> validation and entity resolution
  -> accepted / rejected / review-needed outputs
  -> versioned storage and exports
  -> run report and operator controls
```

The design must show configuration-driven source and rule changes, structured logging, safe concurrency, retry policy, checkpoints, run IDs, and reproducible exports. AI may assist classification or document extraction only where its output is labeled, bounded, and independently validated.

Deliverable: `design/ARCHITECTURE_BRIEF.md` plus a diagram source that can be reused in the PDF.

### 7. Portfolio storyboard

Create the case-study story before coding so every implementation choice produces visible evidence.

Draft the first three pages as:

- **Page 1 - The result:** a screenshot/mockup of the operator report and a sample verified output, with the business question answered in one sentence.
- **Page 2 - How it works:** a readable architecture diagram and the important collection/data-quality controls.
- **Page 3 - Proof:** real benchmark metrics, failure/recovery evidence, tests, and links to the demonstration or repository.

Later pages may cover source-specific techniques, schema design, ethics/compliance, and selected code. Avoid generic biography, long introductions, and unmeasured superlatives.

Deliverable: `portfolio/THREE_PAGE_STORYBOARD.md`.

## Phase 1 exit criteria

Phase 1 is complete only when:

- current demand evidence supports the chosen project;
- one use case and its intended buyer are clearly named;
- each target source has an acceptable access path and documented boundary;
- the schema, provenance model, and review states are defined;
- benchmark samples and truthful success metrics are specified;
- the architecture can recover from expected failures;
- the first-three-page story can be populated by planned implementation evidence;
- the implementation scope fits a focused portfolio release.

## Approval gate before implementation

Before Phase 2, review and approve:

1. selected use case and target client;
2. target sources and compliance ledger;
3. data contract and expected exports;
4. proof metrics and benchmark method;
5. Phase 2 minimum viable build scope.

Phase 2 should not expand into authentication bypass, large-scale infrastructure, paid data acquisition, or collection of sensitive personal information without a new explicit decision.
