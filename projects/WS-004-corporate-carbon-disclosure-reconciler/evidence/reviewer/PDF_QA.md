# Builder PDF QA

**Date:** 2026-09-13

**Artifact:** `output/pdf/Carbon-Disclosure-Reconciliation-Desk.pdf`

**Role:** Builder inspection only - independent visual validation remains required

## Mechanical checks

- PDF metadata reports exactly 3 Letter pages, no encryption, form fields, or embedded JavaScript.
- Text extraction contains the 2/1/3 decisions, `REVIEW_REQUIRED`, the 2025 Version 1 / Final correction, 23/23 tests, 0.177 tCO2e changed result, and the audit/compliance limitation.
- Link annotations resolve to the documented local workbench URL and repository URL.
- Final pages rendered at 150 DPI with Poppler.

## Visual inspection

- **Page 1 - buyer problem and useful result:** title, two plain-English paragraphs, four metrics, actual workbench screenshot, boundary caption, and footer are legible and uncropped. The screenshot displays the real default 2/1/3 result.
- **Page 2 - creative problem solving:** the 2026-to-2025 factor-vintage correction reads in sequence; all three decision boxes, actual code excerpt, four metrics, limitation text, and footer are aligned with no overlap or clipping.
- **Page 3 - reproducible proof:** baseline and changed values, 1/1,000 explanation, local run steps, both links, limitation box, evidence run IDs, and footer are legible with balanced spacing and no clipping.

No builder-observed visual defects remain. This does not replace the fresh non-builder validator's required independent inspection of every rendered page.
