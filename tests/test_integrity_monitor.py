import tempfile
import unittest
from pathlib import Path

from integrity_monitor import build_baseline, compare, load_baseline, save_baseline, sha256_file


class TestIntegrityMonitor(unittest.TestCase):
    def test_hash_is_stable(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "a.txt"
            path.write_text("hello", encoding="utf-8")
            self.assertEqual(sha256_file(path), sha256_file(path))

    def test_detects_added_modified_deleted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "keep.txt").write_text("same", encoding="utf-8")
            (root / "modify.txt").write_text("old", encoding="utf-8")
            (root / "delete.txt").write_text("bye", encoding="utf-8")
            baseline = build_baseline(tmp)
            (root / "modify.txt").write_text("new", encoding="utf-8")
            (root / "delete.txt").unlink()
            (root / "add.txt").write_text("new file", encoding="utf-8")
            report = compare(tmp, baseline)
            self.assertEqual(report["added"], ["add.txt"])
            self.assertEqual(report["modified"], ["modify.txt"])
            self.assertEqual(report["deleted"], ["delete.txt"])
            self.assertEqual(report["unchanged"], ["keep.txt"])

    def test_save_and_load_baseline(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "baseline.json"
            expected = {"a.txt": "abc"}
            save_baseline(expected, str(path))
            self.assertEqual(load_baseline(str(path)), expected)


if __name__ == "__main__":
    unittest.main()
