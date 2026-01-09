from abc import ABC, abstractmethod

from src.domain.models.document import CoreDocument, VectorisedDocument


class IEmbedder(ABC):
    @abstractmethod
    def embed(self, text: str) -> list[float]: ...

    @abstractmethod
    def embed_document(self, document: CoreDocument) -> VectorisedDocument: ...