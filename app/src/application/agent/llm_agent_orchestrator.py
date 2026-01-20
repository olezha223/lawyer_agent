from typing import Optional

from langchain_core.messages import BaseMessage
from langchain_gigachat import GigaChat
from langgraph.prebuilt import create_react_agent
from qdrant_client import QdrantClient

from src.application.tools import AnalyzeRiskTool, RagTool
from src.domain.services.ipdf_adapter import IPdfAdapter
from src.infra.embeddings.bge import BGEEmbedder
from src.infra.pdf.pypdf2_adapter import PyPdf2Adapter
from src.infra.vdb.qdrant_adapter import QdrantAdapter
from src.shared.config import config


class LLMAgentOrchestrator:
    def __init__(
            self,
            # adapters
            pdf_adapter: IPdfAdapter,
            # tools
            analyze_risk_tool: AnalyzeRiskTool,
            rag_tool: RagTool
    ):
        self.pdf_adapter = pdf_adapter
        self.analyze_risk_tool = analyze_risk_tool
        self.rag_tool = rag_tool

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
            model="GigaChat-2-Pro",
            verify_ssl_certs=False,
            credentials=config.GIGACHAT_API_KEY,
            scope='GIGACHAT_API_PERS'
        )
        tools = [self.analyze_risk_tool, self.rag_tool]
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
        response = agent.invoke(self._prepare_messages(text, document_text), {"recursion_limit": 100})
        return response


if __name__ == "__main__":
    qdrant = QdrantAdapter()
    orch = LLMAgentOrchestrator(
        pdf_adapter=PyPdf2Adapter(),
        analyze_risk_tool=AnalyzeRiskTool(),
        rag_tool=RagTool(vdb_adapter=qdrant, embedder=BGEEmbedder())
    )

    with open('../../../examples/data/Договор 10.00.02.26.03 Швецов Олег Андреевич.pdf', 'rb') as f:
        file_bytes = f.read()

    print(orch.execute(
        text='Что ты можешь сказать о соответствии этого договора гражданскому кодексу?',
        pdf_bytes=file_bytes
    )['messages'][-1].content)
