#!/usr/bin/env node

import { existsSync, mkdirSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";

function resolveCodexRouterHome() {
  const explicitHome = process.env.CODEXROUTER_HOME;
  if (explicitHome && explicitHome.trim() !== "") {
    return explicitHome;
  }

  return path.join(os.homedir(), ".codexrouter");
}

const codexRouterHome = resolveCodexRouterHome();
mkdirSync(codexRouterHome, { recursive: true });

const configPath = path.join(codexRouterHome, "config.toml");
if (!existsSync(configPath)) {
  writeFileSync(
    configPath,
    [
      "# Codex Router config",
      "# This file is intentionally stored under .codexrouter so coder stays isolated from Codex.",
      "",
    ].join("\n"),
  );
}
