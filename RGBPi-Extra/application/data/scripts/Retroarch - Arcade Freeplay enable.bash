#!/bin/bash

# Configuration file path
config_file="/opt/rgbpi/ui/config.ini"

# Check if Freeplay is already enabled
if grep -q "free_play = on" "$config_file"; then
    echo "Freeplay is already enabled."
else
    # Enable Freeplay
    sed -i 's/free_play = off/free_play = on/' "$config_file"
    echo "Freeplay enabled."
fi
