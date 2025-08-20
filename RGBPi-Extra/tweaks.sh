#!/bin/bash
set -e
cd "$(dirname "$(readlink -f "$0")")"
python3 application/rgbpi_tweaks.py
