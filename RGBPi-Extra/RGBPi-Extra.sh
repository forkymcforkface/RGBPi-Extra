#!/bin/bash
set -euo pipefail
cd "$(dirname "$(readlink -f "$0")")"
if grep -q bookworm /etc/os-release; then
    python3.9 application/main.py
else
    python3 application/main.py
fi
