from launcher2 import *
import configparser
import os

def read_systems_cores(file_name):
    config_dirs = [os.path.join('/media', subdir, 'gameconfig', 'sys_override') for subdir in os.listdir('/media')]
    config = configparser.ConfigParser()
    systems_cores = {}
    for config_dir in config_dirs:
        config_path = os.path.join(config_dir, file_name)
        if os.path.isfile(config_path):
            config.read(config_path)
            if 'Systems' in config:
                systems_cores.update(config['Systems'])
            break
    return systems_cores

launch_content2 = launch_content

def launch_content():
    systems_cores = read_systems_cores('systems_cores.cfg')
    system = cglobals.launcher['system']
    if system not in systems_cores:
        return launch_content2()
    
    game_path = cglobals.launcher['game_path']
    return_view = cglobals.launcher['return_view']
    is_global_nfs = utils.is_global_nfs()
    
    try:
        cglobals.sound_mgr.pause_music()
        pygame.display.quit()
        
        if system in cglobals.presets:
            cglobals.sound_mgr.set_preset(preset=system)
        
        retroarch_cfg_file = make_console_cfg_file(system, is_global_nfs)
        device_cmd = set_device_type(system, game_path)
        
        utils.cmd('clear')
        
        core = systems_cores[system]
        if '.bash' in game_path:
            launch_command = f'"{game_path}"'
            utils.cmd(f'chmod +x {launch_command}')
        elif system == 'nds':
            launch_command = f'{rtk.path_cores}/launchnds.bash --appendconfig={retroarch_cfg_file} "{game_path}"'
        else:
            launch_command = f'{rtk.path_retroarch} {device_cmd} -L {rtk.path_cores}/{core} --appendconfig={retroarch_cfg_file} "{game_path}"'
        
        utils.cmd(launch_command)
        utils.write_stats(start=time.time(), end=time.time())
    except Exception as error:
        rtk.logging.error('Error in [Launcher]: %s', error)
    finally:
        rtk.init_video()
        utils.reset_key_pressed()
        utils.reset_launcher()
        if cglobals.autoplay['do_launch'] is None:
            utils.clear_navigation(up_to_view=return_view)
            utils.goto_view(return_view)
