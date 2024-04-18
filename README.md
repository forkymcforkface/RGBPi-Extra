
# RGBPi-Extra

RGBpi-Extra is a UI that allows you to apply a collection of unofficial scripts for [RGBPiOS](https://www.rgb-pi.com/#os), enabling you to quickly and easily install emulators, ports, and libretrocores that haven't been included in RGBPi for various reasons. Additionally, it provides the capability to enable RetroArch features that are disabled by default. These scripts are experimental in nature and may not be fully stable. The concept for creating this repository was inspired by [RetroPie-Extra](https://github.com/Exarkuniv/RetroPie-Extra) and represents a collaborative effort across multiple parties within the RGBPi community.




I have found new scripts made by other people and added them to this Repo. I dont take credit for any of them, other then the ones I made. RGBPi OS uses a custom kernel driver and custom compiled version of retroarch. Pre-Compiled Cores from libretro, Retropie, batocera, lakka will not work (mostly). I have found that compiling cores on the RGBpi OS itself works best, but can still take some adjustments in the cmake flags.

 **DO NOT ASK QUESTIONS IN DISCORD/TELEGRAM FOR ANY ISSUES YOU MAY RUN INTO.**
 
 **Notes**
- Please use [Discussions](https://github.com/sd2cv/RGBPi-Extra/discussions) or [Issues](https://github.com/sd2cv/RGBPi-Extra/issues) if you have questions or issues. 
- RGBPi OS runs on Bullseye aarch64
- It uses a [custom kernel driver](https://github.com/rtomasa/rpi-dpidac) for the GPIO output
- It uses a [custom retroarch build](https://github.com/rtomasa/RetroArch) with dynares driver built in, dynares takes a sample of the rom fps and resolution and then adjusts the kernel driver framebuffer to match.
- It does not have xorg out of the box so any emulators that require it wont work. You can install a LXQT desktop which will enable startx and xorg.
- applications that use egl/kms can work, but may be limited to 240p



## Installation

1. Download [Install RGBPi-Extra](https://github.com/sd2cv/RGBPi-Extra/blob/main/Install%20RGBPi-Extra.sh)
2. Place it in your /roms/ports folder
3. Scan for new games in the rgbpi ui
4. Go to ports in rgbpi ui and run Install RGBPi-Extra
5. The RGBPi-Extra UI will appear allowing you to apply the patch and restart. 






https://github.com/sd2cv/RGBPi-Extra/assets/99993735/d4a69f9b-47b7-4d27-95e5-2555a1844ca1






## Usage

After installing **RGBPi-Extra** you will now have a RGBPi-Extra folder within ports and within that the RGBPi-Extra launcher

#### Retroarch Settings 
This allows you to add retroarch features that are disabled by default by RGBPi-OS. Currently only boolean shows up in the UI, but you can add any global configs that you would like to /application/data/tweaks/gobal_configs.ini
#### Update Cores
Still in progress do not use this area
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

Updates are currently implemented in a similar fashion to removing the RGBPi-Extras. The reasoning is that if anything happens during the download or patching process, your system is in a near vanilla state allowing it to work normally. 

## Remove

To remove the patch open RGBPi-Extra ui, go to settings and select remove. This is required prior to reimaging your SD card if you are doing so.

# Systems still in progress, only checked cores are implemented. BIOS files are not included.




https://github.com/sd2cv/RGBPi-Extra/assets/99993735/1b75acd4-bfe8-4d95-8eb5-8481741fbc86



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

#### Libretrocores

- [ ] - `lr-2048` - 2048 engine - 2048 port for libretro
- [ ] - `lr-applewin` - Apple2e emulator - AppleWin (current) port for libretro 
- [ ] - `lr-arduous_lcd` - ArduBoy emulator - arduous port for libretro
- [ ] - `lr-beetle-pce` - PCEngine emu - Mednafen PCE port for libretro
- [ ] - `lr-bk` -  Elektronika БК-0010/0011/Terak 8510a emulator - BK port for libretro
- [ ] - `lr-blastem` - Sega Genesis emu - BlastEm port for libretro
- [ ] - `lr-boom3` -  Doom 3 port for libretro
- [ ] - `lr-bsnes-hd` - "Super Nintendo Emulator - bsnes-HD port for libretro (BETA)"
- [ ] - `lr-canary` - Citra Canary for libretro
- [ ] - `lr-cannonball` - An Enhanced OutRun engine for libretro
- [ ] - `lr-chailove` - 2D Game Framework with ChaiScript roughly inspired by the LÖVE API to libretro
- [ ] - `lr-citra` - Citra port for libretro
- [ ] - `lr-crocods` - CrocoDS port for libretro 
- [ ] - `lr-daphne` - Daphne port to libretro - laserdisk arcade games.
- [ ] - `lr-duckstation` -"PlayStation emulator - Duckstation for libretro"
- [ ] - `lr-fceumm-mod` - Modified fceumm core to specifically support the Super Mario Bros 1/3 hack
- [ ] - `lr-freej2me` - A J2ME implementation for old JAVA phone games.
- [ ] - `lr-gearboy` - Game Boy (Color) emulator - Gearboy port for libretro. 
- [ ] - `lr-gearcoleco` - ColecoVision emulator - GearColeco port for libretro.
- [ ] - `lr-lutro` - Lua engine - lua game framework (WIP) for libretro following the LÖVE API 
- [ ] - `lr-mame2003_midway` - MAME 0.78 core with Midway games optimizations. 
- [X] - `lr-melondsds` - NDS emu - MelonDS port for libretro - **runs great**
- [X] - `lr-mesen-s` - Super Nintendo emu - Mesen-S port for libretro
- [X] - `lr-atari800` - 400, 800, 600 XL, 800XL, 130XE and 5200 game console emulator.
- [X] - `lr-mednafen-vb` - Virtual Boy emulator - **runs great, not pixel perfect**
- [ ] - `lr-mess-jaguar` - atari jaguar system emu
- [ ] - `lr-mu` - Palm OS emu - Mu port for libretro 
- [ ] - `lr-oberon` - Oberon RISC emulator for libretro
- [ ] - `lr-openlara` - Tomb Raider engine - OpenLara port for libretro
- [ ] - `lr-play` - PlayStation 2 emulator - Play port for libretro
- [ ] - `lr-potator` -  Watara Supervision emulator based on Normmatt version - Potator port for libretro
- [X] - `lr-ppsspp` - PlayStation Portable emu - PPSSPP port for libretro - **works well some grapahics missing, included in current patch**
- [ ] - `lr-prboom-system` - For setting up DOOM as an emulated system, not a port.  - 
- [ ] - `lr-race` - Neo Geo Pocket (Color) emulator - RACE! port for libretro. 
- [ ] - `lr-reminiscence` - Flashback engine - Gregory Montoir’s Flashback emulator port for libretro
- [ ] - `lr-sameboy` - Game Boy and Game Boy Color, emulator - SameBoy Port for libretro
- [ ] - `lr-samecdi` - Philips CDI - same_cdi port for libretro
- [ ] - `lr-simcoupe` - SAM Coupe emulator - SimCoupe port for libretro
- [ ] - `lr-swanstation` - Playstation emulator - Duckstation fork for libretro
- [X] - `lr-TIC-80` - Fantasy Game Emulator - **runs great**
- [ ] - `lr-thepowdertoy` - Sandbox physics game for libretro - 
- [ ] - `lr-uzem` - Uzebox engine - Uzem port for libretro
- [ ] - `lr-vemulator` - SEGA VMU emulator - 
- [X] - `lr-yabasanshiro` - Saturn & ST-V emulator - **runs great, included in current patch**

#### Ports
- [ ] - `0ad` - Battle of Survival - is a futuristic real-time strategy game 
- [ ] - `abuse` - Classic action game 
- [ ] - `adom` - Ancient Domains of Mystery - a free roguelike by Thomas Biskup -  
- [ ] - `augustus` - Enhanced Caesar III source port - 
- [ ] - `avp` - AVP - Aliens versus Predator port - 
- [ ] - `barrage` - Shooting Gallery action game -
- [ ] - `bermudasyndrome` - Bermuda Syndrome engine 
- [ ] - `berusky` - Advanced sokoban clone with nice graphics - 
- [ ] - `bloboats` - Fun physics game -
- [ ] - `boswars` - Battle of Survival - is a futuristic real-time strategy game - 
- [ ] - `breaker` - Arkanoid clone - 
- [ ] - `bstone` - BStone A source port of Blake Stone: Aliens of Gold and Blake Stone: Planet Strike 
- [ ] - `burgerspace` - BurgerTime clone - 
- [ ] - `captains`- Captain 'S' The Remake - 
- [ ] - `chocolate-doom`- DOOM source port - 
- [ ] - `chocolate-doom-system`- For setting up DOOM as an emulated system, not port. - 
- [ ] - `chopper258` - Chopper Commando Revisited - A modern port of Chopper Commando (DOS, 1990) -
- [ ] - `corsixth` - CorsixTH - Theme Hospital Engine - 
- [ ] - `crack-attack` - Tetris Attack clone - 
- [ ] - `crispy-doom` - DOOM source port - 
- [ ] - `crispy-doom-system` - For setting up DOOM as an emulated system, not port. - 
- [ ] - `cytadela` - Cytadela project - a conversion of an Amiga first person shooter. - 
- [ ] - `devilutionx` - Diablo source port -
- [ ] - `dhewm3` - Doom 3 port - 
- [ ] - `diablo2` - Diablo 2 - Lord of Destruction port - 
- [ ] - `dosbox-x` - DOSbox-X - Testing of a new DOSbox system - 
- [ ] - `dunelegacy` - Dune 2 Building of a Dynasty port - 
- [ ] - `easyrpgplayer` - RPG Maker 2000/2003 interpreter - 
- [ ] - `ecwolf` - ECWolf is an advanced source port for Wolfenstein 3D - 
- [ ] - `eternity` - Enhanced port of the official DOOM source - 
- [ ] - `extremetuxracer` -  Linux verion of Mario cart - 
- [ ] - `fallout1` -  Fallout2-ce - Fallout 2 Community Edition - 
- [ ] - `fallout2` -  Fallout2-ce - Fallout 2 Community Edition - 
- [ ] - `freeciv` - Civilization online clone - 
- [ ] - `freedink` - Dink Smallwood engine - 
- [ ] - `freesynd` - Syndicate clone - 
- [ ] - `fruity` - inspired by the Kaiko classic Gem'X - 
- [ ] - `fs2open` - FreeSpace 2 Open - Origin Repository for FreeSpace 2 - 
- [ ] - `galius` - - Maze of Galius - 
- [ ] - `gmloader` - GMLoader - play GameMaker Studio games for Android on non-Android operating systems - 
- [ ] - `gnukem` - Dave Gnukem - Duke Nukem 1 look-a-like - 
- [ ] - `gtkboard` - Board games system - 
- [ ] - `hcl` - Hydra Castle Labrinth - 
- [ ] - `heboris` - Tetris The Grand Master clone - 
- [ ] - `hero2` - FHeroes2 - Heroes of Might and Magic II port - 
- [ ] - `hexen2` - Hexen II - Hammer of Thyrion source port Non-OpenGL - 
- [ ] - `hexen2gl` - Hexen II - Hammer of Thyrion source port using OpenGL - 
- [ ] - `hheretic` - Heretic GL port - 
- [ ] - `hhexen` - Hexen GL portt - 
- [ ] - `hurrican` - Turrican clone. - 
- [ ] - `ikemen-go` - I.K.E.M.E.N GO - Clone of M.U.G.E.N. - 
- [ ] - `ja2` - Stracciatella - Jagged Alliance 2 engine - 
- [ ] - `jfsw` - Shadow warrior port - 
- [ ] - `julius` - Caesar III source port - 
- [ ] - `kraptor` - Shoot em up scroller game - 
- [ ] - `lbreakout2` - Open Source Breakout game - 
- [ ] - `lgeneral` - Open Source strategy game - 
- [ ] - `lmarbles` - Open Source Atomix game - 
- [ ] - `ltris` - Open Source Tetris game - 
- [ ] - `manaplus` - manaplus - 2D MMORPG Client - 
- [ ] - `meritous` - Port of an action-adventure dungeon crawl game - 
- [ ] - `nblood` - Blood source port - 
- [ ] - `nkaruga` - Ikaruga demake. - 
- [ ] - `nxengine-evo` - The standalone version of the open-source clone/rewrite of Cave Story - 
- [ ] - `openclaw` - Reimplementation of Captain Claw - 
- [ ] - `opendune` - Dune 2 source port -
- [ ] - `openjazz` - An enhanced Jazz Jackrabbit source port - 
- [ ] - `openjk_ja` - OpenJK: JediAcademy (SP + MP) - 
- [ ] - `openjk_jo` - OpenJK: Jedi Outcast (SP) - 
- [ ] - `openmw` - Morrowind source port - 
- [ ] - `openra` - Real Time Strategy game engine supporting early Westwood classics - 
- [ ] - `openrct2` - RollerCoaster Tycoon 2 port - 
- [ ] - `pcexhumed` - PCExhumed - Powerslave source port - 
- [ ] - `piegalaxy` - Pie Galaxy - Download and install GOG.com games in RetroPie - 
- [ ] - `pingus` - Lemmings clone - 
- [ ] - `pokerth` - open source online poker  - 
- [ ] - `prboom-plus` - Enhanced DOOM source port - 
- [ ] - `prototype` - Free R-Type remake by Ron Bunce - Gamepad support incomplete. 
- [ ] - `pydance` - Open Source Dancing Game  - 
- [ ] - `quakespasm` - Another enhanced engine for quake  - 
- [ ] - `rawgl` - Another World Engine  - 
- [ ] - `rednukem` -  Rednukem - Redneck Rampage source port - 
- [ ] - `relive` - Oddworld engine for Abe's Oddysee and Abe's Exoddus 
- [ ] - `reminiscence` - Flashback engine clone - 
- [ ] - `revolt` - REvolt - a radio control car racing themed video game - 
- [ ] - `rickyd` - Rick Dangerous clone - 
- [ ] - `rigelengine` - RigelEngine - Duke Nukem 2 source port - 
- [ ] - `rocksndiamonds` - Rocks'n'Diamonds - Emerald Mine Clone - 
- [ ] - `rott-darkwar` - Rise of the Triad source port with joystick support - 
- [ ] - `rott-huntbgin` - Rise of the Triad (shareware version) source port with joystick support. - 
- [ ] - `rtcw`- IORTCW source port of Return to Castle Wolfenstein. - 
- [ ] - `samtfe`- Serious Sam Classic The First Encounter. - 
- [ ] - `samtse`- Serious Sam Classic The Second Encounter. - 
- [ ] - `sdl-bomber` - Simple Bomberman clone - 
- [ ] - `seahorse` - a side scrolling platform game 
- [ ] - `septerra` - Septerra Core: Legacy of the Creator port  
- [ ] - `shiromino` - Tetris The Grand Master Clone  
- [ ] - `shockolate` - Source port of System Shock  
- [ ] - `simutrans` - freeware and open-source transportation simulator  
- [ ] - `sm64ex` - Super Mario 64 PC Port for Pi4 - Works extremely well on Pi 4. 
- [ ] - `sorr` - Streets of Rage Remake port - 
- [ ] - `sorrv2` - Streets of Rage Remake port - 
- [ ] - `sqrxz2` - Sqrxz 2 - Two seconds until death - 
- [ ] - `sqrxz3` - Sqrxz 3 - Adventure For Love - 
- [ ] - `sqrxz4` - Sqrxz 4 - Cold Cash - 
- [ ] - `starcraft` - Starcraft - 
- [ ] - `supaplex` - Reverse engineering Supaplex - 
- [ ] - `vanillacc` - Vanilla-Command and Conquer - 
- [ ] - `vcmi` - Open-source engine for Heroes of Might and Magic III - 
- [ ] - `supertuxkart` - a free kart-racing game - 
- [ ] - `temptations` - Enhanced version of the MXS game - 
- [ ] - `warmux` - Worms Clone - 
- [ ] - `wesnoth` - Turn-based strategy game - 
- [ ] - `wine` - WINEHQ - Wine Is Not an Emulator - 
- [ ] - `xash3d-fwgs` - Half-Life engine source port. - 
- [ ] - `xump` - The Final Run - 
- [ ] - `zeldansq` - Zelda: Navi's Quest fangame - 

#### Supplementary
- [ ] - `audacity` - Audacity open-source digital audio editor - 
- [ ] - `chromium` - Open Source Web Browser - **Installs, Work well, requires sandbox mode. Firefox is recommended**
- [ ] - `epiphany` - epiphany lightweight web browser - 
- [X] - `LXQT Desktop` - Linux Desktop Environment, optimized for 720x480 - **Installs Runs fine**
- [X] - `firefox-esr` - FireFox-ESR - Formally known as IceWeasel, the Rebranded Firefox Web Browser - **Installs Runs fine**
- [X] - `videolan` - VLC media player - **Installs Runs fine, but cant figure out how to get it out of default 240p**

### Removed broken scripts


## Hall of Fame - Ports added that made it to the official OS release

- [X] - Kodi - Media Player
