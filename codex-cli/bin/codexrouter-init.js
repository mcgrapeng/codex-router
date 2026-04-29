#!/usr/bin/env node

import { mkdirSync } from "node:fs";
import os from "node:os";
import path from "node:path";

function resolveCodexRouterHome() {
  const explicitHome = process.env.CODEXROUTER_HOME;
  if (explicitHome && explicitHome.trim() !== "") {
    return explicitHome;
  }

  return path.join(os.homedir(), ".codexrouter");
}

mkdirSync(resolveCodexRouterHome(), { recursive: true });
