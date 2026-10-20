"""Integration tests for the global skill link installers."""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


def installer_command(target_root: Path, *extra_args: str) -> list[str]:
    if os.name == "nt":
        powershell = shutil.which("powershell") or shutil.which("pwsh")
        if not powershell:
            raise unittest.SkipTest("PowerShell is required to test the Windows installer")
        return [
            powershell,
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(ROOT / "scripts" / "link-global-skills.ps1"),
            "-TargetRoot",
            str(target_root),
            *extra_args,
        ]

    bash = shutil.which("bash")
    if not bash:
        raise unittest.SkipTest("Bash is required to test the shell installer")
    return [
        bash,
        str(ROOT / "scripts" / "link-global-skills.sh"),
        "--target-root",
        str(target_root),
        *extra_args,
    ]


def run_installer(target_root: Path, *extra_args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        installer_command(target_root, *extra_args),
        check=False,
        capture_output=True,
        text=True,
    )


class LinkGlobalSkillsTests(unittest.TestCase):
    def test_links_all_skills_and_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target_root = Path(temp_dir) / "skills"

            first = run_installer(target_root)
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)

            for skill in SKILLS.iterdir():
                if (skill / "SKILL.md").is_file():
                    destination = target_root / skill.name
                    self.assertTrue(destination.is_dir(), str(destination))
                    self.assertEqual(destination.resolve(), skill.resolve())

            second = run_installer(target_root)
            self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
            self.assertIn("Already linked:", second.stdout)

    def test_preserves_existing_real_skill_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target_root = Path(temp_dir) / "skills"
            conflicted = target_root / "oss-pull-request-review"
            conflicted.mkdir(parents=True)
            marker = conflicted / "keep.txt"
            marker.write_text("preserve this local skill", encoding="utf-8")

            result = run_installer(target_root)
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(marker.read_text(encoding="utf-8"), "preserve this local skill")
            self.assertFalse(conflicted.is_symlink())

    def test_can_link_a_single_skill(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target_root = Path(temp_dir) / "skills"
            args = (
                ["-SkillName", "oss-pull-request-review"]
                if os.name == "nt"
                else ["--skill", "oss-pull-request-review"]
            )
            result = run_installer(target_root, *args)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue(
                (target_root / "oss-pull-request-review").exists()
                or (target_root / "oss-pull-request-review").is_symlink()
            )
            self.assertFalse((target_root / "devto-publish-expert").exists())


if __name__ == "__main__":
    unittest.main()
