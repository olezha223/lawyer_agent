from dishka import FromDishka
from dishka.integrations.fastapi import inject_sync
from fastapi import APIRouter, Form, File, UploadFile

from src.application.agent.llm_agent_orchestrator import LLMAgentOrchestrator
from src.domain.models.response import LLMResponse

document_router = APIRouter(
    prefix="/document",
)


@document_router.post("/upload")
@inject_sync
def upload_document():
    """Загрузка документа в базу знаний для RAG"""
    pass

@document_router.post("/analyze")
@inject_sync
def analyze_document(
    orchestrator: FromDishka[LLMAgentOrchestrator],
    query: str = Form(..., description="Что сделать с документом"),
    file: UploadFile = File(..., description="Загружаемый файл"),
) -> None:
    """Анализ документа через агента"""
    if file.content_type != "application/pdf":
        return {"error": "Доступны для анализа только PDF файлы"}
    pdf_bytes = file.read()

    res = orchestrator.execute(
        text=query,
        pdf_bytes=pdf_bytes
    )
    return None
