"""节点编辑器"""

import dearpygui.dearpygui as dpg


__all__ = ["NodeEditor", "delete_selected_items", "clear_node_editor"]


class NodeEditor:
    """节点编辑器类"""

    def __init__(self):
        """初始化节点编辑器"""
        with dpg.node_editor(
            tag="__node_editor__",
            callback=self.on_link_created,
            delink_callback=self.on_link_deleted,
            minimap=True,
            minimap_location=dpg.mvNodeMiniMap_Location_BottomRight,
        ):
            pass

    def on_link_created(self, sender, app_data):
        """链接创建回调"""
        dpg.add_node_link(app_data[0], app_data[1], parent=sender)

    def on_link_deleted(self, sender, app_data):
        """链接删除回调"""
        dpg.delete_item(app_data)


def delete_selected_items():
    """删除选中的节点和链接"""
    selected_nodes = dpg.get_selected_nodes("__node_editor__")
    for node_tag in selected_nodes:
        if dpg.does_item_exist(node_tag):
            dpg.delete_item(node_tag)
    selected_links = dpg.get_selected_links("__node_editor__")
    for link_tag in selected_links:
        if dpg.does_item_exist(link_tag):  # ty: ignore[invalid-argument-type]
            dpg.delete_item(link_tag)  # ty: ignore[invalid-argument-type]


def clear_node_editor():
    """清空节点编辑器"""
    dpg.delete_item("__node_editor__", children_only=True)
