"""Verify the demo executes real pipeline logic, not saved result reports."""
import copy
import http.client
import json
import sys
import threading
import unittest
from pathlib import Path
from unittest.mock import patch
from http.server import ThreadingHTTPServer

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / 'src'))
import demo_server as demo


class ProofLabTests(unittest.TestCase):
    def setUp(self):
        self.profile = json.loads((PROJECT / 'examples/qualification-profile.json').read_text())

    def test_replay_calls_real_pipeline_each_time(self):
        with patch.object(demo.pipeline, 'run_pipeline', wraps=demo.pipeline.run_pipeline) as actual:
            first = demo.run_case('noise', self.profile)
            second = demo.run_case('noise', self.profile)
        self.assertEqual(actual.call_count, 2)
        self.assertNotEqual(first['run_id'], second['run_id'])
        self.assertEqual(first['result'], second['result'])

    def test_live_noise_has_six_unchanged_pairs(self):
        run = demo.run_case('noise', self.profile)
        self.assertEqual(6, len(run['comparisons']))
        self.assertTrue(all(not f['changed'] for row in run['comparisons'] for f in row['fields']))
        self.assertEqual(6, run['result']['summary']['rejected'])

    def test_live_cancellation_retains_missing_evidence(self):
        run = demo.run_case('cancellation', self.profile)
        row = run['comparisons'][0]
        self.assertEqual(5, sum(f['changed'] for f in row['fields']))
        self.assertEqual('review-needed', row['decision'])
        self.assertEqual({'MISSING_CLASSIFICATION','MISSING_VALUE','MISSING_DEADLINE'}, set(row['reason_codes']))

    def test_editing_maximum_changes_synthetic_decision_not_input(self):
        yes = demo.run_case('sandbox', self.profile)
        changed = copy.deepcopy(self.profile)
        changed['maximumValue'] = 300000
        no = demo.run_case('sandbox', changed)
        self.assertEqual(1, yes['result']['summary']['accepted'])
        self.assertEqual(1, no['result']['summary']['rejected'])
        self.assertEqual(yes['input_sha256'], no['input_sha256'])
        self.assertEqual(yes['snapshots'], no['snapshots'])
        self.assertIn('VALUE_ABOVE_MAXIMUM', no['comparisons'][0]['reason_codes'])

    def test_profile_rejects_nonfinite_values_and_unknown_fields(self):
        for bad in [float('nan'), float('inf'), -1, True, 'bad']:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                demo.validate_profile({**self.profile, 'maximumValue':bad})
        with self.assertRaises(ValueError):
            demo.validate_profile({**self.profile,'url':'https://example.com'})

    def test_unknown_case_cannot_select_files(self):
        with self.assertRaises(ValueError):
            demo.load_case('../../.env')

    def test_export_includes_decision_and_source(self):
        run = demo.run_case('cancellation', self.profile)
        self.assertIn('review-needed', run['csv'])
        self.assertIn(run['captured_at'], run['csv'])
        self.assertIn(run['source_url'], run['csv'])


class ProofLabHttpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),demo.Handler)
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def request(self,path,body=None,headers=None):
        conn=http.client.HTTPConnection('127.0.0.1',self.server.server_port,timeout=5)
        conn.request('POST' if body is not None else 'GET',path,body=json.dumps(body) if body is not None else None,headers={'Content-Type':'application/json',**(headers or {})})
        response=conn.getresponse()
        status,payload=response.status,response.read()
        conn.close()
        return status,payload

    def test_http_execution_returns_fresh_report(self):
        profile=json.loads((PROJECT/'examples/qualification-profile.json').read_text())
        status,payload=self.request('/api/run',{'case_id':'noise','profile':profile})
        self.assertEqual(200,status)
        self.assertEqual(6,json.loads(payload)['result']['summary']['comparisons'])
        run=json.loads(payload)
        status,exported=self.request('/api/export/'+run['run_id']+'.json')
        self.assertEqual(200,status)
        self.assertEqual(run,json.loads(exported))
        self.assertEqual(200,self.request('/api/export/'+run['run_id']+'.csv')[0])

    def test_cross_origin_execution_is_rejected(self):
        status,_=self.request('/api/run',{},headers={'Origin':'https://unrelated.example'})
        self.assertEqual(403,status)

    def test_private_paths_and_invalid_inputs_are_rejected(self):
        self.assertEqual(404,self.request('/.env')[0])
        self.assertEqual(400,self.request('/api/run',{'case_id':'noise','profile':{}})[0])


if __name__ == '__main__':
    unittest.main()
