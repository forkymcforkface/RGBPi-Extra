# OS4.5 isn't currently supported.


# RGBPi-Extra

RGBpi-Extra is a UI that allows you to apply a collection of unofficial scripts, install new systems/cores, and allow for full* retroarch access for [RGB-Pi OS4](https://www.rgb-pi.com/#os) on the Pi4 and Pi5. The system overrides are advanced features that require manual configuration. These scripts are experimental in nature and may not be fully stable. The concept for creating this repository was inspired by [RetroPie-Extra](https://github.com/Exarkuniv/RetroPie-Extra) and represents a collaborative effort across multiple parties within the RGBPi community. 

Thank you [Ruben](https://github.com/rtomasa) for your guidance so that RGBPi-Extra does not affect the RGB-Pi highscore community.

*This is not part of official OS4 and is not supported. Do not ask for help for issues in discord or telegram of you ise rgbpi-extra.

*when playing high score games via nfs all extra overrides are disabled and runs like stock OS4. This prevents cheating.
 
 **Important Notes**
- Don't use it if you only use an SD card for games. USB game drive supported only. 
- read the FAQ https://github.com/forkymcforkface/RGBPi-Extra/wiki/FAQ
- Please use [Discussions](https://github.com/forkymcforkface/RGBPi-Extra/discussions) or [Issues](https://github.com/forkymcforkface/RGBPi-Extra/issues) if you have questions or issues.

## Installation Options

A: Online Installer

1. Download [Install RGBPi-Extra](https://github.com/forkymcforkface/RGBPi-Extra/blob/main/Install%20RGBPi-Extra.sh)
2. Place it in your /roms/ports folder
3. Scan for new games in the rgbpi ui
4. Go to ports in rgbpi ui and run RGBPi-Extra
5. The RGBPi-Extra UI will appear allowing you to apply make any tweaks

B: Offline Install

1. Download the repo
 - [Pi-4 RGBPi-Extra zip](https://github.com/forkymcforkface/RGBPi-Extra/archive/refs/heads/main.zip)
 - [Pi-5 RGBPi-Extra zip](https://github.com/forkymcforkface/RGBPi-Extra/archive/refs/heads/pi-5.zip)  (Migration of OS4 to Pi5 using this tool https://github.com/forkymcforkface/RGUI-Pi)
3. Open the zip and extract the RGBPi-Extra folder to your ports folder
4. Scan for games
5. Open rgbpi-extra UI and install

## Usage

After installing **RGBPi-Extra** you will now have a RGBPi-Extra folder within ports and within that the RGBPi-Extra launcher

#### Core Updater
This allows you to updates cores to the lateset manually compiled version. it also allows you replace the nes core with mesen. There is a restore all cores button that will restore all default os4 core. 
#### System Manager
This allows you to install cores that do not come installed on OS4 by defualt. You can select the core you want, drop the roms into the new core folder in your roms dir and you are set. BIOS are already included. See core selection at the bottom of this page.
#### Tweaks
A collection of scripts to modify RGBPi OS settings, Bullseye settings or just general improvements
#### Settings
Update or Removal of RGBPi-Extra, You will need to rescan for games after updating.

## Updates

1. Go to settings
2. Press update and allow the package to download and update

Since we are using CRTs not all cores/emulators will look good. This all depends on the native resolution and fps of the games

#### Additons
Zapper core in New Systems allows for the use of the Arduino NES zapper hardware.
https://github.com/riggles1/Zapper-Arduino

Sega Channel Revival core in New Systems allows for BillyTimeGames larger sized ROMs.
https://github.com/BillyTimeGames/Genesis-Plus-GX-Expanded-Rom-Size

BennuGD core in New System allows for BennuGD games like Streets of Rage Remake to be played natively. 
Instructions: Extract and copy Streets of Rage Remake (folder containing the .exe) to the "bennugd" roms folder on the USB drive. 
Start the .exe on your computer and map your controllers, exit the game (saves this to the USB), plug the USB into the Pi, mount and scan. The game should be in proper 240p if the core was added correctly.
https://github.com/diekleinekuh/BennuGD_libretro/

#### Added Libretro cores

- [X] - `lr-mame2003-plus` - MAME emu - mame2003-plus port for libretro - **runs great**
- [X] - `lr-opera` - 3DO Emu - 3DO port for libretro - **runs great*, Pi5 only*
- [X] - `lr-melondsds` - NDS emu - MelonDS port for libretro - **runs 2d games fullspeed on Pi4, Pi5 everything runs**
- [X] - `lr-dolphin` - Gamecube/wii emu - Dolphin port for libretro - **runs great, Pi5 only**
- [X] - `lr-mesen` - NES emu - Mesen port for libretro **higher accuracy, fullspeed on Pi4**
- [X] - `lr-atari5200` - 400, 800, 600 XL, 800XL, 130XE and 5200 game console emulator.
- [X] - `lr-mednafen-vb` - Virtual Boy emulator - **runs great, not pixel perfect**
- [X] - `lr-mednafen-pcfx` - NEC PC-FX emulator **fullspeed on Pi4**
- [X] - `lr-ppsspp` - PlayStation Portable emu - PPSSPP port for libretro - **works well, included in current patch**
- [X] - `lr-samecdi` - Philips CDI - same_cdi port for libretro - **runs great and at correct resolution, included in current patch**
- [X] - `lr-TIC-80` - Fantasy Game Emulator - **runs great**
- [X] - `lr-virtualjaguar` - Atari Jaguar emulator - **runs ok on pi4, runs well on pi5, not all games work, included in current patch**
- [X] - `lr-WonderSwan` - WonderSwan and WonderSwan Color emulator - **runs great, included in current patch**
- [X] - `lr-AtariLynx` - Atari Lynx emulator - **runs great, included in current patch**
- [X] - `lr-Videopac` - Videopac/Odyssey emulator - **runs great, included in current patch**

#### Example of custom controller keys+keys (per USB controller device ID)

Navigate in WinSCP or similar to opt\rgbpi\ui\data\joyconfig\
select the .cfg file of your controller device (for example USB_Gamepad__121_17.cfg) 
and edit the keys to your preferences, enable button + hotkey functions for fast-forward for example.
```
input_device = "USB Gamepad "
input_device_display_name = "USB Gamepad"
input_vendor_id = "121"
input_product_id = "17"
input_btn_style = "snes"
input_up_axis = "-1"
input_down_axis = "+1"
input_left_axis = "-0"
input_right_axis = "+0"
input_a_btn = "4"
input_b_btn = "2"
input_x_btn = "3"
input_y_btn = "1"
input_l_btn = "6"
input_r_btn = "7"
input_l2_btn = "0"
input_r2_btn = "5"
input_start_btn = "9"
input_select_btn = "8"

input_enable_hotkey_btn = "8"
input_menu_toggle_btn = "9"
input_hold_fast_forward_btn = "6"
input_volume_down_btn = "1"
input_volume_up_btn = "3"


input_save_state_axis = "+1"
input_load_state_axis = "-1"
input_state_slot_increase_axis = "+0"
input_state_slot_decrease_axis = "-0"
input_save_state_btn = "h0down"
input_load_state_btn = "h0up"
input_state_slot_increase_btn = "h0right"
input_state_slot_decrease_btn = "h0left"
```

If your USB controller device is an Arduino adapter for 2+ controllers, you'll need to add the following strings to the end of cmdline.txt (boot partition of the SD card)
Has to be on the same line of code, just add this at the very end.
For the Arduino Leonardo add:
usbhid.quirks=0x2341:0x8036:0x040
For the Arduino Micro add:
usbhid.quirks=0x2341:0x8037:0x040 



