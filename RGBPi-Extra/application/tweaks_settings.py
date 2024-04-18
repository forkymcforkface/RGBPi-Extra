import os
import shutil
import pygame_menu
import subprocess
import glob
import sys
import configparser

def remove_patch():
    allowed_systems = set([
        'lightgun', 'arcade', 'atari2600', 'atari7800', 'pcengine', 'pcenginecd',
        'nes', 'snes', 'n64', 'sgb', 'gba', 'sg1000', 'mastersystem', 'megadrive',
        'segacd', 'sega32x', 'dreamcast', 'neogeo', 'neocd', 'ngp', 'psx', 'amstradcpc',
        'c64', 'amiga', 'amigacd', 'x68000', 'msx', 'zxspectrum', 'pc', 'ports', 'scripts'
    ])

    RGBPI_UI_ROOT = '/opt/rgbpi/ui'
    launcher_py_path = os.path.join(RGBPI_UI_ROOT, 'launcher.py')
    launcher2_pyc_path = os.path.join(RGBPI_UI_ROOT, 'launcher2.pyc')
    tweaks_folder_path = os.path.join(RGBPI_UI_ROOT, 'tweaks')

    os.remove(launcher_py_path)
    os.rename(launcher2_pyc_path, os.path.join(RGBPI_UI_ROOT, 'launcher.pyc'))
    shutil.rmtree(tweaks_folder_path)

    games_dat_path = '/media/*/dats/games.dat'
    favorites_dat_path = '/media/*/dats/favorites.dat'
    systems_dat_path = '/opt/rgbpi/ui/data/systems.dat'

    def filter_system_entries(dat_file_path):
        try:
            with open(dat_file_path, 'r+') as file:
                lines = file.readlines()
                file.seek(0)
                if 'Id' in lines[0]:
                    file.write(lines[0])
                    for line in lines[1:]:
                        system = line.split(',')[2].strip('"')
                        if system.lower() in allowed_systems:
                            file.write(line)
                    file.truncate()
                else:
                    file.write(lines[0])
                    for line in lines[1:]:
                        system = line.split(',')[0].strip('"')
                        if system.lower() in allowed_systems:
                            file.write(line)
                    file.truncate()
        except Exception as e:
            pass

    for file_path in glob.glob(games_dat_path):
        filter_system_entries(file_path)
    for file_path in glob.glob(favorites_dat_path):
        filter_system_entries(file_path)
    filter_system_entries(systems_dat_path)

    config_ini_path = os.path.join(RGBPI_UI_ROOT, 'config.ini')
    try:
        config = configparser.ConfigParser()
        config.read(config_ini_path)
        config.set('cfg', 'adv_mode', 'user')
        with open(config_ini_path, 'w') as config_file:
            config.write(config_file)
    except Exception as e:
        pass

    try:
        shutil.copy('data/retroarch.cfg', '/root/.config/retroarch/retroarch.cfg')
    except Exception as e:
        pass

    os.system('reboot')

def update_and_restart():
    subprocess.Popen(['python', 'updater.py'])
    sys.exit()

def get_tweaks_settings_menu(menu_theme, WINDOW_SIZE):
    menu = pygame_menu.Menu(
        title='',
        theme=menu_theme,
        joystick_enabled=True,
        width=WINDOW_SIZE[0],
        height=WINDOW_SIZE[1],
        mouse_visible_update=False,
    )

    menu.add.button('Update to latest version (internet required)', update_and_restart)
    menu.add.button('Remove RGBPi Extra patches and reboot', remove_patch)
    menu.add.button('Return to menu', pygame_menu.events.BACK)

    return menu
