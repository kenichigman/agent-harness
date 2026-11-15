import os
import sys
import tempfile
import time
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
import grade
import liveness


class GradeTest(unittest.TestCase):
    def test_verdict_rules(self):
        self.assertEqual(grade.verdict_for([]), "PASS")
        self.assertEqual(
            grade.verdict_for([{"severity": "minor"}]), "PASS-WITH-NOTES")
        self.assertEqual(
            grade.verdict_for([{"severity": "minor"},
                               {"severity": "major"}]), "FAIL-WITH-FIXES")
        self.assertEqual(
            grade.verdict_for([{"severity": "major"},
                               {"severity": "critical"}]), "FAIL")


class LivenessTest(unittest.TestCase):
    def test_both_signals_pass_for_self(self):
        with tempfile.TemporaryDirectory() as tmp:
            pid_file = os.path.join(tmp, "job.pid")
            out_file = os.path.join(tmp, "job.log")
            with open(pid_file, "w", encoding="utf-8") as fh:
                fh.write(str(os.getpid()))
            with open(out_file, "w", encoding="utf-8") as fh:
                fh.write("tick\n")
            alive, _ = liveness.check(pid_file, out_file, 300)
            self.assertTrue(alive)

    def test_stale_output_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            pid_file = os.path.join(tmp, "job.pid")
            out_file = os.path.join(tmp, "job.log")
            with open(pid_file, "w", encoding="utf-8") as fh:
                fh.write(str(os.getpid()))
            with open(out_file, "w", encoding="utf-8") as fh:
                fh.write("tick\n")
            alive, reason = liveness.check(
                pid_file, out_file, 300, now=time.time() + 10000)
            self.assertFalse(alive)
            self.assertIn("signal 2", reason)

    def test_missing_pid_file_fails(self):
        alive, reason = liveness.check("/nonexistent.pid", "/nonexistent.log", 60)
        self.assertFalse(alive)
        self.assertIn("signal 1", reason)


if __name__ == "__main__":
    unittest.main()
