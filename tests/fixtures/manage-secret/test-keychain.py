#!/usr/bin/env python3
"""Run on macOS with python3 tests/fixtures/manage-secret/test-keychain.py."""
from pathlib import Path
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent
HELPER = HERE.parents[2] / "skills/manage-secret/scripts/manage-keychain.js"
OSASCRIPT = "/usr/bin/osascript"
SECURITY = "/usr/bin/security"


def security(*args):
    return subprocess.check_output([SECURITY, *args], stderr=subprocess.PIPE, timeout=15)


def main():
    source = HELPER.read_bytes()
    fixture = (HERE / "keychain-tests.js").read_bytes()
    original_search_list = security("list-keychains", "-d", "user")
    with tempfile.TemporaryDirectory(prefix="manage-secret-test-") as temporary:
        directory = Path(temporary)
        combined = directory / "keychain-tests.js"
        combined.write_bytes(source + b"\n" + fixture)
        created = []
        try:
            for name in ("first.keychain", "second.keychain"):
                path = str(directory / name)
                security("create-keychain", "-p", "test-only-keychain-password", path)
                created.append(path)
            result = subprocess.run(
                [OSASCRIPT, "-l", "JavaScript", str(combined), *created],
                check=True, timeout=30, capture_output=True, text=True,
            )
            assert result.stdout.strip() == "Passed metadata and clipboard checks with isolated Keychain items."
            assert not result.stderr
            print(result.stdout.strip())
            invalid = subprocess.run(
                [OSASCRIPT, "-l", "JavaScript", str(HELPER), "accounts", "fixture-test-api"],
                timeout=15, capture_output=True, text=True,
            )
            assert invalid.returncode != 0 and not invalid.stdout and "Usage:" in invalid.stderr
            print("Verified the standalone helper rejects invalid arguments.")
        except subprocess.CalledProcessError as error:
            raise SystemExit(error.stderr) from error
        finally:
            for path in reversed(created):
                security("delete-keychain", path)
            assert security("list-keychains", "-d", "user") == original_search_list


if __name__ == "__main__":
    main()
