
# RGBPi-Extra

RGBpi-Extra is a UI that allows you to apply a collection of unofficial scripts for [RGBPiOS](https://www.rgb-pi.com/#os), enabling you to quickly and easily install emulators, ports, and libretrocores that haven't been included in RGBPi for various reasons. Additionally, it provides the capability to enable RetroArch features that are disabled by default. These scripts are experimental in nature and may not be fully stable. The concept for creating this repository was inspired by [RetroPie-Extra](https://github.com/Exarkuniv/RetroPie-Extra) and represents a collaborative effort across multiple parties within the RGBPi community.




I have found new scripts made by other people and added them to this Repo. I dont take credit for any of them, other then the ones I made. RGBPi OS uses a custom kernel driver and custom compiled version of retroarch. Pre-Compiled Cores from libretro, Retropie, batocera, lakka will not work (mostly). I have found that compiling cores on the RGBpi OS itself works best, but can still take some adjustments in the cmake flags.

 **DO NOT ASK QUESTIONS IN DISCORD/TELEGRAM FOR ANY ISSUES YOU MAY RUN INTO.**
 
 **Notes**
- Please use [Discussions](https://github.com/forkymcforkface/RGBPi-Extra/discussions) or [Issues](https://github.com/forkymcforkface/RGBPi-Extra/issues) if you have questions or issues. 

## Installation Options 
## DO NOT INSTALL RGBPI-EXTRA IF YOU ONLY USE AN SD CARD or NFS. 
## EXTERNAL USB DRIVE INSTALLS ONLY
A: Online Installer

1. Download [Install RGBPi-Extra](https://github.com/forkymcforkface/RGBPi-Extra/blob/main/Install%20RGBPi-Extra.sh)
2. Place it in your /roms/ports folder
3. Scan for new games in the rgbpi ui
4. Go to ports in rgbpi ui and run Install RGBPi-Extra
5. The RGBPi-Extra UI will appear allowing you to apply the patch and restart. All cores and BIOS are included in the initial patch, you will have new system folders in your roms folder after reboot.

B: Offline Installer (This will not have the latest minor changes)

1. Download the lastest offline zip [RGBPi-Extra zip installer](https://github.com/forkymcforkface/RGBPi-Extra/releases/)
2. Extract to your usb drive.
3. Scan for games
4. Open rgbpi UI and patch and reboot
5. If you want to get the latest changes, open the rgbpi UI again and go to settings>update. This will get the latest changes.


https://github.com/sd2cv/RGBPi-Extra/assets/99993735/d4a69f9b-47b7-4d27-95e5-2555a1844ca1






## Usage

After installing **RGBPi-Extra** you will now have a RGBPi-Extra folder within ports and within that the RGBPi-Extra launcher

#### Retroarch Settings 
This allows you to add retroarch features that are disabled by default by RGBPi-OS. Currently only boolean shows up in the UI, but you can add any global configs that you would like to /application/data/tweaks/gobal_configs.ini
#### Update Cores
This allows you to updates cores to the lateset manually compiled version. it also allows you replace the nes core with mesen. There is a restore all cores button that will restore all default os4 core. 
#### Tweaks
A collection of scripts to modify RGBPi OS settings, Bullseye settings or just general improvements
#### Settings
Update or Removal of RGBPi-Extra, You will need to rescan for games after updating.

IF YOU ARE REIMAGING YOUR SD CARD YOU MUST REMOVE RGBPI-EXTRA BEFORE DOING SO.


## Updates

1. Go to settings
2. Press update and allow the package to download
3. Press patch and reboot
4. ReScan for games

## Removal

To remove the patch open RGBPi-Extra ui, go to settings and select remove. This is required prior to reimaging your SD card if you are doing so.


If there is a [X] that means it Installs and Plays. 
I'll have a note at the end with some Info about it. if there is NO note or  [ ] **PLEASE LET ME KNOW** if it works for you 

Since we are using CRTs not all cores/emulators will look good. This all depends on the native resolution and fps of the games

#### Emulators 

- [ ] - `box86` -"Box86 emulator"
- [ ] - `openbor` - Beat 'em Up Game Engine (newest version) -
- [X] - `pico8` - Fantasy Game Emulator - **Included in ports from RGBPi OS official**
- [ ] - `supermodel-mechafatnick` - Sega Model 3 Arcade emulator
- [ ] - `supermodel-svn` - Sega Model 3 Arcade emulator
- [X] - `Hypseus-singe` - LaserDisc emulator - **Included in ports from RGBPi OS official**

#### Added Libretro cores

- [X] - `lr-melondsds` - NDS emu - MelonDS port for libretro - **runs great**
- [X] - `lr-mesen-s` - Nes emu - Mesen-S port for libretro
- [X] - `lr-atari5200` - 400, 800, 600 XL, 800XL, 130XE and 5200 game console emulator.
- [X] - `lr-mednafen-vb` - Virtual Boy emulator - **runs great, not pixel perfect**
- [X] - `lr-ppsspp` - PlayStation Portable emu - PPSSPP port for libretro - **works well, included in current patch**
- [X] - `lr-samecdi` - Philips CDI - same_cdi port for libretro - **runs great and at correct resolution, included in current patch**
- [X] - `lr-TIC-80` - Fantasy Game Emulator - **runs great**
- [X] - `lr-virtualjaguar` - Atari Jaguar emulator - **runs ok at beat and has sound issues, included in current patch**
- [X] - `lr-WonderSwan` - WonderSwan and WonderSwan Color emulator - **runs great, included in current patch**
- [X] - `lr-AtariLynx` - Atari Lynx emulator - **runs great, included in current patch**
- [X] - `lr-Videopac` - Videopac/Odyssey emulator - **runs great, included in current patch**


#### Supplementary
- [X] - `LXQT Desktop` - Linux Desktop Environment, optimized for 720x480 - **Installs Runs fine**
- [X] - `firefox-esr` - FireFox-ESR - Formally known as IceWeasel, the Rebranded Firefox Web Browser - **Installs Runs fine**
- [X] - `videolan` - VLC media player - **Installs Runs fine, but cant figure out how to get it out of default 240p**

### Removed broken scripts


## Hall of Fame - Ports added that made it to the official OS release

- [X] - Kodi - Media Player
