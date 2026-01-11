from dishka import make_container

from .agent_provider import AgentProvider
from .infra_provider import InfraProvider
from .tools_provider import ToolsProvider

container = make_container(ToolsProvider(), InfraProvider(), AgentProvider())


__all__ = ("container",)

