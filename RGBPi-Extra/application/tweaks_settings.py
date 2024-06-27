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

def remove_patch():
    try:
        os.remove(os.path.join(RGBPI_ROOT, 'launcher.py'))
        os.rename(os.path.join(RGBPI_ROOT, 'launcher2.pyc'), os.path.join(RGBPI_ROOT, 'launcher.pyc'))
        os.remove(os.path.join(RGBPI_ROOT, 'patch_applied.flag'))
        os.remove(os.path.join(RA_ROOT, 'retroarch'))
        os.rename(os.path.join(RA_ROOT, 'retroarch.bak'), os.path.join(RA_ROOT, 'retroarch'))
        config = configparser.ConfigParser()
        config.read(os.path.join(RGBPI_ROOT, 'config.ini'))
        config['cfg']['adv_mode'] = 'user'
        with open(os.path.join(RGBPI_ROOT, 'config.ini'), 'w') as config_file:
            config.write(config_file)
        
        shutil.copy('data/retroarch.cfg', '/root/.config/retroarch/retroarch.cfg')
    except Exception as e:
        pass

    restore_default_systems()
    restore_default_cores()

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

def update_and_restart():
    display_message("Checking Internet Connection...")
    pygame.display.flip()
    
    try:
        urllib.request.urlopen('http://www.github.com', timeout=1)
    except urllib.error.URLError:
        display_message("Check Internet Connection")
        pygame.display.flip()
        time.sleep(5)
        return
    
    subprocess.Popen(['python3.9', 'updater.py'])
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

    menu.add.button('Update to latest version', update_and_restart)
    menu.add.button('Remove RGBPi Extra patches and reboot', remove_patch)
    menu.add.button('Return to menu', pygame_menu.events.BACK)

    return menu
