from typing import Optional

from langchain_core.messages import BaseMessage
from langchain_gigachat import GigaChat
from langgraph.prebuilt import create_react_agent

from src.application.tools import AnalyzeRiskTool
from src.domain.services.ipdf_adapter import IPdfAdapter
from src.shared.config import config


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
        return {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        }

    def get_agent(self):
        model = GigaChat(
            model="GigaChat-2-Max",
            verify_ssl_certs=False,
            credentials=config.GIGACHAT_API_KEY,
            scope='GIGACHAT_API_PERS'
        )
        tools = [self.analyze_risk_tool]
        agent = create_react_agent(model=model, tools=tools)
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
        return response


if __name__ == "__main__":
    orch = LLMAgentOrchestrator(
        pdf_adapter=IPdfAdapter(),
        analyze_risk_tool=AnalyzeRiskTool()
    )

    with open('../../../examples/data/Договор 10.00.02.26.03 Швецов Олег Андреевич.pdf', 'rb') as f:
        file_bytes = f.read()

    print(orch.execute(
        text='какие основные пункты в договоре?',
        pdf_bytes=file_bytes
    )['messages'][-1].content)