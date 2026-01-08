from dishka import make_container

from .tools_provider import ToolsProvider

container = make_container(ToolsProvider())


__all__ = ("container",)

