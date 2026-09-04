"""Stateless public adapter. The comparison engine remains the local demo's Python engine."""
import io
import json
import sys
import threading
import time
import unittest
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

from flask import Flask, jsonify, request, send_file

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'src'))
import demo_server as demo

app = Flask(__name__, static_folder=None)
app.config['MAX_CONTENT_LENGTH'] = 8192
CHECK_LOCK = threading.Lock()
LAST_CHECK = 0.0


@app.after_request
def headers(response):
    response.headers['Cache-Control'] = 'no-store'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'"
    return response


@app.before_request
def guard():
    if request.method == 'POST':
        origin = request.headers.get('Origin')
        if request.headers.get('Sec-Fetch-Site') == 'cross-site' or (origin and urlsplit(origin).netloc != request.host):
            return jsonify(error='Use the demo from its own page.'), 403
        if not request.is_json:
            return jsonify(error='Send a small JSON request.'), 400


@app.errorhandler(413)
def too_large(error):
    return jsonify(error='Request exceeds the 8 KB limit.'), 413


@app.get('/')
def index():
    return send_file(ROOT / 'demo/index.html')


@app.get('/app.js')
def script():
    return send_file(ROOT / 'demo/app.js')


@app.get('/style.css')
def style():
    return send_file(ROOT / 'demo/style.css')


@app.get('/api/cases')
def cases():
    return jsonify(cases=[{'id': key, **{k:v for k,v in value.items() if k != 'file'}} for key,value in demo.CASES.items()],
                   profile=json.loads((ROOT / 'examples/qualification-profile.json').read_text()))


@app.get('/api/code')
def code():
    return jsonify(diff=demo.inspect.getsource(demo.pipeline.diff_releases),
                   qualification=demo.inspect.getsource(demo.pipeline.qualify), file='src/tender_pipeline.py')


@app.get('/api/input')
def source():
    try:
        payload, _, _, _ = demo.load_case(request.args.get('case', ''))
        return jsonify(payload)
    except ValueError as error:
        return jsonify(error=str(error)), 400


@app.post('/api/run')
def run():
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or set(data) != {'case_id', 'profile'} or not isinstance(data['case_id'], str):
        return jsonify(error='Choose an example and provide its rule profile.'), 400
    try:
        return jsonify(demo.run_case(data['case_id'], data['profile']))
    except (ValueError, TypeError) as error:
        return jsonify(error=str(error)), 400


@app.post('/api/verify')
def verify():
    # Only fixed, in-process core tests: no public shell/subprocess or socket tests.
    global LAST_CHECK
    if not CHECK_LOCK.acquire(blocking=False):
        return jsonify(error='Checks are already running.'), 429
    try:
        if time.monotonic() - LAST_CHECK < 10:
            return jsonify(error='Please wait 10 seconds before running checks again.'), 429
        LAST_CHECK = time.monotonic()
        sys.path.insert(0, str(ROOT / 'tests'))
        import test_pipeline
        import test_demo_server
        suite = unittest.TestSuite([
            unittest.defaultTestLoader.loadTestsFromModule(test_pipeline),
            unittest.defaultTestLoader.loadTestsFromTestCase(test_demo_server.ProofLabTests),
        ])
        output = io.StringIO()
        result = unittest.TextTestRunner(stream=output, verbosity=2).run(suite)
        return jsonify(passed=result.wasSuccessful(), exit_code=0 if result.wasSuccessful() else 1,
                       output='Hosted checks: core engine and replay tests. HTTP adapter tests run in CI.\n'+output.getvalue(),
                       executed_at=datetime.now(timezone.utc).isoformat(), tests_run=result.testsRun)
    finally:
        CHECK_LOCK.release()
