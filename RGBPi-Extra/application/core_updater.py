import os
import pygame_menu
import subprocess
import pygame
import shutil

SOURCE_CORES_FOLDER = 'data/update_cores'
DESTINATION_CORES_FOLDER = '/opt/retroarch/cores'
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WINDOW_SIZE = (290, 240)

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

def extract_file(script_path, extracted_folder):
    if script_path.endswith('.7z'):
        subprocess.run(["7z", "x", script_path, "-o" + extracted_folder, "-aoa"])
    elif script_path.endswith('.zip'):
        subprocess.run(["unzip", "-o", script_path, "-d", extracted_folder])

def update_core(core_name, core_ext):
    extracted_folder = "/root/temp"
    if core_ext.lower() in ['.7z', '.zip']:
        core_path = os.path.join(SOURCE_CORES_FOLDER, f"{core_name}{core_ext}")
        display_message('Extracting Core...')
        start_time = pygame.time.get_ticks()
        try:
            extract_file(core_path, extracted_folder)
        except Exception as e:
            print(f"Error extracting core: {e}")
            return
        while pygame.time.get_ticks() - start_time < 3000:
            pass
        extracted_core_path = os.path.join(extracted_folder, f"{core_name}.so")
    elif core_ext.lower() == '.so':
        extracted_core_path = os.path.join(SOURCE_CORES_FOLDER, f"{core_name}.so")

    destination_core_file = os.path.join(DESTINATION_CORES_FOLDER, f"{core_name}.so")
    bak_file = destination_core_file + '.bak'

    if os.path.exists(destination_core_file):
        if not os.path.exists(bak_file):
            try:
                os.rename(destination_core_file, bak_file)
            except Exception as e:
                print(f"Error creating .bak file: {e}")
                return

        try:
            shutil.copy(extracted_core_path, destination_core_file)
        except Exception as e:
            print(f"Error copying core to {DESTINATION_CORES_FOLDER} folder: {e}")
            return

        display_message('Updating Core...')
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < 2000:
            pass
    else:
        display_message('No matching core to update')
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < 2000:
            pass

def restore_default_cores():
    display_message('Restoring')
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < 3000:
        pass

    for file in os.listdir(DESTINATION_CORES_FOLDER):
        if file.endswith(".bak"):
            bak_file = os.path.join(DESTINATION_CORES_FOLDER, file)
            so_file = bak_file[:-4]
            try:
                os.rename(bak_file, so_file)
            except Exception as e:
                print(f"Error restoring core {so_file}: {e}")

def get_core_updater_menu(menu_theme, WINDOW_SIZE):
    menu = pygame_menu.Menu(
        title='',
        theme=menu_theme,
        joystick_enabled=True,
        width=WINDOW_SIZE[0],
        height=WINDOW_SIZE[1],
        mouse_visible_update=False,
    )
    core_files = sorted(f for f in os.listdir(SOURCE_CORES_FOLDER) if os.path.isfile(os.path.join(SOURCE_CORES_FOLDER, f)))
    for core_file in core_files:
        core_name, core_ext = os.path.splitext(core_file)
        if core_ext.lower() in ['.7z', '.zip', '.so']:
            menu.add.button(core_name, update_core, core_name, core_ext)
    menu.add.button('Restore Default Cores', restore_default_cores)
    menu.add.button('Return to menu', pygame_menu.events.BACK)
    return menu
