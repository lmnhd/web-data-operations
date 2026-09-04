"""Build the three-page WS-002 case study from actual reviewer captures."""
from pathlib import Path
import inspect
import sys

from PIL import Image
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projects/WS-002-recall-to-catalog-impact-review"
CAPTURES = PROJECT / "evidence/reviewer"
OUTPUT = ROOT / "output/pdf/Product-Recall-Match-Desk.pdf"
sys.path.insert(0, str(PROJECT / "src"))
from catalog_matcher import compare_pair  # noqa: E402

INK = HexColor("#14343B")
GREEN = HexColor("#0B7963")
LIME = HexColor("#B9E769")
MUTED = HexColor("#52666A")
PALE = HexColor("#EEF5F2")
AMBER = HexColor("#B56722")
REPO = "https://github.com/lmnhd/web-data-operations"
LOCAL_DEMO = "http://127.0.0.1:8766"


def paragraph(c, words, y, size=10, color=MUTED, x=38, width=536, leading=None):
    style = ParagraphStyle(
        "p", fontName="Helvetica", fontSize=size,
        leading=leading or size * 1.35, textColor=color,
    )
    block = Paragraph(words, style)
    _, height = block.wrap(width, 800)
    block.drawOn(c, x, y - height)
    return y - height


def header(c, page, title, subtitle):
    c.setFillColor(INK)
    c.rect(0, 690, 612, 102, fill=1, stroke=0)
    paragraph(c, "PRODUCT RECALL MATCH DESK / WORKING DEMO", 768, 8, LIME)
    paragraph(c, f"<b>{title}</b>", 746, 22, white)
    paragraph(c, subtitle, 712, 9, white)
    paragraph(c, f"WS-002 / {page} of 3", 24, 8, x=474, width=104)


def draw_crop(c, source, crop_box, top, width, x=38):
    temp = CAPTURES / (Path(source).stem + "-pdf-crop.png")
    with Image.open(CAPTURES / source) as image:
        image.crop(crop_box).save(temp)
    with Image.open(temp) as image:
        w, h = image.size
    height = width * h / w
    c.drawImage(str(temp), x, top - height, width=width, height=height)
    return top - height


def metric(c, x, y, value, label, color=GREEN):
    c.setFillColor(PALE)
    c.roundRect(x, y, 123, 58, 7, fill=1, stroke=0)
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(x + 12, y + 28, value)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawString(x + 12, y + 13, label)


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=LETTER)
    c.setTitle("Product Recall Match Desk - Working Demo")
    c.setAuthor("lmnhd")

    header(c, 1, "An identifier hit is not always a safe match.", "A catalog operator needs an explainable queue, not a guessed answer.")
    y = paragraph(
        c,
        "<b>The buyer problem:</b> regulator records and internal catalog rows can share an identifier while disagreeing on product strength. "
        "A confident-looking false match could send the wrong SKU into an operational workflow.",
        674,
    )
    y = paragraph(
        c,
        "<b>The useful result:</b> the real matcher preserves both candidates, shows the conflicting evidence, and routes the row to a person as <b>REVIEW NEEDED</b>.",
        y - 8, color=INK,
    )
    draw_crop(c, "ambiguous.png", (0, 0, 756, 710), y - 14, 470, x=71)
    paragraph(
        c,
        "Actual local-browser execution on 8 synthetic catalog rows and 10 selected, recorded openFDA enforcement records. The source request, capture time and fingerprints remain visible in the workbench.",
        70, 8,
    )
    c.showPage()

    header(c, 2, "Identity evidence has to agree by field.", "The creative obstacle: a shared UPC can span strengths and package variants.")
    y = paragraph(
        c,
        "<b>What failed in the first expansion run:</b> broad text overlap and a shared identifier were too permissive. Only 7 of 20 independently declared benchmark labels matched the output.",
        674,
    )
    y = paragraph(
        c,
        "<b>The correction:</b> compare strength values within the same unit, use an overlap coefficient for short names, and keep a visible review band. "
        "An exact identifier with a strength conflict is capped as review evidence; matching NDC, lot and strength can make one candidate decisive.",
        y - 10, color=INK,
    )
    c.setFillColor(PALE)
    c.roundRect(38, 354, 536, 205, 8, fill=1, stroke=0)
    paragraph(c, "<b>Actual evidence ladder excerpt</b>", 540, 10, INK, x=52, width=500)
    code = inspect.getsource(compare_pair).splitlines()
    selected = [line for line in code if any(token in line for token in (
        "exact_upc", "exact_ndc_family", "exact_lot_code", "strength_conflict", "strength_match", "score",
    ))][:13]
    c.setFillColor(INK)
    c.setFont("Courier", 7.5)
    for index, line in enumerate(selected):
        c.drawString(54, 512 - index * 11, line[:82])
    metric(c, 38, 258, "50", "conflict score - review", AMBER)
    metric(c, 178, 258, "200", "clarified score - match")
    metric(c, 318, 258, "2", "source candidates retained")
    metric(c, 458, 258, "0", "silent conflict overrides", AMBER)
    paragraph(
        c,
        "The repair was bounded to one pass. It changed reusable matching logic and tests; it did not hand-edit output rows or alter the independent labels.",
        234, 10, INK,
    )
    paragraph(
        c,
        "Boundary: this is entity-resolution evidence for human catalog review. It is not a medical determination, public alert, current recall-status service or proof of source-wide coverage.",
        116, 8,
    )
    c.showPage()

    header(c, 3, "Change the evidence. Watch the decision change.", "Reproduce the result, inspect provenance and export the executed run.")
    metric(c, 38, 610, "20/20", "independent labels reproduced")
    metric(c, 178, 610, "21", "automated tests passed")
    metric(c, 318, 610, "13/1/6", "match / no match / review")
    metric(c, 458, 610, "1", "recorded source request")
    paragraph(
        c,
        "<b>Contrasting case:</b> change CAT-005 from 100 mcg with no NDC or lot to 75 mcg plus NDC 55154-3560 and lot N02172A. "
        "The queue changes from 6 match / 1 review / 1 no match to 7 / 0 / 1, and CAT-005 becomes one explainable match.",
        594, 10, INK,
    )
    draw_crop(c, "clarified.png", (390, 0, 1310, 480), 515, 440, x=86)
    paragraph(
        c,
        "<b>Try it locally in about one minute</b><br/>"
        "1. In the project folder, run <font name='Courier'>python -B src/demo_server.py</font>.<br/>"
        "2. Open the local link below and click Run the matcher.<br/>"
        "3. Click Add decisive evidence, rerun, and compare the reasons and input hash.<br/>"
        "4. Download JSON/CSV and click Run automated checks.",
        266, 9,
    )
    paragraph(c, f'<link href="{LOCAL_DEMO}" color="#0B7963"><u><b>Local working demo: 127.0.0.1:8766</b></u></link>', 154, 11, INK)
    paragraph(c, f'<link href="{REPO}" color="#0B7963"><u>Repository, data, evidence and launch instructions</u></link>', 128, 9)
    paragraph(
        c,
        "20 synthetic benchmark rows reproduced 20 independently declared labels: 13 match, 1 no match and 6 review-needed. "
        "All 21 automated tests passed. A separate non-builder validation and public signed-out check are required before release.",
        104, 8,
    )
    c.save()
    print(OUTPUT)


if __name__ == "__main__":
    main()
