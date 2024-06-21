#!/bin/bash

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

pkill -STOP python

if [ -n "$append_config" ]; then
  /opt/retroarch/retroarch --appendconfig="$append_config" -L /opt/retroarch/cores/melondsds_libretro.so "$rom_path" &
else
  /opt/retroarch/retroarch -L /opt/retroarch/cores/melondsds_libretro.so "$rom_path" &
fi

wait
pkill -CONT python
