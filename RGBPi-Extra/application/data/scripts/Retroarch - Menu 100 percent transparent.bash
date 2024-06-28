#!/bin/bash

# Define paths
ORIGINAL_CFG="/opt/rgbpi/ui/raassets/themes/bw.cfg"
BACKUP_CFG="/opt/rgbpi/ui/raassets/themes/bw.cfg.bak"

# Check if the backup file already exists
if [ ! -f "$BACKUP_CFG" ]; then
    # Backup the original config file
    cp "$ORIGINAL_CFG" "$BACKUP_CFG"
    echo "Backup of bw.cfg created."
else
    echo "Backup file bw.cfg.bak already exists. Skipping backup creation."
fi

# Replace the contents of the original config file
cat << EOF > "$ORIGINAL_CFG"
rgui_entry_normal_color = "0xffb9b9b9"
rgui_entry_hover_color = "0xffffffff"
rgui_title_color = "0xffffffff"
rgui_bg_dark_color = "0x00000000"
rgui_bg_light_color = "0x00000000"
rgui_border_dark_color = "0xFF878787"
rgui_border_light_color = "0xFF878787"
rgui_shadow_color = "0xFF242424"
rgui_particle_color = "0xFF878787"
EOF

echo "bw.cfg has been modified."
