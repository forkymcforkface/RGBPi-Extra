# OS4-Tools WIP
OS4-Tools is a refactor of RGBPi-Extra that utilizes bash scripts instead of a python ui. This is make it more user friendly, and easier for others to contribute to the project.


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
- [X] - `lr-opera` - 3DO Emu - 3DO port for libretro - **runs great**
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
