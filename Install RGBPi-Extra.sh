#!/bin/bash

set -o pipefail
timedatectl set-timezone UTC
timedatectl set-ntp true

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
installer_url="https://raw.githubusercontent.com/forkymcforkface/RGBPi-Extra/main/RGBPi-Extra/application/installer.py"
installer_file="$script_dir/installer.py"

if wget -q -O "$installer_file" "$installer_url"; then
    if grep -q bookworm /etc/os-release; then
        python3.9 "$installer_file"
    else
        python3 "$installer_file"
    fi
    rm "$0"
else
    echo "Failed to download installer.py from $installer_url"
    exit 1
fi
