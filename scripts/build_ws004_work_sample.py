"""Build the three-page WS-004 client-facing case-study PDF."""

from __future__ import annotations

import inspect
import json
import sys
from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projects" / "WS-004-corporate-carbon-disclosure-reconciler"
OUTPUT = ROOT / "output" / "pdf" / "Carbon-Disclosure-Reconciliation-Desk.pdf"
SCREENSHOT = PROJECT / "evidence" / "reviewer" / "working-demo.png"
RUN_PATH = PROJECT / "evidence" / "evaluated_run.json"
CHANGED_PATH = PROJECT / "evidence" / "changed_input_run.json"
sys.path.insert(0, str(PROJECT / "src"))
import reconcile  # noqa: E402


INK = HexColor("#112D35")
FOREST = HexColor("#0B5C4C")
MINT = HexColor("#98EFC8")
MUTED = HexColor("#58716C")
PALE = HexColor("#EDF2EF")
AMBER = HexColor("#A45B10")
RED = HexColor("#A4372C")
BLUE = HexColor("#315D7A")
LOCAL_DEMO = "http://127.0.0.1:5000"
REPO = "https://github.com/lmnhd/web-data-operations"


def paragraph(
    pdf,
    words,
    y,
    size=10,
    color=MUTED,
    x=38,
    width=536,
    leading=None,
):
    style = ParagraphStyle(
        "body",
        fontName="Helvetica",
        fontSize=size,
        leading=leading or size * 1.35,
        textColor=color,
    )
    block = Paragraph(words, style)
    _, height = block.wrap(width, 800)
    block.drawOn(pdf, x, y - height)
    return y - height


def header(pdf, page, title, subtitle):
    pdf.setFillColor(INK)
    pdf.rect(0, 690, 612, 102, fill=1, stroke=0)
    paragraph(pdf, "CARBON DISCLOSURE RECONCILIATION DESK / WORKING DEMO", 768, 8, MINT)
    title_bottom = paragraph(pdf, f"<b>{title}</b>", 746, 17, white, leading=19)
    paragraph(pdf, subtitle, title_bottom - 2, 8.5, white, leading=10)
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica", 8)
    pdf.drawRightString(574, 20, f"WS-004 / {page} of 3")


def metric(pdf, x, y, value, label, color=FOREST):
    pdf.setFillColor(PALE)
    pdf.roundRect(x, y, 123, 58, 7, fill=1, stroke=0)
    pdf.setFillColor(color)
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(x + 12, y + 28, value)
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica", 7.5)
    pdf.drawString(x + 12, y + 13, label)


def labeled_box(pdf, x, y, width, title, body, accent=FOREST):
    pdf.setFillColor(PALE)
    pdf.roundRect(x, y, width, 78, 7, fill=1, stroke=0)
    pdf.setFillColor(accent)
    pdf.rect(x, y, 4, 78, fill=1, stroke=0)
    paragraph(pdf, f"<b>{title}</b>", y + 62, 8, accent, x=x + 13, width=width - 24)
    paragraph(pdf, body, y + 45, 7.7, INK, x=x + 13, width=width - 24, leading=10)


def build_pdf():
    run = json.loads(RUN_PATH.read_text(encoding="utf-8"))
    changed = json.loads(CHANGED_PATH.read_text(encoding="utf-8"))
    if run["summary"] != {
        "totalCases": 6,
        "RECONCILED": 2,
        "MISMATCH": 1,
        "REVIEW_REQUIRED": 3,
    }:
        raise ValueError("Default evidence run does not match the frozen oracle.")
    if not SCREENSHOT.is_file():
        raise FileNotFoundError(f"Missing working-demo screenshot: {SCREENSHOT}")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(OUTPUT), pagesize=LETTER)
    pdf.setTitle("Carbon Disclosure Reconciliation Desk - Working Demo")
    pdf.setAuthor("lmnhd")

    # Page 1: buyer problem and working result.
    header(
        pdf,
        1,
        "Can the disclosed number be reproduced?",
        "A reviewer workbench that computes explicit evidence and escalates the rest.",
    )
    y = paragraph(
        pdf,
        "<b>The buyer problem:</b> energy and emissions figures sit inside filings with different layouts, units, factor vintages, and levels of detail. Reviewers lose time determining which arithmetic can be reproduced and which claims need follow-up.",
        670,
        10,
        INK,
    )
    y = paragraph(
        pdf,
        "<b>The useful result:</b> this working prototype preserves a narrow source locator and hashes, converts supported units with decimal arithmetic, checks one pinned factor set, and returns <b>RECONCILED</b>, <b>MISMATCH</b>, or <b>REVIEW_REQUIRED</b> with a reason.",
        y - 10,
        10,
        FOREST,
    )
    metric(pdf, 38, 505, "2", "RECONCILED", FOREST)
    metric(pdf, 178, 505, "1", "MISMATCH", RED)
    metric(pdf, 318, 505, "3", "REVIEW REQUIRED", AMBER)
    metric(pdf, 458, 505, "6/6", "ORACLE CASES", BLUE)
    paragraph(pdf, "<b>Actual working-output screenshot</b>", 490, 8.5, INK)
    pdf.drawImage(
        ImageReader(str(SCREENSHOT)),
        38,
        145,
        width=536,
        height=335,
        preserveAspectRatio=True,
        anchor="c",
        mask="auto",
    )
    paragraph(
        pdf,
        "Evidence boundary: three minimized recorded filing sources plus two labeled controlled scenarios. No company names or personal fields are displayed. Results assess arithmetic reproducibility only.",
        132,
        7.5,
        MUTED,
    )
    pdf.showPage()

    # Page 2: actual problem-solving correction and implemented guard.
    header(
        pdf,
        2,
        "The right factor year mattered more than the newest file.",
        "Source inspection corrected the obvious approach before implementation.",
    )
    y = paragraph(
        pdf,
        "<b>The observed obstacle:</b> preliminary feasibility selected the newer 2026 UK factor workbook. The three chosen filings explicitly cited 2025 factors. Comparing their arithmetic with 2026 values would create a confident-looking but false mismatch.",
        670,
        10,
        INK,
    )
    y = paragraph(
        pdf,
        "<b>The implemented correction:</b> freeze the official 2025 Version 1 / Final workbook, retain only the exact rows needed, hash both the source workbook and minimized factor subset, and refuse calculations when evidence does not identify a compatible basis.",
        y - 10,
        10,
        FOREST,
    )

    labeled_box(pdf, 38, 500, 164, "BEFORE", "Newest 2026 factor file selected during preliminary feasibility.", RED)
    labeled_box(pdf, 224, 500, 164, "SOURCE CHECK", "All selected filings reference the 2025 reporting factors.", BLUE)
    labeled_box(pdf, 410, 500, 164, "AFTER", "2025 V1 Final pinned by row ID, date, and SHA-256.", FOREST)

    pdf.setFillColor(PALE)
    pdf.roundRect(38, 272, 536, 205, 8, fill=1, stroke=0)
    paragraph(pdf, "<b>Actual code excerpt: compute only after evidence gates</b>", 458, 9, INK, x=50, width=510)
    source_lines = inspect.getsource(reconcile.evaluate_case).splitlines()
    excerpt_start = next(
        index for index, line in enumerate(source_lines) if "SUPPORTED_SOURCE_FORMATS" in line
    )
    excerpt = source_lines[excerpt_start : excerpt_start + 15]
    pdf.setFillColor(INK)
    pdf.setFont("Courier", 7.1)
    for index, line in enumerate(excerpt):
        pdf.drawString(50, 431 - index * 10.5, line[:91])

    metric(pdf, 38, 190, "2025", "MATCHED FACTOR YEAR", FOREST)
    metric(pdf, 178, 190, "3", "PINNED FACTOR ROWS", BLUE)
    metric(pdf, 318, 190, "27/27", "AUTOMATED TESTS", FOREST)
    metric(pdf, 458, 190, "FAIL", "CLOSED ON AMBIGUITY", AMBER)
    paragraph(
        pdf,
        "Example: a natural-gas kWh value that does not say gross or net calorific value returns REVIEW_REQUIRED. The engine never chooses the factor that happens to match the disclosed result.",
        175,
        8.2,
        MUTED,
    )
    pdf.showPage()

    # Page 3: reproducible proof and local try-it path.
    header(
        pdf,
        3,
        "Change one unit. Watch the evidence decision change.",
        "The controlled scenario makes the calculation and hash behavior independently testable.",
    )
    metric(pdf, 38, 610, "1,000", "BASELINE MWh", FOREST)
    metric(pdf, 178, 610, "177.000", "BASELINE tCO2e", FOREST)
    metric(pdf, 318, 610, "0.177", "CHANGED tCO2e", RED)
    metric(pdf, 458, 610, "27/27", "TESTS PASSING", BLUE)

    y = paragraph(
        pdf,
        "<b>Reviewer-operated proof:</b> keep the numeric activity at 1,000 and change only the unit from MWh to kWh. Normalized activity and recomputed emissions become exactly 1/1,000 of baseline. The input hash changes; source, factor, and engine hashes remain stable; RECONCILED becomes MISMATCH.",
        592,
        10,
        INK,
    )
    labeled_box(pdf, 38, 455, 255, "BASELINE / MWh", "1,000,000 kWh normalized -> 177.000 tCO2e -> RECONCILED", FOREST)
    labeled_box(pdf, 319, 455, 255, "REVIEW CHANGE / kWh", "1,000 kWh normalized -> 0.177 tCO2e -> MISMATCH", RED)

    y = paragraph(
        pdf,
        "<b>Try it locally in about one minute:</b><br/>"
        "1. Run <code>python app.py</code> in the WS-004 project folder.<br/>"
        "2. Open the local workbench link below; the six-case run executes automatically.<br/>"
        "3. Click <b>Try the 1/1,000 unit change</b>.<br/>"
        "4. Inspect reason codes and download the executed JSON and CSV.",
        435,
        9,
        INK,
    )

    y = paragraph(
        pdf,
        f'<link href="{LOCAL_DEMO}" color="#0B5C4C"><u><b>Local working demo: 127.0.0.1:5000</b></u></link>',
        y - 14,
        10.5,
        INK,
    )
    y = paragraph(
        pdf,
        f'<link href="{REPO}" color="#0B5C4C"><u>Repository and reproducible evidence</u></link>',
        y - 7,
        9,
        INK,
    )

    pdf.setFillColor(PALE)
    pdf.roundRect(38, 160, 536, 90, 8, fill=1, stroke=0)
    paragraph(pdf, "<b>Limits that matter</b>", 233, 9, INK, x=50, width=510)
    paragraph(
        pdf,
        "Six bounded cases are not production accuracy. Recorded facts are minimized; controlled scenarios are labeled. No full filing bodies, company names, or personal fields are bundled. A result is not an audit opinion, compliance certification, environmental score, or statement that reported emissions are true.",
        213,
        8,
        MUTED,
        x=50,
        width=510,
        leading=10.5,
    )
    paragraph(
        pdf,
        f"Evidence run {run['runId']} / changed run {changed['runId']} / UK-GHG-2025-V1-FINAL",
        143,
        7.2,
        MUTED,
    )
    pdf.save()
    print(f"Generated PDF at {OUTPUT}")


if __name__ == "__main__":
    build_pdf()
