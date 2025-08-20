#!/bin/bash
set -euo pipefail

SOURCE_CORES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../RGBPi-Extra/application/data/update_cores" && pwd)"
DESTINATION_CORES_DIR="/opt/retroarch/cores"
TEMP_DIR="$(mktemp -d)"

cleanup() {
    rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <core_name>" >&2
    exit 1
fi

CORE_NAME="$1"
CORE_ARCHIVE=""

if [[ -f "$SOURCE_CORES_DIR/${CORE_NAME}.7z" ]]; then
    CORE_ARCHIVE="$SOURCE_CORES_DIR/${CORE_NAME}.7z"
    7z x "$CORE_ARCHIVE" -o"$TEMP_DIR" -aoa >/dev/null
elif [[ -f "$SOURCE_CORES_DIR/${CORE_NAME}.zip" ]]; then
    CORE_ARCHIVE="$SOURCE_CORES_DIR/${CORE_NAME}.zip"
    unzip -o "$CORE_ARCHIVE" -d "$TEMP_DIR" >/dev/null
elif [[ -f "$SOURCE_CORES_DIR/${CORE_NAME}.so" ]]; then
    cp "$SOURCE_CORES_DIR/${CORE_NAME}.so" "$TEMP_DIR/"
else
    echo "Core $CORE_NAME not found in $SOURCE_CORES_DIR" >&2
    exit 1
fi

EXTRACTED_CORE="$TEMP_DIR/${CORE_NAME}.so"
if [[ ! -f "$EXTRACTED_CORE" ]]; then
    echo "Extracted core not found: $EXTRACTED_CORE" >&2
    exit 1
fi

DEST_CORE="$DESTINATION_CORES_DIR/${CORE_NAME}.so"
BAK_CORE="${DEST_CORE}.bak"

if [[ ! -f "$DEST_CORE" ]]; then
    echo "No matching core to update: $DEST_CORE" >&2
    exit 0
fi

if [[ ! -f "$BAK_CORE" ]]; then
    mv "$DEST_CORE" "$BAK_CORE"
fi

cp "$EXTRACTED_CORE" "$DEST_CORE"

echo "Updated core: $CORE_NAME"
