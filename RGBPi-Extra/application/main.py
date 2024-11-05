import shutil
import os
import pygame
import pygame_menu
import time
from retroarch_settings import get_retroarch_settings_menu
from rgbpi_tweaks import get_rgbpi_tweaks_menu
from core_updater import get_core_updater_menu
from system_manager import get_main_menu
from tweaks_settings import get_tweaks_settings_menu

os.chdir(os.path.dirname(os.path.abspath(__file__)))

RGBPI_UI_ROOT = '/opt/rgbpi/ui'
PATCH_FLAG_FILE = os.path.join(RGBPI_UI_ROOT, 'patch_applied.flag')
LAUNCHER_FILE = os.path.join(RGBPI_UI_ROOT, 'launcher.py')
VERSION = 'v.21a'

WINDOW_SIZE = (290, 240)

surface = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
pygame.mouse.set_visible(False)

menu_theme = pygame_menu.themes.THEME_DARK.copy()
menu_theme.background_color = (0, 0, 0, 255)
menu_theme.title_offset = (3, 20)
menu_theme.title_font_size = 16
menu_theme.title_font = pygame_menu.font.FONT_MUNRO
menu_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
menu_theme.widget_font_size = 13
menu_theme.widget_font = pygame_menu.font.FONT_MUNRO
menu_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT
menu_theme.scrollbar_color = (0, 0, 0, 255)
menu_theme.scrollbar_slider_color = (0, 0, 0, 255)
menu_theme.widget_padding = (1, 2)

menu = pygame_menu.Menu(
    title=f'RGBPi Extra {VERSION}',
    theme=menu_theme,
    joystick_enabled=True,
    width=WINDOW_SIZE[0],
    height=WINDOW_SIZE[1],
    mouse_visible_update=False,
)

def apply_patch():
    error = None
    try:
        shutil.copytree('data/shaders', '/root/.config/retroarch/shaders', dirs_exist_ok=True)
        
        retroarch_path = '/opt/retroarch/retroarch'
        backup_path = retroarch_path + '.bak'
        if os.path.exists(backup_path):
            os.remove(retroarch_path)
        else:
            shutil.move(retroarch_path, backup_path)
        
        shutil.copy('data/retroarch', retroarch_path)
        os.chmod(retroarch_path, 0o777)
        
        with open('data/new_cores/cores.cfg', 'r') as source_file:
            data_to_append = source_file.read()
        with open('/opt/rgbpi/ui/data/cores.cfg', 'a') as dest_file:
            dest_file.write(data_to_append)

        shutil.copy('data/launcher.py', LAUNCHER_FILE)
        launcher_pyc_path = os.path.join(RGBPI_UI_ROOT, 'launcher.pyc')
        if os.path.exists(launcher_pyc_path):
            os.rename(launcher_pyc_path, os.path.join(RGBPI_UI_ROOT, 'launcher2.pyc'))

        script_dir = os.path.dirname(os.path.abspath(__file__))
        drive = script_dir.split(os.sep)[2]
        media_mountpoint = os.path.join('/', 'media', drive)
        source_dir = os.path.join(os.path.dirname(__file__), 'data', 'drive')
        shutil.copytree(source_dir, media_mountpoint, dirs_exist_ok=True)
        dats_dir = os.path.join(media_mountpoint, 'dats')   

        dat_files_to_process = ['games.dat', 'favorites.dat', 'favorites_tate.dat']

        if os.path.exists(dats_dir):
            for dat_file in dat_files_to_process:
                file_path = os.path.join(dats_dir, dat_file)
                extra_file_path = os.path.join(dats_dir, dat_file.replace('.dat', '_extra.dat'))

                if os.path.exists(file_path):
                    if os.path.exists(extra_file_path):
                        os.remove(extra_file_path)
                    
                    shutil.copy(file_path, extra_file_path)

        io_file_path = '/usr/lib/python3.9/io.py'
        modification_text = """
#BELOW THIS LINE
import os
from _io import open as _original_open

def open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
    if isinstance(file, str):
        if file.endswith('/games.dat'):
            file = file.replace('/games.dat', '/games_extra.dat')
        elif file.endswith('/favorites.dat'):
            file = file.replace('/favorites.dat', '/favorites_extra.dat')
        elif file.endswith('/favorites_tate.dat'):
            file = file.replace('/favorites_tate.dat', '/favorites_tate_extra.dat')

        if not os.path.exists(file):
            with _original_open(file, 'w') as f:
                pass

    return _original_open(file, mode, buffering, encoding, errors, newline, closefd, opener)

OpenWrapper = open
"""
        with open(io_file_path, 'r') as io_file:
            io_content = io_file.read()

        if modification_text not in io_content:
            with open(io_file_path, 'a') as io_file:
                io_file.write('\n\n' + modification_text)

        with open(PATCH_FLAG_FILE, 'w') as f:
            f.write(VERSION)
        os.system('chmod 777 /media/sd')

    except Exception as e:
        error = 'patch'
    
    load_menu(error=error)
    os.system('reboot')



def load_menu(error=None):
    menu.clear()
    if error:
        if error == 'patch':
            menu.add.label('Error applying patch!', wordwrap=False)
        menu.add.vertical_margin(margin=10)
        menu.add.button('OK', load_menu)
    else:
        patch_needed = True
        if os.path.exists(PATCH_FLAG_FILE) and os.path.exists(LAUNCHER_FILE):
            with open(PATCH_FLAG_FILE, 'r') as f:
                applied_version = f.read().strip()
                if applied_version >= VERSION:
                    patch_needed = False

        if patch_needed:
            menu.add.button('Install RGBPi-Extra and reboot', apply_patch)
        else:
            retroarch_settings_menu = get_retroarch_settings_menu(menu_theme, WINDOW_SIZE)
            rgbpi_tweaks_menu = get_rgbpi_tweaks_menu(menu_theme, WINDOW_SIZE)
            settings_menu = get_tweaks_settings_menu(menu_theme, WINDOW_SIZE)                
            menu.add.button('Retroarch Settings', retroarch_settings_menu)
            menu.add.button('Core Updater', get_core_updater_menu(menu_theme, WINDOW_SIZE))
            menu.add.button('System Manager', get_main_menu(menu_theme, WINDOW_SIZE))
            menu.add.button('Tweaks', rgbpi_tweaks_menu)
            menu.add.button('Settings', settings_menu)
        menu.add.vertical_margin(margin=10)
        if not patch_needed:
            menu.add.button('Quit', pygame_menu.events.EXIT)

    pygame.display.update()

load_menu()

if __name__ == '__main__':
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
        if menu.is_enabled():
            menu.update(events)
            menu.draw(surface)
        time.sleep(0.01)
        pygame.display.update()
