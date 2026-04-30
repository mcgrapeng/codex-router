#!/usr/bin/env python3
"""Tests for staging Codex Router npm release packages."""

import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT_PATH = Path(__file__).with_name("stage_npm_packages.py")
SPEC = importlib.util.spec_from_file_location("stage_npm_packages", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load {SCRIPT_PATH}")

stage_npm_packages = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(stage_npm_packages)


class StageNpmPackagesTests(unittest.TestCase):
    def test_codex_expands_only_to_macos_platform_packages(self) -> None:
        packages = stage_npm_packages.expand_packages(["codex"])

        self.assertEqual(
            packages,
            ["codex", "codex-darwin-x64", "codex-darwin-arm64"],
        )
        self.assertEqual(
            stage_npm_packages.collect_native_targets(packages),
            {"x86_64-apple-darwin", "aarch64-apple-darwin"},
        )

    def test_install_native_components_limits_downloads_to_selected_targets(self) -> None:
        with patch.object(stage_npm_packages, "run_command") as run_command:
            stage_npm_packages.install_native_components(
                "https://github.com/example/repo/actions/runs/123",
                {"codex", "rg"},
                {"x86_64-apple-darwin", "aarch64-apple-darwin"},
                Path("/tmp/vendor-root"),
            )

        run_command.assert_called_once_with(
            [
                str(stage_npm_packages.INSTALL_NATIVE_DEPS),
                "--workflow-url",
                "https://github.com/example/repo/actions/runs/123",
                "--component",
                "codex",
                "--component",
                "rg",
                "--target",
                "aarch64-apple-darwin",
                "--target",
                "x86_64-apple-darwin",
                "/tmp/vendor-root",
            ]
        )


if __name__ == "__main__":
    unittest.main()
