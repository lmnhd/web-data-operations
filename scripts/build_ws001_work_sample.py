"""Build the reviewer-facing three-page WS-001 PDF work sample."""

from __future__ import annotations

import json
from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projects" / "WS-001-qualified-tender-change-intelligence"
OUTPUT = ROOT / "output" / "pdf" / "Government-Contract-Change-Monitor.pdf"

INK = HexColor("#102A43")
MUTED = HexColor("#52667A")
TEAL = HexColor("#007C78")
TEAL_LIGHT = HexColor("#E8F6F4")
ORANGE = HexColor("#E47C22")
ORANGE_LIGHT = HexColor("#FFF2E8")
BLUE_LIGHT = HexColor("#EDF4FC")
LINE = HexColor("#D8E2EA")
PAPER = HexColor("#F8FAFC")


def load_summary(slug: str) -> dict[str, int]:
    path = PROJECT / "evidence" / "live" / slug / "run-report.json"
    return json.loads(path.read_text(encoding="utf-8"))["summary"]


def paragraph(c: canvas.Canvas, text: str, x: float, y: float, width: float, size: int = 10,
              color=MUTED, leading: float | None = None, bold: bool = False) -> float:
    style = ParagraphStyle(
        "body",
        fontName="Helvetica-Bold" if bold else "Helvetica",
        fontSize=size,
        leading=leading or size * 1.35,
        textColor=color,
        alignment=TA_LEFT,
        spaceAfter=0,
    )
    item = Paragraph(text, style)
    _, height = item.wrap(width, 10 * inch)
    item.drawOn(c, x, y - height)
    return y - height


def header(c: canvas.Canvas, page: int, kicker: str, title: str, subtitle: str) -> float:
    width, height = LETTER
    c.setFillColor(INK)
    c.rect(0, height - 1.52 * inch, width, 1.52 * inch, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(0, height - 1.52 * inch, 0.12 * inch, 1.52 * inch, fill=1, stroke=0)
    c.setFillColor(HexColor("#8EE3D8"))
    c.setFont("Helvetica-Bold", 8)
    c.drawString(0.52 * inch, height - 0.38 * inch, kicker.upper())
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(0.52 * inch, height - 0.78 * inch, title)
    paragraph(c, subtitle, 0.52 * inch, height - 0.96 * inch, 6.95 * inch, 9, HexColor("#D8E5EE"), 12)
    c.setFillColor(HexColor("#A9B8C4"))
    c.setFont("Helvetica", 8)
    c.drawRightString(width - 0.45 * inch, 0.30 * inch, f"WS-001  |  {page} / 3")
    return height - 1.82 * inch


def rounded_box(c: canvas.Canvas, x: float, y: float, w: float, h: float, fill, stroke=LINE, radius=9):
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1)


def metric(c: canvas.Canvas, x: float, y: float, w: float, value: str, label: str, fill=TEAL_LIGHT):
    rounded_box(c, x, y, w, 0.82 * inch, fill)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(x + 0.18 * inch, y + 0.40 * inch, value)
    paragraph(c, label, x + 0.18 * inch, y + 0.31 * inch, w - 0.36 * inch, 8, MUTED, 10, True)


def footer_source(c: canvas.Canvas, text: str):
    paragraph(c, text, 0.52 * inch, 0.52 * inch, 5.55 * inch, 6.8, MUTED, 9)


def redraw_page_number(c: canvas.Canvas, page: int):
    width, _ = LETTER
    c.setFillColor(HexColor("#A9B8C4"))
    c.setFont("Helvetica", 8)
    c.drawRightString(width - 0.45 * inch, 0.30 * inch, f"WS-001  |  {page} / 3")


def page_one(c: canvas.Canvas, noise: dict[str, int], change: dict[str, int]):
    y = header(
        c, 1, "Portfolio project - government contract monitoring",
        "Stop rereading contract notices",
        "I built a system that checks updated government opportunities, ignores meaningless reissues, and shows a business which changes need attention.",
    )
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(0.52 * inch, y, "The client problem")
    y = paragraph(c, "Government contract websites may publish several versions of the same opportunity. A business can waste time reopening every version even when the deadline, value, status, and eligibility details have not changed.", 0.52 * inch, y - 0.15 * inch, 6.95 * inch, 10, MUTED, 14)

    y -= 0.23 * inch
    metric(c, 0.52 * inch, y - 0.82 * inch, 1.58 * inch, "7", "versions in one live notice", TEAL_LIGHT)
    metric(c, 2.23 * inch, y - 0.82 * inch, 1.58 * inch, str(noise["comparisons"]), "versions labeled as updates", ORANGE_LIGHT)
    metric(c, 3.94 * inch, y - 0.82 * inch, 1.58 * inch, str(noise["material_change_comparisons"]), "important changes in those updates", BLUE_LIGHT)
    metric(c, 5.65 * inch, y - 0.82 * inch, 1.58 * inch, "1", "real cancellation found", TEAL_LIGHT)
    y -= 1.14 * inch

    rounded_box(c, 0.52 * inch, y - 1.38 * inch, 3.31 * inch, 1.38 * inch, PAPER)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.72 * inch, y - 0.28 * inch, "CASE 1  |  SIX FALSE ALARMS REMOVED")
    paragraph(c, "The source called six versions updates. The system compared the details a contractor cares about and found that <b>nothing important changed</b>. All six were removed from the action list.", 0.72 * inch, y - 0.45 * inch, 2.90 * inch, 9, MUTED, 12)

    rounded_box(c, 4.01 * inch, y - 1.38 * inch, 3.22 * inch, 1.38 * inch, PAPER)
    c.setFillColor(ORANGE)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(4.21 * inch, y - 0.28 * inch, "CASE 2  |  REAL CANCELLATION FOUND")
    paragraph(c, "A second notice actually changed: it was cancelled, its deadline and value disappeared, and its work package closed. The system found <b>five important changes</b> and sent it for review.", 4.21 * inch, y - 0.45 * inch, 2.82 * inch, 9, MUTED, 12)
    y -= 1.68 * inch

    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(0.52 * inch, y, "What the client receives")
    bullets = [
        "A short list of opportunities that actually changed",
        "An ignore list showing why an update was dismissed",
        "A review list when the source does not provide enough information",
        "Downloadable results that can feed email, a CRM, or a spreadsheet",
    ]
    for index, item in enumerate(bullets):
        bx = 0.54 * inch + (index % 2) * 3.48 * inch
        by = y - 0.38 * inch - (index // 2) * 0.52 * inch
        c.setFillColor(TEAL)
        c.circle(bx + 0.06 * inch, by + 0.05 * inch, 0.045 * inch, fill=1, stroke=0)
        paragraph(c, item, bx + 0.18 * inch, by + 0.16 * inch, 3.08 * inch, 8.5, MUTED, 11, True)

    footer_source(c, "This document presents one working portfolio project. It does not describe the separate development workflow used to create portfolio projects.")
    redraw_page_number(c, 1)


def page_two(c: canvas.Canvas):
    y = header(c, 2, "How the solution works", "From a crowded update feed to a short action list", "The system follows four understandable steps. The client's business rules remain editable instead of being hidden inside an AI prompt.")

    stages = [
        ("1", "Collect", "Download official\nnotice history"),
        ("2", "Compare", "Check deadline, value,\nstatus, category and lots"),
        ("3", "Filter", "Apply the client's\nbusiness rules"),
        ("4", "Deliver", "Create act, ignore and\nreview lists"),
    ]
    box_w = 1.57 * inch
    gap = 0.18 * inch
    x = 0.52 * inch
    for index, (number, title, detail) in enumerate(stages):
        rounded_box(c, x, y - 1.22 * inch, box_w, 1.10 * inch, TEAL_LIGHT if index < 2 else PAPER)
        c.setFillColor(TEAL)
        c.circle(x + 0.19 * inch, y - 0.34 * inch, 0.12 * inch, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(x + 0.19 * inch, y - 0.37 * inch, number)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x + 0.38 * inch, y - 0.37 * inch, title)
        paragraph(c, detail.replace("\n", "<br/>"), x + 0.14 * inch, y - 0.59 * inch, box_w - 0.28 * inch, 7.5, MUTED, 10)
        if index < len(stages) - 1:
            c.setStrokeColor(ORANGE)
            c.setLineWidth(1.5)
            c.line(x + box_w + 0.03 * inch, y - 0.67 * inch, x + box_w + gap - 0.03 * inch, y - 0.67 * inch)
        x += box_w + gap
    y -= 1.55 * inch

    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(0.52 * inch, y, "Rules a client can customize")
    fields = ["Contract category", "Minimum and maximum value", "Closing-date window", "Opportunity status", "Work-package status", "Required information"]
    for index, field in enumerate(fields):
        col = index % 2
        row = index // 2
        fx = 0.52 * inch + col * 3.48 * inch
        fy = y - 0.32 * inch - row * 0.36 * inch
        rounded_box(c, fx, fy - 0.22 * inch, 3.18 * inch, 0.27 * inch, BLUE_LIGHT, BLUE_LIGHT, 4)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(fx + 0.10 * inch, fy - 0.13 * inch, field)
    y -= 1.35 * inch

    rounded_box(c, 0.52 * inch, y - 1.70 * inch, 3.30 * inch, 1.70 * inch, PAPER)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.72 * inch, y - 0.30 * inch, "Why there are three output lists")
    paragraph(c, "<b>Act:</b> something important changed and the opportunity still fits.<br/><b>Ignore:</b> nothing useful changed, or the opportunity does not fit.<br/><b>Review:</b> something changed, but the source is missing information needed for a safe decision.", 0.72 * inch, y - 0.50 * inch, 2.88 * inch, 8.7, MUTED, 11.5)

    rounded_box(c, 4.01 * inch, y - 1.70 * inch, 3.22 * inch, 1.70 * inch, PAPER)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(4.21 * inch, y - 0.30 * inch, "Every result explains itself")
    evidence = ["what changed, including old and new values", "why the opportunity was accepted or rejected", "which information was missing", "where and when the source data was retrieved", "a fingerprint proving which source version was used"]
    for index, item in enumerate(evidence):
        c.setFillColor(TEAL)
        c.rect(4.22 * inch, y - (0.58 + index * 0.21) * inch, 0.07 * inch, 0.07 * inch, fill=1, stroke=0)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 8)
        c.drawString(4.38 * inch, y - (0.60 + index * 0.21) * inch, item)

    footer_source(c, "Possible delivery formats include a spreadsheet, CSV export, email alert, CRM update, dashboard, or API response. This demonstration currently produces JSON and CSV files.")
    redraw_page_number(c, 2)


def page_three(c: canvas.Canvas):
    y = header(c, 3, "Working demonstration and evidence", "What I built and proved", "The demonstration uses both repeatable test cases and two real public contract records. The technical evidence is available for a client or engineering reviewer to inspect.")

    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(0.52 * inch, y, "Plain-English verification")
    rows = [
        ("Can it remove meaningless updates?", "6 live updates", "Yes - all 6 ignored"),
        ("Can it find a real cancellation?", "1 live cancellation", "Yes - 5 changes found"),
        ("Will it guess when details are missing?", "Live missing data", "No - sent to review"),
        ("Can saved data be processed again?", "Automated replay", "Yes - same result"),
        ("Are contact details kept out?", "Automated privacy check", "Yes - excluded"),
        ("Do the repeatable tests pass?", "7 automated tests", "Yes - 7 of 7"),
    ]
    x0 = 0.52 * inch
    widths = [3.12 * inch, 1.55 * inch, 2.28 * inch]
    headers = ["CLIENT QUESTION", "HOW TESTED", "RESULT"]
    y0 = y - 0.28 * inch
    c.setFillColor(INK)
    c.rect(x0, y0 - 0.34 * inch, sum(widths), 0.34 * inch, fill=1, stroke=0)
    x = x0
    for label, width in zip(headers, widths):
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(x + 0.10 * inch, y0 - 0.22 * inch, label)
        x += width
    row_y = y0 - 0.34 * inch
    for index, row in enumerate(rows):
        c.setFillColor(PAPER if index % 2 == 0 else white)
        c.rect(x0, row_y - 0.43 * inch, sum(widths), 0.43 * inch, fill=1, stroke=0)
        x = x0
        for value, width in zip(row, widths):
            paragraph(c, value, x + 0.10 * inch, row_y - 0.11 * inch, width - 0.18 * inch, 7.4, INK if x == x0 else MUTED, 9, x == x0)
            x += width
        row_y -= 0.43 * inch
    y = row_y - 0.30 * inch

    rounded_box(c, 0.52 * inch, y - 1.32 * inch, 3.30 * inch, 1.32 * inch, TEAL_LIGHT, TEAL_LIGHT)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.72 * inch, y - 0.28 * inch, "WHAT THIS DEMO IS")
    paragraph(c, "A working example of contract-update monitoring, business-rule filtering, privacy-conscious data handling, explainable decisions, and downloadable results. The code, tests, sanitized samples, and results are included.", 0.72 * inch, y - 0.48 * inch, 2.88 * inch, 8.5, MUTED, 11.5)

    rounded_box(c, 4.01 * inch, y - 1.32 * inch, 3.22 * inch, 1.32 * inch, ORANGE_LIGHT, ORANGE_LIGHT)
    c.setFillColor(ORANGE)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(4.21 * inch, y - 0.28 * inch, "WHAT IT IS NOT YET")
    paragraph(c, "It is not an always-on hosted service. Scheduling, dashboards, email or CRM delivery, document comparison, and production-scale monitoring would be configured around a client's sources and workflow.", 4.21 * inch, y - 0.48 * inch, 2.80 * inch, 8.5, MUTED, 11.5)
    y -= 1.65 * inch

    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.52 * inch, y, "Technical handoff")
    rounded_box(c, 0.52 * inch, y - 0.73 * inch, 6.71 * inch, 0.58 * inch, INK, INK, 5)
    paragraph(c, "Python  |  Find a Tender OCDS API  |  Rule-based filtering  |  JSON + CSV  |  7 automated tests", 0.70 * inch, y - 0.34 * inch, 6.32 * inch, 7.2, white, 9)

    footer_source(c, "Evidence: github.com/lmnhd/web-data-operations | Public data: Find a Tender OCDS API, accessed 2026-09-03 and licensed under the Open Government Licence v3.0.")
    redraw_page_number(c, 3)


def main() -> int:
    noise = load_summary("run-06d396")
    change = load_summary("run-06bb7d")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=LETTER, pageCompression=1)
    c.setTitle("Government Contract Change Monitor - Portfolio Project")
    c.setAuthor("lmnhd")
    page_one(c, noise, change)
    c.showPage()
    page_two(c)
    c.showPage()
    page_three(c)
    c.showPage()
    c.save()
    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
