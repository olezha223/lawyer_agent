import json

from langchain_core.documents import Document
from qdrant_client import QdrantClient
from tqdm import tqdm

from scripts.splitter import split_by_numbered_points
from src.domain.models.document import CoreDocument
from src.infra.embeddings.bge import BGEEmbedder
from src.infra.vdb.qdrant_adapter import QdrantAdapter

qdrant = QdrantAdapter(client=QdrantClient(host='localhost', port=6333))
embedder = BGEEmbedder()
from langchain_text_splitters import RecursiveCharacterTextSplitter


with open("../examples/data/Гражданский кодекс.json", encoding='utf-8') as f:
    documents = json.load(f)

def convert_to_core(docs: list[dict]) -> list[CoreDocument]:
    res = []
    for doc in docs:
        res.append(CoreDocument(text=doc['text'], metadata={
            "codex_name": doc['codex_name'],
            "part": doc['part'],
            "section": doc['section'],
            "section_title": doc['section_title'],
            "subsection_title": doc['subsection_title'],
            "chapter": doc['chapter'],
            "chapter_title": doc['chapter_title'],
            "article": doc['article'],
            "article_title": doc['article_title'],
        }))
    return res


core_docs = convert_to_core(documents)


def to_langchain(document: CoreDocument) -> Document:
    return Document(
        page_content=document.text,
        metadata=document.metadata
    )

def from_langchain(document: Document) -> CoreDocument:
    return CoreDocument(
        text=document.page_content,
        metadata=document.metadata
    )

def split_point(text: CoreDocument):
    document = to_langchain(text)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents([document])
    chunks = [from_langchain(chunk) for chunk in chunks]
    return chunks


for doc in tqdm(core_docs, desc="Загружаем документы в базу данных"):
    split_document = split_by_numbered_points(doc)

    result = []
    for point in split_document:
        if len(point.text) > 500:
            chunked_point = split_point(point)
            for point_ in chunked_point:
                result += chunked_point
        else:
            result.append(point)

    embedded_chunks = [
       embedder.embed_document(document) for document in result
    ]
    for batch_index in range(0, len(embedded_chunks), 50):
        qdrant.bulk_add(
            embedded_chunks[batch_index:batch_index + 50],
            collection_name="Гражданский кодекс"
        )
