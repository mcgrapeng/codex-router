import { spawnSync } from "node:child_process";
import {
  chmodSync,
  copyFileSync,
  existsSync,
  mkdirSync,
  mkdtempSync,
  readFileSync,
  writeFileSync,
} from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import assert from "node:assert/strict";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function targetTripleForCurrentPlatform() {
  switch (process.platform) {
    case "linux":
    case "android":
      switch (process.arch) {
        case "x64":
          return "x86_64-unknown-linux-musl";
        case "arm64":
          return "aarch64-unknown-linux-musl";
        default:
          return null;
      }
    case "darwin":
      switch (process.arch) {
        case "x64":
          return "x86_64-apple-darwin";
        case "arm64":
          return "aarch64-apple-darwin";
        default:
          return null;
      }
    case "win32":
      switch (process.arch) {
        case "x64":
          return "x86_64-pc-windows-msvc";
        case "arm64":
          return "aarch64-pc-windows-msvc";
        default:
          return null;
      }
    default:
      return null;
  }
}

function runLauncher(extraEnv = {}) {
  const targetTriple = targetTripleForCurrentPlatform();
  if (targetTriple === null || process.platform === "win32") {
    return null;
  }

  const tempRoot = mkdtempSync(path.join(os.tmpdir(), "codexrouter-launcher-"));
  const packageRoot = path.join(tempRoot, "package");
  const binDir = path.join(packageRoot, "bin");
  mkdirSync(binDir, { recursive: true });
  copyFileSync(path.join(__dirname, "..", "bin", "coder.js"), path.join(binDir, "coder.js"));

  const binaryPath = path.join(packageRoot, "vendor", targetTriple, "codex", "codex");
  mkdirSync(path.dirname(binaryPath), { recursive: true });
  const captureFile = path.join(tempRoot, "capture.json");
  writeFileSync(
    binaryPath,
    [
      "#!/usr/bin/env node",
      'const fs = require("node:fs");',
      "fs.writeFileSync(",
      "  process.env.CAPTURE_FILE,",
      "  JSON.stringify({",
      "    CODEX_HOME: process.env.CODEX_HOME,",
      "    CODEXROUTER_HOME: process.env.CODEXROUTER_HOME ?? null,",
      "    CODEX_MANAGED_BY_NPM: process.env.CODEX_MANAGED_BY_NPM ?? null,",
      "  }),",
      ");",
    ].join("\n"),
  );
  chmodSync(binaryPath, 0o755);

  const homeDir = path.join(tempRoot, "home");
  mkdirSync(homeDir, { recursive: true });

  const env = {
    ...process.env,
    CAPTURE_FILE: captureFile,
    HOME: homeDir,
    USERPROFILE: homeDir,
    CODEX_HOME: path.join(homeDir, ".codex"),
  };
  delete env.CODEXROUTER_HOME;
  Object.assign(env, extraEnv);

  const result = spawnSync(process.execPath, [path.join(binDir, "coder.js")], {
    env,
    encoding: "utf8",
  });
  assert.equal(result.status, 0, result.stderr || result.stdout);

  return {
    capture: JSON.parse(readFileSync(captureFile, "utf8")),
    homeDir,
  };
}

test("launcher replaces inherited CODEX_HOME with the default Codex Router home", (t) => {
  const result = runLauncher();
  if (result === null) {
    t.skip("current platform is not supported by the launcher test");
    return;
  }

  const inheritedCodexHome = path.join(result.homeDir, ".codex");
  const expectedCodexRouterHome = path.join(result.homeDir, ".codexrouter");
  assert.equal(result.capture.CODEX_HOME, expectedCodexRouterHome);
  assert.notEqual(result.capture.CODEX_HOME, inheritedCodexHome);
  assert.equal(result.capture.CODEX_MANAGED_BY_NPM, "1");
  assert.equal(existsSync(expectedCodexRouterHome), true);
  assert.equal(existsSync(inheritedCodexHome), false);
});

test("launcher maps CODEXROUTER_HOME to CODEX_HOME for the native binary", (t) => {
  const tempHome = mkdtempSync(path.join(os.tmpdir(), "codexrouter-home-"));
  const customHome = path.join(tempHome, "custom-router-home");
  const result = runLauncher({
    CODEXROUTER_HOME: customHome,
    CODEX_HOME: path.join(tempHome, ".codex"),
  });
  if (result === null) {
    t.skip("current platform is not supported by the launcher test");
    return;
  }

  assert.equal(result.capture.CODEX_HOME, customHome);
  assert.equal(result.capture.CODEXROUTER_HOME, customHome);
  assert.equal(existsSync(customHome), true);
});

test("postinstall creates the default Codex Router home without touching .codex", () => {
  const tempHome = mkdtempSync(path.join(os.tmpdir(), "codexrouter-postinstall-"));
  const inheritedCodexHome = path.join(tempHome, ".codex");
  const expectedCodexRouterHome = path.join(tempHome, ".codexrouter");

  const env = {
    ...process.env,
    HOME: tempHome,
    USERPROFILE: tempHome,
    CODEX_HOME: inheritedCodexHome,
  };
  delete env.CODEXROUTER_HOME;

  const result = spawnSync(
    process.execPath,
    [path.join(__dirname, "..", "bin", "coder-init.js")],
    {
      env,
      encoding: "utf8",
    },
  );
  assert.equal(result.status, 0, result.stderr || result.stdout);
  assert.equal(existsSync(expectedCodexRouterHome), true);
  assert.equal(existsSync(inheritedCodexHome), false);
});
