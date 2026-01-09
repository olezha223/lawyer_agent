from abc import ABC, abstractmethod


class IPdfAdapter(ABC):
    @abstractmethod
    def parse_bytes(self, pdf_bytes: bytes) -> str: ...
