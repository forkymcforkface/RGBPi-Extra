#!/bin/bash

# Path to the scraper.dat file
scraper_dat="/opt/rgbpi/ui/data/scraper/scraper.dat"
# Backup path
backup_path="/opt/rgbpi/ui/data/scraper/scraper_backup.dat"

# Function to backup the existing scraper.dat file
backup_scraper_dat() {
    if [ ! -f "$backup_path" ]; then
        cp "$scraper_dat" "$backup_path"
        echo "Backup created: $backup_path"
    else
        echo "Backup already exists: $backup_path"
    fi
}

# Check if the scraper.dat file exists
if [ -f "$scraper_dat" ]; then
    # Backup the existing scraper.dat file
    backup_scraper_dat
    
    # Clear the contents of the scraper.dat file
    : > "$scraper_dat"
    echo "Data removed from scraper.dat."
else
    echo "Scraper.dat file not found: $scraper_dat"
fi
