import os
import tarfile
import shutil
import subprocess
import urllib.request
import pygame
import glob
from tweaks_settings import remove_patch

remove_patch(reboot=False)

def display_loading_screen(screen, font, message):
    screen.fill(BLACK)
    text_surface = font.render(message, True, WHITE)
    screen.blit(text_surface, (WINDOW_SIZE[0] // 2 - text_surface.get_width() // 2,
                               WINDOW_SIZE[1] // 2 - text_surface.get_height() // 2))
    pygame.display.flip()

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

try:
    with open('/etc/os-release') as f:
        os_release = f.read()
    if 'bookworm' in os_release:
        branch = "pi-5"
except Exception:
    pass

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

display_loading_screen(screen, font, "Update Complete")
pygame.time.wait(3000)
remove_patch()

python_exec = 'python'
try:
    with open('/etc/os-release') as f:
        os_release = f.read()
    if 'bookworm' in os_release:
        python_exec = 'python3.9'
except Exception as e:
    print(f"An error occurred while determining the OS version: {e}")

main_script = os.path.join(destination_dir, "application", "main.py")
subprocess.Popen([python_exec, main_script])
