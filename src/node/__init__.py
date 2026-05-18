"""节点库"""

# ruff: noqa: E402, F403

from __future__ import annotations
from abc import ABC, abstractmethod

__all__ = ["Node", "node_category", "add_node"]

_counter: int = 0  # 用于生成短唯一标签的计数器
node_category: dict[str, dict[str, type[Node]]] = {}  # 分类 -> 节点名称 -> 节点类


class Node(ABC):
    """节点基类"""

    NAME: str

    def __init_subclass__(cls, category: str | None = None, **kwargs):
        super().__init_subclass__(**kwargs)
        if "NAME" not in cls.__dict__:
            raise TypeError(
                f"{cls.__name__} 必须定义 NAME 类属性，例如 NAME = '串口收发器'"
            )
        if category is None:
            category = "默认分类"
        if category not in node_category:
            node_category[category] = {}
        if cls.NAME in node_category[category]:
            raise ValueError(
                f"节点名称 '{cls.NAME}' 在分类 '{category}' 中已存在，请修改节点类 {cls.__name__} 的 NAME 属性"
            )
        node_category[category][cls.NAME] = cls

    @abstractmethod
    def __init__(self):
        pass

    @classmethod
    def generate_tag(cls, prefix: str = "node") -> str:
        """生成短唯一标签"""
        global _counter
        _counter += 1
        return f"{prefix}_{_counter}"


def add_node(sender, app_data, user_data):
    """
    添加节点到编辑器

    Args:
        sender: 事件发送者
        app_data: 事件数据
        user_data: 节点类
    """
    user_data()


from .fft import *
from .codec import *
from .regex import *
from .terminal import *
from .serial_node import *
from .wave_display import *

from .fft import __all__ as _fft_all
from .codec import __all__ as _codec_all
from .regex import __all__ as _regex_all
from .terminal import __all__ as _terminal_all
from .serial_node import __all__ as _serial_all
from .wave_display import __all__ as _wave_display_all

__all__.extend(_fft_all)
__all__.extend(_codec_all)
__all__.extend(_regex_all)
__all__.extend(_serial_all)
__all__.extend(_terminal_all)
__all__.extend(_wave_display_all)
