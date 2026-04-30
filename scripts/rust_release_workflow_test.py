#!/usr/bin/env python3
"""Tests for the Rust release workflow shape."""

import unittest
from pathlib import Path

WORKFLOW_PATH = Path(__file__).resolve().parent.parent / ".github" / "workflows" / "rust-release.yml"


class RustReleaseWorkflowTests(unittest.TestCase):
    def test_macos_code_signing_is_skipped_without_apple_secrets(self) -> None:
        workflow = WORKFLOW_PATH.read_text(encoding="utf-8")

        self.assertIn("id: macos_signing", workflow)
        self.assertIn("enabled=false", workflow)
        self.assertIn("steps.macos_signing.outputs.enabled == 'true'", workflow)

        signing_calls = workflow.count("uses: ./.github/actions/macos-code-sign")
        guarded_signing_calls = workflow.count(
            "if: ${{ steps.macos_signing.outputs.enabled == 'true' }}"
        )
        self.assertEqual(signing_calls, 2)
        self.assertEqual(guarded_signing_calls, 2)

    def test_release_workflow_only_builds_and_publishes_macos_npm_packages(self) -> None:
        workflow = WORKFLOW_PATH.read_text(encoding="utf-8")

        self.assertIn("target: aarch64-apple-darwin", workflow)
        self.assertIn("target: x86_64-apple-darwin", workflow)
        self.assertIn('"codex-npm-darwin-*-${version}.tgz"', workflow)

        for removed_platform in (
            "aarch64-unknown-linux-gnu",
            "x86_64-unknown-linux-musl",
            "x86_64-pc-windows-msvc",
            "aarch64-pc-windows-msvc",
            "codex-npm-linux",
            "codex-npm-windows",
            "codex-runners",
            "macos-15-xlarge",
        ):
            self.assertNotIn(removed_platform, workflow)

    def test_npm_publish_skips_versions_that_already_exist(self) -> None:
        workflow = WORKFLOW_PATH.read_text(encoding="utf-8")

        self.assertIn("package_name=", workflow)
        self.assertIn("package_version=", workflow)
        self.assertIn('npm view "${package_name}@${package_version}" version --json', workflow)
        self.assertIn("Skipping already-published npm package", workflow)


if __name__ == "__main__":
    unittest.main()
