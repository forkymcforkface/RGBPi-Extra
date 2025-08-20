#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
DRIVE="$(echo "$ROOT_DIR" | cut -d/ -f3)"
SYSTEMS_CORES_FILE="/media/$DRIVE/gameconfig/sys_override/systems_cores.cfg"
DESTINATION_SYSTEMS_FILE="/opt/rgbpi/ui/data/systems.dat"
BACKUP_SYSTEMS_FILE="/opt/rgbpi/ui/data/systems.dat.bak"
SYSTEMS_CORES_TEMPLATE='[Systems]\n'

delete_cores() {
    echo "Removing installed cores"
    if [[ -f "$SYSTEMS_CORES_FILE" ]]; then
        grep '=' "$SYSTEMS_CORES_FILE" | while IFS='=' read -r _ core; do
            core=$(echo "$core" | xargs)
            core_path="/opt/retroarch/cores/$core"
            [[ -f "$core_path" ]] && rm "$core_path"
            info_path="${core_path%.so}.info"
            [[ -f "$info_path" ]] && rm "$info_path"
            bashhelper_path="${core_path%.so}.bash"
            [[ -f "$bashhelper_path" ]] && rm "$bashhelper_path"
        done
    fi
}

reset_systems_cores() {
    echo "Resetting systems_cores.cfg"
    mkdir -p "$(dirname "$SYSTEMS_CORES_FILE")"
    echo -e "$SYSTEMS_CORES_TEMPLATE" > "$SYSTEMS_CORES_FILE"
}

restore_default_systems() {
    if [[ -f "$BACKUP_SYSTEMS_FILE" ]]; then
        echo "Restoring systems.dat from backup"
        cp "$BACKUP_SYSTEMS_FILE" "$DESTINATION_SYSTEMS_FILE"
        delete_cores
        reset_systems_cores
        rm "$BACKUP_SYSTEMS_FILE"
        echo "Default systems restored"
    else
        echo "No backup found"
    fi
}

restore_default_systems
