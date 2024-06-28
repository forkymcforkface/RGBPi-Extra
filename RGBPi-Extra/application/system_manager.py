import os
import pygame_menu
import pygame
import shutil
import time

SOURCE_SYSTEMS_FILE = 'data/new_cores/!new_cores.dat'
DESTINATION_SYSTEMS_FILE = '/opt/rgbpi/ui/data/systems.dat'
BACKUP_SYSTEMS_FILE = '/opt/rgbpi/ui/data/systems.dat.bak'
SYSTEMS_CORES_FILE_TEMPLATE = '[Systems]\n'
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WINDOW_SIZE = (290, 240)

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
font = pygame.font.Font(pygame_menu.font.FONT_MUNRO, 14)

def display_message(message, duration=0):
    screen.fill(BLACK)
    text = font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    if duration > 0:
        time.sleep(duration)

def get_systems_from_cores():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    drive = script_dir.split(os.sep)[2]
    systems_cores_file = f'/media/{drive}/gameconfig/sys_override/systems_cores.cfg'
    systems = []
    cores = []
    if os.path.exists(systems_cores_file):
        with open(systems_cores_file, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if '=' in line:
                    system, core = line.split('=')
                    systems.append(system.strip())
                    cores.append(core.strip())
    return systems, cores

def restore_default_systems():
    def clean_dats():
        script_dir = os.path.dirname(os.path.abspath(__file__))
        drive = script_dir.split(os.sep)[2]
        dats_folder = f'/media/{drive}/dats/'
        systems_to_remove, _ = get_systems_from_cores()

        for dat_file in ['games.dat', 'favorites.dat']:
            dat_file_path = os.path.join(dats_folder, dat_file)
            if os.path.exists(dat_file_path):
                with open(dat_file_path, 'r') as file:
                    lines = file.readlines()

                with open(dat_file_path, 'w') as file:
                    header = lines[0]
                    file.write(header)
                    for line in lines[1:]:
                        system = line.strip().split(',')[2].strip('"')
                        if system not in systems_to_remove:
                            file.write(line)

    def delete_cores():
        _, cores_to_delete = get_systems_from_cores()
        for core in cores_to_delete:
            core_path = f'/opt/retroarch/cores/{core}'
            if os.path.exists(core_path):
                os.remove(core_path)
            
            info_path = core_path.replace('.so', '.info')
            if os.path.exists(info_path):
                os.remove(info_path)
            
            bashhelper_path = core_path.replace('.so', '.bash')
            if os.path.exists(bashhelper_path):
                os.remove(bashhelper_path)

    def reset_systems_cores():
        script_dir = os.path.dirname(os.path.abspath(__file__))
        drive = script_dir.split(os.sep)[2]
        systems_cores_file = f'/media/{drive}/gameconfig/sys_override/systems_cores.cfg'
        if os.path.exists(systems_cores_file):
            with open(systems_cores_file, 'w') as file:
                file.write(SYSTEMS_CORES_FILE_TEMPLATE)

    if os.path.exists(BACKUP_SYSTEMS_FILE):
        shutil.copy(BACKUP_SYSTEMS_FILE, DESTINATION_SYSTEMS_FILE)
        clean_dats()
        delete_cores()
        reset_systems_cores()
        os.remove(BACKUP_SYSTEMS_FILE)
        display_message('Default systems restored', 2)

def backup_systems_file():
    if not os.path.exists(BACKUP_SYSTEMS_FILE):
        shutil.copy(DESTINATION_SYSTEMS_FILE, BACKUP_SYSTEMS_FILE)

def load_systems(file_path):
    systems = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()[1:]
        for line in lines:
            parts = line.strip().split(',')
            system = parts[0].strip('"')
            name = parts[1].strip('"')
            release = parts[2].strip('"')
            developer = parts[3].strip('"')
            formats = parts[4].strip('"')
            core = parts[5].strip('"')
            bashhelper = parts[6].strip('"') if len(parts) > 6 else None
            systems[name] = {
                'system': system,
                'name': name,
                'release': release,
                'developer': developer,
                'formats': formats,
                'core': core,
                'bashhelper': bashhelper
            }
    return systems

def system_exists_in_cfg(system, systems_cores_file):
    if not os.path.exists(systems_cores_file):
        return False
    with open(systems_cores_file, 'r') as file:
        lines = file.readlines()
    for line in lines:
        if line.strip().startswith(system):
            return True
    return False

def system_exists_in_dat(system, destination_systems_file):
    if not os.path.exists(destination_systems_file):
        return False
    with open(destination_systems_file, 'r') as file:
        lines = file.readlines()[1:]  # Skip header
    for line in lines:
        if line.strip().split(',')[0].strip('"') == system:
            return True
    return False

def update_systems_cores(system, core):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    drive = script_dir.split(os.sep)[2]
    systems_cores_file = f'/media/{drive}/gameconfig/sys_override/systems_cores.cfg'
    
    if system_exists_in_cfg(system, systems_cores_file):
        return
    
    if not os.path.exists(systems_cores_file):
        os.makedirs(os.path.dirname(systems_cores_file), exist_ok=True)
        with open(systems_cores_file, 'w') as file:
            file.write(SYSTEMS_CORES_FILE_TEMPLATE)
    
    with open(systems_cores_file, 'a') as file:
        file.write(f'{system} = {core}\n')

def append_system_data(system, source_data):
    backup_systems_file()
    
    if system_exists_in_dat(system, DESTINATION_SYSTEMS_FILE):
        return
    
    with open(DESTINATION_SYSTEMS_FILE, 'a') as file:
        line = f'\n"{source_data["system"]}","{source_data["name"]}","{source_data["release"]}","{source_data["developer"]}","{source_data["formats"]}",'
        file.write(line)

def install_core(name):
    systems = load_systems(SOURCE_SYSTEMS_FILE)
    selected_system = systems[name]
    
    display_message('Installing new system...', 1)
    
    core_to_use = selected_system['bashhelper'] if selected_system['bashhelper'] else selected_system['core']
    try:
        copy_core_file(selected_system['core'])
        if selected_system['bashhelper']:
            copy_bashhelper_file(selected_system['bashhelper'])
        update_systems_cores(selected_system['system'], core_to_use)
        append_system_data(selected_system['system'], selected_system)
        display_message('System installed successfully', 2)
    except FileNotFoundError:
        display_message('Core, bashhelper, or info file not found, check new_cores.dat', 2)

def copy_core_file(core):
    source_path = f'data/new_cores/{core}'
    destination_path = f'/opt/retroarch/cores/{core}'
    shutil.copy2(source_path, destination_path)

    # Copy the .info file
    info_file = core.replace('.so', '.info')
    source_info_path = f'data/new_cores/{info_file}'
    destination_info_path = f'/opt/retroarch/cores/{info_file}'
    if os.path.exists(source_info_path):
        shutil.copy2(source_info_path, destination_info_path)
    else:
        display_message(f'Must provide {info_file} file', 5)
        raise FileNotFoundError(f'Info file {info_file} not found.')

    core_info_cache = '/opt/retroarch/cores/core_info.cache'
    if os.path.exists(core_info_cache):
        os.remove(core_info_cache)

def copy_bashhelper_file(bashhelper):
    source_path = f'data/new_cores/{bashhelper}'
    destination_path = f'/opt/retroarch/cores/{bashhelper}'
    shutil.copy2(source_path, destination_path)

def get_systems_from_file(file_path):
    systems = []
    with open(file_path, 'r') as file:
        lines = file.readlines()[1:]  # Skip header
        for line in lines:
            parts = line.strip().split(',')
            system = parts[0].strip('"')
            name = parts[1].strip('"')
            systems.append(name)
    return systems

def get_core_install_menu(menu_theme, window_size):
    menu = pygame_menu.Menu(
        title='System Installer',
        theme=menu_theme,
        width=window_size[0],
        height=window_size[1],
        mouse_visible=False,
    )
    systems = get_systems_from_file(SOURCE_SYSTEMS_FILE)
    for name in systems:
        menu.add.button(name, install_core, name)
    menu.add.button('Return to menu', pygame_menu.events.BACK)
    return menu

def get_main_menu(menu_theme, window_size):
    menu = pygame_menu.Menu(
        title='System Manager',
        theme=menu_theme,
        width=window_size[0],
        height=window_size[1],
        mouse_visible=False,
    )
    core_install_menu = get_core_install_menu(menu_theme, window_size)
    menu.add.button('System Installer', core_install_menu)
    menu.add.button('Restore Default Systems', restore_default_systems)
    menu.add.button('Return to menu', pygame_menu.events.BACK)
    return menu

if __name__ == '__main__':
    pygame.init()
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

    main_menu = get_main_menu(menu_theme, WINDOW_SIZE)
    main_menu.mainloop(surface)
