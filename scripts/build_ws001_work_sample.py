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
OUTPUT = ROOT / "output" / "pdf" / "WS-001-qualified-tender-change-intelligence.pdf"

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
    paragraph(c, text, 0.52 * inch, 0.52 * inch, 6.05 * inch, 6.8, MUTED, 9)


def redraw_page_number(c: canvas.Canvas, page: int):
    width, _ = LETTER
    c.setFillColor(HexColor("#A9B8C4"))
    c.setFont("Helvetica", 8)
    c.drawRightString(width - 0.45 * inch, 0.30 * inch, f"WS-001  |  {page} / 3")


def page_one(c: canvas.Canvas, noise: dict[str, int], change: dict[str, int]):
    y = header(
        c, 1, "Web data operations - live evidence",
        "Qualified Tender Change Intelligence",
        "A procurement-data pipeline that separates republication noise from material changes, then routes each result through explainable qualification rules.",
    )
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(0.52 * inch, y, "The operational problem")
    y = paragraph(c, "An update label is not proof that a bid-relevant field changed. A small pursuit team needs fewer false alarms, clear rejection reasons, and a safe review path when the source lacks evidence.", 0.52 * inch, y - 0.15 * inch, 6.95 * inch, 10, MUTED, 14)

    y -= 0.23 * inch
    metric(c, 0.52 * inch, y - 0.82 * inch, 1.58 * inch, str(noise["comparisons"]), "update-tagged comparisons", TEAL_LIGHT)
    metric(c, 2.23 * inch, y - 0.82 * inch, 1.58 * inch, str(noise["material_change_comparisons"]), "material changes found", ORANGE_LIGHT)
    metric(c, 3.94 * inch, y - 0.82 * inch, 1.58 * inch, str(change["material_change_comparisons"]), "real cancellation surfaced", BLUE_LIGHT)
    metric(c, 5.65 * inch, y - 0.82 * inch, 1.58 * inch, "7/7", "automated tests passing", TEAL_LIGHT)
    y -= 1.14 * inch

    rounded_box(c, 0.52 * inch, y - 1.38 * inch, 3.31 * inch, 1.38 * inch, PAPER)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.72 * inch, y - 0.28 * inch, "LIVE CASE A  |  NOISE SUPPRESSION")
    paragraph(c, "One procurement process contained 7 releases. Six later releases carried <b>tenderUpdate</b>, yet none changed status, deadline, value, currency, classification, or lot state. All six were rejected as <b>NO_MATERIAL_CHANGE</b>.", 0.72 * inch, y - 0.45 * inch, 2.90 * inch, 9, MUTED, 12)

    rounded_box(c, 4.01 * inch, y - 1.38 * inch, 3.22 * inch, 1.38 * inch, PAPER)
    c.setFillColor(ORANGE)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(4.21 * inch, y - 0.28 * inch, "LIVE CASE B  |  SAFE ESCALATION")
    paragraph(c, "A second process changed from active to complete, removed its deadline and value, and closed its lot. The pipeline surfaced 5 field changes, then routed the record to <b>review-needed</b> because qualification evidence was absent.", 4.21 * inch, y - 0.45 * inch, 2.82 * inch, 9, MUTED, 12)
    y -= 1.68 * inch

    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(0.52 * inch, y, "What this demonstrates")
    bullets = [
        "Direct field comparison instead of trusting source labels",
        "Deterministic accepted, rejected, and review-needed queues",
        "Reason codes and provenance on every retained decision",
        "No persisted contact details, descriptions, or unstructured prose",
    ]
    for index, item in enumerate(bullets):
        bx = 0.54 * inch + (index % 2) * 3.48 * inch
        by = y - 0.38 * inch - (index // 2) * 0.52 * inch
        c.setFillColor(TEAL)
        c.circle(bx + 0.06 * inch, by + 0.05 * inch, 0.045 * inch, fill=1, stroke=0)
        paragraph(c, item, bx + 0.18 * inch, by + 0.16 * inch, 3.08 * inch, 8.5, MUTED, 11, True)

    footer_source(c, "Observed 2026-09-03 from two bounded Find a Tender record-package requests. Results describe these records only; no claim of source-wide prevalence, completeness, or business savings is made.")
    redraw_page_number(c, 1)


def page_two(c: canvas.Canvas):
    y = header(c, 2, "Architecture", "From public record to decision queue", "A small, auditable pipeline: one sanctioned API path, a strict persistence boundary, deterministic transformations, and human review where evidence is incomplete.")

    stages = [
        ("1", "Acquire", "One record-package request\nNo pagination or retry"),
        ("2", "Sanitize", "Allowlisted tender fields\nRaw payload never written"),
        ("3", "Compare", "Consecutive snapshots\nDeclared material fields"),
        ("4", "Qualify", "Configured rules\nExplicit missing evidence"),
        ("5", "Route", "Accept / reject / review\nJSON and CSV evidence"),
    ]
    box_w = 1.24 * inch
    gap = 0.16 * inch
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
    c.drawString(0.52 * inch, y, "Declared material field set")
    fields = ["tender.status", "tender.tenderPeriod.endDate", "tender.value.amount", "tender.value.currency", "tender.classification.id", "tender.lots"]
    for index, field in enumerate(fields):
        col = index % 2
        row = index // 2
        fx = 0.52 * inch + col * 3.48 * inch
        fy = y - 0.32 * inch - row * 0.36 * inch
        rounded_box(c, fx, fy - 0.22 * inch, 3.18 * inch, 0.27 * inch, BLUE_LIGHT, BLUE_LIGHT, 4)
        c.setFillColor(INK)
        c.setFont("Courier-Bold", 7.5)
        c.drawString(fx + 0.10 * inch, fy - 0.13 * inch, field)
    y -= 1.35 * inch

    rounded_box(c, 0.52 * inch, y - 1.70 * inch, 3.30 * inch, 1.70 * inch, PAPER)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.72 * inch, y - 0.30 * inch, "Qualification is a separate decision")
    paragraph(c, "A material change is not automatically a good lead. The profile independently checks classification prefix, value range, and deadline threshold. Failed rules are rejected; missing inputs go to review.", 0.72 * inch, y - 0.50 * inch, 2.88 * inch, 9, MUTED, 12)
    paragraph(c, "This separation prevents a change detector from silently becoming a lead-scoring black box.", 0.72 * inch, y - 1.22 * inch, 2.88 * inch, 8.5, TEAL, 11, True)

    rounded_box(c, 4.01 * inch, y - 1.70 * inch, 3.22 * inch, 1.70 * inch, PAPER)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(4.21 * inch, y - 0.30 * inch, "Evidence retained with every result")
    evidence = ["source URL + retrieval timestamp", "SHA-256 source fingerprint", "release ID + procurement process ID", "changed fields + old/new values", "decision + reason codes"]
    for index, item in enumerate(evidence):
        c.setFillColor(TEAL)
        c.rect(4.22 * inch, y - (0.58 + index * 0.21) * inch, 0.07 * inch, 0.07 * inch, fill=1, stroke=0)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 8)
        c.drawString(4.38 * inch, y - (0.60 + index * 0.21) * inch, item)

    footer_source(c, "Implementation: Python standard library plus ReportLab for this reviewer artifact. The data pipeline itself has no third-party runtime dependency.")
    redraw_page_number(c, 2)


def page_three(c: canvas.Canvas):
    y = header(c, 3, "Proof and trust boundaries", "What was verified - and what was not claimed", "The portfolio value is operational honesty: reproducible evidence, visible failure paths, and strict limits around source access and personal data.")

    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(0.52 * inch, y, "Verification matrix")
    rows = [
        ("Update tag without declared field change", "6 live comparisons", "Rejected as noise"),
        ("Material cancellation/status transition", "1 live comparison", "Five changes surfaced"),
        ("Missing qualification evidence", "1 live comparison", "Sent to review-needed"),
        ("Sanitized capture replay", "Automated test", "Same result after reload"),
        ("Contact and prose exclusion", "Automated test", "Absent from saved records"),
        ("Fixture behavior suite", "7 automated tests", "All passing"),
    ]
    x0 = 0.52 * inch
    widths = [3.12 * inch, 1.55 * inch, 2.28 * inch]
    headers = ["CONTROL", "EVIDENCE", "OUTCOME"]
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
    c.drawString(0.72 * inch, y - 0.28 * inch, "COMPLIANCE BY DESIGN")
    paragraph(c, "Two explicit record-package requests. No login, browser scraping, pagination, retry, proxying, rate-limit discovery, or adaptive polling. Raw responses remained in memory and were reduced to an allowlist before disk persistence.", 0.72 * inch, y - 0.48 * inch, 2.88 * inch, 8.5, MUTED, 11.5)

    rounded_box(c, 4.01 * inch, y - 1.32 * inch, 3.22 * inch, 1.32 * inch, ORANGE_LIGHT, ORANGE_LIGHT)
    c.setFillColor(ORANGE)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(4.21 * inch, y - 0.28 * inch, "LIMITATIONS STATED UP FRONT")
    paragraph(c, "This sample does not prove source-wide change frequency, complete recall, production scale, real-time operation, or customer savings. PDF reconciliation, scheduling, deployment, and CRM delivery remain outside WS-001.", 4.21 * inch, y - 0.48 * inch, 2.80 * inch, 8.5, MUTED, 11.5)
    y -= 1.65 * inch

    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.52 * inch, y, "Reproduce the proof")
    rounded_box(c, 0.52 * inch, y - 0.73 * inch, 6.71 * inch, 0.58 * inch, INK, INK, 5)
    paragraph(c, "python -m unittest discover -s projects/WS-001-qualified-tender-change-intelligence/tests -v", 0.70 * inch, y - 0.34 * inch, 6.32 * inch, 7.2, white, 9)

    footer_source(c, "Sources: Find a Tender OCDS record package API and Terms and Conditions, accessed 2026-09-03. Data licensed under the Open Government Licence v3.0. github.com/lmnhd/web-data-operations")
    redraw_page_number(c, 3)


def main() -> int:
    noise = load_summary("run-06d396")
    change = load_summary("run-06bb7d")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=LETTER, pageCompression=1)
    c.setTitle("WS-001 - Qualified Tender Change Intelligence")
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
