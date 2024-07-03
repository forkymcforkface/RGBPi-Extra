
# RGBPi-Extra

RGBpi-Extra is a UI that allows you to apply a collection of unofficial scripts, install new systems, and allow for full retroarch access for [RGBPiOS](https://www.rgb-pi.com/#os). The system overrides are advanced features that require manual configuration. These scripts are experimental in nature and may not be fully stable. The concept for creating this repository was inspired by [RetroPie-Extra](https://github.com/Exarkuniv/RetroPie-Extra) and represents a collaborative effort across multiple parties within the RGBPi community.


I have found new scripts made by other people and added them to this Repo. I dont take credit for any of them, other then the ones I made. 
 
 **Important Notes**
- Please use [Discussions](https://github.com/forkymcforkface/RGBPi-Extra/discussions) or [Issues](https://github.com/forkymcforkface/RGBPi-Extra/issues) if you have questions or issues. DO NOT ASK QUESTIONS IN DISCORD/TELEGRAM FOR ANY ISSUES YOU MAY RUN INTO.
- IF YOU ARE ON V.19A OR LOWER YOU MUST RUN THE UNINSTALL IN THE MENU, DELETE YOUR RGBPI-EXTRA FOLDER, AND REINSTALL AS A FRESH INSTALL.
- OVERRIDES DISABLED ON NFS STORAGE
- DO NOT INSTALL RGBPI-EXTRA IF YOU ONLY USE AN SD CARD. 
- GAMEPAD REQUIRED TO NAVIGATE RGBPI-EXTRA UI

## Installation Options 

A: Online Installer

1. Download [Install RGBPi-Extra](https://github.com/forkymcforkface/RGBPi-Extra/blob/main/Install%20RGBPi-Extra.sh)
2. Place it in your /roms/ports folder
3. Scan for new games in the rgbpi ui
4. Go to ports in rgbpi ui and run RGBPi-Extra
5. The RGBPi-Extra UI will appear allowing you to apply make any tweaks

B: Offline Install (This will not have the latest minor changes)

1. Download the repo [RGBPi-Extra zip](https://github.com/forkymcforkface/RGBPi-Extra/archive/refs/heads/main.zip))
2. Open the zip and extract the RGBPi-Extra folder to your ports folder
3. Scan for games
4. Open rgbpi UI and install

## Usage

After installing **RGBPi-Extra** you will now have a RGBPi-Extra folder within ports and within that the RGBPi-Extra launcher

#### Update Cores
This allows you to updates cores to the lateset manually compiled version. it also allows you replace the nes core with mesen. There is a restore all cores button that will restore all default os4 core. 
#### Tweaks
A collection of scripts to modify RGBPi OS settings, Bullseye settings or just general improvements
#### Settings
Update or Removal of RGBPi-Extra, You will need to rescan for games after updating.

## Updates

1. Go to settings
2. Press update and allow the package to download

If there is a [X] that means it works in OS4
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
- [X] - `lr-dolphin` - Gamecube/wii emu - Dolphin port for libretro - **runs great, Pi5 only** 
- [X] - `lr-mesen-s` - Nes emu - Mesen-S port for libretro
- [X] - `lr-atari5200` - 400, 800, 600 XL, 800XL, 130XE and 5200 game console emulator.
- [X] - `lr-mednafen-vb` - Virtual Boy emulator - **runs great, not pixel perfect**
- [X] - `lr-ppsspp` - PlayStation Portable emu - PPSSPP port for libretro - **works well, included in current patch**
- [X] - `lr-samecdi` - Philips CDI - same_cdi port for libretro - **runs great and at correct resolution, included in current patch**
- [X] - `lr-TIC-80` - Fantasy Game Emulator - **runs great**
- [X] - `lr-virtualjaguar` - Atari Jaguar emulator - **runs ok on pi4, runs well on pi5, not all games work, included in current patch**
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
