#!/bin/bash

# New content for the first configuration file
new_content_cfg1=$(cat <<EOF
run_ahead_enabled = "false"
video_frame_delay_auto = "false"
run_ahead_frames = "0"
run_ahead_hide_warnings = "false"
run_ahead_secondary_instance = "false"
audio_dsp_plugin = "/opt/rgbpi/ui/data/dsp_filters/stereo.dsp"
video_smooth = "true"
EOF
)

# New content for the second configuration file
new_content_cfg2=$(cat <<EOF
input_libretro_device_p1 = "1"
input_libretro_device_p2 = "1"
input_libretro_device_p3 = "1"
input_libretro_device_p4 = "1"
input_libretro_device_p5 = "1"
input_player1_analog_dpad_mode = "1"
input_player1_btn_l = "15"
input_player1_btn_l2 = "10"
input_player1_btn_r = "13"
input_player1_btn_r2 = "11"
input_player1_btn_r3 = "-1"
input_player1_stk_r_x+ = "22"
input_player1_stk_r_x- = "23"
input_player1_stk_r_y+ = "21"
input_player1_stk_r_y- = "20"
input_player2_analog_dpad_mode = "1"
input_player3_analog_dpad_mode = "1"
input_player4_analog_dpad_mode = "1"
input_player5_analog_dpad_mode = "1"
input_remap_port_p1 = "0"
input_remap_port_p2 = "1"
input_remap_port_p3 = "2"
input_remap_port_p4 = "3"
input_remap_port_p5 = "4"
EOF
)


# Path to the first configuration file
cfg_file_path1="/media/usb1/gameconfig/sys_override/nds.cfg"

# Path to the second configuration file
cfg_file_path2="/media/usb1/remaps/system/melonDS DS/melonDS DS.rmp"

# Path to the cores configuration file
cores_cfg_file_path="/opt/rgbpi/ui/data/cores.cfg"

# Write new content to the first configuration file
echo "$new_content_cfg1" > "$cfg_file_path1"

# Write new content to the second configuration file
echo "$new_content_cfg2" > "$cfg_file_path2"

# Replace specific lines in the cores configuration file
sed -i 's/^melonds_screen_layout1 = .*/melonds_screen_layout1 = "bottom"/' "$cores_cfg_file_path"
sed -i 's/^melonds_screen_layout2 = .*/melonds_screen_layout2 = "rotate-right"/' "$cores_cfg_file_path"
sed -i 's/^melonds_screen_layout3 = .*/melonds_screen_layout3 = "rotate-left"/' "$cores_cfg_file_path"
sed -i 's/^melonds_screen_gap = .*/melonds_screen_gap = "18"/' "$cores_cfg_file_path"

echo "Configuration files updated successfully."


