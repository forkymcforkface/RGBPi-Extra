#!/bin/bash
set -euo pipefail

cd "$(dirname "$(readlink -f "$0")")"

# Define the path to the retroarch file and its backup
retroarch_path="/opt/retroarch/retroarch"
backup_path="/opt/retroarch/retroarch.bak"

# Check if the backup exists
if [ -f "$backup_path" ]; then
  echo "Backup found. Restoring backup..."
  mv -vf "$backup_path" "$retroarch_path"
else
  echo "Backup not found. Cannot restore."
fi
