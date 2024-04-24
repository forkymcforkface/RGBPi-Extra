import os
import pygame_menu
import subprocess
import pygame

SCRIPTS_FOLDER = 'scripts'
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WINDOW_SIZE = (320, 240)

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
font = pygame.font.Font(pygame_menu.font.FONT_MUNRO, 14)

def make_script_executable(script_path):
    convert_to_unix_format(script_path)
    os.chmod(script_path, os.stat(script_path).st_mode | 0o111)

def convert_to_unix_format(script_path):
    with open(script_path, 'r', newline=None) as f:
        content = f.read()
    content = content.replace('\r\n', '\n')
    with open(script_path, 'w') as f:
        f.write(content)

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
    script_path = os.path.join(SCRIPTS_FOLDER, f"{script_name}.bash")
    make_script_executable(script_path)
    display_message('Script Executing')
    loading_text = ''
    loading_dots = 0
    loading_max_dots = 3
    loading_delay = 500
    last_loading_time = pygame.time.get_ticks()
    script_start_time = last_loading_time
    try:
        process = subprocess.Popen([script_path])
        while process.poll() is None or pygame.time.get_ticks() - script_start_time < 1900:
            current_time = pygame.time.get_ticks()
            if current_time - last_loading_time > loading_delay:
                last_loading_time = current_time
                loading_dots = (loading_dots + 1) % (loading_max_dots + 1)
                loading_text = '.' * loading_dots
                display_message('Script Executing', loading_text)
    except Exception as e:
        print(f"Error running script: {e}")
    screen.fill(BLACK)
    pygame.display.flip()

def get_rgbpi_tweaks_menu(menu_theme, WINDOW_SIZE):
    menu = pygame_menu.Menu(
        title='',
        theme=menu_theme,
        joystick_enabled=True,
        width=WINDOW_SIZE[0],
        height=WINDOW_SIZE[1],
        mouse_visible_update=False,
    )
    script_files = sorted(f for f in os.listdir(SCRIPTS_FOLDER) if os.path.isfile(os.path.join(SCRIPTS_FOLDER, f)))
    for script_file in script_files:
        script_name, script_ext = os.path.splitext(script_file)
        if script_ext.lower() == '.bash':
            menu.add.button(script_name, run_script, script_name, menu)
    menu.add.button('Return to menu', pygame_menu.events.BACK)
    return menu

if __name__ == '__main__':
    menu_theme = pygame_menu.themes.THEME_DEFAULT
    menu = get_rgbpi_tweaks_menu(menu_theme, WINDOW_SIZE)
    menu.mainloop(screen)
