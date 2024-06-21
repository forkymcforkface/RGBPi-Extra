#!/bin/bash

# Define paths
ORIGINAL_CFG="/opt/rgbpi/ui/raassets/themes/bw.cfg"
BACKUP_CFG="/opt/rgbpi/ui/raassets/themes/bw.cfg.bak"

# Check if the backup file exists
if [ -f "$BACKUP_CFG" ]; then
    # Restore the backup
    cp "$BACKUP_CFG" "$ORIGINAL_CFG"
    echo "Backup restored successfully."
else
    echo "Backup file bw.cfg.bak does not exist."
fi
