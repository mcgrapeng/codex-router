#!/bin/bash

set -euo pipefail

SCRIPT_DIR=$(realpath "$(dirname "$0")")
trap "popd >> /dev/null" EXIT
pushd "$SCRIPT_DIR/.." >> /dev/null || {
  echo "Error: Failed to change directory to $SCRIPT_DIR/.."
  exit 1
}
pnpm install
pnpm run build
rm -f ./dist/zhang3f-codexrouter-*.tgz ./dist/codexrouter.tgz
pnpm pack --pack-destination ./dist
shopt -s nullglob
tarballs=(./dist/zhang3f-codexrouter-*.tgz)
if (( ${#tarballs[@]} != 1 )); then
  echo "Error: expected one Codex Router npm tarball, found ${#tarballs[@]}" >&2
  exit 1
fi
mv "${tarballs[0]}" ./dist/codexrouter.tgz
docker build -t codex -f "./Dockerfile" .
