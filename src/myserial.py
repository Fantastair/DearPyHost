"""串口相关接口 — 非阻塞、缓冲区驱动的 STM32 串口封装"""

import threading
from queue import Queue, Empty
from typing import Callable

import serial
import serial.tools.list_ports

__all__ = ["SerialManager", "list_serial_ports"]

_SENTINEL_FLUSH = object()


def list_serial_ports() -> list[str]:
    """列出当前可用的串口设备名"""
    return [p.device for p in serial.tools.list_ports.comports()]


class SerialManager:
    """非阻塞串口管理器

    - 收发均在后端线程完成，方法调用立即返回
    - 发送基于 Queue（线程安全），数据到达阈值后一次性写出
    - 接收自动攒包，达到阈值回调用户函数
    - 缓冲区阈值可动态调整（≥1 字节）
    """

    _DATA_BITS_MAP = {8: serial.EIGHTBITS}
    _STOP_BITS_MAP = {1: serial.STOPBITS_ONE, 2: serial.STOPBITS_TWO}
    _PARITY_MAP = {
        "无校验": serial.PARITY_NONE,
        "奇校验": serial.PARITY_ODD,
        "偶校验": serial.PARITY_EVEN,
    }

    def __init__(self):
        # ── 连接参数 ──
        self.port: str = ""
        self.baudrate: int = 115200
        self.data_bits: int = 8
        self.stop_bits: int = 1
        self.parity: str = "无校验"

        # ── 内部状态 ──
        self._serial: serial.Serial | None = None
        self._send_queue: Queue = Queue()
        self._recv_cb: Callable[[bytes], None] | None = None
        self._recv_size: int = 1
        self._send_size: int = 1
        self._size_lock = threading.Lock()
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    # ------------------------------------------------------------------
    # 公开属性
    # ------------------------------------------------------------------

    @property
    def connected(self) -> bool:
        """是否已连接"""
        return self._serial is not None and self._serial.is_open

    @property
    def recv_buffer_size(self) -> int:
        """接收缓冲区阈值（字节）"""
        return self._recv_size

    @recv_buffer_size.setter
    def recv_buffer_size(self, size: int) -> None:
        if size < 1:
            raise ValueError("recv_buffer_size 必须 >= 1")
        with self._size_lock:
            self._recv_size = size

    @property
    def send_buffer_size(self) -> int:
        """发送缓冲区阈值（字节）"""
        return self._send_size

    @send_buffer_size.setter
    def send_buffer_size(self, size: int) -> None:
        if size < 1:
            raise ValueError("send_buffer_size 必须 >= 1")
        with self._size_lock:
            self._send_size = size

    @property
    def send_waiting(self) -> int:
        """发送队列中待发出的字节数（近似值）"""
        return self._send_queue.qsize()

    # ------------------------------------------------------------------
    # 连接管理
    # ------------------------------------------------------------------

    def connect(self) -> None:
        """打开串口并启动后台 I/O 线程"""
        if self.connected:
            self.disconnect()

        self._stop.clear()
        try:
            self._serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=self._DATA_BITS_MAP.get(self.data_bits, serial.EIGHTBITS),
                stopbits=self._STOP_BITS_MAP.get(self.stop_bits, serial.STOPBITS_ONE),
                parity=self._PARITY_MAP.get(self.parity, serial.PARITY_NONE),
                timeout=0.1,
                write_timeout=0.1,
            )
        except serial.SerialException as e:
            raise ConnectionError(f"无法打开串口 {self.port}: {e}") from e
        self._thread = threading.Thread(target=self._io_loop, daemon=True)
        self._thread.start()

    def disconnect(self) -> None:
        """关闭串口、停止后台线程、清空队列"""
        self._stop.set()
        if self._thread is not None and self._thread.is_alive():
            self._thread.join(timeout=1.0)
        if self._serial is not None and self._serial.is_open:
            self._serial.close()
        self._serial = None
        # 清空发送队列
        while not self._send_queue.empty():
            try:
                self._send_queue.get_nowait()
            except Empty:
                break

    # ------------------------------------------------------------------
    # 回调设置
    # ------------------------------------------------------------------

    def on_receive(self, callback: Callable[[bytes], None] | None) -> None:
        """设置接收回调（数据达到 recv_buffer_size 时触发）"""
        self._recv_cb = callback

    # ------------------------------------------------------------------
    # 发送（非阻塞）
    # ------------------------------------------------------------------

    def send(self, data: bytes) -> None:
        """将数据投入发送队列，立即返回。由后台线程攒够阈值后一次性发出。"""
        if not self.connected:
            raise ConnectionError("串口未连接")
        self._send_queue.put(data)

    def flush_send(self) -> None:
        """通知后台线程立即发出所有已入队数据"""
        self._send_queue.put(_SENTINEL_FLUSH)

    # ------------------------------------------------------------------
    # 后台 I/O 线程
    # ------------------------------------------------------------------

    def _io_loop(self) -> None:
        """单一线程处理收发：读串口 → 攒包回调；取发送队列 → 攒包写出"""
        recv_buf = bytearray()
        send_buf = bytearray()

        while not self._stop.is_set():
            ser = self._serial
            if ser is None or not ser.is_open:
                self._stop.wait(0.05)
                continue

            # ── 接收 ──
            try:
                n = ser.in_waiting
                if n > 0:
                    recv_buf.extend(ser.read(n))
                    with self._size_lock:
                        chunk_size = self._recv_size
                    while len(recv_buf) >= chunk_size:
                        chunk = bytes(recv_buf[:chunk_size])
                        del recv_buf[:chunk_size]
                        cb = self._recv_cb
                        if cb is not None:
                            cb(chunk)
            except (serial.SerialException, OSError):
                self._stop.wait(0.1)

            # ── 发送 ──
            try:
                while True:
                    item = self._send_queue.get_nowait()
                    if item is _SENTINEL_FLUSH:
                        # 强制发出 send_buf 中所有不足阈值的剩余数据
                        if send_buf:
                            self._safe_write(ser, bytes(send_buf))
                            send_buf.clear()
                    else:
                        send_buf.extend(item)
            except Empty:
                pass

            with self._size_lock:
                threshold = self._send_size
            while len(send_buf) >= threshold:
                chunk = bytes(send_buf[:threshold])
                del send_buf[:threshold]
                self._safe_write(ser, chunk)

            self._stop.wait(0.01)

    @staticmethod
    def _safe_write(ser: serial.Serial, data: bytes) -> None:
        """吞掉写入异常"""
        try:
            ser.write(data)
        except serial.SerialException:
            pass
