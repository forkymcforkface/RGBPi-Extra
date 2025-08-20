#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SCRIPT_PATH="RGBPi-Extra/application/data/scripts/General - Set correct 0777 permissions for Media.bash"
bash "$REPO_ROOT/$SCRIPT_PATH" "$@"
