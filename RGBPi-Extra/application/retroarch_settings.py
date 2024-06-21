import configparser
import pygame_menu
import shutil

SOURCE_OVERRIDES_INI = 'data/tweaks/global_overrides.ini'
DESTINATION_OVERRIDES_INI = '/opt/rgbpi/ui/tweaks/global_overrides.ini'

def load_ini(ini_file):
    extra_config = configparser.ConfigParser()
    extra_config.read(ini_file)
    return extra_config

def toggle_boolean_parameter(value, key):
    extra_config = load_ini(SOURCE_OVERRIDES_INI)
    extra_config['common_config_overrides'][key] = 'true' if value else 'false'
    
    with open(SOURCE_OVERRIDES_INI, 'w') as source_file:
        extra_config.write(source_file)
        
    shutil.copy(SOURCE_OVERRIDES_INI, DESTINATION_OVERRIDES_INI)

def get_retroarch_settings_menu(menu_theme, WINDOW_SIZE):
    extra_config = load_ini(SOURCE_OVERRIDES_INI)
    overrides = extra_config['common_config_overrides']

    menu = pygame_menu.Menu(
        title='',
        theme=menu_theme,
        joystick_enabled=True,
        width=WINDOW_SIZE[0],
        height=WINDOW_SIZE[1],
        mouse_visible_update=False,
    )
    
    for key, value in overrides.items():
        try:
            int_value = int(value)
        except ValueError:
            menu.add.toggle_switch(
                key,
                value == 'true',
                toggle_boolean_parameter,
                toggleswitch_id=key,
                width=50,
                slider_thickness=0,
                single_click=True,
                key=key,
                state_text=('false', 'true')
            )

    menu.add.button('Return to menu', pygame_menu.events.BACK)

    return menu
