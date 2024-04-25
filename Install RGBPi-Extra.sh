#!/bin/bash

set -o pipefail
timedatectl set-timezone UTC
timedatectl set-ntp true

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
installer_url="https://raw.githubusercontent.com/forkymcforkface/RGBPi-Extra/main/RGBPi-Extra/application/installer.py"
installer_file="$script_dir/installer.py"

if wget -q -O "$installer_file" "$installer_url"; then
    python3 "$installer_file"
    rm "$0"
fi

