#!/bin/bash

set -euo pipefail

cd "$(dirname "$(readlink -f "$0")")"

#!/bin/bash

# Path to the source cores.cfg file
source_cfg="cores.cfg"

# Path to the target cores.cfg file
target_cfg="/opt/rgbpi/ui/data/cores.cfg"

# Check if the source file exists
if [ ! -f "$source_cfg" ]; then
    echo "Source cores.cfg file not found: $source_cfg"
    exit 1
fi

# Check if the target file exists
if [ ! -f "$target_cfg" ]; then
    echo "Target cores.cfg file not found: $target_cfg"
    exit 1
fi

# Read data from source_cfg and append or change data in target_cfg
while IFS= read -r line; do
    # Check if the line is already present in the target_cfg
    if grep -q "^$line$" "$target_cfg"; then
        echo "Line already exists in target cores.cfg: $line"
    else
        # Append the line to the target_cfg
        echo "$line" >> "$target_cfg"
        echo "Line appended to target cores.cfg: $line"
    fi
done < "$source_cfg"

echo "Script execution completed."
