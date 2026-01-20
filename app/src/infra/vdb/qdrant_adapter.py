import uuid
from typing import List
from qdrant_client import QdrantClient, models

from src.domain.models.document import VectorisedDocument, ExtendedVectorisedDocument
from src.domain.services.ivdb_adapter import IVectorDB


class QdrantAdapter(IVectorDB):
    __slots__ = ("_client", )

    def __init__(self):
        self._client = QdrantClient(host='localhost', port=6333)

    @staticmethod
    def get_payload(document: VectorisedDocument) -> dict:
        payload = document.metadata
        payload['text'] = document.text
        return payload

    def add(
            self,
            document: VectorisedDocument,
            collection_name: str = 'baseline'
    ) ->str:
        res = self._client.upsert(
            collection_name=collection_name,
            points=[
                models.PointStruct(
                    id=str(uuid.uuid4()),
                    payload=self.get_payload(document),
                    vector=document.embedding
                ),
            ],
        )

        return res

    def bulk_add(
            self,
            documents: list[VectorisedDocument],
            collection_name: str = 'baseline'
    ) -> str:
        res = self._client.upsert(
            collection_name=collection_name,
            points=[
                models.PointStruct(
                    id=str(uuid.uuid4()),
                    payload=self.get_payload(document),
                    vector=document.embedding
                )
                for document in documents
            ],
        )

        return res

    def search(
            self,
            embedding: list[float],
            collection_name: str = 'baseline'
    ) -> List[ExtendedVectorisedDocument]:
        response = self._client.query_points(
            collection_name=collection_name,
            query=embedding,
            limit=10,
            with_vectors=True,
            with_payload=True
        )
        return [
            ExtendedVectorisedDocument(
                text=res.payload['text'],
                metadata=res.payload,
                embedding=res.vector,
                id=res.id,
                distance=res.score,
            )
            for res in response.points
        ]

    def create_collection(self, collection_name: str = 'baseline', size: int = 1024) -> str:
        self._client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=size, distance="Cosine"),
        )
        return 'success'

    def delete_collection(self, collection_name: str = 'baseline') -> str:
        self._client.delete_collection(collection_name=collection_name)
        return 'success'