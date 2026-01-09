from typing import Optional

from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.messages import SystemMessage, HumanMessage, AIMessage

from ..tools import AnalyzeRiskTool
from ...domain.services.ipdf_adapter import IPdfAdapter


class LLMAgentOrchestrator:
    def __init__(
            self,
            # adapters
            pdf_adapter: IPdfAdapter,
            # tools
            analyze_risk_tool: AnalyzeRiskTool,
    ):
        self.pdf_adapter = pdf_adapter
        self.analyze_risk_tool = analyze_risk_tool

    def _prepare_messages(self, user_prompt: str, document_text: str = "") -> list[BaseMessage | dict[str, str]]:
        system_prompt = (
            "Ты ассистент, который помогает анализировать договор на наличие ошибок, "
            "уязвимостей, уловок и потенциальных опасностей для пользователя. "
            "Используй в своем ответе базу знаний законов РФ, а также инструменты для анализа документов. "
            "При использовании законов РФ приводи ссылку на соответствующую статью и свод законов. "
        )
        if document_text:
            system_prompt += f"Документ для анализа:\n{document_text[:10000]}\n\n"
        return [
            SystemMessage(system_prompt),
            HumanMessage(user_prompt)
        ]

    def get_agent(self):
        model = ChatOpenAI(
            model="deepseek-r1",
            temperature=0.3,
            base_url="https://api.llm7.io/v1"
        )
        tools = [self.analyze_risk_tool]
        agent = create_agent(model=model, tools=tools)
        return agent

    def execute(
            self,
            text: str,
            pdf_bytes: Optional[bytes] = None
    ) -> str:
        """
        Выполнить анализ документа

        Args:
            text: Семантический запрос пользователя
            pdf_bytes: Сырые байты PDF (Если пользователь указал их)
        """
        document_text = ""
        if pdf_bytes:
            document_text = self.pdf_adapter.parse_bytes(pdf_bytes)
        agent = self.get_agent()
        response = agent.invoke(self._prepare_messages(text, document_text))
        return response.content
