#!/bin/bash

#remove unused camera driver error in retroarch
ra_file="/root/.config/retroarch/retroarch.cfg"

# Lines to remove
lines_to_remove=(
    "camera_device = \"\""
    "camera_driver = \"video4linux2\""
)

# Check if the configuration file exists
if [ -f "$ra_file" ]; then
    # Loop through lines to remove and remove them from the configuration file
    for line in "${lines_to_remove[@]}"; do
        # Use sed to remove the line from the configuration file
        sed -i "/$line/d" "$ra_file"
        echo "Removed: $line"
    done
    echo "Configuration updated successfully."
else
    echo "Error: Configuration file not found: $ra_file"
fi


#Disable Bluetooth
# Lines to add to /boot/config.txt
lines_to_add=(
    "blacklist btbcm"
    "blacklist bnep"
    "blacklist bluetooth"
    "dtoverlay=disable-bt"
)

# Path to /boot/config.txt
boot_file="/boot/config.txt"

# Check if /boot/config.txt exists
if [ -f "$boot_file" ]; then
    # Loop through lines to add and append them to /boot/config.txt
    for line in "${lines_to_add[@]}"; do
        # Check if the line already exists in /boot/config.txt
        if ! grep -q "$line" "$boot_file"; then
            echo "$line" | sudo tee -a "$boot_file" > /dev/null
            echo "Added: $line"
        else
            echo "Line already exists: $line"
        fi
    done
    echo "Configuration updated successfully."
else
    echo "Error: /boot/config.txt not found."
fi

sudo systemctl disable hciuart
sudo systemctl disable bluetooth

reboot
