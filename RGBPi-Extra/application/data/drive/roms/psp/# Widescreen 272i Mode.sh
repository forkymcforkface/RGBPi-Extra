#!/bin/bash

# New content for the first configuration file
new_content_cfg1=$(cat <<EOF
dynares_mode = "custom"
video_fullscreen_x = "640"
video_fullscreen_y = "480"
custom_viewport_height = "480"
custom_viewport_width = "640"
aspect_ratio_index = "21"
run_ahead_enabled = "false"
video_frame_delay_auto = "false"
run_ahead_frames = "0"
run_ahead_hide_warnings = "false"
run_ahead_secondary_instance = "false"
audio_dsp_plugin = "/opt/rgbpi/ui/data/dsp_filters/stereo.dsp"
dynares_flicker_reduction = "true"
video_font_path = "/opt/rgbpi/ui/raassets/fonts/native.ttf"
video_font_size = "12.000000"
EOF
)


# Path to the first configuration file
cfg_file_path1="/opt/rgbpi/ui/tweaks/sys_overrides/psp.cfg"

# Write new content to the first configuration file
echo "$new_content_cfg1" > "$cfg_file_path1"


echo "Configuration files updated successfully."