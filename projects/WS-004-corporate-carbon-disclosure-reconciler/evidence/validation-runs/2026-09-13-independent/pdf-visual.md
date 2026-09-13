# Independent PDF inspection

`output/pdf/Carbon-Disclosure-Reconciliation-Desk.pdf` was rendered with Poppler at 150 DPI. It is an unencrypted, three-page Letter PDF with no forms or JavaScript. Every rendered page is preserved under `pdf-pages/` and was visually inspected.

- Page 1 is readable and unclipped, states the buyer problem and bounded result, and contains the actual default workbench screenshot with 2/1/3 counts.
- Page 2 is readable and unclipped, explains the observed 2026-to-2025 factor-vintage correction, includes implemented fail-closed code, and reports 2025, three pinned rows, and 23/23 tests.
- Page 3 is readable and unclipped, shows 1,000 MWh / 177.000 tCO2e versus 1,000 kWh / 0.177 tCO2e, gives local try-it steps, and states material limitations.

No overlap, crop, unreadable glyph, or placeholder was observed. Page-edge pixel inspection confirmed header ink and footers remain inside every 1275 x 1650 render. Link annotations target `http://127.0.0.1:5000` and `https://github.com/lmnhd/web-data-operations`.
