# Independent local-demo operation

The validator started the documented Flask app with `python app.py` from the project directory and opened `http://127.0.0.1:5000` in the in-app browser.

Observed default state:

- run `ws004-1984fbedb2ae05ca`;
- 6 cases;
- 2 RECONCILED, 1 MISMATCH, 3 REVIEW_REQUIRED;
- recorded filing facts and reviewer-supplied controlled scenarios visibly distinguished;
- reason codes, source locators, shortened source hashes, and the fail-closed Python excerpt visible.

The validator clicked `Try the 1/1,000 unit change`. The UI selected controlled Case 02 and `kWh - reviewer change`, then showed run `ws004-52cd149712424e77`, activity `1,000 kWh`, recomputed emissions `0.177 tCO2e`, decision MISMATCH, and reason `DISCLOSED RESULT OUTSIDE TOLERANCE`. Restoring the six-case benchmark returned the original 2/1/3 state. Visual inspection found the running workbench readable and operable.
