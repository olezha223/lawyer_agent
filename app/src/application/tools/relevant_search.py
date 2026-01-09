from typing import List, Dict, Any

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field, model_validator

from src.domain.services.iembedder import IEmbedder
from src.domain.services.ivdb_adapter import IVectorDB
from src.infra.documents.tools import to_core_document


class RagToolInput(BaseModel):
    """Входные данные для поиска в базе законов"""
    query: str = Field(
        description="Кусок документа или суждение языковой модели для поиска релевантных статей"
    )

    codex_name: str = Field(
        description=(
            "Название кодекса для поиска. "
            "Допустимые значения: Гражданский кодекс, Земельный кодекс, Жилищный кодекс"
        ),
        examples=["Гражданский кодекс", "Земельный кодекс", "Жилищный кодекс"]
    )

    @model_validator(mode='after')
    def validate_codex_name(self) -> str:
        """Валидация названия кодекса"""
        v_lower = self.codex_name.lower().strip()
        valid_codexes = {
            "Гражданский кодекс", "Земельный кодекс", "Жилищный кодекс",
        }
        if v_lower not in valid_codexes:
            raise ValueError(f"Недопустимый кодекс. Допустимые: {', '.join(valid_codexes)}")
        return self


class RagTool(BaseTool):
    name: str = "relevant_documents_search"
    description: str = (
        "Ищет релевантные статьи законов РФ на основе запроса. "
        "Используйте для поиска юридических норм, статей кодексов, правовых позиций. "
        "Принимает запрос и название кодекса (Гражданский кодекс, Земельный кодекс, Жилищный кодекс). "
        "Возвращает список документов с текстом статьи и метаданными."
    )
    args_schema: type[BaseModel] = RagToolInput

    def __init__(
            self,
            vdb_adapter: IVectorDB,
            embedder: IEmbedder,
    ):
        super().__init__()
        self._vdb_adapter = vdb_adapter
        self._embedder = embedder

    def _run(self, query: str, codex_name: str) -> List[Dict[str, str | Dict[str, str]]]:
        # 1) векторизовать запрос
        embedding = self._embedder.embed(query)

        # 2) найти похожие в базе данных в нужной коллекции
        documents = self._vdb_adapter.search(embedding, collection_name=codex_name)

        # 3) преобразовать в сущность CoreDocument
        core_documents = to_core_document(documents)
        return [doc.model_dump() for doc in core_documents]

    def to_dict(self) -> Dict[str, Any]:
        """Возвращает описание инструмента для агента"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "query": {"type": "string", "description": "Текст для поиска"},
                "codex_name": {
                    "type": "string",
                    "enum": ["Гражданский кодекс", "Земельный кодекс", "Жилищный кодекс"],
                    "description": "Название кодекса"
                }
            }
        }