#!/bin/bash

# Define source and destination
SOURCE_FILE="/opt/rgbpi/ui/data/retroarch.cfg"
HISTORY_FILE="/root/.config/retroarch/content_history.lpl"
CORES_DIRECTORY="/opt/retroarch/cores/"

# Extract the latest run game's core path
LATEST_CORE_PATH=$(grep -m 1 '"core_path":' "$HISTORY_FILE" | awk -F '"' '{print $4}')

# Check if the latest core path was found in the history file
if [ -z "$LATEST_CORE_PATH" ]; then
  echo "The latest core path was not found in $HISTORY_FILE."
  exit 1
fi

# Extract the core name from the core path
CORE_NAME=$(basename "$LATEST_CORE_PATH" | sed 's/_libretro.so//')

# Find the corresponding .info file
INFO_FILE=$(find "$CORES_DIRECTORY" -name "$CORE_NAME*.info")

if [ -z "$INFO_FILE" ]; then
  echo "The .info file for core $CORE_NAME was not found."
  exit 1
fi

CORE_DISPLAY_NAME=$(grep 'corename =' "$INFO_FILE" | cut -d '"' -f 2)

# Check if the core name was found in the file
if [ -z "$CORE_DISPLAY_NAME" ]; then
  echo "The corename line was not found in $INFO_FILE."
  exit 1
fi

# Remove any text within parentheses and trim leading/trailing whitespace
CORE_DISPLAY_NAME=$(echo "$CORE_DISPLAY_NAME" | sed 's/ *([^)]*)*//g' | xargs)

# Replace underscores with spaces in the core name
CORE_DISPLAY_NAME=$(echo "$CORE_DISPLAY_NAME" | sed 's/_/ /g')
USER_FOLDER="$CORE_DISPLAY_NAME"
NEW_FILE_NAME="$CORE_DISPLAY_NAME.cfg"

# Extract the base destination path from the retroarch.cfg file
BASE_DESTINATION=$(grep 'rgui_config_directory' "$SOURCE_FILE" | cut -d '"' -f 2)

# Check if the base destination was found in the file
if [ -z "$BASE_DESTINATION" ]; then
  echo "The rgui_config_directory line was not found in $SOURCE_FILE."
  exit 1
fi

# Combine base destination with the core name to form the final destination folder
DESTINATION_FOLDER="$BASE_DESTINATION/$USER_FOLDER"

# Check if destination folder exists, create if it doesn't
if [ ! -d "$DESTINATION_FOLDER" ]; then
  mkdir -p "$DESTINATION_FOLDER"
fi

# Copy and rename the file
cp "$SOURCE_FILE" "$DESTINATION_FOLDER/$NEW_FILE_NAME"

# Remove the specified lines from the new file
sed -i '/settings_show_user_interface = "false"/d' "$DESTINATION_FOLDER/$NEW_FILE_NAME"
sed -i '/rgbpi_restrict_ui = "true"/d' "$DESTINATION_FOLDER/$NEW_FILE_NAME"

# Add the required line to the new file
echo 'notification_show_config_override_load = "false"' >> "$DESTINATION_FOLDER/$NEW_FILE_NAME"

echo "File for core $CORE_DISPLAY_NAME has been copied, renamed, modified, and updated with the new setting successfully."
