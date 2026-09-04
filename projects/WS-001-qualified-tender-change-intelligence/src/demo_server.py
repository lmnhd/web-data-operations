"""Local, read-only Proof Lab. Every replay calls the production pipeline function."""
from __future__ import annotations

import argparse
import csv
import hashlib
import inspect
import io
import json
import math
import re
import subprocess
import sys
import threading
import time
import uuid
from collections import OrderedDict
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import tender_pipeline as pipeline

PROJECT = Path(__file__).resolve().parents[1]
CASES = {
    "noise": {"title": "Six updates. Nothing changed in our tracked fields.", "kind": "Captured public data", "file": "evidence/live/sanitized-record.json", "story": "The source marked six later versions as updates. Checking the actual fields keeps those labels from becoming six unnecessary alerts."},
    "cancellation": {"title": "A cancellation with missing details.", "kind": "Captured public data", "file": "evidence/live/sanitized-record-06bb7d.json", "story": "The status changed, but the later version does not supply a deadline or value. Keep the change visible and ask for review rather than guessing."},
    "sandbox": {"title": "Change a rule. Watch the decision change.", "kind": "Synthetic test scenario", "file": "tests/fixtures/release-package.json", "story": "This invented opportunity is worth 400,000 GBP. Lower the maximum to 300,000 and rerun: the same deadline change no longer fits the business rules."},
}
LABELS = dict(zip(pipeline.MATERIAL_FIELDS, ["Status", "Closing date", "Contract value", "Currency", "Contract category", "Work packages"]))
VERIFY_LOCK = threading.Lock()
RUN_LOCK = threading.Lock()
RUNS = OrderedDict()


def load_case(case_id):
    if case_id not in CASES:
        raise ValueError("Choose a known example.")
    raw = (PROJECT / CASES[case_id]["file"]).read_bytes()
    payload = json.loads(raw)
    if case_id == "sandbox":
        payload = {"releases": [r for r in pipeline.extract_releases(payload) if r["ocid"] == "ocds-demo-qualified-change"]}
    capture = payload.get("capture", {})
    return payload, capture.get("sourceUrl", "fixture://synthetic-qualified-change"), capture.get("retrievedAt", "synthetic-no-retrieval"), hashlib.sha256(raw).hexdigest()


def validate_profile(profile):
    if not isinstance(profile, dict) or set(profile) - {"minimumValue", "maximumValue", "allowedClassificationPrefixes", "deadlineOnOrAfter"}:
        raise ValueError("Unsupported rule profile.")
    for key in ("minimumValue", "maximumValue"):
        value = profile.get(key)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 1e12:
            raise ValueError("Values must be finite numbers between 0 and 1 trillion.")
    if profile["minimumValue"] > profile["maximumValue"]:
        raise ValueError("Minimum value cannot exceed maximum value.")
    prefixes = profile.get("allowedClassificationPrefixes")
    if not isinstance(prefixes, list) or not 1 <= len(prefixes) <= 20 or any(not isinstance(p, str) or not re.fullmatch(r"[0-9]{1,8}", p) for p in prefixes):
        raise ValueError("Supply 1 to 20 numeric category prefixes.")
    date = profile.get("deadlineOnOrAfter")
    if not isinstance(date, str) or len(date) > 40:
        raise ValueError("Supply a closing-date threshold with timezone.")
    try:
        parsed = datetime.fromisoformat(date.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError("Invalid closing-date threshold.") from error
    if parsed.tzinfo is None:
        raise ValueError("Closing-date threshold must include a timezone.")
    return profile


def run_case(case_id, profile):
    profile = validate_profile(profile)
    payload, source, captured, input_hash = load_case(case_id)
    started = time.perf_counter()
    result = pipeline.run_pipeline(payload, profile, source, captured)
    snapshots = [pipeline.normalize_release(r, source, captured) for r in pipeline.extract_releases(payload)]
    lookup = {r["release_id"]: r for r in snapshots}
    comparisons = []
    for queue in result["queues"].values():
        for row in queue:
            before, after = lookup[row["previous_release_id"]], lookup[row["current_release_id"]]
            changed = {change["field"] for change in row["changes"]}
            comparisons.append({**row, "date": after["release_date"], "fields": [{"path": field, "label": LABELS[field], "before": pipeline._get(before, field), "after": pipeline._get(after, field), "changed": field in changed} for field in pipeline.MATERIAL_FIELDS]})
    comparisons.sort(key=lambda row: (row["date"], row["current_release_id"]))
    csv_buffer = io.StringIO(newline="")
    writer = csv.writer(csv_buffer)
    writer.writerow(["process_id", "previous_version", "current_version", "decision", "reason_codes", "changed_fields", "source_url", "captured_at"])
    for row in comparisons:
        writer.writerow([row["ocid"], row["previous_release_id"], row["current_release_id"], row["decision"], "|".join(row["reason_codes"]), "|".join(c["field"] for c in row["changes"]), source, captured])
    return {"run_id": str(uuid.uuid4()), "executed_at": datetime.now(timezone.utc).isoformat(), "elapsed_ms": round((time.perf_counter()-started)*1000, 3), "engine": "tender_pipeline.run_pipeline (Python)", "case_id": case_id, "case": {k:v for k,v in CASES[case_id].items() if k != "file"}, "profile": profile, "source_url": source, "captured_at": captured, "input_sha256": input_hash, "engine_sha256": hashlib.sha256(Path(pipeline.__file__).read_bytes()).hexdigest(), "result": result, "comparisons": comparisons, "snapshots": snapshots, "csv": csv_buffer.getvalue()}


class Handler(BaseHTTPRequestHandler):
    def reply(self, status, body, content_type="application/json; charset=utf-8", filename=None):
        if not isinstance(body, bytes):
            body = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        if filename:
            self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self'; frame-ancestors 'none'; base-uri 'none'")
        self.end_headers()
        self.wfile.write(body)

    def allowed(self):
        host = self.headers.get("Host", "")
        valid = {f"127.0.0.1:{self.server.server_port}", f"localhost:{self.server.server_port}"}
        origin = self.headers.get("Origin")
        if host not in valid or (origin and origin != f"http://{host}"):
            self.reply(403, {"error": "Local same-origin requests only."})
            return False
        return True

    def do_GET(self):
        if not self.allowed():
            return
        parsed = urlsplit(self.path)
        export = re.fullmatch(r"/api/export/([a-f0-9-]{36})\.(json|csv)", parsed.path)
        if export:
            run_id, kind = export.groups()
            with RUN_LOCK:
                run = RUNS.get(run_id)
            if run is None:
                return self.reply(404, {"error": "Run expired. Run the comparison again."})
            content = json.dumps(run, indent=2).encode() if kind == "json" else run["csv"].encode()
            return self.reply(200, content, "application/json" if kind == "json" else "text/csv", f"proof-{run['case_id']}-{run_id[:8]}.{kind}")
        assets = {"/": ("index.html", "text/html; charset=utf-8"), "/app.js": ("app.js", "text/javascript; charset=utf-8"), "/style.css": ("style.css", "text/css; charset=utf-8")}
        if parsed.path in assets:
            name, mime = assets[parsed.path]
            return self.reply(200, (PROJECT / "demo" / name).read_bytes(), mime)
        if parsed.path == "/api/cases":
            return self.reply(200, {"cases": [{"id": key, **{k:v for k,v in value.items() if k != "file"}} for key,value in CASES.items()], "profile": json.loads((PROJECT / "examples/qualification-profile.json").read_text())})
        if parsed.path == "/api/code":
            return self.reply(200, {"diff": inspect.getsource(pipeline.diff_releases), "qualification": inspect.getsource(pipeline.qualify), "file": "src/tender_pipeline.py"})
        if parsed.path == "/api/input":
            try:
                payload, _, _, _ = load_case(parse_qs(parsed.query).get("case", [""])[0])
                return self.reply(200, payload)
            except ValueError as error:
                return self.reply(400, {"error": str(error)})
        return self.reply(404, {"error": "Not found."})

    def do_POST(self):
        if not self.allowed():
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 8192 or self.headers.get_content_type() != "application/json":
                return self.reply(400, {"error": "Send a small JSON request."})
            data = json.loads(self.rfile.read(length))
            if not isinstance(data, dict):
                raise ValueError("Expected a JSON object.")
            if self.path == "/api/run":
                run = run_case(data.get("case_id"), data.get("profile"))
                with RUN_LOCK:
                    RUNS[run["run_id"]] = run
                    while len(RUNS) > 64:
                        RUNS.popitem(last=False)
                return self.reply(200, run)
            if self.path == "/api/verify":
                if not VERIFY_LOCK.acquire(blocking=False):
                    return self.reply(409, {"error": "Checks already running."})
                try:
                    completed = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", str(PROJECT / "tests"), "-v"], capture_output=True, text=True, timeout=20, cwd=PROJECT)
                    return self.reply(200, {"passed": completed.returncode == 0, "exit_code": completed.returncode, "output": completed.stdout + completed.stderr, "executed_at": datetime.now(timezone.utc).isoformat()})
                finally:
                    VERIFY_LOCK.release()
            return self.reply(404, {"error": "Not found."})
        except (ValueError, TypeError) as error:
            return self.reply(400, {"error": str(error)})
        except subprocess.TimeoutExpired:
            return self.reply(504, {"error": "Checks exceeded 20 seconds."})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"Proof Lab: http://127.0.0.1:{server.server_port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
