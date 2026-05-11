"""侧边栏"""

import dearpygui.dearpygui as dpg


class Sidebar:
    """侧边栏类"""

    _SIDEBAR_WIDTH = 180

    def __init__(self):
        """初始化侧边栏"""
        with dpg.child_window(
            width=Sidebar._SIDEBAR_WIDTH, tag="__sidebar__", resizable_x=True
        ):
            pass
