#!/usr/bin/env python3
"""Exercise the pull-request translation step with real Git paths."""

import json
import pathlib
import subprocess
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class TranslationWorkflowTest(unittest.TestCase):
    def test_changed_paths_are_passed_intact_and_deleted_paths_are_skipped(self):
        workflow = (ROOT / ".github/workflows/lint.yml").read_text()
        step = workflow.split("      - name: language migration invariants\n", 1)[1]
        body = step.split("        run: |\n", 1)[1]
        script = "\n".join(line[10:] for line in body.splitlines())

        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)

            def git(*args):
                return subprocess.run(
                    ["git", *args], cwd=root, check=True, capture_output=True, text=True
                ).stdout.strip()

            git("init", "-q")
            git("config", "user.email", "test@example.com")
            git("config", "user.name", "Test")
            (root / "with space.md").write_text("before\n")
            (root / "deleted.md").write_text("before\n")
            git("add", ".")
            git("commit", "-qm", "baseline")
            base = git("rev-parse", "HEAD")
            (root / "with space.md").write_text("after\n")
            (root / "deleted.md").unlink()
            git("add", "-A")
            git("commit", "-qm", "change")
            (root / "scripts").mkdir()
            (root / "scripts/verify-translation.py").write_text(
                "import json, pathlib, sys\n"
                "pathlib.Path('args.json').write_text(json.dumps(sys.argv[1:]))\n"
            )
            script = script.replace("${{ github.event.pull_request.base.sha }}", base)
            subprocess.run(["bash", "-e", "-c", script], cwd=root, check=True)
            self.assertEqual(
                json.loads((root / "args.json").read_text()),
                ["--mode=rewrite", base, "with space.md"],
            )


if __name__ == "__main__":
    unittest.main()
