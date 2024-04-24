#!/bin/bash

# Lines to remove from /boot/config.txt
lines_to_remove=(
    "blacklist btbcm"
    "blacklist bnep"
    "blacklist bluetooth"
    "dtoverlay=disable-bt"
)

# Path to /boot/config.txt
boot_file="/boot/config.txt"

# Check if /boot/config.txt exists
if [ -f "$boot_file" ]; then
    # Loop through lines to remove and remove them from /boot/config.txt
    for line in "${lines_to_remove[@]}"; do
        # Use sed to remove the line from /boot/config.txt
        sudo sed -i "/$line/d" "$boot_file"
        echo "Removed: $line"
    done
    echo "Configuration updated successfully."
else
    echo "Error: /boot/config.txt not found."
fi

# Reenable Bluetooth
sudo systemctl enable hciuart
sudo systemctl enable bluetooth

echo "Bluetooth reenabled. Rebooting..."
sudo reboot
