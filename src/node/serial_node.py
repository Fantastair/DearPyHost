"""串口收发器节点"""

import dearpygui.dearpygui as dpg

from modal_window import ModalWindow
from node import Node
from myserial import SerialManager, list_serial_ports

__all__ = ["SerialNode"]

connect_error_window: None | ModalWindow = None


class SerialNode(Node, category="串口"):
    """串口收发器节点"""

    NAME = "串口收发器"

    def __init__(self):
        """初始化串口收发器节点"""
        self.tag_id = Node.generate_tag(prefix="serial_node")[12:]
        self.serial_manager = SerialManager()
        self.serial_manager.on_receive(self.on_serial_receive)

        with dpg.node(
            label=f"串口接收器{self.tag_id}",
            tag=f"serial_receiver_{self.tag_id}",
            parent="__node_editor__",
        ):
            with dpg.node_attribute(
                label="数据流",
                tag=f"serial_receive_{self.tag_id}",
                attribute_type=dpg.mvNode_Attr_Output,
            ):
                with dpg.group(horizontal=True):
                    dpg.add_button(
                        label="连接",
                        tag=f"serial_connect_{self.tag_id}",
                        callback=self.on_connect,
                    )
                    dpg.add_loading_indicator(
                        tag=f"serial_loading_{self.tag_id}",
                        style=3,
                        radius=1,
                        color=(233, 233, 233),
                        show=False,
                    )
                    dpg.add_text("数据流输出")
            with dpg.node_attribute(
                label="串口号",
                tag=f"serial_port_{self.tag_id}",
                attribute_type=dpg.mvNode_Attr_Static,
            ):
                dpg.add_combo(
                    items=list_serial_ports(),
                    label="串口号",
                    width=100,
                    tag=f"serial_port_combo_{self.tag_id}",
                )
            with dpg.node_attribute(
                label="波特率",
                tag=f"serial_baudrate_{self.tag_id}",
                attribute_type=dpg.mvNode_Attr_Static,
            ):
                dpg.add_input_int(
                    label="波特率",
                    default_value=115200,
                    width=100,
                    tag=f"serial_baudrate_input_{self.tag_id}",
                    min_value=1,
                    min_clamped=True,
                )
            with dpg.node_attribute(
                label="数据位",
                tag=f"serial_databits_{self.tag_id}",
                attribute_type=dpg.mvNode_Attr_Static,
            ):
                dpg.add_combo(
                    items=["8"],
                    label="数据位",
                    width=100,
                    tag=f"serial_databits_combo_{self.tag_id}",
                    default_value="8",
                )
            with dpg.node_attribute(
                label="停止位",
                tag=f"serial_stopbits_{self.tag_id}",
                attribute_type=dpg.mvNode_Attr_Static,
            ):
                dpg.add_combo(
                    items=["1", "2"],
                    label="停止位",
                    width=100,
                    tag=f"serial_stopbits_combo_{self.tag_id}",
                    default_value="1",
                )
            with dpg.node_attribute(
                label="校验位",
                tag=f"serial_parity_{self.tag_id}",
                attribute_type=dpg.mvNode_Attr_Static,
            ):
                dpg.add_combo(
                    items=["无校验", "偶校验", "奇校验"],
                    label="校验位",
                    width=100,
                    tag=f"serial_parity_combo_{self.tag_id}",
                    default_value="无校验",
                )
            with dpg.node_attribute(
                label="接收长度",
                tag=f"serial_recv_threshold_{self.tag_id}",
                attribute_type=dpg.mvNode_Attr_Static,
            ):
                dpg.add_input_int(
                    label="接收长度",
                    default_value=1,
                    width=100,
                    tag=f"serial_recv_threshold_input_{self.tag_id}",
                    min_value=1,
                    max_value=65536,
                    min_clamped=True,
                    max_clamped=True,
                )
        with dpg.node(
            label=f"串口发送器{self.tag_id}",
            tag=f"serial_sender_{self.tag_id}",
            parent="__node_editor__",
            pos=(200, 0),
        ):
            with dpg.node_attribute(
                label="数据流",
                tag=f"serial_send_{self.tag_id}",
                attribute_type=dpg.mvNode_Attr_Input,
            ):
                dpg.add_text("数据流输入")
            with dpg.node_attribute(
                label="发送长度",
                tag=f"serial_send_threshold_{self.tag_id}",
                attribute_type=dpg.mvNode_Attr_Static,
            ):
                dpg.add_input_int(
                    label="发送长度",
                    default_value=1,
                    width=100,
                    tag=f"serial_send_threshold_input_{self.tag_id}",
                    min_value=1,
                    max_value=65536,
                    min_clamped=True,
                    max_clamped=True,
                )

    def on_connect(self, sender, app_data, user_data):
        """连接按钮回调"""
        if not self.serial_manager.connected:
            dpg.configure_item(f"serial_loading_{self.tag_id}", show=True)
            dpg.configure_item(f"serial_connect_{self.tag_id}", label="连接中...")
            dpg.configure_item(f"serial_connect_{self.tag_id}", enabled=False)

            try:
                self.serial_manager.port = dpg.get_value(
                    f"serial_port_combo_{self.tag_id}"
                )
                self.serial_manager.baudrate = dpg.get_value(
                    f"serial_baudrate_input_{self.tag_id}"
                )
                self.serial_manager.data_bits = int(
                    dpg.get_value(f"serial_databits_combo_{self.tag_id}")
                )
                self.serial_manager.stop_bits = int(
                    dpg.get_value(f"serial_stopbits_combo_{self.tag_id}")
                )
                self.serial_manager.parity = dpg.get_value(
                    f"serial_parity_combo_{self.tag_id}"
                )
                self.serial_manager.recv_buffer_size = dpg.get_value(
                    f"serial_recv_threshold_input_{self.tag_id}"
                )
                self.serial_manager.connect()
            except ConnectionError as e:
                dpg.configure_item(f"serial_loading_{self.tag_id}", show=False)
                dpg.configure_item(f"serial_connect_{self.tag_id}", label="连接")
                dpg.configure_item(f"serial_connect_{self.tag_id}", enabled=True)
                global connect_error_window
                if connect_error_window is None:
                    connect_error_window = ModalWindow(
                        label="连接错误",
                        tag="__serial_connect_error_window__",
                        width=200,
                        height=80,
                    )
                    dpg.add_text(
                        f"连接失败：{str(e)}", parent="__serial_connect_error_window__"
                    )
                    dpg.add_button(
                        label="确定",
                        width=-1,
                        callback=connect_error_window.hide,
                        parent="__serial_connect_error_window__",
                    )
                connect_error_window.show()
                return

            dpg.configure_item(f"serial_loading_{self.tag_id}", show=False)
            dpg.configure_item(f"serial_connect_{self.tag_id}", label="断开连接")
            dpg.configure_item(f"serial_connect_{self.tag_id}", enabled=True)

            dpg.configure_item(f"serial_port_combo_{self.tag_id}", enabled=False)
            dpg.configure_item(f"serial_baudrate_input_{self.tag_id}", enabled=False)
            dpg.configure_item(f"serial_databits_combo_{self.tag_id}", enabled=False)
            dpg.configure_item(f"serial_stopbits_combo_{self.tag_id}", enabled=False)
            dpg.configure_item(f"serial_parity_combo_{self.tag_id}", enabled=False)
        else:
            self.serial_manager.disconnect()
            dpg.configure_item(f"serial_connect_{self.tag_id}", label="连接")
            dpg.configure_item(f"serial_port_combo_{self.tag_id}", enabled=True)
            dpg.configure_item(f"serial_baudrate_input_{self.tag_id}", enabled=True)
            dpg.configure_item(f"serial_databits_combo_{self.tag_id}", enabled=True)
            dpg.configure_item(f"serial_stopbits_combo_{self.tag_id}", enabled=True)
            dpg.configure_item(f"serial_parity_combo_{self.tag_id}", enabled=True)

    def on_serial_receive(self, data: bytes):
        """串口接收回调"""
        pass
