#!/bin/bash
set -euo pipefail

DESTINATION_CORES_DIR="/opt/retroarch/cores"

for bak in "$DESTINATION_CORES_DIR"/*.bak; do
    if [[ -f "$bak" ]]; then
        mv "$bak" "${bak%.bak}"
    fi
done

echo "Default cores restored."
