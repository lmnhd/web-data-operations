"""Tests for WS-003 Flask Web Adapter (`app.py`)."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from app import app


class TestFlaskAdapter(unittest.TestCase):

    def setUp(self) -> None:
        self.client = app.test_client()

    def test_get_index(self) -> None:
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Municipal 311 SLA Operations Desk", response.data)

    def test_get_config(self) -> None:
        response = self.client.get("/api/config")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("default_rules", data)
        self.assertIn("boundary", data)

    def test_post_run_success(self) -> None:
        response = self.client.post(
            "/api/run",
            json={"rules": {"Pothole Repair": 3}},
            headers={"Origin": "http://localhost"},
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["total_records"], 15)
        self.assertEqual(data["fixture_kind"], "synthetic_sla_scenario")
        self.assertIn("ward_analytics", data)
        self.assertIn("evaluated_records", data)


if __name__ == "__main__":
    unittest.main()
