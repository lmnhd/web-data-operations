# WS-004 independent repair recheck - local reviewer demo

- Validator: `/root/ws004_independent_validator`
- Candidate: `c624ea5da67e8838ed96064560e83298767cb943`
- Local command: `python app.py` from the WS-004 project directory
- Browser: installed Google Chrome, local URL `http://127.0.0.1:5000`

The live page loaded its actual static assets and invoked `POST /api/run` successfully. The default page state showed run `ws004-6fd5836905285efd`, six cases, and exactly 2 RECONCILED, 1 MISMATCH, and 3 REVIEW REQUIRED. Each case displayed its expected decision, reason, values, locator, and source-hash trace.

I operated `Try the 1/1,000 unit change`. The live page changed to run `ws004-944aa2c7c09f7480` and displayed controlled Case 02 as 1,000 kWh, 177 tCO2e disclosed, 0.177 tCO2e recomputed, and MISMATCH. The default Case 02 state was 1,000 MWh, 1,000,000 normalized kWh, 177.000 tCO2e recomputed, and RECONCILED.

The browser state therefore agreed with the executed CLI evidence: only the input and run hashes changed; source, factor-subset, factor-workbook, and engine hashes remained stable. Two optional validator screenshot capture attempts timed out in Chrome's screenshot command after the page state had already been read and operated; this did not affect the live-state inspection. The committed 1440 x 900 default and changed-input screenshots were separately opened and visually matched the live states. The local server and browser tab were closed after inspection.
