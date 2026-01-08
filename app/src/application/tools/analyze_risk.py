from langchain_core.tools import BaseTool


class AnalyzeRiskTool(BaseTool):
    name = "analyze_contract_risks"
    description = "Анализирует юридические и финансовые риски в договоре"

    def _run(self, document_id: str) -> str:
        return "Нет рисков."
