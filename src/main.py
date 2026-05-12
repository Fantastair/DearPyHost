"""
DearPyHost — 主入口
"""

from pathlib import Path
import dearpygui.dearpygui as dpg

from keyboard import init_keyboard_handlers
from menubar import MenuBar
from sidebar import Sidebar
from node_editor import NodeEditor

CWD = Path(__file__).parent
DEFAULT_FONT_PATH = CWD / "assets" / "fonts" / "MapleMono.ttf"


def _on_window_close(sender, app_data, user_data):
    """窗口关闭回调"""
    dpg.delete_item(sender)


def _load_default_font(font_path: str | Path, size: int = 18):
    """加载默认字体"""
    if isinstance(font_path, Path):
        font_path = str(font_path)

    if not Path(font_path).exists():
        raise FileNotFoundError(f"字体文件未找到: {font_path}")

    with dpg.font_registry():
        default_font = dpg.add_font(font_path, size)
        dpg.bind_font(default_font)


def show_window():
    """构建主窗口和布局"""
    with dpg.window(
        label="DearPyHost", tag="__main_window__", on_close=_on_window_close
    ):
        MenuBar()
        with dpg.group(horizontal=True):
            Sidebar()
            NodeEditor()


def main():
    """入口函数"""
    dpg.create_context()
    _load_default_font(DEFAULT_FONT_PATH)
    dpg.create_viewport(title="DearPyHost", width=1280, height=720)

    init_keyboard_handlers()
    show_window()

    dpg.set_primary_window("__main_window__", True)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
