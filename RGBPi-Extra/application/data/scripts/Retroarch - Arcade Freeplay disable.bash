#!/bin/bash

# Configuration file path
config_file="/opt/rgbpi/ui/config.ini"

# Check if Freeplay is already disabled
if grep -q "free_play = off" "$config_file"; then
    echo "Freeplay is already disabled."
else
    # Disable Freeplay
    sed -i 's/free_play = on/free_play = off/' "$config_file"
    echo "Freeplay disabled."
fi
