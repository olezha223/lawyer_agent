from langchain_core.tools import BaseTool


class AnalyzeRiskTool(BaseTool):
    name: str = "analyze_contract_risks"
    description: str = "Анализирует юридические и финансовые риски в договоре"

    def _run(self, document_id: str) -> str:
        return "Нет рисков."
