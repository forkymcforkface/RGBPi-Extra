#!/bin/bash

image_paths=(
    "/opt/rgbpi/ui/images/boot_2.bmp"
    "/opt/rgbpi/ui/images/boot_3.bmp"
    "/opt/rgbpi/ui/images/boot_4.bmp"
    "/opt/rgbpi/ui/images/boot_5.bmp"
)

small_bmp="small.bmp"
{
    printf '\x42\x4D'
    printf '\x1E\x00\x00\x00'
    printf '\x00\x00'
    printf '\x00\x00'
    printf '\x1A\x00\x00\x00'
    printf '\x0C\x00\x00\x00'
    printf '\x01\x00'
    printf '\x01\x00'
    printf '\x01'
    printf '\x18'
    printf '\x00\x00'
    printf '\x00\x00\x00'
    printf '\x00\x00\x00\x00'
    printf '\x00\x00\x00\x00'
    printf '\x00\x00'
    printf '\x00\x00'
    printf '\x00\x00\x00'
} > "$small_bmp"

for image_path in "${image_paths[@]}"; do
    cp "$small_bmp" "$image_path"
done

rm "$small_bmp"

echo "Image files have been replaced with 1x1 pixel BMPs."

