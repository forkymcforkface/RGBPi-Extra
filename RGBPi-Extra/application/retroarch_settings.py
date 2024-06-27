import pygame_menu
import os

# Determine the dynamic location based on the mount point of the Python file
script_dir = os.path.dirname(os.path.abspath(__file__))
drive = script_dir.split(os.sep)[2]
media_mountpoint = os.path.join('/', 'media', drive)
GLOBAL_CFG_PATH = os.path.join(media_mountpoint, 'gameconfig', 'sys_override', 'global.cfg')

def load_config(file_path):
    config = {}
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip().strip('"')
    return config

def save_config(file_path, config):
    with open(file_path, 'w') as f:
        for key, value in config.items():
            f.write(f'{key} = "{value}"\n')

def toggle_boolean_parameter(value, key):
    config = load_config(GLOBAL_CFG_PATH)
    config[key] = 'true' if value else 'false'
    save_config(GLOBAL_CFG_PATH, config)

def get_retroarch_settings_menu(menu_theme, WINDOW_SIZE):
    config = load_config(GLOBAL_CFG_PATH)

    menu = pygame_menu.Menu(
        title='',
        theme=menu_theme,
        joystick_enabled=True,
        width=WINDOW_SIZE[0],
        height=WINDOW_SIZE[1],
        mouse_visible_update=False,
    )

    for key, value in config.items():
        if value.lower() in ('true', 'false'):
            menu.add.toggle_switch(
                key,
                value == 'true',
                toggle_boolean_parameter,
                toggleswitch_id=key,
                width=40,
                slider_thickness=0,
                single_click=True,
                key=key,
                state_text=('false', 'true')
            )

    menu.add.button('Return to menu', pygame_menu.events.BACK)

    return menu
