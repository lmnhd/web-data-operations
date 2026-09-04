"""Build the three-page work sample from actual Proof Lab browser captures."""
from pathlib import Path
import inspect
import json
import sys
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'projects/WS-001-qualified-tender-change-intelligence'
CAPTURES = PROJECT / 'evidence/proof-lab'
OUTPUT = ROOT / 'output/pdf/Government-Contract-Change-Monitor.pdf'
sys.path.insert(0, str(PROJECT / 'src'))
from tender_pipeline import diff_releases

INK = HexColor('#102A43')
TEAL = HexColor('#007C78')
MUTED = HexColor('#52667A')
REPO = 'https://github.com/lmnhd/web-data-operations/tree/iteration/ws-001-qualified-tender-change-intelligence'


def text(c, words, y, size=10, color=MUTED, x=38, width=536):
    p = Paragraph(words, ParagraphStyle('p', fontName='Helvetica', fontSize=size,
                  leading=size * 1.35, textColor=color))
    _, height = p.wrap(width, 800)
    p.drawOn(c, x, y-height)
    return y-height


def header(c, number, title, subtitle):
    c.setFillColor(INK)
    c.rect(0, 690, 612, 102, fill=1, stroke=0)
    text(c, 'GOVERNMENT CONTRACT CHANGE MONITOR / WORKING DEMO', 766, 8, HexColor('#8EE3D8'))
    text(c, '<b>'+title+'</b>', 744, 23, white)
    text(c, subtitle, 711, 9, white)
    text(c, 'WS-001 / '+str(number)+' of 3', 24, 8, x=483, width=105)


def screenshot(c, filename, top, max_height, width=536, x=38):
    path = CAPTURES / filename
    with Image.open(path) as im:
        w, h = im.size
    scale = min(width/w, max_height/h)
    c.drawImage(str(path), x, top-h*scale, width=w*scale, height=h*scale)
    return top-h*scale


def main():
    # Crop only: preserve the actual browser pixels and retain full originals.
    for case in ('noise', 'cancellation', 'sandbox-act', 'sandbox-ignore'):
        bounds = json.loads((CAPTURES / (case+'-crop.json')).read_text())
        with Image.open(CAPTURES / (case+'-full.png')) as original:
            x, y = round(bounds['x']), round(bounds['y'])
            crop = original.crop((x, y, x+round(bounds['width']), y+round(bounds['height'])))
            name = case+'-result.png' if case in ('noise', 'cancellation') else case+'.png'
            crop.save(CAPTURES / name)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=LETTER)
    c.setTitle('Government Contract Change Monitor - See it run')
    c.setAuthor('lmnhd')
    header(c, 1, 'Six update labels. Zero tracked changes.', 'The problem: an update label is not evidence that a useful detail changed.')
    y = text(c, '<b>My fix:</b> compare the actual values in consecutive versions, not the source label. '
             'Below is a real browser run on a saved, sanitized government record. All six pairs were ignored because none of the six tracked fields changed.', 674)
    screenshot(c, 'noise-result.png', y-12, 448)
    text(c, '<b>The actual comparison loop</b> - extracted from the Python module used by the Run button:', 163, 9, INK)
    c.setFillColor(INK)
    c.setFont('Courier', 8)
    for n, line in enumerate(inspect.getsource(diff_releases).splitlines()[1:]):
        c.drawString(44, 135-n*10, line)
    text(c, 'Boundary: zero changes means zero differences in the declared fields, not identical documents. '
             'This selected example does not establish the rate of unnecessary updates across the source.', 50, 8)
    c.showPage()
    header(c, 2, 'Missing information is not a safe answer.', 'The second problem: a real change can leave too little evidence to qualify the opportunity.')
    y = text(c, '<b>My fix:</b> separate change detection from qualification. This cancellation has five tracked '
             'differences, but important qualification values are not supplied. The system sends it to <b>Review</b>, not a guessed approval.', 674)
    screenshot(c, 'cancellation-result.png', y-12, 470)
    text(c, '<b>What to inspect in the running demo</b><br/>'
             'Orange rows show the exact before/after values. The source trail exposes the release IDs, '
             'capture time, source URL and saved-input hash. JSON and CSV downloads preserve the result of that run.', 128, 10)
    text(c, 'Two selected historical records from Find a Tender, captured 2026-09-03; Open Government Licence v3.0. '
             'A hash identifies the saved input; it does not independently authenticate the government source. '
             'Missing in a version does not prove a fact was removed from the original contract.', 61, 8)
    c.showPage()
    header(c, 3, 'Do not take the screenshots on trust.', 'Run the same engine. Change a rule. Download the result. Run the checks.')
    text(c, '<b>Try to change the outcome.</b> The deliberately invented example is worth 400,000 GBP. '
             'Its deadline extension stays the same; only the maximum-value rule changes. '
             'These are actual screenshots of two server executions, not designed result cards.', 674)
    text(c, '<b>Maximum 5,000,000 GBP: ACT</b>', 608, 10, TEAL, width=260)
    text(c, '<b>Maximum 300,000 GBP: IGNORE</b>', 608, 10, TEAL, x=314, width=260)
    screenshot(c, 'sandbox-act.png', 582, 290, width=260)
    screenshot(c, 'sandbox-ignore.png', 582, 290, width=260, x=314)
    text(c, '<b>Reproduce it in about a minute</b><br/>'
             '1. Get the iteration branch from the repository linked below.<br/>'
             '2. From the repository root, run the command below (Python 3.10+).<br/>'
             '3. Open http://127.0.0.1:8765 and choose an example. Click Run.<br/>'
             '4. Change a rule and rerun. Download JSON/CSV; compare input hashes.<br/>'
             '5. Click Run automated checks to execute the 17-test suite yourself.', 283, 10)
    c.setFillColor(INK)
    c.setFont('Courier', 8)
    c.drawString(38, 168, 'python projects/WS-001-qualified-tender-change-intelligence/')
    c.drawString(38, 156, '       src/demo_server.py')
    text(c, 'Command above wraps for readability: join it into one line without spaces around the slash.', 143, 8)
    text(c, '<b>17 tests passed during browser verification.</b> Tests cover real execution, repeatability, '
             'changed rules, missing data, exports and local access boundaries. Implementation and browser checks '
             'were performed by the same agent; this is not an independent audit.', 119, 9)
    text(c, '<link href="'+REPO+'" color="#007C78"><u>Open code, data, tests and launch instructions on GitHub</u></link>', 69, 9)
    text(c, 'Local replay, not a hosted live feed. No scheduling, source-wide coverage, customer savings or production readiness is claimed. '
             'The PDF is a tour; the executable project is the evidence.', 48, 8)
    c.save()
    print(OUTPUT)


if __name__ == '__main__':
    main()
