import os
import pygame_menu
import pygame
import shutil

SOURCE_SYSTEMS_FILE = 'data/systems.dat'
DESTINATION_SYSTEMS_FILE = '/opt/rgbpi/ui/data/systems.dat'
BACKUP_SYSTEMS_FILE = '/opt/rgbpi/ui/data/systems.dat.bak'
AUTOSTART_FILE = '/opt/rgbpi/autostart.sh'
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WINDOW_SIZE = (290, 240)

EXCLUDED_SYSTEMS = [
    'arcade', 'lightgun', 'fbneo', 'mame', 'naomi', 'dreamcast', 'ports', 'scripts', 'amstradcpc', 'c64', 'amiga', 'msx', 'zxspectrum', 'pc'
]

SYSTEMS_TO_SO = {
    'atari2600': 'stella_libretro.so',
    'atari7800': 'prosystem_libretro.so',
    'pcengine': 'mednafen_supergrafx_libretro.so',
    'pcenginecd': 'mednafen_supergrafx_libretro.so',
    'nes': 'fceumm_libretro.so',
    'snes': 'snes9x_libretro.so',
    'n64': 'mupen64plus_next_libretro.so',
    'sgb': 'mgba_libretro.so',
    'gba': 'mgba_libretro.so',
    'sg1000': 'genesis_plus_gx_libretro.so',
    'mastersystem': 'genesis_plus_gx_libretro.so',
    'megadrive': 'genesis_plus_gx_libretro.so',
    'segacd': 'genesis_plus_gx_libretro.so',
    'sega32x': 'picodrive_libretro.so',
    'neocd': 'neocd_libretro.so',
    'ngp': 'mednafen_ngp_libretro.so',
    'psx': 'swanstation_libretro.so',
    'amstradcpc': 'cap32_libretro.so',
    'c64': 'vice_x64_libretro.so',
    'amiga': 'puae_libretro.so',
    'amigacd': 'puae_libretro.so',
    'x68000': 'px68k_libretro.so',
    'msx': 'bluemsx_libretro.so',
    'zxspectrum': 'fuse_libretro.so',
    'pc': 'dosbox_pure_libretro.so'
}

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
font = pygame.font.Font(pygame_menu.font.FONT_MUNRO, 14)

def display_message(message, loading_text=''):
    screen.fill(BLACK)
    text = font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
    screen.blit(text, text_rect)
    if loading_text:
        loading = font.render(loading_text, True, WHITE)
        loading_rect = loading.get_rect(center=(WINDOW_SIZE[0] // 2, (WINDOW_SIZE[1] // 2) + 20))
        screen.blit(loading, loading_rect)
    pygame.display.flip()

def load_systems(file_path):
    systems = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()[1:]  # Skip header
        for line in lines:
            parts = line.strip().split(',')
            system = parts[0].strip('"')
            name = parts[1].strip('"')
            release = parts[2].strip('"')
            developer = parts[3].strip('"')
            formats = parts[4].strip('"')
            newcore = parts[5].strip('"')
            romfolder = parts[6].strip('"')
            systems[name] = {
                'system': system,
                'name': name,
                'release': release,
                'developer': developer,
                'formats': formats,
                'newcore': newcore,
                'romfolder': romfolder
            }
    return systems

def backup_systems_file():
    if not os.path.exists(BACKUP_SYSTEMS_FILE):
        shutil.copy(DESTINATION_SYSTEMS_FILE, BACKUP_SYSTEMS_FILE)

def update_system(system, source_data):
    backup_systems_file()
    dest_file = DESTINATION_SYSTEMS_FILE
    with open(dest_file, 'r') as file:
        lines = file.readlines()

    with open(dest_file, 'w') as file:
        for line in lines:
            if line.startswith(f'"{system}"'):
                parts = line.strip().split(',')
                parts[1] = f'"{source_data["name"]}"'
                parts[2] = source_data["release"]
                parts[3] = f'"{source_data["developer"]}"'
                parts[4] = f'"{source_data["formats"]}"'
                line = ','.join(parts) + '\n'
            file.write(line)

def update_autostart(romfolder, dest_system, newcore, oldcore):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    drive = script_dir.split(os.sep)[2]
    bind_redirect = f'sudo mount --bind /media/{drive}/roms/{romfolder} /media/{drive}/roms/{dest_system}\n'
    bind_core = f'sudo mount --bind /opt/retroarch/cores/{newcore} /opt/retroarch/cores/{oldcore}\n'
    
    # Read the current autostart.sh content
    with open(AUTOSTART_FILE, 'r') as file:
        lines = file.readlines()
    
    # Check if redirect comments are already present
    redirect_rom_present = any('# redirect rom folders' in line for line in lines)
    redirect_core_present = any('# redirect cores' in line for line in lines)

    # Modify the autostart.sh content
    with open(AUTOSTART_FILE, 'w') as file:
        for line in lines:
            if line.startswith('/usr/bin/python3.9 /opt/rgbpi/ui/rgbpiui.pyc'):
                line = '/usr/bin/python3.9 /opt/rgbpi/ui/rgbpiui.pyc 2> /opt/rgbpi/ui/logs/error.log\n'
            file.write(line)
        if not redirect_rom_present:
            file.write('# redirect rom folders\n')
        file.write(bind_redirect)
        if not redirect_core_present:
            file.write('# redirect cores\n')
        file.write(bind_core)

def bind_mounts(source_data, dest_system):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    drive = script_dir.split(os.sep)[2]
    media_mountpoint = os.path.join('/', 'media', drive)
    
    romfolder = source_data['romfolder']
    newcore = source_data['newcore']
    
    dest_rom_path = os.path.join(media_mountpoint, 'roms', dest_system)
    source_rom_path = os.path.join(media_mountpoint, 'roms', romfolder)
    
    dest_core_path = os.path.join('/opt/retroarch/cores', SYSTEMS_TO_SO[dest_system])
    source_core_path = os.path.join('/opt/retroarch/cores', newcore)
    
    os.system(f'sudo mount --bind {source_rom_path} {dest_rom_path}')
    os.system(f'sudo mount --bind {source_core_path} {dest_core_path}')
    
    update_autostart(romfolder, dest_system, newcore, SYSTEMS_TO_SO[dest_system])

def swap_systems(source_system, dest_system):
    source_data = load_systems(SOURCE_SYSTEMS_FILE)[source_system]
    update_system(dest_system, source_data)
    bind_mounts(source_data, dest_system)
    display_message('System Swapped Successfully, Scan for Games')
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < 4000:
        pass

def restore_default_systems():
    if os.path.exists(BACKUP_SYSTEMS_FILE):
        shutil.copy(BACKUP_SYSTEMS_FILE, DESTINATION_SYSTEMS_FILE)
    
    with open(AUTOSTART_FILE, 'r') as file:
        lines = file.readlines()
    
    with open(AUTOSTART_FILE, 'w') as file:
        for line in lines:
            if not line.startswith(('sudo mount --bind', '# redirect rom folders', '# redirect cores')):
                line = line.replace('sleep 10\n', '')
                line = line.replace('&', '')
                file.write(line)

    display_message('Restored Default Systems')
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < 2000:
        pass

def get_systems_from_file(file_path):
    systems = []
    with open(file_path, 'r') as file:
        lines = file.readlines()[1:]  # Skip header
        for line in lines:
            parts = line.strip().split(',')
            system = parts[0].strip('"')
            name = parts[1].strip('"')
            if system not in EXCLUDED_SYSTEMS:
                systems.append((system, name))
    return systems

def select_dest_system_menu(source_system, menu_theme):
    dest_systems = get_systems_from_file(DESTINATION_SYSTEMS_FILE)
    dest_menu = pygame_menu.Menu(
        title='Select Destination System',
        width=WINDOW_SIZE[0],
        height=WINDOW_SIZE[1],
        theme=menu_theme,
        mouse_visible=False,
    )
    for system, name in dest_systems:
        dest_menu.add.button(name, swap_systems, source_system, system)
    dest_menu.add.button('Return to menu', pygame_menu.events.BACK)
    return dest_menu

def select_source_system_menu(menu_theme):
    source_systems = get_systems_from_file(SOURCE_SYSTEMS_FILE)
    source_menu = pygame_menu.Menu(
        title='Select Source System',
        width=WINDOW_SIZE[0],
        height=WINDOW_SIZE[1],
        theme=menu_theme,
        mouse_visible=False,
    )
    for system, name in source_systems:
        submenu = select_dest_system_menu(name, menu_theme)
        source_menu.add.button(name, submenu)
    source_menu.add.button('Return to menu', pygame_menu.events.BACK)
    return source_menu

def get_core_swap_menu(menu_theme, window_size):
    menu = pygame_menu.Menu(
        title='Core Swapper',
        theme=menu_theme,
        joystick_enabled=True,
        width=window_size[0],
        height=window_size[1],
        mouse_visible_update=False,
    )
    source_system_menu = select_source_system_menu(menu_theme)
    menu.add.button('Swap Systems', source_system_menu)
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

    core_swap_menu = get_core_swap_menu(menu_theme, WINDOW_SIZE)
    core_swap_menu.mainloop(surface)
