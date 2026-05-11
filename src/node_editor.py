"""节点编辑器"""

import dearpygui.dearpygui as dpg


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
