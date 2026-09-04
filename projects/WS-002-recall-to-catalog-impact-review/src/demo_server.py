"""Local reviewer workbench that executes the WS-002 Python matcher."""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import inspect
import io
import json
import re
import subprocess
import sys
import threading
import time
import uuid
from collections import Counter, OrderedDict
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

import catalog_matcher as matcher


PROJECT = Path(__file__).resolve().parents[1]
FIXTURES = PROJECT / "tests" / "fixtures"
RUNS: OrderedDict[str, dict] = OrderedDict()
RUN_LOCK = threading.Lock()
VERIFY_LOCK = threading.Lock()
EDITABLE_FIELDS = {"product_name", "manufacturer", "upc", "ndc", "lot_code"}


def load_json(name: str):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def default_row() -> dict:
    return next(row for row in load_json("catalog.json") if row["catalog_id"] == "CAT-005")


def validate_override(value: object) -> dict[str, str]:
    if not isinstance(value, dict) or set(value) != EDITABLE_FIELDS:
        raise ValueError("Submit exactly the five editable catalog fields.")
    clean: dict[str, str] = {}
    for key, item in value.items():
        if not isinstance(item, str) or len(item) > 160:
            raise ValueError(f"Invalid {key} value.")
        if key == "product_name" and not item.strip():
            raise ValueError("Product name is required.")
        clean[key] = item.strip()
    return clean


def run_demo(override: dict[str, str]) -> dict:
    catalog = copy.deepcopy(load_json("catalog.json"))
    clean = validate_override(override)
    for row in catalog:
        if row["catalog_id"] == "CAT-005":
            row.update(clean)
    recalls = load_json("recalls.json")
    started = time.perf_counter()
    results = matcher.match_catalog(catalog, recalls["records"], recalls["provenance"])
    target = next(row for row in results if row["catalog_id"] == "CAT-005")
    counts = Counter(row["classification"] for row in results)
    catalog_bytes = json.dumps(catalog, sort_keys=True, separators=(",", ":")).encode()
    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(["catalog_id", "classification", "matched_recall_number", "candidates", "reasons"])
    for row in results:
        writer.writerow([
            row["catalog_id"], row["classification"], row["matched_recall_number"] or "",
            "|".join(row["candidate_recall_numbers"]), "|".join(row["reasons"]),
        ])
    return {
        "run_id": str(uuid.uuid4()),
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "elapsed_ms": round((time.perf_counter() - started) * 1000, 3),
        "engine": "catalog_matcher.match_catalog (Python)",
        "engine_sha256": hashlib.sha256(Path(matcher.__file__).read_bytes()).hexdigest(),
        "input_sha256": hashlib.sha256(catalog_bytes).hexdigest(),
        "source": recalls["provenance"],
        "edited_row": {"catalog_id": "CAT-005", **clean},
        "summary": {
            "catalog_rows": len(catalog),
            "match": counts["match"],
            "review_needed": counts["review_needed"],
            "no_match": counts["no_match"],
        },
        "target": target,
        "results": results,
        "csv": output.getvalue(),
    }


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):  # noqa: A003
        return

    def reply(self, status: int, body, content_type="application/json; charset=utf-8", filename=None):
        if not isinstance(body, bytes):
            body = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self'; frame-ancestors 'none'; base-uri 'none'")
        if filename:
            self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.end_headers()
        self.wfile.write(body)

    def allowed(self) -> bool:
        host = self.headers.get("Host", "")
        allowed_hosts = {f"127.0.0.1:{self.server.server_port}", f"localhost:{self.server.server_port}"}
        origin = self.headers.get("Origin")
        if host not in allowed_hosts or (origin and origin != f"http://{host}"):
            self.reply(403, {"error": "Local same-origin requests only."})
            return False
        return True

    def do_GET(self):
        if not self.allowed():
            return
        path = urlsplit(self.path).path
        assets = {
            "/": ("index.html", "text/html; charset=utf-8"),
            "/app.js": ("app.js", "text/javascript; charset=utf-8"),
            "/style.css": ("style.css", "text/css; charset=utf-8"),
        }
        if path in assets:
            name, content_type = assets[path]
            return self.reply(200, (PROJECT / "demo" / name).read_bytes(), content_type)
        export = re.fullmatch(r"/api/export/([a-f0-9-]{36})\.(json|csv)", path)
        if export:
            run_id, kind = export.groups()
            with RUN_LOCK:
                run = RUNS.get(run_id)
            if run is None:
                return self.reply(404, {"error": "Run not found."})
            content = json.dumps(run, indent=2).encode() if kind == "json" else run["csv"].encode()
            return self.reply(200, content, "application/json" if kind == "json" else "text/csv", f"recall-match-{run_id[:8]}.{kind}")
        if path == "/api/config":
            return self.reply(200, {
                "default": default_row(),
                "clarified": {
                    "product_name": "Levothyroxine Sodium 75 mcg",
                    "manufacturer": "Major Pharmaceuticals",
                    "upc": "0055154356305",
                    "ndc": "55154-3560",
                    "lot_code": "N02172A",
                },
                "boundary": "Recorded openFDA fixture. Not medical advice, a public alert, or current recall status.",
            })
        if path == "/api/code":
            return self.reply(200, {"file": "src/catalog_matcher.py", "excerpt": inspect.getsource(matcher.compare_pair)})
        return self.reply(404, {"error": "Not found."})

    def do_POST(self):
        if not self.allowed():
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 4096 or self.headers.get_content_type() != "application/json":
                return self.reply(400, {"error": "Send a small JSON request."})
            data = json.loads(self.rfile.read(length))
            if self.path == "/api/run":
                if not isinstance(data, dict) or set(data) != {"catalog_row"}:
                    raise ValueError("Expected a catalog_row object.")
                run = run_demo(data["catalog_row"])
                with RUN_LOCK:
                    RUNS[run["run_id"]] = run
                    while len(RUNS) > 32:
                        RUNS.popitem(last=False)
                return self.reply(200, run)
            if self.path == "/api/verify":
                if not VERIFY_LOCK.acquire(blocking=False):
                    return self.reply(409, {"error": "Checks are already running."})
                try:
                    completed = subprocess.run(
                        [sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-v"],
                        cwd=PROJECT, capture_output=True, text=True, timeout=30,
                    )
                    return self.reply(200, {
                        "passed": completed.returncode == 0,
                        "output": completed.stdout + completed.stderr,
                        "executed_at": datetime.now(timezone.utc).isoformat(),
                    })
                finally:
                    VERIFY_LOCK.release()
            return self.reply(404, {"error": "Not found."})
        except (ValueError, TypeError, json.JSONDecodeError) as error:
            return self.reply(400, {"error": str(error)})
        except subprocess.TimeoutExpired:
            return self.reply(504, {"error": "Checks exceeded 30 seconds."})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8766)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"Product Recall Match Desk: http://127.0.0.1:{server.server_port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
