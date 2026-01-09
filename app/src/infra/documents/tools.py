from src.domain.models.document import CoreDocument, VectorisedDocument, ExtendedVectorisedDocument


def to_core_document(documents: list[VectorisedDocument | ExtendedVectorisedDocument]) -> list[CoreDocument]:
    return [CoreDocument(text=doc.text, metadata=doc.metadata) for doc in documents]