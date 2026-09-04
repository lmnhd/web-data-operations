import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import app as hosted


class HostedAppTests(unittest.TestCase):
    def setUp(self):
        self.client = hosted.app.test_client()
        self.profile = json.loads((ROOT / 'examples/qualification-profile.json').read_text())

    def test_all_public_assets_and_code_are_available(self):
        for route in ('/', '/app.js', '/style.css', '/api/cases', '/api/code', '/api/input?case=noise'):
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200, route)
            self.assertIn("frame-ancestors 'none'", response.headers['Content-Security-Policy'])
            response.close()

    def test_execution_uses_actual_engine_and_is_stateless(self):
        with patch.object(hosted.demo.pipeline, 'run_pipeline', wraps=hosted.demo.pipeline.run_pipeline) as engine:
            first = self.client.post('/api/run', json={'case_id':'noise','profile':self.profile}).get_json()
            second = self.client.post('/api/run', json={'case_id':'noise','profile':self.profile}).get_json()
        self.assertEqual(engine.call_count, 2)
        self.assertNotEqual(first['run_id'], second['run_id'])
        self.assertEqual(first['result'], second['result'])
        self.assertEqual(first['result']['summary']['material_change_comparisons'], 0)
        self.assertIn('csv', first)

    def test_rules_change_the_synthetic_result(self):
        body = {'case_id':'sandbox','profile':self.profile}
        accepted = self.client.post('/api/run', json=body).get_json()
        self.profile['maximumValue'] = 300000
        rejected = self.client.post('/api/run', json=body).get_json()
        self.assertEqual(accepted['result']['summary']['accepted'], 1)
        self.assertEqual(rejected['result']['summary']['accepted'], 0)
        self.assertEqual(accepted['input_sha256'], rejected['input_sha256'])

    def test_request_boundaries(self):
        self.assertEqual(self.client.post('/api/run', json={}, headers={'Origin':'https://evil.example'}).status_code, 403)
        self.assertEqual(self.client.post('/api/run', json={'case_id':[],'profile':{}}).status_code, 400)
        self.assertEqual(self.client.post('/api/run', json={'case_id':'../../.env','profile':self.profile}).status_code, 400)
        self.assertEqual(self.client.post('/api/run', data='x'*9000, content_type='application/json').status_code, 413)
        self.assertEqual(self.client.get('/.env').status_code, 404)

    def test_hosted_checks_execute_core_tests_without_subprocess(self):
        hosted.LAST_CHECK = 0
        with patch.object(hosted.demo.subprocess, 'run', side_effect=AssertionError('No public subprocess')):
            response = self.client.post('/api/verify', json={})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()['passed'])
        self.assertEqual(response.get_json()['tests_run'], 14)
        self.assertEqual(self.client.post('/api/verify', json={}).status_code, 429)


if __name__ == '__main__':
    unittest.main()
