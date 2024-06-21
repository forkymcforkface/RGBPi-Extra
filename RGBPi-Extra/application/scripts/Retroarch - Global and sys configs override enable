#!/bin/bash
set -euo pipefail

cd "$(dirname "$(readlink -f "$0")")"

# Define the path to the retroarch file and its backup
retroarch_path="/opt/retroarch/retroarch"
backup_path="/opt/retroarch/retroarch.bak"

# Check if the backup exists
if [ ! -f "$backup_path" ]; then
  echo "Backup not found. Creating backup..."
  cp -vf "$retroarch_path" "$backup_path"
else
  echo "Backup already exists."
fi

# Copy the new retroarch file
cp -vf files/retroarch "$retroarch_path"
