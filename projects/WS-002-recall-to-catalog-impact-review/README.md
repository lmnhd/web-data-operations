# Product Recall Match Desk

Bounded WS-002 reviewer workbench that compares a synthetic product catalog with a recorded, sanitized openFDA enforcement fixture. It emits explainable `match`, `no_match` and `review_needed` queues and preserves source provenance.

This is not medical advice, a public alert, a current recall-status determination or a production recall-monitoring service.

**Public demo:** [Product Recall Match Desk](https://product-recall-match-desk.vercel.app) - no login required.

## Launch the reviewer workbench

From this project directory:

```powershell
python -B src/demo_server.py
```

Open `http://127.0.0.1:8766`. Run the ambiguous 100 mcg example, then choose **Add decisive evidence** and run again. The same Python matcher used by the command-line proof changes `CAT-005` from `review_needed` to a single explainable match. JSON and CSV exports are generated from the executed result.

## Run the proof

From this project directory:

```powershell
python src/run_proof.py `
  --catalog tests/fixtures/catalog.json `
  --recalls tests/fixtures/recalls.json `
  --expected tests/fixtures/expected-labels.json `
  --output-dir evidence/latest-run
```

Run the changed-input scenario:

```powershell
python src/run_proof.py `
  --catalog tests/fixtures/catalog-changed.json `
  --recalls tests/fixtures/recalls.json `
  --expected tests/fixtures/expected-labels-changed.json `
  --output-dir evidence/changed-input
```

Run tests:

```powershell
python -B -m unittest discover -s tests -v
```

Run the independently declared 20-row expansion benchmark:

```powershell
python -B src/run_proof.py `
  --catalog tests/fixtures/benchmark-catalog.json `
  --recalls tests/fixtures/recalls.json `
  --expected tests/fixtures/benchmark-labels.json `
  --output-dir evidence/benchmark
```

## Reviewer scenario

Compare `CAT-005` in the two catalog fixtures. In the baseline it says `100 mcg`, while the same harmonized UPC appears on recorded 75 mcg and 150 mcg recalls; the row safely routes to review. In the changed fixture, the catalog supplies `75 mcg`, an exact NDC family and lot code, so the result changes to a single explainable match.

## Outputs

- `results.json`: complete decision and top pair evidence
- `matches.csv`: confident matches
- `review-needed.csv`: ambiguous records requiring human verification
- `no-matches.csv`: rows with no viable source candidate
- `run-report.json`: observed counts and independent-label evaluation

See [SOURCE_CONTRACT.md](SOURCE_CONTRACT.md) for acquisition, field allowlist and usage boundaries.
