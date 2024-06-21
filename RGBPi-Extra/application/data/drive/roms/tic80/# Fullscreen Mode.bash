#!/bin/bash

# New content for the first configuration file
new_content_cfg1=$(cat <<EOF
dynares_mode = "custom"
aspect_ratio_index = "24"
video_scale_integer = "false"
run_ahead_enabled = "true"
video_frame_delay_auto = "false"
run_ahead_frames = "1"
run_ahead_hide_warnings = "false"
run_ahead_secondary_instance = "false"
audio_dsp_plugin = "/opt/rgbpi/ui/data/dsp_filters/stereo.dsp"
video_font_size = "48.000000"
EOF
)


# Path to the first configuration file
cfg_file_path1="/opt/rgbpi/ui/tweaks/sys_overrides/tic80.cfg"

# Write new content to the first configuration file
echo "$new_content_cfg1" > "$cfg_file_path1"


echo "Configuration files updated successfully."