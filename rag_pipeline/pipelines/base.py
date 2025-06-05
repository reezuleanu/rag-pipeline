from abc import ABC, abstractmethod
from uuid import UUID, uuid4
import logging

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader


class BasePipeline(ABC):
    """Pipeline blueprint"""

    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.logger = logging.getLogger(__name__)

    @abstractmethod
    def acquire_pdfs(self, *args, **kwargs) -> list[str]:
        """Acquire pdfs to ingest into a vector store

        Returns:
            list[str]: paths of the acquired pdfs
        """
        raise NotImplementedError

    @abstractmethod
    def ingest_pdf(self, pdf_path: str) -> UUID:
        """Ingest the pdf into a vector store and returns its id

        Args:
            pdf_path (str): path to the pdf to ingest

        Returns:
            UUID: id of the ingested pdf
        """
        raise NotImplementedError

    def run(self, return_ids: bool = False) -> UUID | None:
        """Run the pipeline

        Args:
            return_ids (bool, optional): should this method return the ids of the ingested files. Defaults to False.

        Returns:
            (UUID | None): ids of the newly ingested files
        """
        ingested_ids = []

        pdfs = self.acquire_pdfs()

        for pdf in pdfs:
            vector_store_id = self.ingest_pdf(pdf)
            ingested_ids.append(vector_store_id)

        self.logger.info(f"Successfully ingested {len(ingested_ids)} documents!")

        if return_ids:
            return ingested_ids
