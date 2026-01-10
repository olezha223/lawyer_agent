import re
from typing import List, Tuple

from src.domain.models.document import CoreDocument


def split_by_numbered_points(doc: CoreDocument) -> List[CoreDocument]:
    text = doc.text
    metadata = doc.metadata

    result = []
    pattern = r'(\d+)\.'
    parts = re.split(pattern, text)
    if len(parts) == 1:
        doc.text = text.strip()
        doc.metadata["point"] = "1"
        return [doc,]

    if parts[0].strip():
        new_metadata = metadata.copy()
        new_metadata["point"] = "0"
        new_doc = CoreDocument(text=parts[0].strip(), metadata=new_metadata)
        result.append(new_doc)

    for i in range(1, len(parts), 2):
        if i + 1 < len(parts):
            number = parts[i]
            chunk_text = parts[i + 1].strip()
            if chunk_text:
                new_metadata = metadata.copy()
                new_metadata["point"] = str(number)
                new_doc = CoreDocument(text=chunk_text, metadata=new_metadata)
                result.append(new_doc)

    return result
