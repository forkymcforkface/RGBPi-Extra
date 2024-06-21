#!/bin/bash
set -euo pipefail
cd "$(dirname "$(readlink -f "$0")")"
cp -vf files/retroarch.cfg /root/.config/retroarch/retroarch.cfg