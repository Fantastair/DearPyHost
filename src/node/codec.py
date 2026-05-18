"""编解码器节点"""

import dearpygui.dearpygui as dpg

from node import Node

__all__ = ["EncoderNode", "DecoderNode"]


class EncoderNode(Node, category="数据处理"):
    """编码器节点"""

    NAME = "编码器"

    def __init__(self):
        """初始化编码器节点"""
        self.tag_id = Node.generate_tag(prefix="encoder_node")[12:]

        with dpg.node(
            label="编码器",
            tag=f"encoder_node_{self.tag_id}",
            parent="__node_editor__",
        ):
            with dpg.node_attribute(
                label="数据流",
                tag=f"encoder_input_{self.tag_id}",
                attribute_type=dpg.mvNode_Attr_Input,
            ):
                dpg.add_text("数据流输入")
            with dpg.node_attribute(
                label="编码方式",
                tag=f"encoder_method_{self.tag_id}",
                attribute_type=dpg.mvNode_Attr_Static,
            ):
                dpg.add_combo(
                    items=["ASCII", "十六进制", "Base64"],
                    label="编码方式",
                    width=80,
                    tag=f"encoder_method_combo_{self.tag_id}",
                    default_value="ASCII",
                )
            with dpg.node_attribute(
                label="数据流",
                tag=f"encoder_output_{self.tag_id}",
                attribute_type=dpg.mvNode_Attr_Output,
            ):
                dpg.add_text("数据流输出")


class DecoderNode(Node, category="数据处理"):
    """解码器节点"""

    NAME = "解码器"

    def __init__(self):
        """初始化解码器节点"""
        self.tag_id = Node.generate_tag(prefix="decoder_node")[12:]

        with dpg.node(
            label="解码器",
            tag=f"decoder_node_{self.tag_id}",
            parent="__node_editor__",
        ):
            with dpg.node_attribute(
                label="数据流",
                tag=f"decoder_input_{self.tag_id}",
                attribute_type=dpg.mvNode_Attr_Input,
            ):
                dpg.add_text("数据流输入")
            with dpg.node_attribute(
                label="解码方式",
                tag=f"decoder_method_{self.tag_id}",
                attribute_type=dpg.mvNode_Attr_Static,
            ):
                dpg.add_combo(
                    items=["ASCII", "十六进制", "Base64"],
                    label="解码方式",
                    width=80,
                    tag=f"decoder_method_combo_{self.tag_id}",
                    default_value="ASCII",
                )
            with dpg.node_attribute(
                label="数据流",
                tag=f"decoder_output_{self.tag_id}",
                attribute_type=dpg.mvNode_Attr_Output,
            ):
                dpg.add_text("数据流输出")
