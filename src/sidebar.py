"""侧边栏"""

import dearpygui.dearpygui as dpg

from node import node_category, add_node


class Sidebar:
    """侧边栏类"""

    _SIDEBAR_WIDTH = 180

    def __init__(self):
        """初始化侧边栏"""
        with dpg.child_window(
            width=Sidebar._SIDEBAR_WIDTH, tag="__sidebar__", resizable_x=True
        ):
            for category, nodes in node_category.items():
                with dpg.collapsing_header(label=category, default_open=True):
                    for node in nodes:
                        dpg.add_button(
                            label=node,
                            callback=add_node,
                            user_data=nodes[node],
                            width=-1,
                        )
