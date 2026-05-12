"""键盘动作"""

import dearpygui.dearpygui as dpg

import node_editor

__all__ = ["init_keyboard_handlers", "on_key_pressed"]


def init_keyboard_handlers():
    """初始化键盘事件处理器"""
    with dpg.handler_registry():
        dpg.add_key_press_handler(callback=on_key_pressed)


def on_key_pressed(sender, app_data, user_data):
    """键盘按下回调"""
    ctrl = dpg.is_key_down(dpg.mvKey_ModCtrl)  # noqa: F841
    shift = dpg.is_key_down(dpg.mvKey_ModShift)  # noqa: F841
    alt = dpg.is_key_down(dpg.mvKey_ModAlt)  # noqa: F841
    badge = dpg.is_key_down(dpg.mvKey_ModSuper)  # noqa: F841

    if app_data == dpg.mvKey_Delete:
        if ctrl and shift:
            node_editor.clear_node_editor()
        else:
            node_editor.delete_selected_items()
