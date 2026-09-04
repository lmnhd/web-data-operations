import json
import sys
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
import app as public_app  # noqa: E402


class PublicAdapterTests(unittest.TestCase):
    def setUp(self):
        public_app.app.config["TESTING"] = True
        self.client = public_app.app.test_client()
        public_app.LAST_CHECK = 0.0

    def test_page_and_security_headers(self):
        response = self.client.get("/")
        self.assertEqual(200, response.status_code)
        self.assertIn(b"Product Recall Match Desk", response.data)
        self.assertIn("default-src 'self'", response.headers["Content-Security-Policy"])

    def test_cross_site_post_is_rejected(self):
        response = self.client.post(
            "/api/run", json={"catalog_row": {}},
            headers={"Origin": "https://example.com", "Host": "localhost"},
        )
        self.assertEqual(403, response.status_code)

    def test_real_run_and_export(self):
        row = public_app.demo.default_row()
        editable = {key: row[key] for key in public_app.demo.EDITABLE_FIELDS}
        response = self.client.post("/api/run", json={"catalog_row": editable})
        self.assertEqual(200, response.status_code)
        result = response.get_json()
        self.assertEqual("review_needed", result["target"]["classification"])
        exported = self.client.get(f"/api/export/{result['run_id']}.csv")
        self.assertEqual(200, exported.status_code)
        self.assertIn(b"CAT-005,review_needed", exported.data)

    def test_clarified_run_matches_expected_recall(self):
        config = self.client.get("/api/config").get_json()
        response = self.client.post("/api/run", json={"catalog_row": config["clarified"]})
        result = response.get_json()
        self.assertEqual("match", result["target"]["classification"])
        self.assertEqual("D-0709-2026", result["target"]["matched_recall_number"])

    def test_hosted_verification_executes_core_suite(self):
        response = self.client.post("/api/verify", json={})
        self.assertEqual(200, response.status_code)
        result = response.get_json()
        self.assertTrue(result["passed"])
        self.assertEqual(13, result["tests_run"])


if __name__ == "__main__":
    unittest.main()
