import io

import PyPDF2

from src.domain.services.ipdf_adapter import IPdfAdapter


class PyPdf2Adapter(IPdfAdapter):
    def parse_bytes(self, pdf_bytes: bytes) -> str:
        try:
            pdf_stream = io.BytesIO(pdf_bytes)
            reader = PyPDF2.PdfReader(pdf_stream)

            text_parts = []
            for page_num, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text.strip():
                    text_parts.append(f"=== Страница {page_num + 1} ===\n{page_text}")
            return "\n\n".join(text_parts)

        except Exception as e:
            raise ValueError(f"Ошибка парсинга PDF: {str(e)}")
