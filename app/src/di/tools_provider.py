from dishka import Provider, Scope, provide

from src.application.tools import AnalyzeRiskTool


class ToolsProvider(Provider):
    scope = Scope.REQUEST

    analyze_risk_tool = provide(AnalyzeRiskTool, provides=AnalyzeRiskTool)
