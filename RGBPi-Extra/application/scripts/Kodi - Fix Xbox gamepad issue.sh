#!/bin/bash

# Define the rules
rules=(
    "# Microsoft Controllers"
    'SUBSYSTEM=="input", ATTRS{name}=="Microsoft X-Box One pad", KERNEL=="event*", MODE="0666", ENV{LIBINPUT_IGNORE_DEVICE}="1"'
    'SUBSYSTEM=="input", ATTRS{name}=="Microsoft X-Box One pad", KERNEL=="event*", MODE="0666", ENV{ID_INPUT_JOYSTICK}="1"'
    'SUBSYSTEM=="input", ATTRS{name}=="Xbox Wireless Controller", KERNEL=="event*", MODE="0666", ENV{LIBINPUT_IGNORE_DEVICE}="1"'
    'SUBSYSTEM=="input", ATTRS{name}=="Xbox Wireless Controller", KERNEL=="event*", MODE="0666", ENV{ID_INPUT_JOYSTICK}="1"'
)

# File path
rules_file="/etc/udev/rules.d/10-local.rules"

# Check if each rule already exists in the file and append if not
for rule in "${rules[@]}"; do
    if ! grep -qF "$rule" "$rules_file"; then
        echo "$rule" | sudo sed -i '$ a\'"$rule" "$rules_file"
    fi
done

echo "Xbox controller rules added to udev rules."
