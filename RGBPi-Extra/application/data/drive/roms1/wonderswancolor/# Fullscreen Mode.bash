#!/bin/bash

# New content for the first configuration file
new_content_cfg1=$(cat <<EOF
dynares_mode = "custom"
video_scale_integer = "false"
aspect_ratio_index = "21"
video_fullscreen = "false"
video_force_aspect = "true"
audio_dsp_plugin = "/opt/rgbpi/ui/data/dsp_filters/stereo.dsp"
video_font_path = "/opt/rgbpi/ui/raassets/fonts/native.ttf"
video_font_size = "6.000000"
rgui_aspect_ratio_lock = "1"
EOF
)


# Path to the first configuration file
cfg_file_path1="/opt/rgbpi/ui/tweaks/sys_overrides/wonderswancolor.cfg"

# Write new content to the first configuration file
echo "$new_content_cfg1" > "$cfg_file_path1"


echo "Configuration files updated successfully."