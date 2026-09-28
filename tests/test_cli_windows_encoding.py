from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class WindowsCliEncodingTests(unittest.TestCase):
    def test_help_does_not_crash_when_terminal_uses_cp1258(self) -> None:
        environment = dict(os.environ)
        environment["PYTHONIOENCODING"] = "cp1258"

        for script in ("load_test.py", "inject_incident.py"):
            with self.subTest(script=script):
                completed = subprocess.run(
                    [sys.executable, str(REPO_ROOT / "scripts" / script), "--help"],
                    cwd=REPO_ROOT,
                    env=environment,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(completed.returncode, 0, completed.stderr.decode(errors="replace"))


if __name__ == "__main__":
    unittest.main()
