import os
import shutil
import pygame
import pygame_menu
import subprocess
import sys
import configparser
import urllib.request
import time

from system_manager import restore_default_systems
from core_updater import restore_default_cores

RGBPI_ROOT = '/opt/rgbpi/ui'
RA_ROOT = '/opt/retroarch'

dats_directories = [
    '/media/sd/dats',
    '/media/usb1/dats',
    '/media/usb2/dats',
    '/media/nfsl/dats',
    '/media/nfsg/dats'
]

def remove_patch(reboot=True):
    try:
        os.remove(os.path.join(RGBPI_ROOT, 'launcher.py'))
        os.rename(os.path.join(RGBPI_ROOT, 'launcher2.pyc'), os.path.join(RGBPI_ROOT, 'launcher.pyc'))
        os.remove(os.path.join(RGBPI_ROOT, 'patch_applied.flag'))
        shutil.copy('data/scripts/files/retroarch.cfg', '/root/.config/retroarch/retroarch.cfg')

        extra_dat_files = ['games_extra.dat', 'favorites_extra.dat', 'favorites_tate_extra.dat']
        for dat_dir in dats_directories:
            if os.path.exists(dat_dir):
                for extra_file in extra_dat_files:
                    extra_file_path = os.path.join(dat_dir, extra_file)
                    if os.path.exists(extra_file_path):
                        os.remove(extra_file_path)

        io_file_path = '/usr/lib/python3.9/io.py'
        with open(io_file_path, 'r') as io_file:
            io_content = io_file.read()

        if '#BELOW THIS LINE' in io_content:
            io_content = io_content.split('#BELOW THIS LINE')[0]

            with open(io_file_path, 'w') as io_file:
                io_file.write(io_content)

    except Exception as e:
        print(f"An error occurred: {e}")

    restore_default_systems()
    restore_default_cores()

    if reboot:
        os.system('reboot')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WINDOW_SIZE = (290, 240)

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
font = pygame.font.Font(pygame_menu.font.FONT_MUNRO, 14)

def display_message(message):
    screen.fill(BLACK)
    text = font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

def update_and_restart(menu):
    display_message("Checking Internet Connection...")
    pygame.display.flip()

    python_exec = 'python'
    try:
        with open('/etc/os-release') as f:
            os_release = f.read()
        if 'bookworm' in os_release:
            python_exec = 'python3.9'
    except Exception:
        pass

    try:
        urllib.request.urlopen('http://www.github.com', timeout=1)
        subprocess.Popen([python_exec, 'updater.py'])
        sys.exit()
    except urllib.error.URLError:
        display_message("Check Your Internet Connection")
        pygame.display.flip()
        time.sleep(5)
        menu.reset(1)

def get_tweaks_settings_menu(menu_theme, window_size):
    menu = pygame_menu.Menu(
        title='',
        theme=menu_theme,
        joystick_enabled=True,
        width=window_size[0],
        height=window_size[1],
        mouse_visible_update=False,
    )

    menu.add.button('Update to latest version', lambda: update_and_restart(menu))
    menu.add.button('Remove RGBPi Extra patches and reboot', lambda: remove_patch(reboot=True))
    menu.add.button('Return to menu', pygame_menu.events.BACK)

    return menu
