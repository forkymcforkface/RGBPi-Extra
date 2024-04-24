#!/bin/bash

# Path to the config.ini file
config_file="/opt/rgbpi/ui/config.ini"

# New value for adv_mode
new_value="adv_mode = user"

# Check if the config.ini file exists
if [ -f "$config_file" ]; then
    # Use sed to find and replace the line with the specified value
    sed -i 's/^adv_mode\s*=.*/'"$new_value"'/' "$config_file"
    echo "Value updated successfully."
else
    echo "Config file not found: $config_file"
fi

reboot