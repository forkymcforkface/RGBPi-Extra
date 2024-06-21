#!/bin/bash

# New content for the first configuration file
new_content_cfg1=$(cat <<EOF
aspect_ratio_index = "24"
run_ahead_enabled = "false"
video_frame_delay_auto = "false"
run_ahead_frames = "0"
run_ahead_hide_warnings = "false"
run_ahead_secondary_instance = "false"
audio_dsp_plugin = "/opt/rgbpi/ui/data/dsp_filters/stereo.dsp"
EOF
)


# Path to the first configuration file
cfg_file_path1="/opt/rgbpi/ui/tweaks/sys_overrides/psp.cfg"

# Write new content to the first configuration file
echo "$new_content_cfg1" > "$cfg_file_path1"


echo "Configuration files updated successfully."