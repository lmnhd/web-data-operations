"""Stateless hosted adapter for the Product Recall Match Desk."""
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
sys.path.insert(0, str(ROOT / "src"))
import demo_server as demo  # noqa: E402


app = Flask(__name__, static_folder=None)
app.config["MAX_CONTENT_LENGTH"] = 8192
CHECK_LOCK = threading.Lock()
LAST_CHECK = 0.0


@app.after_request
def security_headers(response):
    response.headers["Cache-Control"] = "no-store"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self'; style-src 'self'; "
        "connect-src 'self'; img-src 'self'; frame-ancestors 'none'; "
        "base-uri 'none'; form-action 'self'"
    )
    return response


@app.before_request
def same_origin_guard():
    if request.method == "POST":
        origin = request.headers.get("Origin")
        cross_site = request.headers.get("Sec-Fetch-Site") == "cross-site"
        if cross_site or (origin and urlsplit(origin).netloc != request.host):
            return jsonify(error="Use the demo from its own page."), 403
        if not request.is_json:
            return jsonify(error="Send a small JSON request."), 400


@app.errorhandler(413)
def too_large(_error):
    return jsonify(error="Request exceeds the 8 KB limit."), 413


@app.get("/")
def index():
    return send_file(ROOT / "demo/index.html")


@app.get("/app.js")
def script():
    return send_file(ROOT / "demo/app.js")


@app.get("/style.css")
def style():
    return send_file(ROOT / "demo/style.css")


@app.get("/api/config")
def config():
    return jsonify(
        default=demo.default_row(),
        clarified={
            "product_name": "Levothyroxine Sodium 75 mcg",
            "manufacturer": "Major Pharmaceuticals",
            "upc": "0055154356305",
            "ndc": "55154-3560",
            "lot_code": "N02172A",
        },
        boundary="Recorded openFDA fixture. Not medical advice, a public alert, or current recall status.",
    )


@app.get("/api/code")
def code():
    return jsonify(file="src/catalog_matcher.py", excerpt=demo.inspect.getsource(demo.matcher.compare_pair))


@app.post("/api/run")
def run():
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or set(data) != {"catalog_row"}:
        return jsonify(error="Expected a catalog_row object."), 400
    try:
        result = demo.run_demo(data["catalog_row"])
    except (ValueError, TypeError) as error:
        return jsonify(error=str(error)), 400
    with demo.RUN_LOCK:
        demo.RUNS[result["run_id"]] = result
        while len(demo.RUNS) > 32:
            demo.RUNS.popitem(last=False)
    return jsonify(result)


@app.get("/api/export/<run_id>.<kind>")
def export(run_id, kind):
    if kind not in {"json", "csv"} or not demo.re.fullmatch(r"[a-f0-9-]{36}", run_id):
        return jsonify(error="Export not found."), 404
    with demo.RUN_LOCK:
        result = demo.RUNS.get(run_id)
    if result is None:
        return jsonify(error="Run not found."), 404
    if kind == "json":
        payload = io.BytesIO(json.dumps(result, indent=2).encode("utf-8"))
        mimetype = "application/json"
    else:
        payload = io.BytesIO(result["csv"].encode("utf-8"))
        mimetype = "text/csv"
    return send_file(payload, mimetype=mimetype, as_attachment=True, download_name=f"recall-match-{run_id[:8]}.{kind}")


@app.post("/api/verify")
def verify():
    global LAST_CHECK
    if not CHECK_LOCK.acquire(blocking=False):
        return jsonify(error="Checks are already running."), 429
    try:
        if time.monotonic() - LAST_CHECK < 10:
            return jsonify(error="Please wait 10 seconds before running checks again."), 429
        LAST_CHECK = time.monotonic()
        sys.path.insert(0, str(ROOT / "tests"))
        import test_demo_server
        import test_matcher
        suite = unittest.TestSuite([
            unittest.defaultTestLoader.loadTestsFromModule(test_matcher),
            unittest.defaultTestLoader.loadTestsFromTestCase(test_demo_server.DemoEngineTests),
        ])
        output = io.StringIO()
        result = unittest.TextTestRunner(stream=output, verbosity=2).run(suite)
        return jsonify(
            passed=result.wasSuccessful(),
            exit_code=0 if result.wasSuccessful() else 1,
            output="Hosted checks: matcher and bounded demo engine. HTTP adapter tests run in CI.\n" + output.getvalue(),
            executed_at=datetime.now(timezone.utc).isoformat(),
            tests_run=result.testsRun,
        )
    finally:
        CHECK_LOCK.release()
