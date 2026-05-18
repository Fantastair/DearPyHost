"""正则提取器节点"""

import dearpygui.dearpygui as dpg

from node import Node

__all__ = ["RegexExtractorNode"]


class RegexExtractorNode(Node, category="数据处理"):
    """正则提取器节点"""

    NAME = "正则提取器"

    def __init__(self):
        """初始化正则提取器节点"""
        self.tag_id = Node.generate_tag(prefix="regex_extractor_node")[20:]

        with dpg.node(
            label="正则提取器",
            tag=f"regex_extractor_node_{self.tag_id}",
            parent="__node_editor__",
        ):
            with dpg.node_attribute(
                label="数据流",
                tag=f"regex_input_{self.tag_id}",
                attribute_type=dpg.mvNode_Attr_Input,
            ):
                dpg.add_text("数据流输入")
            with dpg.node_attribute(
                label="正则表达式",
                tag=f"regex_pattern_{self.tag_id}",
                attribute_type=dpg.mvNode_Attr_Static,
            ):
                dpg.add_input_text(
                    label="正则表达式",
                    width=150,
                    tag=f"regex_pattern_input_{self.tag_id}",
                )
            with dpg.node_attribute(
                label="数据流",
                tag=f"regex_output_{self.tag_id}",
                attribute_type=dpg.mvNode_Attr_Output,
            ):
                dpg.add_text("数据流输出")
