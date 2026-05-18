"""波形显示器节点"""

import dearpygui.dearpygui as dpg

from node import Node

__all__ = ["WaveDisplayNode"]


class WaveDisplayNode(Node, category="显示"):
    """波形显示器节点"""

    NAME = "示波器"

    def __init__(self):
        """初始化波形显示器节点"""
        self.tag_id = Node.generate_tag(prefix="wave_display_node")[17:]

        with dpg.node(
            label="示波器",
            tag=f"wave_display_node_{self.tag_id}",
            parent="__node_editor__",
        ):
            with dpg.node_attribute(
                label="数据流",
                tag=f"wave_display_input_{self.tag_id}",
                attribute_type=dpg.mvNode_Attr_Input,
            ):
                dpg.add_text("数据流输入")
            with dpg.node_attribute(
                label="显示屏",
                tag=f"wave_display_{self.tag_id}",
                attribute_type=dpg.mvNode_Attr_Static,
            ):
                dpg.add_plot(
                    width=480,
                    height=160,
                    tag=f"wave_display_plot_{self.tag_id}",
                    anti_aliased=True,
                    equal_aspects=True,
                )
