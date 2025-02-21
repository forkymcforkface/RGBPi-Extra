#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Correct kodi.sh timings
script_content='#!/bin/bash

# Timings to add
timings=(
    "320 1 20 32 45 240 1 2 3 16 0 0 0 60.000000 0 6514560 1"
    "720 1 46 69 100 480 1 3 6 34 0 0 0 30 1 14670150 1"
    "720 1 29 69 117 576 1 7 6 38 0 0 0 25 1 14656125 1"
    "640 1 41 61 89 480 1 3 6 34 0 0 0 30 1 13038390 1"
)

# File path
file="/opt/rgbpi/ui/data/timings.dat"

# Check if the timings already exist in the file
for line in "${timings[@]}"; do
    if ! grep -qF "$line" "$file"; then
        echo "$line" >> "$file"
    fi
done

# Execute Kodi
kodi
'

# File path to kodi.sh
kodi_script="/opt/rgbpi/kodi.sh"

# Backup the original kodi.sh file
cp "$kodi_script" "$kodi_script.backup"

# Write new content to kodi.sh
echo "$script_content" > "$kodi_script"

echo "kodi.sh updated successfully."

# Correct Kodi in timings.dat
timings=(
    "320 1 20 32 45 240 1 2 3 16 0 0 0 60.000000 0 6514560 1"
    "720 1 46 69 100 480 1 3 6 34 0 0 0 30 1 14670150 1"
    "720 1 29 69 117 576 1 7 6 38 0 0 0 25 1 14656125 1"
    "640 1 41 61 89 480 1 3 6 34 0 0 0 30 1 13038390 1"
)

file="/opt/rgbpi/ui/data/timings.dat"

# Remove all data from the file
> "$file"

# Add the new data to the file
for line in "${timings[@]}"; do
    echo "$line" >> "$file"
done
rm -rf /usr/share/kodi/addons/skin.confluence.480/media/DialogCloseButton.png
rm -rf /usr/share/kodi/addons/skin.confluence.480/media/DialogCloseButton-focus.png
rm -rf /usr/share/kodi/addons/skin.confluence.480/media/kodi-logo.png
rm -rf /usr/share/kodi/addons/skin.confluence.480/media/separator2.png
rm -rf /usr/share/kodi/addons/skin.confluence.480/media/separator_vertical.png
rm -rf /usr/share/kodi/addons/skin.confluence.480/media/Confluence_Logo.png
rm -rf /usr/share/kodi/addons/plugin.close.kodi


sudo reboot