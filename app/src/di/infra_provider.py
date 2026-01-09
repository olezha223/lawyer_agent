from dishka import Provider, Scope, provide

from src.domain.services.iembedder import IEmbedder
from src.domain.services.ipdf_adapter import IPdfAdapter
from src.domain.services.ivdb_adapter import IVectorDB
from src.infra.embeddings.bge import BGEEmbedder
from src.infra.pdf.pypdf2_adapter import PyPdf2Adapter
from src.infra.vdb.qdrant_adapter import QdrantAdapter


class InfraProvider(Provider):
    scope = Scope.REQUEST

    pdf_adapter = provide(PyPdf2Adapter, provides=IPdfAdapter)
    vdb_adapter = provide(QdrantAdapter, provides=IVectorDB)
    embedder_provider = provide(BGEEmbedder, provides=IEmbedder)