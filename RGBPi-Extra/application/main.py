import os
import pygame
import pygame_menu
from retroarch_settings import get_retroarch_settings_menu
from rgbpi_tweaks import get_rgbpi_tweaks_menu
from core_updates import get_core_updates_menu
from tweaks_settings import get_tweaks_settings_menu

os.chdir(os.path.dirname(os.path.abspath(__file__)))

RGBPI_UI_ROOT = '/opt/rgbpi/ui'

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
    title='RGBPi Extra v.19a',
    theme=menu_theme,
    joystick_enabled=True,
    width=WINDOW_SIZE[0],
    height=WINDOW_SIZE[1],
    mouse_visible_update=False,
)

def load_menu(error=None):
    menu.clear()
    if error:
        if error == 'patch':
            menu.add.label('Error applying patch!', wordwrap=False)
        menu.add.vertical_margin(margin=10)
        menu.add.button('OK', load_menu)
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
