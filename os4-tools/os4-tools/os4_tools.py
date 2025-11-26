#!/usr/bin/env python3
from os4_bridge import OS4
from os4_tools_view import OS4_Tools_View
OS4.init_system()
view = OS4_Tools_View()
OS4.run_loop(view, 'os4_tools_view')
