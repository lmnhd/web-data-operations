"""Stateless hosted adapter for the Municipal 311 SLA Operations Desk (WS-003)."""
import sys
import threading
from pathlib import Path
from urllib.parse import urlsplit

from flask import Flask, jsonify, request, send_file

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
import demo_server as demo  # noqa: E402

app = Flask(__name__, static_folder=None)
app.config["MAX_CONTENT_LENGTH"] = 8192


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
    return (ROOT / "demo/index.html").read_text(encoding="utf-8")


@app.get("/app.js")
def script():
    return app.response_class((ROOT / "demo/app.js").read_text(encoding="utf-8"), mimetype="application/javascript")


@app.get("/style.css")
def style():
    return app.response_class((ROOT / "demo/style.css").read_text(encoding="utf-8"), mimetype="text/css")


@app.get("/api/config")
def config():
    return jsonify(
        default_rules=demo.default_rules(),
        reference_now=demo.default_reference_now(),
        boundary=(
            "Synthetic SLA scenario inspired by the City of Toronto 311 public schema. "
            "The public export does not provide target or closure timestamps."
        ),
    )


@app.get("/api/code")
def code():
    return jsonify(file="src/sla_engine.py", excerpt=demo.inspect.getsource(demo.sla_engine.evaluate_record))


@app.post("/api/run")
def run():
    data = request.get_json(silent=True) or {}
    rules_override = data.get("rules")
    try:
        result = demo.run_demo(rules_override=rules_override)
    except (ValueError, TypeError) as error:
        return jsonify(error=str(error)), 400
    except Exception as error:
        return jsonify(error=f"Engine error: {type(error).__name__}: {error}"), 500
    with demo.RUN_LOCK:
        demo.RUNS[result["run_id"]] = result
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
