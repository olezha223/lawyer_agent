from typing import List
from abc import ABC, abstractmethod

from src.domain.models.document import VectorisedDocument, ExtendedVectorisedDocument


class IVectorDB(ABC):

    @abstractmethod
    async def create_collection(self, collection_name: str = 'alpha', **kwargs) -> str: ...

    @abstractmethod
    async def add(self, document: VectorisedDocument, collection_name: str = 'alpha') -> str: ...

    @abstractmethod
    async def search(self, embedding: list[float], collection_name: str = 'alpha') -> List[ExtendedVectorisedDocument]: ...

    @abstractmethod
    async def bulk_add(self, documents: List[VectorisedDocument], collection_name: str = 'alpha') -> str: ...