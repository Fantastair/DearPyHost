"""FFT分析器节点"""

import dearpygui.dearpygui as dpg

from node import Node

__all__ = ["FFTNode"]


class FFTNode(Node, category="数据处理"):
    """FFT分析器节点"""

    NAME = "FFT分析器"

    def __init__(self):
        """初始化FFT分析器节点"""
        self.tag_id = Node.generate_tag(prefix="fft_node")[8:]

        with dpg.node(
            label="FFT分析器",
            tag=f"fft_node_{self.tag_id}",
            parent="__node_editor__",
        ):
            with dpg.node_attribute(
                label="数据流",
                tag=f"fft_input_{self.tag_id}",
                attribute_type=dpg.mvNode_Attr_Input,
            ):
                dpg.add_text("数据流输入")
            with dpg.node_attribute(
                label="频谱图",
                tag=f"fft_spectrum_{self.tag_id}",
                attribute_type=dpg.mvNode_Attr_Static,
            ):
                dpg.add_plot(
                    width=480,
                    height=160,
                    tag=f"fft_spectrum_plot_{self.tag_id}",
                    anti_aliased=True,
                    equal_aspects=True,
                )
