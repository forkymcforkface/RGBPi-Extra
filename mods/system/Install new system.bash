#!/usr/bin/env bash

set -euo pipefail

# Directory setup
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
NEW_CORES_DIR="$ROOT_DIR/RGBPi-Extra/application/data/new_cores"
SOURCE_SYSTEMS_FILE="$NEW_CORES_DIR/!new_cores.dat"
DESTINATION_SYSTEMS_FILE="/opt/rgbpi/ui/data/systems.dat"
BACKUP_SYSTEMS_FILE="/opt/rgbpi/ui/data/systems.dat.bak"
DRIVE="$(echo "$ROOT_DIR" | cut -d/ -f3)"
SYSTEMS_CORES_FILE="/media/$DRIVE/gameconfig/sys_override/systems_cores.cfg"
SYSTEMS_CORES_TEMPLATE='[Systems]\n'

backup_systems_file() {
    if [[ ! -f "$BACKUP_SYSTEMS_FILE" ]]; then
        echo "Backing up systems.dat"
        cp "$DESTINATION_SYSTEMS_FILE" "$BACKUP_SYSTEMS_FILE"
    fi
}

system_exists_in_cfg() {
    local system="$1"
    [[ -f "$SYSTEMS_CORES_FILE" ]] && grep -q "^$system" "$SYSTEMS_CORES_FILE"
}

system_exists_in_dat() {
    local system="$1"
    [[ -f "$DESTINATION_SYSTEMS_FILE" ]] && grep -q "^\"$system\"" "$DESTINATION_SYSTEMS_FILE"
}

update_systems_cores() {
    local system="$1" core="$2"
    if system_exists_in_cfg "$system"; then
        echo "Entry for $system already in systems_cores.cfg"
        return
    fi
    echo "Updating systems_cores.cfg"
    mkdir -p "$(dirname "$SYSTEMS_CORES_FILE")"
    [[ -f "$SYSTEMS_CORES_FILE" ]] || echo -e "$SYSTEMS_CORES_TEMPLATE" > "$SYSTEMS_CORES_FILE"
    echo "$system = $core" >> "$SYSTEMS_CORES_FILE"
}

append_system_data() {
    local system="$1" name="$2" release="$3" developer="$4" formats="$5" core="$6" bashhelper="$7"
    backup_systems_file
    if system_exists_in_dat "$system"; then
        echo "$system already exists in systems.dat"
        return
    fi
    echo "Appending system data to systems.dat"
    printf '\n"%s","%s","%s","%s","%s","%s"' "$system" "$name" "$release" "$developer" "$formats" "${bashhelper:-$core}" >> "$DESTINATION_SYSTEMS_FILE"
}

copy_core_file() {
    local core="$1"
    echo "Copying core $core"
    cp "$NEW_CORES_DIR/$core" "/opt/retroarch/cores/$core"
    local info_file="${core%.so}.info"
    if [[ -f "$NEW_CORES_DIR/$info_file" ]]; then
        cp "$NEW_CORES_DIR/$info_file" "/opt/retroarch/cores/$info_file"
    else
        echo "Missing $info_file" >&2
        return 1
    fi
    local cache="/opt/retroarch/cores/core_info.cache"
    [[ -f "$cache" ]] && rm "$cache"
}

copy_bashhelper_file() {
    local bashhelper="$1"
    echo "Copying bashhelper $bashhelper"
    cp "$NEW_CORES_DIR/$bashhelper" "/opt/retroarch/cores/$bashhelper"
}

install_core() {
    local target_name="$1"
    local found=0
    while IFS=',' read -r system name release developer formats core bashhelper _; do
        system=$(echo "$system" | tr -d '"')
        name=$(echo "$name" | tr -d '"')
        release=$(echo "$release" | tr -d '"')
        developer=$(echo "$developer" | tr -d '"')
        formats=$(echo "$formats" | tr -d '"')
        core=$(echo "$core" | tr -d '"')
        bashhelper=$(echo "$bashhelper" | tr -d '"')
        if [[ "$name" == "$target_name" ]]; then
            found=1
            echo "Installing $name"
            copy_core_file "$core"
            [[ -n "$bashhelper" ]] && copy_bashhelper_file "$bashhelper"
            local core_to_use="${bashhelper:-$core}"
            update_systems_cores "$system" "$core_to_use"
            append_system_data "$system" "$name" "$release" "$developer" "$formats" "$core" "$bashhelper"
            echo "System installed successfully"
            break
        fi
    done < <(tail -n +2 "$SOURCE_SYSTEMS_FILE")
    [[ $found -eq 1 ]] || echo "System $target_name not found" >&2
}

list_systems() {
    echo "Available systems:"
    tail -n +2 "$SOURCE_SYSTEMS_FILE" | awk -F',' '{gsub(/"/,""); print " - "$2}'
}

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <system name>"
    list_systems
    exit 1
fi

install_core "$1"
