"""Stateless web adapter for the WS-004 reconciliation workbench."""

from __future__ import annotations

import sys
from pathlib import Path
from urllib.parse import urlsplit

from flask import Flask, jsonify, request


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
import demo_server as demo  # noqa: E402


app = Flask(__name__, static_folder=None)
app.config["MAX_CONTENT_LENGTH"] = 4096


@app.after_request
def security_headers(response):
    response.headers["Cache-Control"] = "no-store"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self'; style-src 'self'; "
        "connect-src 'self'; img-src 'self' data:; frame-ancestors 'none'; "
        "base-uri 'none'; form-action 'self'"
    )
    return response


@app.before_request
def same_origin_guard():
    if request.method != "POST":
        return None
    origin = request.headers.get("Origin")
    cross_site = request.headers.get("Sec-Fetch-Site") == "cross-site"
    origin_parts = urlsplit(origin) if origin else None
    origin_mismatch = bool(
        origin_parts
        and (origin_parts.scheme != request.scheme or origin_parts.netloc != request.host)
    )
    if cross_site or origin_mismatch:
        return jsonify(error="Use the workbench from its own page."), 403
    if not request.is_json:
        return jsonify(error="Send a small JSON request."), 400
    return None


@app.errorhandler(413)
def too_large(_error):
    return jsonify(error="Request exceeds the 4 KB limit."), 413


@app.get("/")
def index():
    return (ROOT / "demo" / "index.html").read_text(encoding="utf-8")


@app.get("/app.js")
def script():
    return app.response_class(
        (ROOT / "demo" / "app.js").read_text(encoding="utf-8"),
        mimetype="application/javascript",
    )


@app.get("/style.css")
def style():
    return app.response_class(
        (ROOT / "demo" / "style.css").read_text(encoding="utf-8"),
        mimetype="text/css",
    )


@app.get("/api/config")
def config():
    return jsonify(
        cases=demo.available_cases(),
        defaultSummary={"RECONCILED": 2, "MISMATCH": 1, "REVIEW_REQUIRED": 3},
        factorSetId="UK-GHG-2025-V1-FINAL",
        reviewerCaseId="CASE-02-CONTROLLED-MWH-RECONCILED",
        boundary=(
            "Three minimized recorded filing sources plus two controlled scenarios. "
            "Arithmetic reproducibility only; not audit assurance or compliance."
        ),
    )


@app.get("/api/code")
def code():
    return jsonify(file="src/reconcile.py", excerpt=demo.code_excerpt())


@app.post("/api/run")
def run():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="Request body must be a JSON object."), 400
    unknown = sorted(set(data) - {"caseId", "activityUnit"})
    if unknown:
        return jsonify(error=f"Unknown request fields: {', '.join(unknown)}."), 400

    case_id = data.get("caseId")
    activity_unit = data.get("activityUnit")
    if case_id is not None and not isinstance(case_id, str):
        return jsonify(error="caseId must be a string or null."), 400
    if activity_unit is not None and not isinstance(activity_unit, str):
        return jsonify(error="activityUnit must be a string or null."), 400

    try:
        return jsonify(demo.run_demo(case_id=case_id, activity_unit=activity_unit))
    except (ValueError, TypeError) as error:
        return jsonify(error=str(error)), 400
    except Exception as error:  # pragma: no cover - last-resort safe adapter boundary
        return jsonify(error=f"Engine error: {type(error).__name__}."), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
