#!/bin/bash
set -euo pipefail
cd "$(dirname "$(readlink -f "$0")")"
mv -vn /opt/rgbpi/ui/raassets/sounds/unlock.ogg /opt/rgbpi/ui/raassets/sounds/unlock.ogg.bak
cp -v files/unlock.ogg /opt/rgbpi/ui/raassets/sounds/unlock.ogg