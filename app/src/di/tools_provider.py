from dishka import Provider, Scope, provide

from src.application.tools import AnalyzeRiskTool
from src.application.tools.relevant_search import RagTool


class ToolsProvider(Provider):
    scope = Scope.REQUEST

    analyze_risk_tool = provide(AnalyzeRiskTool, provides=AnalyzeRiskTool)
    rag_tool = provide(RagTool, provides=RagTool)
