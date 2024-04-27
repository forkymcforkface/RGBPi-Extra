#!/bin/bash
set -euo pipefail
cd "$(dirname "$(readlink -f "$0")")"
python_command="python3.9"
if [[ "$(lsb_release -cs)" != "bookworm" ]]; then
    python_command="python3"
fi
$python_command application/main.py
