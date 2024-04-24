#!/bin/bash

# Path to the scraper.dat file
scraper_dat="/opt/rgbpi/ui/data/scraper/scraper.dat"
# Backup path
backup_path="/opt/rgbpi/ui/data/scraper/scraper_backup.dat"

# Check if the backup file exists
if [ -f "$backup_path" ]; then
    # Restore the backup to the scraper.dat file
    cp "$backup_path" "$scraper_dat"
    echo "Scraper.dat file restored from backup."
else
    echo "Backup file not found: $backup_path"
fi
