#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR" || exit

timings=(
    "320 1 20 32 45 240 1 2 3 16 0 0 0 60.000000 0 6514560 1"
    "2624 1 170 252 366 480 1 2 6 36 0 0 0 29.942748 1 53502900 1"
)

file="/opt/rgbpi/ui/data/timings.dat"

> "$file"

for line in "${timings[@]}"; do
    echo "$line" >> "$file"
done

usage() {
  echo "Usage: $0 [--appendconfig=<CONFIG_PATH>] <ROM_PATH>"
  echo "Options:"
  echo "  --appendconfig=<CONFIG_PATH>  Path to the configuration file"
  echo "  <ROM_PATH>                    Path to the ROM file"
  exit 1
}

while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    --appendconfig=*)
      append_config="${key#*=}"
      shift
      ;;
    *)
      break
      ;;
  esac
done

if [ $# -eq 0 ]; then
  usage
fi

rom_path="$1"

if [ -z "$rom_path" ]; then
  echo "Error: ROM path is required."
  usage
fi

if [ ! -f "$rom_path" ]; then
  echo "Error: ROM file '$rom_path' not found."
  exit 1
fi

/opt/retroarch/retroarch --appendconfig="$append_config" -L /opt/retroarch/cores/same_cdi_libretro.so "$rom_path" &
wait
