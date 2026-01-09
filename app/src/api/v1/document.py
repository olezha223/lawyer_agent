from dishka import FromDishka
from fastapi import APIRouter, Form, File, UploadFile

from src.application.agent.llm_agent_orchestrator import LLMAgentOrchestrator

document_router = APIRouter(
    prefix="/document",
)


@document_router.post("/upload")
def upload_document():
    """Загрузка документа в базу знаний для RAG"""
    pass

@document_router.post("/analyze")
def analyze_document(
    orchestrator: FromDishka[LLMAgentOrchestrator],
    query: str = Form(..., description="Что сделать с документом"),
    file: UploadFile = File(..., description="Загружаемый"),
):
    """Анализ документа через агента"""
    if file.content_type != "application/pdf":
        return {"error": "Только PDF файлы"}
    pdf_bytes = file.read()

    return orchestrator.execute(
        text=query,
        pdf_bytes=pdf_bytes
    )
