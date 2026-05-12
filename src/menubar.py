"""菜单栏"""

import dearpygui.dearpygui as dpg

from modal_window import ModalWindow
from node import node_category, add_node
from node_editor import delete_selected_items, clear_node_editor


class MenuBar:
    """菜单栏类"""

    _MINIMAP_POS_MAP = {
        "__minimap_tl": dpg.mvNodeMiniMap_Location_TopLeft,
        "__minimap_tr": dpg.mvNodeMiniMap_Location_TopRight,
        "__minimap_bl": dpg.mvNodeMiniMap_Location_BottomLeft,
        "__minimap_br": dpg.mvNodeMiniMap_Location_BottomRight,
    }

    def __init__(self):
        """初始化菜单栏"""
        self.instructions_window: ModalWindow | None = None
        self.about_window: ModalWindow | None = None

        # 缩略图位置按钮选中态主题
        with dpg.theme(tag="__minimap_selected"):
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, [50, 70, 140])
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [70, 90, 170])
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [30, 50, 120])
                dpg.add_theme_color(dpg.mvThemeCol_Text, [255, 255, 255])

        with dpg.menu_bar(tag="__menu_bar__"):
            with dpg.menu(label="文件"):
                dpg.add_menu_item(label="新建")
                dpg.add_menu_item(label="打开")
                dpg.add_menu_item(label="保存")
                dpg.add_menu_item(label="另存为")
                dpg.add_menu_item(
                    label="退出 DearPyHost", callback=lambda: dpg.stop_dearpygui()
                )

            with dpg.menu(label="编辑"):
                with dpg.menu(label="放置"):
                    for category, nodes in node_category.items():
                        with dpg.menu(label=category):
                            for node in nodes:
                                dpg.add_menu_item(
                                    label=node, callback=add_node, user_data=nodes[node]
                                )
                dpg.add_menu_item(
                    label="删除选中项",
                    shortcut="(Del)",
                    callback=lambda sender, app_data, user_data: (
                        delete_selected_items()
                    ),
                )
                dpg.add_menu_item(
                    label="清空画布",
                    shortcut="(Ctrl+Shift+Del)",
                    callback=lambda sender, app_data, user_data: clear_node_editor(),
                )

            with dpg.menu(label="视图"):
                dpg.add_menu_item(
                    label="侧边栏",
                    check=True,
                    default_value=True,
                    callback=self.on_sidebar_show,
                )
                with dpg.menu(label="节点编辑器缩略图"):
                    dpg.add_menu_item(
                        label="显示",
                        check=True,
                        default_value=True,
                        callback=self.on_minimap_show,
                    )
                    with dpg.menu(label="位置"):
                        with dpg.group(horizontal=True):
                            user_data = [
                                "__minimap_tl",
                                "__minimap_tr",
                                "__minimap_bl",
                                "__minimap_br",
                            ]
                            size = 30
                            dpg.add_button(
                                label="↖",
                                tag=user_data[0],
                                callback=self.on_minimap_pos,
                                user_data=user_data,
                                width=size,
                                height=size,
                            )
                            dpg.add_button(
                                label="↗",
                                tag=user_data[1],
                                callback=self.on_minimap_pos,
                                user_data=user_data,
                                width=size,
                                height=size,
                            )
                        with dpg.group(horizontal=True):
                            dpg.add_button(
                                label="↙",
                                tag=user_data[2],
                                callback=self.on_minimap_pos,
                                user_data=user_data,
                                width=size,
                                height=size,
                            )
                            dpg.add_button(
                                label="↘",
                                tag=user_data[3],
                                callback=self.on_minimap_pos,
                                user_data=user_data,
                                width=size,
                                height=size,
                            )

            with dpg.menu(label="其他"):
                dpg.add_menu_item(label="操作说明", callback=self.show_instructions)
                dpg.add_menu_item(label="关于", callback=self.show_about)

        dpg.bind_item_theme(user_data[3], "__minimap_selected")

    def on_sidebar_show(self, sender, app_data, user_data):
        """侧边栏显示/隐藏回调"""
        if app_data:
            dpg.show_item("__sidebar__")
        else:
            dpg.hide_item("__sidebar__")

    def on_minimap_show(self, sender, app_data, user_data):
        """缩略图显示/隐藏回调"""
        dpg.configure_item("__node_editor__", minimap=app_data)

    def show_instructions(self):
        """显示操作说明窗口"""
        if self.instructions_window is None:
            self.instructions_window = ModalWindow(
                label="操作说明", tag="__instructions_window__", width=560, height=240
            )
        self.instructions_window.show()

    def show_about(self):
        """显示关于窗口"""
        if self.about_window is None:
            self.about_window = ModalWindow(
                label="关于 DearPyHost", tag="__about_window__", width=560, height=240
            )
        self.about_window.show()

    def on_minimap_pos(self, sender, app_data, user_data):
        """缩略图位置单选回调：通过主题高亮当前选中按钮"""
        for tag in user_data:
            if tag != sender:
                dpg.bind_item_theme(tag, 0)
            else:
                dpg.bind_item_theme(sender, "__minimap_selected")
        dpg.configure_item(
            "__node_editor__", minimap_location=MenuBar._MINIMAP_POS_MAP[sender]
        )
