#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DRIVE="$(echo "$SCRIPT_DIR" | cut -d'/' -f3)"
GLOBAL_CFG="/media/$DRIVE/gameconfig/sys_override/global.cfg"
KEY="$1"

if [ -z "$KEY" ]; then
  echo "Usage: $0 <key>" >&2
  exit 1
fi

if command -v crudini >/dev/null 2>&1; then
  current=$(crudini --get "$GLOBAL_CFG" '' "$KEY" 2>/dev/null)
  if [ "$current" = "true" ]; then new="false"; else new="true"; fi
  crudini --set "$GLOBAL_CFG" '' "$KEY" "$new"
else
  line=$(grep -m1 "^$KEY" "$GLOBAL_CFG" || true)
  current=$(echo "$line" | sed -e 's/.*= *"\?//' -e 's/"$//')
  if [ "$current" = "true" ]; then new="false"; else new="true"; fi
  sed -i "s/^$KEY\s*=\s*\"\?.*\"\?/$KEY = \"$new\"/" "$GLOBAL_CFG"
fi
