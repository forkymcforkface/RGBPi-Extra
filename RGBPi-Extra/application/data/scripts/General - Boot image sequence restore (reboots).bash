#!/bin/bash

image_paths=(
    "/opt/rgbpi/ui/images/boot_2.bmp"
    "/opt/rgbpi/ui/images/boot_3.bmp"
    "/opt/rgbpi/ui/images/boot_4.bmp"
    "/opt/rgbpi/ui/images/boot_5.bmp"
)

src_dir="/opt/rgbpi/ui/images/src"

for image_path in "${image_paths[@]}"; do
    src_path="$src_dir/$(basename "$image_path")"
    if [ -f "$src_path" ]; then
        cp "$src_path" "$image_path"
        echo "Restored $image_path from $src_path"
    else
        echo "Source file for $image_path not found in $src_dir"
    fi
done

echo "Image files have been restored from $src_dir."
