#!/bin/bash
set -e
cd "$(dirname "$(readlink -f "$0")")"
python3 application/system_manager.py
