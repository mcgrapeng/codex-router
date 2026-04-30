#!/usr/bin/env python3
"""Tests for installing Codex Router native npm dependencies."""

import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT_PATH = Path(__file__).with_name("install_native_deps.py")
SPEC = importlib.util.spec_from_file_location("install_native_deps", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load {SCRIPT_PATH}")

install_native_deps = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(install_native_deps)


class InstallNativeDepsTests(unittest.TestCase):
    def test_download_artifacts_uses_repo_from_workflow_url(self) -> None:
        dest_dir = Path("/tmp/artifacts")

        with patch.object(install_native_deps.subprocess, "check_call") as check_call:
            install_native_deps.download_artifacts_from_workflow(
                "https://github.com/mcgrapeng/codex-router/actions/runs/25171101232",
                dest_dir,
            )

        check_call.assert_called_once_with(
            [
                "gh",
                "run",
                "download",
                "--dir",
                str(dest_dir),
                "--repo",
                "mcgrapeng/codex-router",
                "25171101232",
            ]
        )

    def test_download_artifacts_limits_downloads_to_selected_targets(self) -> None:
        dest_dir = Path("/tmp/artifacts")

        with patch.object(install_native_deps.subprocess, "check_call") as check_call:
            install_native_deps.download_artifacts_from_workflow(
                "https://github.com/mcgrapeng/codex-router/actions/runs/25171101232",
                dest_dir,
                selected_targets=["aarch64-apple-darwin", "x86_64-apple-darwin"],
            )

        check_call.assert_any_call(
            [
                "gh",
                "run",
                "download",
                "--dir",
                str(dest_dir),
                "--repo",
                "mcgrapeng/codex-router",
                "--name",
                "aarch64-apple-darwin",
                "25171101232",
            ]
        )
        check_call.assert_any_call(
            [
                "gh",
                "run",
                "download",
                "--dir",
                str(dest_dir),
                "--repo",
                "mcgrapeng/codex-router",
                "--name",
                "x86_64-apple-darwin",
                "25171101232",
            ]
        )
        self.assertEqual(check_call.call_count, 2)


if __name__ == "__main__":
    unittest.main()
