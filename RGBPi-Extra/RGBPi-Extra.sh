#!/bin/bash
set -euo pipefail
cd "$(dirname "$(readlink -f "$0")")"
python application/main.py