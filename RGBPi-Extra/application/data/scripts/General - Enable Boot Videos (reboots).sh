#!/bin/bash

systemctl disable boot-image.service
sudo apt-get update
sudo apt-get install -y vlc --no-install-recommends
sudo sed -i 's/geteuid/getppid/' /usr/bin/vlc
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
sudo cp -r "$SCRIPT_DIR/files/ui" /opt/rgbpi
sudo chmod -R 0777 /opt/rgbpi/ui/mods

if ! grep -q "/usr/bin/python3 /opt/rgbpi/ui/mods/boot/boot_videos.py" /opt/rgbpi/autostart.sh; then
    sudo sed -i '1a \/usr\/bin\/python3 \/opt\/rgbpi\/ui\/mods\/boot\/boot_videos.py' /opt/rgbpi/autostart.sh
fi

sync
sudo reboot