"""模态窗口"""

import dearpygui.dearpygui as dpg


class ModalWindow:
    """模态窗口类"""

    def __init__(self, label: str, tag: str, width: int, height: int):
        """初始化模态窗口"""
        self.tag = tag
        self.width = width
        self.height = height

        with dpg.window(
            label=label,
            modal=True,
            tag=tag,
            width=width,
            height=height,
            no_resize=True,
            no_move=True,
            no_scrollbar=True,
        ):
            pass

    def show(self):
        """显示模态窗口"""
        dpg.show_item(self.tag)
        vp_width = dpg.get_viewport_client_width()
        vp_height = dpg.get_viewport_client_height()
        dpg.set_item_pos(
            self.tag, [(vp_width - self.width) // 2, (vp_height - self.height) // 2]
        )

    def hide(self):
        """隐藏模态窗口"""
        dpg.hide_item(self.tag)
