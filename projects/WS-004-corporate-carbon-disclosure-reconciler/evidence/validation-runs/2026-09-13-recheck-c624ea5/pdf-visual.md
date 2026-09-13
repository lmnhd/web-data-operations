# WS-004 independent repair recheck - PDF inspection

- Artifact: `output/pdf/Carbon-Disclosure-Reconciliation-Desk.pdf`
- Mechanical inspection: `pdfinfo`
- Rendering: `pdftoppm -r 150 -png`
- Render directory: `pdf-pages/`

Mechanical inspection reports exactly three unencrypted US Letter pages, no forms, no embedded JavaScript, and a 104,373-byte PDF. Independent text/annotation inspection found two page-3 URI annotations: `http://127.0.0.1:5000` and `https://github.com/lmnhd/web-data-operations`.

Every rendered page was opened at original detail:

- Page 1 is readable and unclipped, with the buyer problem, bounded claim, 2/1/3 metrics, actual repaired default workbench screenshot, and evidence boundary.
- Page 2 is readable and unclipped, with the observed 2026-to-2025 factor-vintage correction, actual fail-closed code excerpt, 2025 factor year, three rows, 27/27 test count, and ambiguity limitation.
- Page 3 is readable and unclipped, with baseline 1,000 MWh / 177.000 tCO2e, changed 0.177 tCO2e, 27/27 tests, operating steps, both links, run IDs, and explicit limitations.

No clipping, overlap, illegible text, substituted screenshot, or disagreement with the frozen demo was observed. The rendered PNGs are retained in this recheck directory.
