import shutil
import os
import pygame
import pygame_menu
from retroarch_settings import get_retroarch_settings_menu
from rgbpi_tweaks import get_rgbpi_tweaks_menu
from core_updates import get_core_updates_menu
from tweaks_settings import get_tweaks_settings_menu

os.chdir(os.path.dirname(os.path.abspath(__file__)))

RGBPI_UI_ROOT = '/opt/rgbpi/ui'
SUDOERS_FILE = '/etc/sudoers.d/010_pi-nopasswd'

root_enabled = os.path.exists(SUDOERS_FILE)
patch_enabled = os.path.exists(f'{RGBPI_UI_ROOT}/launcher2.pyc')

WINDOW_SIZE = (320, 240)

surface = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
pygame.mouse.set_visible(False)

menu_theme = pygame_menu.themes.THEME_DARK.copy()
menu_theme.background_color = (0, 0, 0, 255)
menu_theme.title_offset = (20, 20)
menu_theme.title_font_size = 16
menu_theme.title_font = pygame_menu.font.FONT_MUNRO
menu_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
menu_theme.widget_font_size = 13
menu_theme.widget_font = pygame_menu.font.FONT_MUNRO
menu_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT
menu_theme.scrollbar_color = (0, 0, 0, 255)
menu_theme.scrollbar_slider_color = (0, 0, 0, 255)
menu_theme.scrollbar_thick = (5)

menu = pygame_menu.Menu(
    title='RGBPi Extra v.19a',
    theme=menu_theme,
    joystick_enabled=True,
    width=WINDOW_SIZE[0],
    height=WINDOW_SIZE[1],
    mouse_visible_update=False,
)

def toggle_root(value) -> None:
    try:
        if value:
            with open(SUDOERS_FILE, 'wt') as f:
                f.write('pi ALL=(ALL) NOPASSWD: ALL')
        else:
            os.remove(SUDOERS_FILE)
    except:
        value = not value

def apply_patch():
    error = None
    try:
        shutil.move(os.path.join(RGBPI_UI_ROOT, 'launcher.pyc'), os.path.join(RGBPI_UI_ROOT, 'launcher2.pyc'))
        shutil.copy('data/launcher.py', os.path.join(RGBPI_UI_ROOT, 'launcher.py'))
        shutil.copy('data/systems.dat', os.path.join(RGBPI_UI_ROOT, 'data', 'systems.dat'))
        shutil.copytree('data/tweaks', os.path.join(RGBPI_UI_ROOT, 'tweaks'), dirs_exist_ok=True)
        shutil.copytree('data/shaders', '/root/.config/retroarch/shaders', dirs_exist_ok=True)
        shutil.copytree('data/cores', '/opt/retroarch/cores', dirs_exist_ok=True)

        with open('data/cores.cfg', 'r') as source_file:
            data_to_append = source_file.read()
        with open('/opt/rgbpi/ui/data/cores.cfg', 'r+') as dest_file:
            lines = dest_file.readlines()
            dest_file.seek(0)
            for line in lines:
                if not line.startswith(('melonds_', 'yabasanshiro_')):
                    dest_file.write(line)
            dest_file.write(data_to_append)
            dest_file.truncate()

        script_dir = os.path.dirname(os.path.abspath(__file__))
        drive = script_dir.split(os.sep)[2]
        media_mountpoint = os.path.join('/', 'media', drive)

        source_dir = os.path.join(os.path.dirname(__file__), 'data', 'drive')
        shutil.copytree(source_dir, media_mountpoint, dirs_exist_ok=True)

        os.system('reboot')
    except Exception as e:
        error = 'patch'
    load_menu(error=error)

def load_menu(error=None):
    menu.clear()
    if error:
        if error == 'patch':
            menu.add.label('Error applying patch!', wordwrap=False)
        menu.add.vertical_margin(margin=10)
        menu.add.button('OK', load_menu)
    else:
        menu.add.toggle_switch('Root access', root_enabled, toggle_root, width=70, slider_thickness=0,
                               single_click=True, state_text=('disabled', 'enabled'))
        menu.add.vertical_margin(margin=10)
        if not patch_enabled:
            menu.add.button('Apply patch to launcher and reboot', apply_patch)
        else:
            retroarch_settings_menu = get_retroarch_settings_menu(menu_theme, WINDOW_SIZE)
            rgbpi_tweaks_menu = get_rgbpi_tweaks_menu(menu_theme, WINDOW_SIZE)
            settings_menu = get_tweaks_settings_menu(menu_theme, WINDOW_SIZE)                
            menu.add.button('Retroarch Settings', retroarch_settings_menu)
            menu.add.button('Core Updater', get_core_updates_menu(menu_theme, WINDOW_SIZE))
            menu.add.button('Tweaks', rgbpi_tweaks_menu)
            menu.add.button('Settings', settings_menu)
            menu.add.vertical_margin(margin=10)
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
        else:
            break
        pygame.display.update()
