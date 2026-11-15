import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
import work_registry


class RegistryTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "registry.json")

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *argv):
        return work_registry.main(["--file", self.path, *argv])

    def test_add_claim_close_cycle(self):
        self.assertEqual(self.run_cli("add", "do a thing"), 0)
        self.assertEqual(self.run_cli("claim", "1", "--owner", "w1"), 0)
        self.assertEqual(
            self.run_cli("close", "1", "--evidence", "artifact exists"), 0)
        item = work_registry.load(self.path)["items"][0]
        self.assertEqual(item["status"], "done")
        self.assertEqual(item["evidence"], "artifact exists")

    def test_close_unknown_item_fails(self):
        self.assertEqual(
            self.run_cli("close", "99", "--evidence", "x"), 1)

    def test_next_skips_claimed_and_done(self):
        self.run_cli("add", "first")
        self.run_cli("add", "second")
        self.run_cli("claim", "1", "--owner", "w1")
        data = work_registry.load(self.path)
        nxt = [i for i in data["items"]
               if i["status"] == "open" and not i["owner"]]
        self.assertEqual([i["id"] for i in nxt], [2])


if __name__ == "__main__":
    unittest.main()
