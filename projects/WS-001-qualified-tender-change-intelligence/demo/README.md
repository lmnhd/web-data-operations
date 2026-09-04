# Proof Lab: run it, do not just read about it

From the repository root, with Python 3.10 or newer:

```powershell
python projects/WS-001-qualified-tender-change-intelligence/src/demo_server.py
```

Open http://127.0.0.1:8765. No packages, API keys or government network calls are needed for the demo. Stop the server with Ctrl+C. This is a local-only demonstration, not a production hosting configuration.

## A two-minute reviewer walkthrough

1. Choose **Six update labels** and click **Run the comparison**. Inspect all six version pairs: no differences in the six declared fields, so all go to Ignore.
2. Choose **A real cancellation** and run again. Five differences are highlighted. Missing qualification evidence routes this case to Review.
3. Choose **Try your own rule**. This example is synthetic, not a real opportunity. Its value is 400,000 GBP. Run with a maximum of 500,000, then 300,000. The same input changes from Act to Ignore.
4. Open **Inspect the source trail**. Compare fresh run IDs, timestamps and input hashes. The hash is of the original sanitized file in the repository; for the synthetic example that file also contains the other test cases. The displayed input link returns only the selected case.
5. Download JSON and CSV. Exports are the exact stored result of that run, not another calculation. The local server retains the last 64 runs in memory; older downloads expire and all downloads expire on restart.
6. Open **Show the actual Python logic**. The server reads these excerpts from the very module it executes.
7. Click **Run automated checks**. This executes the Python tests and displays their actual output and exit status.

## Why this is executable evidence

The browser sends the selected case and visible rules to `POST /api/run`. The server loads the allowlisted input, invokes `tender_pipeline.run_pipeline`, and returns comparisons, snapshots, reason codes, hashes and a unique run ID. The frontend does not invent decisions or read saved run reports. Editing rules clears the old result until you run again.

The central problem-solving move is small: compare declared field values instead of counting source update tags. The second is to distinguish missing evidence from a proven mismatch. Neither requires an LLM.

## Boundaries

- Two deliberately selected historical public records plus one clearly labeled synthetic scenario.
- Replays test transformation and qualification, not current acquisition availability or source-wide coverage.
- Act means the configured category/value/date checks pass, not legal eligibility to bid.
- No scheduling, public server, credentials, arbitrary URL fetching, upload, CRM or email integration.
- The server binds loopback, checks Host/Origin, limits request bodies and exposes fixed routes. Do not bind it publicly; hosting needs a separate deployment/security decision.
- Test execution uses one fixed subprocess command, not user-provided shell input.
- Browser interaction and automated checks were performed by the implementing agent, not an independent reviewer.

## Recorded evidence

See [the screenshot walkthrough](../evidence/proof-lab/WALKTHROUGH.md) and [browser verification](../evidence/proof-lab/BROWSER_VERIFICATION.md). These are supporting records; running the project yourself is the stronger check.
