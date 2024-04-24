import os
import time
import pygame
import configparser
import launcher2 as l2
from launcher2 import *

make_common2 = l2.make_common

def make_common(system, game_path, config, is_global_nfs):
    make_common2(system, game_path, config, is_global_nfs)
    tweaks_dir = '/opt/rgbpi/ui/tweaks'
    sys_overrides_dir = os.path.join(tweaks_dir, 'sys_overrides')
    global_overrides_file = os.path.join(tweaks_dir, 'global_overrides.ini')
    extra_config = configparser.ConfigParser()
    extra_config.read(global_overrides_file)

    if 'common_config_overrides' in extra_config:
        for setting, value in extra_config['common_config_overrides'].items():
            remove_existing(config, setting)  
            config.append('{} = {}\n'.format(setting, value))  

    system_cfg_file = os.path.join(sys_overrides_dir, '{}.cfg'.format(system))
    if os.path.exists(system_cfg_file):
        append_from_cfg(system_cfg_file, config)

def remove_existing(config, setting):
    for c in config[:]:
        if c.startswith('{} ='.format(setting)):
            config.remove(c)

def append_from_cfg(file_path, config):
    if os.path.exists(file_path):
        with open(file_path, 'r') as cfg_file:
            for line in cfg_file:
                line = line.strip()
                if line and not line.startswith('#'): 
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    remove_existing(config, key)
                    config.append('{} = {}\n'.format(key, value))

l2.make_common = make_common
launch_content2 = l2.launch_content

def launch_content():
    supported_systems = ('saturn', 'psp', 'nds', 'tic80', 'vb', 'atari5200', 'jaguar', 'atarilynx', 'wonderswan', 'wonderswancolor', 'videopac', 'cdi',)
    if cglobals.launcher['system'] not in supported_systems:
        return launch_content2()


    arcade_mode = cglobals.launcher['arcade_mode']
    neogeo_mode = cglobals.launcher['neogeo_mode']
    lgun_mode = cglobals.launcher['lgun_mode']
    system = cglobals.launcher['system']
    game_path = cglobals.launcher['game_path']
    game_id = cglobals.launcher['game_id']
    return_view = cglobals.launcher['return_view']
    is_global_nfs = utils.is_global_nfs()
    if os.path.isfile(game_path + '.bussy'):
        rtk.notif_msg.display(text='game_in_use_info')
    else:
        cglobals.sound_mgr.pause_music()
        pygame.display.quit()
        eq_preset = rtk.cfg_preset
        is_system_preset = False
        if system in cglobals.presets:
            is_system_preset = True
            cglobals.sound_mgr.set_preset(preset=system)
        if is_global_nfs:
            utils.cmd('touch ' + game_path + '.bussy')
            auto_load_file = game_path.rsplit('.', 1)[0] + '.state.auto'
            utils.cmd('rm "' + auto_load_file + '"')
        if cglobals.netplay == 'on':
            if cglobals.netplay_mode == 'client':
                netplay_cmd = ' --connect ' + cglobals.network_server_ip
            elif cglobals.netplay_mode == 'server':
                netplay_cmd = ' --host '
        else:
            netplay_cmd = ''
        if cglobals.launcher['lgun_mode'] and rtk.cfg_lgun_color_rep == 'on':
            if rtk.cfg_flicker_reduction == 'on':
                color_cmd = ' --set-shader /opt/rgbpi/ui/data/shaders/lgun_linear.glslp '
            else:
                color_cmd = ' --set-shader /opt/rgbpi/ui/data/shaders/lgun_nolinear.glslp '
        else:
            color_cmd = ''
        path_retroarch = rtk.path_retroarch
        path_cores = rtk.path_cores
        start_date = time.time()
        rtk.logging.info('Game launch info:')
        rtk.logging.info('> arcade_mode: %s', arcade_mode)
        rtk.logging.info('> neogeo_mode: %s', neogeo_mode)
        rtk.logging.info('> lgun_mode: %s', lgun_mode)
        rtk.logging.info('> system: %s', system)
        rtk.logging.info('> game_path: %s', game_path)
        rtk.logging.info('> netplay_cmd: %s', netplay_cmd)
        rtk.logging.info('> color_cmd: %s', color_cmd)
        rtk.logging.info('> path_retroarch: %s', path_retroarch)
        rtk.logging.info('> path_cores: %s', path_cores)
        if cglobals.launcher['lgun_mode']:
            utils.set_core_crosshair(crosshair=False)
        else:
            utils.set_core_crosshair(crosshair=True)
        if cglobals.launcher['lgun_mode']:
            utils.remove_neogeo_remaps()
        retroarch_cfg_file = make_console_cfg_file(system, is_global_nfs)
        rtk.logging.debug('> retroarch_cfg_file (console): %s', retroarch_cfg_file)
        device_cmd = set_device_type(system, game_path)
        if not rtk.cfg_user_scrap == 'on' and cglobals.launcher['lgun_mode']:
            utils.clean_screenshot(system)
        utils.cmd('clear')
        pygame.display.quit()

        try:
            if '.sh' in game_path:
                launch_command = '"' + game_path + '"'
                utils.cmd('chmod +x ' + launch_command)
            elif system == 'videopac':
                launch_command = path_retroarch + color_cmd + device_cmd + netplay_cmd + ' -L ' + path_cores + '/o2em_libretro.so --appendconfig=' + retroarch_cfg_file + ' "' + game_path + '"'
            elif system == 'wonderswancolor':
                launch_command = path_retroarch + color_cmd + device_cmd + netplay_cmd + ' -L ' + path_cores + '/mednafen_wswan_libretro.so --appendconfig=' + retroarch_cfg_file + ' "' + game_path + '"'
            elif system == 'wonderswan':
                launch_command = path_retroarch + color_cmd + device_cmd + netplay_cmd + ' -L ' + path_cores + '/mednafen_wswan_libretro.so --appendconfig=' + retroarch_cfg_file + ' "' + game_path + '"'
            elif system == 'atarilynx':
                launch_command = path_retroarch + color_cmd + device_cmd + netplay_cmd + ' -L ' + path_cores + '/mednafen_lynx_libretro.so --appendconfig=' + retroarch_cfg_file + ' "' + game_path + '"'
            elif system == 'jaguar':
                launch_command = path_retroarch + color_cmd + device_cmd + netplay_cmd + ' -L ' + path_cores + '/virtualjaguar_libretro.so --appendconfig=' + retroarch_cfg_file + ' "' + game_path + '"'
            elif system == 'atari5200':
                launch_command = path_retroarch + color_cmd + device_cmd + netplay_cmd + ' -L ' + path_cores + '/atari800_libretro.so --appendconfig=' + retroarch_cfg_file + ' "' + game_path + '"'   
            elif system == 'psp':
                launch_command = path_retroarch + color_cmd + device_cmd + netplay_cmd + ' -L ' + path_cores + '/ppsspp_libretro.so --appendconfig=' + retroarch_cfg_file + ' "' + game_path + '"'  
            elif system == 'vb':
                launch_command = path_retroarch + color_cmd + device_cmd + netplay_cmd + ' -L ' + path_cores + '/mednafen_vb_libretro.so --appendconfig=' + retroarch_cfg_file + ' "' + game_path + '"'   
            elif system == 'tic80':
                launch_command = path_retroarch + color_cmd + device_cmd + netplay_cmd + ' -L ' + path_cores + '/tic80_libretro.so --appendconfig=' + retroarch_cfg_file + ' "' + game_path + '"'   
            elif system == 'saturn':
                launch_command = path_retroarch + color_cmd + device_cmd + netplay_cmd + ' -L ' + path_cores + '/yabasanshiro_libretro.so --appendconfig=' + retroarch_cfg_file + ' "' + game_path + '"'                  
            elif system == 'cdi':
                launch_command = path_cores + '/launchcdi.bash --appendconfig=' + retroarch_cfg_file + ' "' + game_path + '"'     #CDi script is so it can run at 480i             
            elif system == 'nds':
                launch_command = path_cores + '/launchnds.bash --appendconfig=' + retroarch_cfg_file + ' "' + game_path + '"'     #NDS script is needed since the core wouldnt launch without sleeping UI
        
            utils.cmd(launch_command)
            utils.write_stats(start=start_date, end=time.time())
            rtk.logging.info('> launch_command: %s', launch_command)
        except Exception as e:
            rtk.logging.error('Error in [Launcher]: %s', str(e))
        rtk.init_video()
        if is_global_nfs:
            utils.cmd('rm ' + game_path + '.bussy')
        utils.reset_key_pressed()
        if is_system_preset:
            cglobals.sound_mgr.set_preset(preset=eq_preset)
    if not game_id and rtk.cfg_user_scrap == 'on' and cglobals.launcher['lgun_mode']:
        rtk.popup_msg.display(text='loading')
        utils.gen_screenshot(game_id, system, game_path)
        rtk.popup_msg.hide()
    utils.reset_launcher()
    if cglobals.autoplay['do_launch'] is None:
        utils.clear_navigation(up_to_view=return_view)
        utils.goto_view(return_view)

l2.launch_content = launch_content