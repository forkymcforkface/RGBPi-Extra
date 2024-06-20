import os
import pygame_menu
import pygame
import shutil

CORES_FOLDER = 'data/cores'
SYSTEMS_FILE = '/opt/rgbpi/ui/data/systems.dat'
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WINDOW_SIZE = (290, 240)

# Mapping of systems to .so files
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
    'dreamcast': 'flycast_libretro.so',
    'naomi': 'flycast_libretro.so',
    'neogeo': 'fbneo_libretro.so',
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
    'pc': 'dosbox_pure_libretro.so',
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

def swap_core(core_file, system):
    original_core_file = os.path.join("/opt/retroarch/cores", SYSTEMS_TO_SO[system])
    backup_core_file = original_core_file + '_orig'
    new_core_file = os.path.join("/opt/retroarch/cores", os.path.basename(core_file))

    # Backup the original core file
    if not os.path.exists(backup_core_file):
        try:
            os.rename(original_core_file, backup_core_file)
        except Exception as e:
            print(f"Error creating backup file: {e}")
            return
    
    # Copy the new core file
    try:
        shutil.copy(core_file, new_core_file)
    except Exception as e:
        print(f"Error copying new core file: {e}")
        return

    # Rename the new core file to the original core file name
    try:
        os.rename(new_core_file, original_core_file)
    except Exception as e:
        print(f"Error renaming new core file: {e}")
        return

    display_message('Core Swapped Successfully')
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < 2000:
        pass

def get_systems():
    systems = []
    with open(SYSTEMS_FILE, 'r') as f:
        for line in f.readlines()[1:]:  # Skip header line
            if not any(x in line for x in ['lightgun', 'arcade', 'ports', 'script']):
                systems.append(line.split(',')[0].strip('"'))
    return systems

def select_system_menu(core_file, menu_theme):
    systems = get_systems()
    system_menu = pygame_menu.Menu(
        title='',
        width=WINDOW_SIZE[0],
        height=WINDOW_SIZE[1],
        theme=menu_theme,
        mouse_visible=False,
    )
    for system in systems:
        system_menu.add.button(system, swap_core, core_file, system)
    system_menu.add.button('Return to menu', pygame_menu.events.BACK)
    return system_menu

def get_core_swap_menu(menu_theme, window_size):
    menu = pygame_menu.Menu(
        title='',
        theme=menu_theme,
        joystick_enabled=True,
        width=window_size[0],
        height=window_size[1],
        mouse_visible_update=False,
    )
    core_files = sorted(f for f in os.listdir(CORES_FOLDER) if f.endswith('.so'))
    for core_file in core_files:
        submenu = select_system_menu(os.path.join(CORES_FOLDER, core_file), menu_theme)
        menu.add.button(core_file, submenu)
    menu.add.button('Restore Default Cores', restore_default_cores)
    menu.add.button('Return to menu', pygame_menu.events.BACK)
    return menu

def restore_default_cores():
    cores_directory = "/opt/retroarch/cores"
    display_message('Restoring Default Cores')
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < 3000:
        pass
    
    for file in os.listdir(cores_directory):
        if file.endswith("_orig"):
            orig_file = os.path.join(cores_directory, file)
            so_file = orig_file[:-5]
            try:
                os.rename(orig_file, so_file)
            except Exception as e:
                print(f"Error restoring core {so_file}: {e}")
