from dishka import Provider, Scope, provide

from src.application.agent.llm_agent_orchestrator import LLMAgentOrchestrator


class AgentProvider(Provider):
    scope = Scope.REQUEST

    base_agent = provide(LLMAgentOrchestrator, provides=LLMAgentOrchestrator)
