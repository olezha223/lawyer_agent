from sentence_transformers import SentenceTransformer

from src.domain.models.document import CoreDocument, VectorisedDocument
from src.domain.services.iembedder import IEmbedder


class BGEEmbedder(IEmbedder):
    def __init__(self):
        self.model_name = "BAAI/bge-m3"
        self._model = None

    def _get_model(self):
        if self._model is None:
            try:
                self._model = SentenceTransformer(self.model_name)
            except Exception as e:
                raise ValueError(f"Failed to load model {self.model_name}: {str(e)}")
        return self._model

    def embed(self, text: str) -> list[float]:
        if not text.strip():
            raise ValueError("Empty text provided")
        try:
            model = self._get_model()
            embedding = model.encode([text], normalize_embeddings=True, batch_size=1)
            vector = embedding[0].tolist()
            return vector
        except Exception as e:
            raise RuntimeError(f"Embedding failed: {str(e)}")

    def embed_document(self, document: CoreDocument) -> VectorisedDocument:
        vector = self.embed(document.text)
        try:
            return VectorisedDocument(
                text=document.text,
                metadata=document.metadata,
                embedding=vector
            )
        except Exception as e:
            raise RuntimeError(f"Failed to create VectorisedDocument: {str(e)}")