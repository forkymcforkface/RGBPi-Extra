#!/bin/bash

# Define source and destination
SOURCE_FILE="/opt/rgbpi/ui/data/retroarch.cfg"
CORES_DIRECTORY="/opt/retroarch/cores/"

# Extract the base destination path from the retroarch.cfg file
BASE_DESTINATION=$(grep 'rgui_config_directory' "$SOURCE_FILE" | cut -d '"' -f 2)

# Check if the base destination was found in the file
if [ -z "$BASE_DESTINATION" ]; then
  echo "The rgui_config_directory line was not found in $SOURCE_FILE."
  exit 1
fi

# Iterate over each .info file in the cores directory
for INFO_FILE in "$CORES_DIRECTORY"*.info; do
  # Extract the core name from the .info file
  CORE_NAME=$(grep 'corename =' "$INFO_FILE" | cut -d '"' -f 2)
  
  # Check if the core name was found in the file
  if [ -z "$CORE_NAME" ]; then
    echo "The corename line was not found in $INFO_FILE."
    continue
  fi

  # Remove any text within parentheses and trim leading/trailing whitespace
  CORE_NAME=$(echo "$CORE_NAME" | sed 's/ *([^)]*)*//g' | xargs)
  
  # Replace underscores with spaces in the core name
  CORE_NAME=$(echo "$CORE_NAME" | sed 's/_/ /g')
  USER_FOLDER="$CORE_NAME"
  NEW_FILE_NAME="$CORE_NAME.cfg"

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

  echo "File for core $CORE_NAME has been copied, renamed, modified, and updated with the new setting successfully."
done
