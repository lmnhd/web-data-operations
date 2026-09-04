import http.client
import json
import sys
import threading
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "src"))

import demo_server  # noqa: E402


class DemoEngineTests(unittest.TestCase):
    def test_default_row_routes_to_review(self):
        row = demo_server.default_row()
        result = demo_server.run_demo({key: row[key] for key in demo_server.EDITABLE_FIELDS})
        self.assertEqual("review_needed", result["target"]["classification"])
        self.assertIn("strength_conflict", result["target"]["reasons"])

    def test_clarified_row_becomes_explainable_match(self):
        result = demo_server.run_demo({
            "product_name": "Levothyroxine Sodium 75 mcg",
            "manufacturer": "Major Pharmaceuticals",
            "upc": "0055154356305",
            "ndc": "55154-3560",
            "lot_code": "N02172A",
        })
        self.assertEqual("match", result["target"]["classification"])
        self.assertEqual("D-0709-2026", result["target"]["matched_recall_number"])
        self.assertIn("exact_lot_code", result["target"]["reasons"])

    def test_changed_input_changes_fingerprint(self):
        base = demo_server.default_row()
        first = demo_server.run_demo({key: base[key] for key in demo_server.EDITABLE_FIELDS})
        base["lot_code"] = "N02172A"
        second = demo_server.run_demo({key: base[key] for key in demo_server.EDITABLE_FIELDS})
        self.assertNotEqual(first["input_sha256"], second["input_sha256"])

    def test_rejects_unexpected_or_oversized_fields(self):
        row = {key: "x" for key in demo_server.EDITABLE_FIELDS}
        row["path"] = "../../outside.json"
        with self.assertRaises(ValueError):
            demo_server.validate_override(row)
        row.pop("path")
        row["product_name"] = "x" * 161
        with self.assertRaises(ValueError):
            demo_server.validate_override(row)


class DemoHttpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = demo_server.ThreadingHTTPServer(("127.0.0.1", 0), demo_server.Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def request(self, method, path, body=None, headers=None):
        connection = http.client.HTTPConnection("127.0.0.1", self.server.server_port)
        request_headers = {"Host": f"127.0.0.1:{self.server.server_port}"}
        request_headers.update(headers or {})
        payload = None
        if body is not None:
            payload = json.dumps(body)
            request_headers["Content-Type"] = "application/json"
        connection.request(method, path, payload, request_headers)
        response = connection.getresponse()
        data = response.read()
        response_headers = dict(response.getheaders())
        connection.close()
        return response.status, response_headers, data

    def test_page_has_security_headers(self):
        status, headers, body = self.request("GET", "/")
        self.assertEqual(200, status)
        self.assertIn("default-src 'self'", headers["Content-Security-Policy"])
        self.assertIn(b"Product Recall Match Desk", body)

    def test_foreign_origin_is_rejected(self):
        status, _, _ = self.request("GET", "/api/config", headers={"Origin": "https://example.com"})
        self.assertEqual(403, status)

    def test_run_and_export_are_real(self):
        row = demo_server.default_row()
        editable = {key: row[key] for key in demo_server.EDITABLE_FIELDS}
        status, _, body = self.request("POST", "/api/run", {"catalog_row": editable})
        self.assertEqual(200, status)
        run = json.loads(body)
        self.assertEqual("review_needed", run["target"]["classification"])
        status, headers, exported = self.request("GET", f"/api/export/{run['run_id']}.csv")
        self.assertEqual(200, status)
        self.assertIn("attachment", headers["Content-Disposition"])
        self.assertIn(b"CAT-005,review_needed", exported)


if __name__ == "__main__":
    unittest.main()
