import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
import lease


class LeaseTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "leases.json")

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *argv):
        return lease.main(["--file", self.path, *argv])

    def test_contention_and_release(self):
        self.assertEqual(
            self.run_cli("acquire", "gpu", "--holder", "a", "--ttl", "60"), 0)
        self.assertEqual(
            self.run_cli("acquire", "gpu", "--holder", "b", "--ttl", "60"), 1)
        self.assertEqual(
            self.run_cli("release", "gpu", "--holder", "b"), 1)
        self.assertEqual(
            self.run_cli("release", "gpu", "--holder", "a"), 0)
        self.assertEqual(
            self.run_cli("acquire", "gpu", "--holder", "b", "--ttl", "60"), 0)

    def test_expired_lease_can_be_taken(self):
        data = {"gpu": {"holder": "a", "expires": 1}}
        lease.save(self.path, data)
        self.assertEqual(
            self.run_cli("acquire", "gpu", "--holder", "b", "--ttl", "60"), 0)


if __name__ == "__main__":
    unittest.main()
