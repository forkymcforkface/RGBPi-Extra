#To add more cores, just zip them with 7z and place them in the cores folder. It will automatically show up in the RGBPi-Extra ui on next launch.
import os
import pygame_menu
import subprocess
import pygame
import shutil

CORES_FOLDER = 'cores'
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

def run_script(script_name, menu):
    script_path = os.path.join(CORES_FOLDER, f"{script_name}.7z")
    extracted_folder = "/root/temp"
    display_message('Extracting Core...')
    start_time = pygame.time.get_ticks()
    try:
        subprocess.run(["7z", "x", script_path, "-o" + extracted_folder, "-aoa"])
    except Exception as e:
        print(f"Error extracting core: {e}")
        return
    
    while pygame.time.get_ticks() - start_time < 3000:
        pass

    current_core_file = os.path.join("/opt/retroarch/cores", f"{script_name}.so")
    bak_file = current_core_file + '.bak'
    if not os.path.exists(bak_file):
        try:
            os.rename(current_core_file, bak_file)
        except Exception as e:
            print(f"Error creating .bak file: {e}")
            return

    extracted_core_path = os.path.join(extracted_folder, f"{script_name}.so")
    try:
        shutil.move(extracted_core_path, current_core_file)
    except Exception as e:
        print(f"Error moving core to /opt/retroarch/cores folder: {e}")
        return

    display_message('Moving Core...')
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < 2000:
        pass

def restore_default_cores():
    cores_directory = "/opt/retroarch/cores"
    display_message('Restoring Default Cores')
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < 3000:
        pass
    
    for file in os.listdir(cores_directory):
        if file.endswith(".bak"):
            bak_file = os.path.join(cores_directory, file)
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
    script_files = sorted(f for f in os.listdir(CORES_FOLDER) if os.path.isfile(os.path.join(CORES_FOLDER, f)))
    for script_file in script_files:
        script_name, script_ext = os.path.splitext(script_file)
        if script_ext.lower() == '.7z':
            menu.add.button(script_name, run_script, script_name, menu)
    menu.add.button('Restore Default Cores', restore_default_cores)
    menu.add.button('Return to menu', pygame_menu.events.BACK)
    return menu
