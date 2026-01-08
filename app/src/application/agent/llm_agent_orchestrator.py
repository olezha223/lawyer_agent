from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from ..tools import AnalyzeRiskTool


class LLMAgentOrchestrator:
    def __init__(
            self,
            analyze_risk_tool: AnalyzeRiskTool,
    ):
        self.analyze_risk_tool = analyze_risk_tool

    def get_agent(self):
        model = ChatOpenAI(
            model="deepseek-r1",
            temperature=0.3,
            base_url="https://api.llm7.io/v1"
        )
        tools = [self.analyze_risk_tool]
        agent = create_agent(model=model, tools=tools)
        return agent
