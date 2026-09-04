import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validation_gate import CATEGORIES, check, digest


class GateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.project = self.root / "projects/WS-999-test"
        self.evidence = self.project / "evidence"
        self.evidence.mkdir(parents=True)
        (self.project / "app.py").write_text("print('example')\nprint('done')\n")
        (self.project / "sample.pdf").write_bytes(b"test-fixture-only")
        self.plan = {"iterationId": "WS-999", "builderAgentIds": ["builder"],
                     "artifactPaths": ["projects/WS-999-test/sample.pdf"],
                     "checks": [{"id": c, "category": c, "procedure": "test procedure", "expected": "expected result"} for c in CATEGORIES]}
        self.plan_path = self.evidence / "VALIDATION_PLAN.json"
        self.plan_path.write_text(json.dumps(self.plan))
        log = self.evidence / "validation-runs/log.txt"
        log.parent.mkdir()
        log.write_text("independent observations")
        self.report = {"iterationId": "WS-999", "validatorAgentId": "reviewer", "verdict": "PASS",
                       "unresolvedFindings": [], "planSha256": digest(self.plan_path),
                       "artifactSha256": {p.relative_to(self.root).as_posix(): digest(p) for p in self.project.rglob('*') if p.is_file() and 'validation-runs' not in p.parts},
                       "checks": [{"id": c, "status": "PASS", "observed": "actual result", "evidencePath": log.relative_to(self.root).as_posix(), "evidenceSha256": digest(log)} for c in CATEGORIES]}
        self.report_path = self.evidence / "INDEPENDENT_VALIDATION.json"
        self.state = {"iterationId": "WS-999", "stage": "RELEASE_READY"}
        self.save()

    def save(self):
        self.report_path.write_text(json.dumps(self.report))

    def test_valid(self):
        self.assertEqual(check(self.state, self.root), [])

    def test_machine_local_environment_file_is_excluded(self):
        (self.project / '.env.local').write_text('VERCEL_OIDC_TOKEN=secret-not-validation-evidence')
        self.assertEqual(check(self.state, self.root), [])

    def test_text_hashes_are_portable_across_line_endings(self):
        (self.project / 'app.py').write_bytes(b"print('example')\r\nprint('done')\r\n")
        self.assertEqual(check(self.state, self.root), [])

    def test_missing(self):
        self.report_path.unlink()
        self.assertTrue(check(self.state, self.root))

    def test_same_agent(self):
        self.report['validatorAgentId'] = 'builder'
        self.save()
        self.assertTrue(check(self.state, self.root))

    def test_stale_added_removed_and_changed(self):
        for operation in ('add', 'change', 'remove'):
            with self.subTest(operation=operation):
                path = self.project / 'app.py'
                original = path.read_bytes()
                extra = self.project / 'extra.py'
                if operation == 'add': extra.write_text('new')
                if operation == 'change': path.write_text('changed')
                if operation == 'remove': path.unlink()
                self.assertTrue(check(self.state, self.root))
                path.write_bytes(original)
                if extra.exists(): extra.unlink()

    def test_failed_incomplete_and_findings(self):
        for field, value in [('verdict', 'FAIL'), ('checks', []), ('unresolvedFindings', ['bug']), ('planSha256', 'stale')]:
            with self.subTest(field=field):
                old = copy.deepcopy(self.report)
                self.report[field] = value
                self.save()
                self.assertTrue(check(self.state, self.root))
                self.report = old

    def test_log_tampering(self):
        (self.evidence / 'validation-runs/log.txt').write_text('changed')
        self.assertTrue(check(self.state, self.root))

    def test_malformed(self):
        self.report_path.write_text('[]')
        self.assertTrue(check(self.state, self.root))

    def test_malformed_state(self):
        self.assertTrue(check([], self.root))
        self.assertTrue(check({'stage': []}, self.root))

    def test_empty_or_nontext_observations(self):
        for value in (' ', True):
            self.report['checks'][0]['observed'] = value
            self.save()
            self.assertTrue(check(self.state, self.root))

    def test_no_release_yet(self):
        self.report_path.unlink()
        self.state['stage'] = 'VERIFYING'
        self.assertEqual(check(self.state, self.root), [])

    def test_legacy_release(self):
        self.assertEqual(check({'iterationId': 'WS-001', 'stage': 'RELEASED'}, self.root), [])

    def test_archived_release_still_checked(self):
        self.state.update(stage='ARCHIVED', archivedFrom='RELEASED')
        self.report_path.unlink()
        self.assertTrue(check(self.state, self.root))

    def test_rejected_archive_not_a_release(self):
        self.assertEqual(check({'iterationId': 'WS-999', 'stage': 'ARCHIVED', 'archivedFrom': 'REJECTED'}, self.root), [])


if __name__ == '__main__':
    unittest.main()
