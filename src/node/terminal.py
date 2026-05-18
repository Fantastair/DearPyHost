"""终端节点"""

import dearpygui.dearpygui as dpg

from node import Node

__all__ = ["TerminalNode"]


class TerminalNode(Node, category="显示"):
    """终端节点"""

    NAME = "终端"

    def __init__(self):
        """初始化终端节点"""
        self.tag_id = Node.generate_tag(prefix="terminal_node")[13:]

        with dpg.node(
            label="终端",
            tag=f"terminal_node_{self.tag_id}",
            parent="__node_editor__",
        ):
            with dpg.node_attribute(
                label="数据流",
                tag=f"terminal_input_{self.tag_id}",
                attribute_type=dpg.mvNode_Attr_Input,
            ):
                dpg.add_text("文本流输入")
            with dpg.node_attribute(
                label="显示屏",
                tag=f"terminal_display_{self.tag_id}",
                attribute_type=dpg.mvNode_Attr_Static,
            ):
                dpg.add_input_text(
                    width=320,
                    height=180,
                    tag=f"terminal_display_input_{self.tag_id}",
                    multiline=True,
                    readonly=True,
                )
            with dpg.node_attribute(
                label="控制台",
                tag=f"terminal_console_{self.tag_id}",
                attribute_type=dpg.mvNode_Attr_Output,
            ):
                dpg.add_input_text(
                    width=320,
                    tag=f"terminal_console_input_{self.tag_id}",
                )
