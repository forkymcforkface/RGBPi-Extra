#!/bin/bash
set -e

RGBPI_UI_ROOT="/opt/rgbpi/ui"
PATCH_FLAG_FILE="$RGBPI_UI_ROOT/patch_applied.flag"
LAUNCHER_FILE="$RGBPI_UI_ROOT/launcher.py"
VERSION="v.21a"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$SCRIPT_DIR/RGBPi-Extra/application/data"

# Copy shaders
rsync -a "$DATA_DIR/shaders/" "/root/.config/retroarch/shaders/"

# Replace retroarch binary and backup old one
retroarch_path="/opt/retroarch/retroarch"
backup_path="${retroarch_path}.bak"
if [[ -f "$backup_path" ]]; then
    rm -f "$retroarch_path"
else
    mv "$retroarch_path" "$backup_path"
fi
cp "$DATA_DIR/retroarch" "$retroarch_path"
chmod 777 "$retroarch_path"

# Append new cores configuration
cat "$DATA_DIR/new_cores/cores.cfg" >> "/opt/rgbpi/ui/data/cores.cfg"

# Update launcher
cp "$DATA_DIR/launcher.py" "$LAUNCHER_FILE"
if [[ -f "$RGBPI_UI_ROOT/launcher.pyc" ]]; then
    mv "$RGBPI_UI_ROOT/launcher.pyc" "$RGBPI_UI_ROOT/launcher2.pyc"
fi

# Determine drive and copy drive files
DRIVE=$(echo "$SCRIPT_DIR" | cut -d/ -f3)
media_mountpoint="/media/$DRIVE"
rsync -a "$DATA_DIR/drive/" "$media_mountpoint/"

# Process dat files
dats_dir="$media_mountpoint/dats"
if [[ -d "$dats_dir" ]]; then
    for dat in games.dat favorites.dat favorites_tate.dat; do
        file="$dats_dir/$dat"
        extra="${file%.dat}_extra.dat"
        if [[ -f "$file" ]]; then
            [[ -f "$extra" ]] && rm -f "$extra"
            cp "$file" "$extra"
        fi
    done
fi

# Patch io.py
io_file="/usr/lib/python3.9/io.py"
if ! grep -q "#BELOW THIS LINE" "$io_file"; then
    cat <<'PATCH' >> "$io_file"

#BELOW THIS LINE
import os
from _io import open as _original_open

def open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
    if isinstance(file, str):
        if file.endswith('/games.dat'):
            file = file.replace('/games.dat', '/games_extra.dat')
        elif file.endswith('/favorites.dat'):
            file = file.replace('/favorites.dat', '/favorites_extra.dat')
        elif file.endswith('/favorites_tate.dat'):
            file = file.replace('/favorites_tate.dat', '/favorites_tate_extra.dat')

        if not os.path.exists(file):
            _original_open(file, 'w').close()

    return _original_open(file, mode, buffering, encoding, errors, newline, closefd, opener)

OpenWrapper = open
PATCH
fi

# Write patch flag
echo "$VERSION" > "$PATCH_FLAG_FILE"
chmod 777 "$media_mountpoint"

sudo reboot
