"""Build the three-page WS-003 case study PDF."""
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
PROJECT = ROOT / "projects/WS-003-municipal-sla-operations-explorer"
OUTPUT = ROOT / "output/pdf/Municipal-311-SLA-Operations-Desk.pdf"
SCREENSHOT = PROJECT / "evidence/reviewer/working-demo-pdf.png"
sys.path.insert(0, str(PROJECT / "src"))
import sla_engine  # noqa: E402

INK = HexColor("#17313B")
GREEN = HexColor("#126B55")
LIME = HexColor("#C9F27B")
MUTED = HexColor("#526D67")
PALE = HexColor("#EEF2F0")
AMBER = HexColor("#AA4D16")
RED = HexColor("#8F2D23")
REPO = "https://github.com/lmnhd/web-data-operations"
PUBLIC_DEMO = "https://municipal-311-sla-operations-desk.vercel.app"


def build_ward_summary():
    """Render the ward ranking lines from the engine's synthetic evaluation run.

    The compliance rate divides by evaluable records (total minus data-quality
    exclusions), so the evaluable count is shown explicitly to keep the printed
    arithmetic self-explanatory.
    """
    run = json.loads((PROJECT / "evidence/evaluated_run.json").read_text(encoding="utf-8"))
    analytics = run["ward_analytics"]

    ranked = sorted(
        analytics.items(),
        key=lambda item: item[1]["compliance_rate_pct"],
        reverse=True,
    )
    bottleneck = ranked[-1][0] if ranked else None

    lines = []
    for ward, stats in ranked:
        evaluable = stats["total_requests"] - stats["data_error"]
        line = (
            f"{ward:<26} | Total: {stats['total_requests']}"
            f" | Eval: {evaluable}"
            f" | Compliant: {stats['compliant']}"
            f" | Breached: {stats['breached']}"
            f" | Compliance: {stats['compliance_rate_pct']:.1f}%"
        )
        if ward == bottleneck:
            line += " (BOTTLENECK)"
        lines.append(line)
    return lines


def paragraph(c, words, y, size=10, color=MUTED, x=38, width=536, leading=None):
    style = ParagraphStyle(
        "p",
        fontName="Helvetica",
        fontSize=size,
        leading=leading or size * 1.35,
        textColor=color,
    )
    block = Paragraph(words, style)
    _, height = block.wrap(width, 800)
    block.drawOn(c, x, y - height)
    return y - height


def header(c, page, title, subtitle):
    c.setFillColor(INK)
    c.rect(0, 690, 612, 102, fill=1, stroke=0)
    paragraph(c, "MUNICIPAL 311 SLA OPERATIONS DESK / WORKING DEMO", 768, 8, LIME)
    title_bottom = paragraph(c, f"<b>{title}</b>", 746, 17, white, leading=19)
    paragraph(c, subtitle, title_bottom - 2, 8.5, white, leading=10)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawRightString(574, 16, f"WS-003 / {page} of 3")


def metric(c, x, y, value, label, color=GREEN):
    c.setFillColor(PALE)
    c.roundRect(x, y, 123, 58, 7, fill=1, stroke=0)
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(x + 12, y + 28, value)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawString(x + 12, y + 13, label)


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=LETTER)
    c.setTitle("Municipal 311 SLA Operations Desk - Working Demo")
    c.setAuthor("lmnhd")

    # PAGE 1: Problem & Result
    header(
        c,
        1,
        "Public 311 data alone cannot answer SLA timing questions.",
        "This working prototype uses clearly labeled synthetic records to show the decision workflow.",
    )

    y = paragraph(
        c,
        "<b>The buyer problem:</b> public 311 exports can show creation date, status, ward, request type, division, and section, but Toronto's current public file does not expose target or closure timestamps. An honest SLA workflow must join authorized internal work-order fields before it can calculate timing outcomes.",
        670,
        10,
        INK,
    )

    y = paragraph(
        c,
        "<b>The useful result:</b> an adapter-ready calculation engine that normalizes enriched timestamps, applies configurable response rules, computes margins, and creates a review queue. The bundled proof uses synthetic inputs so its behavior is reproducible without implying official municipal results.",
        y - 12,
        10,
        GREEN,
    )

    metric(c, 38, y - 75, "15/15", "synthetic labels reproduced")
    metric(c, 178, y - 75, "40.0%", "scenario ward rate", RED)
    metric(c, 318, y - 75, "5", "simulated breaches", RED)
    metric(c, 458, y - 75, "1", "data review isolated", AMBER)

    y = y - 95

    if not SCREENSHOT.is_file():
        raise FileNotFoundError(f"Missing reviewer screenshot: {SCREENSHOT}")
    paragraph(c, "<b>Actual working-output screenshot: synthetic SLA scenario</b>", y - 8, 9, INK)
    screenshot_height = 260
    screenshot_y = y - 278
    c.drawImage(
        ImageReader(str(SCREENSHOT)),
        38,
        screenshot_y,
        width=536,
        height=screenshot_height,
        preserveAspectRatio=True,
        anchor="c",
        mask="auto",
    )

    y = screenshot_y - 12

    paragraph(
        c,
        "Source context: City of Toronto 311 public schema and Open Government Licence - Toronto. The displayed IDs, categories, SLA rules, target dates, closure dates, and outcomes are synthetic. Zero personal data is used.",
        y,
        8,
        MUTED,
    )
    c.showPage()

    # PAGE 2: Creative Problem Solving
    header(
        c,
        2,
        "Missing public timing fields require an explicit adapter boundary.",
        "The creative obstacle: prove the workflow without inventing official municipal SLA results.",
    )

    y = paragraph(
        c,
        "<b>The technical challenge:</b> the official Toronto 2026 export includes creation date and current status, but not target or closure timestamps. Treating absent fields as evidence would create false breach or compliance claims.",
        670,
        10,
        INK,
    )

    y = paragraph(
        c,
        "<b>The implemented correction:</b> separate the licensed public schema from a synthetic, adapter-ready SLA contract. The proof exercises ISO8601 parsing, configurable hypothetical targets, explicit <b>INCOMPLETE_DATA_REVIEW</b> routing, and machine-readable fixture labels. Production use would require authorized internal target and closure fields.",
        y - 12,
        10,
        INK,
    )

    c.setFillColor(PALE)
    c.roundRect(38, y - 210, 536, 195, 8, fill=1, stroke=0)
    paragraph(c, "<b>Actual code excerpt: explicit fixture label and failure route</b>", y - 20, 10, INK, x=50, width=510)

    source_lines = inspect.getsource(sla_engine.evaluate_record).splitlines()
    excerpt_start = next(i for i, line in enumerate(source_lines) if "created_dt =" in line)
    code_lines = source_lines[excerpt_start : excerpt_start + 16]
    c.setFillColor(INK)
    c.setFont("Courier", 7.2)
    for idx, line in enumerate(code_lines):
        c.drawString(50, y - 40 - idx * 11, line[:88])

    y = y - 230

    metric(c, 38, y - 60, "15/15", "synthetic labels reproduced")
    metric(c, 178, y - 60, "7/7", "unit & integration tests passed")
    metric(c, 318, y - 60, "1", "malformed record isolated")
    metric(c, 458, y - 60, "SHA-256", "content fingerprinting")

    y = y - 80

    paragraph(
        c,
        "Boundary: scenario calculations demonstrate a review workflow. They are not City of Toronto results, legal SLA certifications, production staffing recommendations, or dispatch commands.",
        y,
        8,
        MUTED,
    )
    c.showPage()

    # PAGE 3: Reproducible Proof & Try-It
    header(
        c,
        3,
        "Change the rule thresholds. Watch the queue update.",
        "Reproduce the synthetic benchmark, inspect scenario analytics, and export labeled queues.",
    )

    metric(c, 38, 610, "15", "records evaluated")
    metric(c, 178, 610, "3", "city wards analyzed")
    metric(c, 318, 610, "8/1/5/1", "compliant / risk / breach / error")
    metric(c, 458, 610, "7/7", "automated tests passing")

    y = paragraph(
        c,
        "<b>Contrasting Rule Scenario:</b> Reducing the hypothetical Pothole Repair target from 5 days to 3 days re-classifies synthetic request <code>SR-311-001</code> (completed in 3.23 days) from <b>COMPLIANT</b> to <b>SLA_BREACHED</b>.",
        590,
        10,
        INK,
    )

    c.setFillColor(PALE)
    c.roundRect(38, y - 130, 536, 115, 8, fill=1, stroke=0)
    paragraph(c, "<b>Synthetic Ward Scenario Ranking</b>", y - 20, 10, INK, x=50, width=510)

    ward_summary = build_ward_summary()

    c.setFillColor(INK)
    c.setFont("Courier", 7.5)
    for idx, line in enumerate(ward_summary):
        c.drawString(50, y - 45 - idx * 22, line)

    y = y - 150

    paragraph(
        c,
        "<b>Try it locally or in the web workbench in about one minute:</b><br/>"
        "1. Open the public web demo link below (no login required).<br/>"
        "2. Click 'Evaluate SLA Engine' to run default 5/3/10/2 day SLA rules.<br/>"
        "3. Click 'Apply Strict Rules (3/2/5/1)' and observe request status re-classifications.<br/>"
        "4. Export evaluated JSON / CSV queues with explicit audit reason codes.",
        y,
        9,
        INK,
    )

    y = y - 90

    paragraph(c, f'<link href="{PUBLIC_DEMO}" color="#126B55"><u><b>Working web demo: municipal-311-sla-operations-desk.vercel.app</b></u></link>', y, 11, INK)
    paragraph(c, f'<link href="{REPO}" color="#126B55"><u>GitHub Repository, evidence, and local launch instructions</u></link>', y - 22, 9, INK)

    c.save()
    print(f"Generated PDF at {OUTPUT}")


if __name__ == "__main__":
    main()
