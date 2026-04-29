#!/usr/bin/env python3
"""Tests for Codex Router npm package staging."""

import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_PATH = Path(__file__).with_name("build_npm_package.py")
SPEC = importlib.util.spec_from_file_location("build_npm_package", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load {SCRIPT_PATH}")

build_npm_package = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(build_npm_package)


class BuildNpmPackageTests(unittest.TestCase):
    def test_codex_meta_package_uses_codexrouter_names_and_home_init(self) -> None:
        version = "0.0.0-test"

        with tempfile.TemporaryDirectory() as temp_dir:
            staging_dir = Path(temp_dir)
            build_npm_package.stage_sources(staging_dir, version, "codex")

            package_json = json.loads((staging_dir / "package.json").read_text())
            self.assertEqual(package_json["name"], "@zhang3f/codexrouter")
            self.assertEqual(package_json["bin"], {"codexrouter": "bin/codex.js"})
            self.assertEqual(
                package_json["scripts"]["postinstall"],
                "node bin/codexrouter-init.js",
            )
            self.assertEqual(package_json["files"], ["bin"])
            self.assertTrue((staging_dir / "bin" / "codex.js").is_file())
            self.assertTrue((staging_dir / "bin" / "codexrouter-init.js").is_file())

            optional_deps = package_json["optionalDependencies"]
            self.assertTrue(optional_deps)
            self.assertTrue(
                all(name.startswith("@zhang3f/codexrouter-") for name in optional_deps)
            )
            self.assertFalse(any(value.startswith("npm:") for value in optional_deps.values()))

    def test_platform_package_uses_platform_package_name(self) -> None:
        version = "0.0.0-test"

        with tempfile.TemporaryDirectory() as temp_dir:
            staging_dir = Path(temp_dir)
            build_npm_package.stage_sources(staging_dir, version, "codex-darwin-arm64")

            package_json = json.loads((staging_dir / "package.json").read_text())
            self.assertEqual(package_json["name"], "@zhang3f/codexrouter-darwin-arm64")
            self.assertEqual(package_json["version"], f"{version}-darwin-arm64")
            self.assertEqual(package_json["files"], ["vendor"])

    def test_platform_package_copies_only_matching_vendor_target(self) -> None:
        version = "0.0.0-test"

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            vendor_src = temp_path / "vendor-src"
            target_root = vendor_src / "aarch64-apple-darwin"
            codex_dir = target_root / "codex"
            rg_dir = target_root / "path"
            codex_dir.mkdir(parents=True)
            rg_dir.mkdir(parents=True)
            binary_name = "codex.exe" if os.name == "nt" else "codex"
            (codex_dir / binary_name).write_text("codex binary")
            (rg_dir / "rg").write_text("rg binary")

            unused_root = vendor_src / "x86_64-apple-darwin" / "codex"
            unused_root.mkdir(parents=True)
            (unused_root / binary_name).write_text("unused")

            staging_dir = temp_path / "stage"
            staging_dir.mkdir()
            build_npm_package.stage_sources(staging_dir, version, "codex-darwin-arm64")
            build_npm_package.copy_native_binaries(
                vendor_src,
                staging_dir,
                build_npm_package.PACKAGE_NATIVE_COMPONENTS["codex-darwin-arm64"],
                target_filter=build_npm_package.PACKAGE_TARGET_FILTERS[
                    "codex-darwin-arm64"
                ],
            )

            self.assertTrue(
                (
                    staging_dir
                    / "vendor"
                    / "aarch64-apple-darwin"
                    / "codex"
                    / binary_name
                ).is_file()
            )
            self.assertTrue(
                (
                    staging_dir
                    / "vendor"
                    / "aarch64-apple-darwin"
                    / "path"
                    / "rg"
                ).is_file()
            )
            self.assertFalse(
                (staging_dir / "vendor" / "x86_64-apple-darwin").exists()
            )

    def test_main_stages_platform_package_with_vendor_filter(self) -> None:
        version = "0.0.0-test"

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            vendor_src = temp_path / "vendor-src"
            target_root = vendor_src / "aarch64-apple-darwin"
            codex_dir = target_root / "codex"
            rg_dir = target_root / "path"
            codex_dir.mkdir(parents=True)
            rg_dir.mkdir(parents=True)
            binary_name = "codex.exe" if os.name == "nt" else "codex"
            (codex_dir / binary_name).write_text("codex binary")
            (rg_dir / "rg").write_text("rg binary")

            staging_dir = temp_path / "stage"
            original_argv = sys.argv
            try:
                sys.argv = [
                    str(SCRIPT_PATH),
                    "--package",
                    "codex-darwin-arm64",
                    "--version",
                    version,
                    "--staging-dir",
                    str(staging_dir),
                    "--vendor-src",
                    str(vendor_src),
                ]

                self.assertEqual(build_npm_package.main(), 0)
            finally:
                sys.argv = original_argv

            self.assertTrue(
                (
                    staging_dir
                    / "vendor"
                    / "aarch64-apple-darwin"
                    / "codex"
                    / binary_name
                ).is_file()
            )


if __name__ == "__main__":
    unittest.main()
