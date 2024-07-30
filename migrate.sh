#!/bin/bash

MOUNT_POINT="/mnt/usb_rgbpi"
TARGET_DIR="/opt/rgbpi"
DEST_DIR="/opt"
CONFIG_FILE="/opt/rgbpi/ui/config.ini"
LOG_FILE="/tmp/rgbpi_script.log"
RSYNC_PID=0
TTY_DEVICE="/dev/tty1"

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root" | tee -a $LOG_FILE > $TTY_DEVICE
  exit 1
fi

log_and_echo() {
  local MESSAGE=$1
  echo "$MESSAGE" | tee -a $LOG_FILE | tee $TTY_DEVICE
}

cleanup() {
  if [ $RSYNC_PID -ne 0 ]; then
    kill $RSYNC_PID
    wait $RSYNC_PID 2>/dev/null
  fi
  umount $MOUNT_POINT 2>/dev/null
  rm -rf $MOUNT_POINT
  log_and_echo "Cleanup done."
  exit 1
}

trap cleanup SIGINT

clear
mkdir -p $MOUNT_POINT

# Function to find and mount the first available drive that is not the current mount point
mount_drive() {
  ROOT_DEV=$(df / | tail -1 | awk '{print $1}')
  CURRENT_MOUNT=$(df . | tail -1 | awk '{print $1}')
  USB_DEVICES=$(lsblk -o NAME,TYPE | grep 'disk' | grep -v "$ROOT_DEV" | grep -v "$CURRENT_MOUNT" | grep -vE 'mmcblk|loop' | awk '{print $1}')

  for USB_DEVICE in $USB_DEVICES; do
    PARTITIONS=$(lsblk -ln -o NAME | grep "^${USB_DEVICE}")

    for PARTITION in $PARTITIONS; do
      if mount "/dev/$PARTITION" $MOUNT_POINT 2>/dev/null; then
        if [ -d "$MOUNT_POINT/$TARGET_DIR" ]; then
          return 0
        else
          umount $MOUNT_POINT 2>/dev/null
        fi
      fi
    done
  done

  return 1
}

ERROR_MESSAGE="RGB-Pi OS4 Application not found, burn the OS4 image onto a USB drive and insert it into the Pi5 before running."

if ! mount_drive; then
  log_and_echo "$ERROR_MESSAGE"
  cleanup
fi

log_and_echo "Copying OS4 Application to Pi5"
stdbuf -oL rsync -a --info=progress2 $MOUNT_POINT/$TARGET_DIR/ $DEST_DIR/rgbpi/ > >(tee /dev/tty1) &
RSYNC_PID=$!
wait $RSYNC_PID
RSYNC_EXIT_CODE=$?

if [ $RSYNC_EXIT_CODE -ne 0 ]; then
  log_and_echo "Rsync failed with exit code $RSYNC_EXIT_CODE. Exiting."
  cleanup
fi

log_and_echo "OS4 Application copied successfully."

AUTOSTART_FILE="$DEST_DIR/rgbpi/autostart.sh"
cat <<EOL > $AUTOSTART_FILE
#!/bin/bash
cd /opt/rgbpi/ui 2> /dev/null
rm -rf /opt/rgbpi/ui/temp/* 2> /dev/null
CRT_TYPE=\$(grep '^crt_type' /opt/rgbpi/ui/config.ini 2> /dev/null | cut -d'=' -f2 | tr -d ' ')
if [[ "\$CRT_TYPE" == "arcade_15_25_31" || "\$CRT_TYPE" == "ms2930" || "\$CRT_TYPE" == "arcade_31" ]]; then
  if [ ! -f /opt/retroarch/retroarch_15khz ] && [ -f /opt/retroarch/retroarch ]; then
    mv /opt/retroarch/retroarch /opt/retroarch/retroarch_15khz
    mv /opt/retroarch/retroarch_31khz /opt/retroarch/retroarch
  fi
elif [[ "\$CRT_TYPE" == "generic_15" || "\$CRT_TYPE" == "arcade_15" || "\$CRT_TYPE" == "arcade_15_25" ]]; then
  if [ ! -f /opt/retroarch/retroarch_31khz ] && [ -f /opt/retroarch/retroarch ]; then
    mv /opt/retroarch/retroarch /opt/retroarch/retroarch_31khz
    mv /opt/retroarch/retroarch_15khz /opt/retroarch/retroarch
  fi
fi
/usr/bin/python3 /opt/rgbpi/ui/rgbpiui.pyc 2> /opt/rgbpi/ui/logs/error.log
EOL

chmod +x $AUTOSTART_FILE

if [ -f "$CONFIG_FILE" ]; then
  sed -i 's/^fst_boot = true$/fst_boot = false/' $CONFIG_FILE
  sed -i 's/^show_kodi = on$/show_kodi = off/' $CONFIG_FILE
  sed -i 's/^wifi = .*$/wifi = off/' $CONFIG_FILE
  sed -i 's/^wifi_ssid = .*$/wifi_ssid = -/' $CONFIG_FILE
  sed -i 's/^wifi_pwd = .*$/wifi_pwd = -/' $CONFIG_FILE
  sed -i 's/^overclock = .*$/overclock = off/' $CONFIG_FILE
fi

sed -i 's/$/ vt.default_red=0,0,0,0,0,0,0,0 vt.default_grn=0,0,0,0,0,0,0,0 vt.default_blu=0,0,0,0,0,0,0,0/' /boot/firmware/cmdline.txt
sed -i '/^pi /d' /etc/sudoers
deluser pi sudo
rm /opt/autostart.sh 2>/dev/null
sync
cleanup
sync
log_and_echo "Rebooting..."
reboot
