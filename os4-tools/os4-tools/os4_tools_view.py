import os
import subprocess
import configparser
import re
from os4_bridge import OS4

class OS4_Tools_View(object):
    def __init__(self):
        self.is_active = True
        self.current_menu = 'main'
        self.current_category = None
        self.is_info_mode = False
        self.main_menu_index = 0
        self.input_lockout_time = 0
        self.last_update_time = OS4.get_time()
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_file = os.path.join(self.base_dir, 'config.ini')
        self.config = configparser.ConfigParser()
        self.load_config()
        self.gen_main_menu()
    def load_config(self):
        try:
            if os.path.exists(self.config_file): self.config.read(self.config_file)
        except: pass
        for sec in ['Toggles', 'Selections']:
            if sec not in self.config: self.config[sec] = {}

    def save_config(self):
        try:
            with open(self.config_file, 'w') as f:
                self.config.write(f)
                OS4.show_notification('Settings Saved') 
        except Exception as e:
            print(f"Error saving config: {e}")

    def __set_positions(self):
        layout = OS4.get_layout()
        self.list_x = layout['list_x']
        self.list_y = layout['list_y']
        self.selector_x = layout['selector_x']
        self.selector_y = layout['selector_y']
        self.title_x = layout['title_x']
        self.title_y = layout['title_y']
        self.value_list_x = layout['value_list_x']
        self.scrap_info_title_y = layout['info_title_y']
        self.scrap_info_x = layout['info_x']
        self.scrap_info_y = layout['info_y']
        self.opt_info_y = layout['opt_info_y']

    def setup_info_widgets(self):
        ui = OS4.get_ui_constants()
        bg_image = OS4.get_theme_path('info_tate.bmp' if OS4.is_tate() else 'info.bmp')
        
        self.info_bg = OS4.Image(name='tools_info_bg', image=bg_image, position=('center', 'center'), colorkey=ui['color_key'])
        self.info_bg._layer = 10
        self.info_bg.hide()
        
        self.item_info_detail_title = OS4.Text(name='tools_info_title', text='details', is_active=True, font='title', is_upper=True, is_tate=OS4.is_tate(), position=('center', self.scrap_info_title_y), colorkey=ui['color_key'])
        self.item_info_detail = OS4.Text(name='tools_info_detail', text='', is_active=True, font='list', is_tate=OS4.is_tate(), position=(self.scrap_info_x, self.scrap_info_y), colorkey=ui['color_key'])
        self.item_info_detail_title._layer = 11
        self.item_info_detail._layer = 11
        self.item_info_detail_title.hide()
        self.item_info_detail.hide()
        self.is_info_mode = False
        
        self.item_info = OS4.Text(name='tools_item_info', text='', is_active=True, font='info', is_upper=True, is_tate=OS4.is_tate(), color=ui['info_color'], translate=False, position=('center', self.opt_info_y), colorkey=ui['color_key'])
        self.update_info()

    def gen_main_menu(self):
        self.__set_positions()
        self.destroy_widgets()
        ui = OS4.get_ui_constants()
        
        self.title = OS4.Text(name='tools_title', text='OS4 Tools', is_active=True, color=ui['title_color'], font='title', is_upper=True, is_tate=OS4.is_tate(), position=(self.title_x, self.title_y), colorkey=ui['color_key'])
        self.menu_items = []
        self.main_menu_data = []
        if os.path.exists(self.base_dir):
            for item in sorted(os.listdir(self.base_dir)):
                item_path = os.path.join(self.base_dir, item)
                if os.path.isdir(item_path) and not item.startswith('.') and not item.startswith('_'):
                    metadata = OS4.Utils.parse_folder_metadata(item_path)
                    clean_name = OS4.Utils.get_clean_name(item, metadata)
                    self.menu_items.append(clean_name)
                    self.main_menu_data.append({
                        'name': clean_name,
                        'path': item_path,
                        'info': metadata.get('info'),
                        'description': metadata.get('description')
                    })
        if not self.menu_items:
            self.menu_items = ['No categories found']
            
        self.option_list = OS4.List(name='tools_list', text=self.menu_items, is_active=True, font='list', translate=False, box_size=ui['line_size'], color=ui['list_color'], color_select=ui['list_select_color'], bg_color=ui['list_select_bg'], position=(self.list_x, self.list_y), line_space=ui['line_space'], list_size=ui['list_size'])
        self.option_list.index = self.main_menu_index
        self.option_list.refresh()
        
        self.item_selector = OS4.Selector(name='tools_sel', is_active=True, position=(self.selector_x, self.selector_y), line_space=ui['line_space'])
        self.option_list.append(self.item_selector)
        
        self.setup_info_widgets()
        
        self.container_view = OS4.Container.create(name='tools_view')
        OS4.Container.append(parent=OS4.Container.get_bg(), child=self.container_view)
        OS4.Container.append(parent=self.container_view, child=(self.title, self.option_list, self.info_bg, self.item_info_detail_title, self.item_info_detail, self.item_info))

    def gen_category_menu(self, category):
        self.__set_positions()
        self.destroy_widgets()
        ui = OS4.get_ui_constants()
        
        self.title = OS4.Text(name='category_title', text=category, is_active=True, color=ui['title_color'], font='title', is_upper=True, is_tate=OS4.is_tate(), position=(self.title_x, self.title_y), colorkey=ui['color_key'])
        category_dir = None
        if os.path.exists(self.base_dir):
            for item in os.listdir(self.base_dir):
                clean = re.sub(r'^\d+_', '', item).replace('_', ' ').title()
                if clean == category:
                    category_dir = os.path.join(self.base_dir, item)
                    break
        if not category_dir:
             category_dir = os.path.join(self.base_dir, category.lower().replace(' ', '_'))
        self.category_items = []
        self.script_items = []
        self.value_items = []
        if os.path.exists(category_dir):
            for file in sorted(os.listdir(category_dir)):
                file_path = os.path.join(category_dir, file)
                if file.endswith('.bash'):
                    metadata = OS4.Utils.parse_metadata(file_path)
                    name = OS4.Utils.get_clean_name(file, metadata)
                    sections = OS4.Utils.parse_bash_file(file_path)
                    item_type = metadata.get('type')
                    
                    if item_type == 'selection' and metadata.get('options'):
                        options = metadata.get('options')
                        status = 'Unknown'
                        if 'status' in sections:
                            try:
                                env = os.environ.copy()
                                env['CONFIG_FILE'] = self.config_file
                                env['RTK_CFG_FILE'] = OS4.get_config_file()
                                p = subprocess.run(['bash', '-c', sections['status']], capture_output=True, text=True, env=env)
                                status = p.stdout.strip()
                            except: pass
                        
                        if not status or status == 'Unknown':
                            status = self.config.get('Selections', name, fallback=metadata.get('default') if metadata.get('default') in options else options[0])

                        current_idx = next((i for i, opt in enumerate(options) if opt.lower() == status.lower()), 0)
                        status = options[current_idx]
                        
                        self.category_items.append({'type': 'selection', 'name': name, 'path': file_path, 'sections': sections, 'options': options, 'current_idx': current_idx, 'description': metadata.get('description'), 'info': metadata.get('info')})
                        self.value_items.append(self._format_selection_value(status, current_idx, len(options)))

                    elif 'on' in sections and 'off' in sections:
                        status = OS4.Utils.get_toggle_status(name, self.config, self.config_file, sections.get('status'))
                        self.category_items.append({'type': 'toggle', 'name': name, 'path': file_path, 'sections': sections, 'status': status, 'description': metadata.get('description'), 'info': metadata.get('info')})
                        self.value_items.append('<l_on><r_on>' if status == 'on' else '<l_off><r_off>')
                    else:
                        self.category_items.append({'type': 'script', 'name': name, 'path': file_path, 'description': metadata.get('description'), 'info': metadata.get('info')})
                        self.value_items.append('')
                        
        if not self.category_items:
            self.script_items.append('No scripts found')
            self.value_items.append('')
        else:
            self.script_items = [item['name'] for item in self.category_items]
            
        self.option_list = OS4.List(name='category_list', text=self.script_items, is_active=True, font='list', translate=False, box_size=ui['line_size'], color=ui['list_color'], color_select=ui['list_select_color'], bg_color=ui['list_select_bg'], position=(self.list_x, self.list_y), line_space=ui['line_space'], list_size=ui['list_size'])
        self.value_list = OS4.List(name='category_values', text='dummy', is_active=True, font='list', translate=False, box_size=ui['line_size'], color=ui['list_val_color'], color_select=ui['list_select_val_color'], bg_color=ui['list_select_bg'], position=(self.value_list_x, ui['value_list_y']), align='right', line_space=ui['line_space'], list_size=ui['list_size'])
        self.value_list.set_txt_list(text=self.value_items, index=0, l_icon_space=False)
        
        self.item_selector = OS4.Selector(name='category_sel', is_active=True, position=(self.selector_x, self.selector_y), line_space=ui['line_space'])
        self.option_list.append(self.item_selector)
        
        self.setup_info_widgets()
        
        self.container_view = OS4.Container.create(name='category_view')
        OS4.Container.append(parent=OS4.Container.get_bg(), child=self.container_view)
        OS4.Container.append(parent=self.container_view, child=(self.title, self.option_list, self.value_list, self.info_bg, self.item_info_detail_title, self.item_info_detail, self.item_info))

    def _format_selection_value(self, status, current_idx, total_options):
        if total_options > 1:
            if current_idx == 0:
                return f"|{status}|r_arrow"
            elif current_idx == total_options - 1:
                return f"l_arrow|{status}"
            else:
                return f"l_arrow|{status}|r_arrow"
        return status

    def activate(self):
        self.container_view.activate()
        if not self.is_info_mode:
            self.info_bg.hide()
            self.item_info_detail_title.hide()
            self.item_info_detail.hide()
            self.option_list.show_selector()
        else:
            self.info_bg.show()
            self.item_info_detail_title.show()
            self.item_info_detail.show()
            self.option_list.hide_selector()

    def deactivate(self):
        self.container_view.deactivate()

    def destroy_widgets(self):
        try:
            if hasattr(self, 'container_view'):
                self.container_view.destroy(opid=OS4.Container.get_random_id())
        except:
            pass

    def update(self, event):
        keys = OS4.get_input_keys()
        
        if event.down and (not OS4.is_action_stopped()):
            OS4.stop_action()
            if event.key == keys['UP']:
                if not self.is_info_mode:
                    self.option_list.goto_prev_item()
                    if self.current_menu == 'category' and hasattr(self, 'value_list'):
                        self.value_list.goto_prev_item()
                    self.update_info()
            elif event.key == keys['DOWN']:
                if not self.is_info_mode:
                    self.option_list.goto_next_item()
                    if self.current_menu == 'category' and hasattr(self, 'value_list'):
                        self.value_list.goto_next_item()
                    self.update_info()
            elif event.key == keys['LEFT']:
                if self.current_menu == 'category' and not self.is_info_mode:
                    self.handle_horizontal_input('left')
            elif event.key == keys['RIGHT']:
                if self.current_menu == 'category' and not self.is_info_mode:
                    self.handle_horizontal_input('right')
            elif event.key == keys['A'] or event.key == keys['ENTER']:
                if self.is_info_mode:
                    self.toggle_info_mode()
                else:
                    self.handle_selection()
            elif event.key == keys['B'] or event.key == keys['BACKSPACE']:
                if self.is_info_mode:
                    self.toggle_info_mode()
                elif self.current_menu == 'category':
                    self.current_menu = 'main'
                    self.current_category = None
                    self.gen_main_menu()
                else:
                    OS4.quit_attempt()
            elif (keys['SELECT'] and event.key == keys['SELECT']) or \
                 (keys['X'] and event.key == keys['X']) or \
                 (keys['KEY_X'] and event.key == keys['KEY_X']):
                self.handle_info()

    def handle_horizontal_input(self, direction):
        item_index = self.option_list.get_list_info()[0]
        if item_index < len(self.category_items):
            item = self.category_items[item_index]
            if item['type'] == 'toggle':
                self.handle_toggle()
            elif item['type'] == 'selection':
                self.handle_selection_change(item, item_index, direction)

    def handle_selection_change(self, item, index, direction):
        options = item['options']
        current_idx = item['current_idx']
        new_idx = current_idx
        
        if direction == 'left':
            if current_idx > 0:
                new_idx -= 1
        elif direction == 'right':
            if current_idx < len(options) - 1:
                new_idx += 1
                
        if new_idx != current_idx:
            item['current_idx'] = new_idx
            new_value = options[new_idx]
            
            func_name = new_value.lower().replace(' ', '_')
            if func_name in item['sections']:
                script = item['sections'][func_name]
                OS4.Utils.run_toggle_script(script, self.config_file)
            
            if 'Selections' not in self.config:
                self.config['Selections'] = {}
            self.config['Selections'][item['name']] = new_value
            self.save_config()
            
            val_str = self._format_selection_value(new_value, new_idx, len(options))
            
            self.value_items[index] = val_str
            self.value_list.set_txt_list(text=self.value_items, index=index, l_icon_space=False)
            self.value_list.refresh(force_refresh=True)

    def get_selected_item_data(self):
        item_index = self.option_list.get_list_info()[0]
        if self.current_menu == 'category':
            if hasattr(self, 'category_items') and item_index < len(self.category_items):
                return self.category_items[item_index]
        elif self.current_menu == 'main':
            if hasattr(self, 'main_menu_data') and item_index < len(self.main_menu_data):
                return self.main_menu_data[item_index]
        return None

    def handle_info(self):
        item = self.get_selected_item_data()
        if item and item.get('description'):
            full_text = item['description']
            if OS4.is_tate():
                max_chars = 20
            else:
                max_chars = 28
            text = OS4.Utils.wrap_text(full_text, max_chars)
            self.item_info_detail.set_text(text=text)
            self.toggle_info_mode()
        else:
            OS4.show_notification('No description available')

    def toggle_info_mode(self):
        if self.is_info_mode:
            self.is_info_mode = False
            self.item_info_detail_title.hide()
            self.item_info_detail.hide()
            self.info_bg.hide()
            self.option_list.show_selector()
        else:
            self.is_info_mode = True
            self.item_info_detail_title.show()
            self.item_info_detail.show()
            self.info_bg.show()
            self.option_list.hide_selector()

    def handle_toggle(self):
        item_index = self.option_list.get_list_info()[0]
        if item_index < len(self.category_items):
            item = self.category_items[item_index]
            if item['type'] == 'toggle':
                current_status = item['status']
                new_status = 'off' if current_status == 'on' else 'on'
                script = item['sections'][new_status]
                success = OS4.Utils.run_toggle_script(script, self.config_file)
                if success:
                    item['status'] = new_status
                    if 'status' not in item['sections']:
                        self.config['Toggles'][item['name']] = new_status
                        self.save_config()
                    if new_status == 'on':
                        self.value_items[item_index] = '<l_on><r_on>'
                    else:
                        self.value_items[item_index] = '<l_off><r_off>'
                    self.value_list.set_txt_list(text=self.value_items, index=item_index, l_icon_space=False)
                    self.value_list.refresh(force_refresh=True)

    def update_info(self):
        item = self.get_selected_item_data()
        if item and item.get('info'):
            self.item_info.set_text(text=item.get('info'))
        else:
            self.item_info.set_text(text='')
        self.item_info.set_position(position=('center', self.opt_info_y), is_tate=OS4.is_tate())

    def handle_selection(self):
        item_index = self.option_list.get_list_info()[0]
        if self.current_menu == 'main':
            self.main_menu_index = item_index
            selection = self.menu_items[item_index]
            if selection == 'No categories found':
                pass
            else:
                self.current_menu = 'category'
                self.current_category = selection
                self.gen_category_menu(selection)
        elif self.current_menu == 'category':
            if not self.category_items:
                pass
            else:
                item = self.category_items[item_index]
                if item['type'] == 'script':
                    OS4.show_notification('Executing...')
                    OS4.force_render()
                    self.draw(OS4.get_time()) 
                    
                    OS4.cmd(f'bash "{item["path"]}"')
                    OS4.show_notification('Complete')
                elif item['type'] == 'toggle':
                    self.handle_toggle()
                elif item['type'] == 'selection':
                    pass

    def draw(self, time_step):
        self.option_list.scroll_item_sel(speed=96, time_step=time_step)
        self.option_list.anim_selector(time_step=time_step)
