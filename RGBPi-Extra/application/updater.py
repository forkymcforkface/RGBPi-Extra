import os
import tarfile
import shutil
import subprocess
import urllib.request
import pygame
import glob

def display_loading_screen(screen, font, message):
    screen.fill(BLACK)
    text_surface = font.render(message, True, WHITE)
    screen.blit(text_surface, (WINDOW_SIZE[0] // 2 - text_surface.get_width() // 2,
                               WINDOW_SIZE[1] // 2 - text_surface.get_height() // 2))
    pygame.display.flip()

def remove_patch():
    allowed_systems = ['lightgun', 'arcade', 'atari2600', 'atari7800', 'pcengine', 'pcenginecd', 'nes', 'snes', 'n64', 'sgb', 'gba', 'sg1000', 'mastersystem', 'megadrive', 'segacd', 'sega32x', 'dreamcast', 'neogeo', 'neocd', 'ngp', 'psx', 'amstradcpc', 'c64', 'amiga', 'amigacd', 'x68000', 'msx', 'zxspectrum', 'pc', 'ports', 'scripts']

    RGBPI_UI_ROOT = '/opt/rgbpi/ui'
    launcher_py_path = os.path.join(RGBPI_UI_ROOT, 'launcher.py')
    launcher2_pyc_path = os.path.join(RGBPI_UI_ROOT, 'launcher2.pyc')
    tweaks_folder_path = os.path.join(RGBPI_UI_ROOT, 'tweaks')

    error_occurred = False

    if os.path.exists(launcher_py_path):
        os.remove(launcher_py_path)

    if os.path.exists(launcher2_pyc_path):
        try:
            os.rename(launcher2_pyc_path, os.path.join(RGBPI_UI_ROOT, 'launcher.pyc'))
        except Exception as e:
            print("Error renaming launcher2.pyc to launcher.pyc:", e)
            error_occurred = True

    if os.path.exists(tweaks_folder_path):
        try:
            shutil.rmtree(tweaks_folder_path)
        except Exception as e:
            print("Error removing tweaks folder:", e)
            error_occurred = True

    games_dat_path = '/media/*/dats/games.dat'
    favorites_dat_path = '/media/*/dats/favorites.dat'
    systems_dat_path = '/opt/rgbpi/ui/data/systems.dat'

    def filter_system_entries(dat_file_path):
        try:
            with open(dat_file_path, 'r+') as file:
                lines = file.readlines()
                file.seek(0)
                if 'Id' in lines[0]:
                    header = lines[0]
                    file.write(header)
                    for line in lines[1:]:
                        system = line.split(',')[2].strip('"')
                        if system.lower() in allowed_systems:
                            file.write(line)
                    file.truncate()
                else:
                    header = lines[0]
                    file.write(header)
                    for line in lines[1:]:
                        system = line.split(',')[0].strip('"')
                        if system.lower() in allowed_systems:
                            file.write(line)
                    file.truncate()
        except Exception as e:
            print("Error processing file:", dat_file_path)
            print("Error message:", e)
            error_occurred = True

    for file_path in glob.glob(games_dat_path):
        filter_system_entries(file_path)

    for file_path in glob.glob(favorites_dat_path):
        filter_system_entries(file_path)

    filter_system_entries(systems_dat_path)

    if error_occurred:
        print("An error occurred while updating files.")

pygame.init()
WINDOW_SIZE = (320, 240)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.event.set_blocked(pygame.MOUSEMOTION)
pygame.mouse.set_visible(False)
font = pygame.font.Font(pygame.font.get_default_font(), 14)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

repo_owner = "forkymcforkface"
repo_name = "RGBPi-Extra"
branch = "main"
path = "RGBPi-Extra"

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
grandparent_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))
os.chdir(grandparent_dir)

archive_file = os.path.join(grandparent_dir, f"{repo_name}-{branch}.tar.gz")
if os.path.exists(archive_file):
    os.remove(archive_file)

archive_url = f"https://github.com/{repo_owner}/{repo_name}/archive/{branch}.tar.gz"
display_loading_screen(screen, font, "Downloading Update")
try:
    urllib.request.urlretrieve(archive_url, archive_file)
except KeyboardInterrupt:
    display_loading_screen(screen, font, "Download Interrupted, Rebooting")
    pygame.time.wait(5000) 
    os.system('reboot')
except urllib.error.URLError:
    display_loading_screen(screen, font, "Download Failed, Rebooting")
    pygame.time.wait(5000)  
    os.system('reboot')
except Exception as e:
    display_loading_screen(screen, font, "Check Internet Connection, Rebooting")
    pygame.time.wait(5000)  
    os.system('reboot') 

temp_dir = os.path.join(grandparent_dir, "rgbpitemp")
os.makedirs(temp_dir, exist_ok=True)
with tarfile.open(archive_file, "r:gz") as tar:
    tar.extractall(path=temp_dir)

source_dir = os.path.join(temp_dir, f"{repo_name}-{branch}", path)
destination_dir = os.path.join(grandparent_dir, path)

if os.path.exists(destination_dir):
    shutil.rmtree(destination_dir)

shutil.move(source_dir, destination_dir)

shutil.rmtree(temp_dir)
os.remove(archive_file)

with subprocess.Popen(['df', '-P', grandparent_dir], stdout=subprocess.PIPE) as proc:
    output = proc.stdout.readlines()
    mount_point = output[1].decode().split()[5]

remove_patch()

main_script = os.path.join(destination_dir, "application", "main.py")
subprocess.Popen(["python", main_script])
