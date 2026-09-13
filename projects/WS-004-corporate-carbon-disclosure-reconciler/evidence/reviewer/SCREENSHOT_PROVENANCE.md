# Reviewer screenshot provenance

Both screenshots were captured on 2026-09-13 from the local Flask workbench at `http://127.0.0.1:5000` using installed Google Chrome in headless mode at a 1440 x 900 viewport.

## `working-demo.png`

- Actual page state after the UI automatically executed the default six-case Python engine run.
- Browser assertion: title `Six evidence cases evaluated`.
- Browser-observed summary: 2 RECONCILED, 1 MISMATCH, 3 REVIEW REQUIRED.
- Used as the page-1 screenshot in the project PDF.

## `changed-input-demo.png`

- Actual page state after clicking `Try the 1/1,000 unit change`.
- Browser assertion: the result contained `0.177 tCO2e` and `MISMATCH`.
- The selected input is the labeled controlled scenario, with numeric value 1,000 and unit changed from MWh to kWh.

These are screenshots of executed local logic, not mockups, official company dashboards, or public-host verification.
