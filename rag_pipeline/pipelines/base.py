from abc import ABC, abstractmethod
from uuid import UUID, uuid4
import logging

from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Document,
    StorageContext,
)
from llama_index.core.vector_stores.types import BasePydanticVectorStore


class BasePipeline(ABC):
    """Pipeline blueprint"""

    def __init__(self, vector_store):
        self.vector_store: BasePydanticVectorStore = vector_store
        self.logger = logging.getLogger(__name__)

    @abstractmethod
    def acquire_pdfs(self, *args, **kwargs) -> list[str]:
        """Acquire pdfs to ingest into a vector store

        Returns:
            list[str]: paths of the acquired pdfs
        """
        raise NotImplementedError

    def ingest_pdf(self, pdf_path: str, file_id: UUID = None) -> UUID:
        """Ingest the pdf into the vector store and returns its id

        Args:
            pdf_path (str): path to the pdf to ingest

        Returns:
            UUID: id of the ingested pdf
        """

        file_id = file_id or uuid4()

        documents = SimpleDirectoryReader(input_files=[pdf_path]).load_data()

        for d in documents:
            d.metadata["file_id"] = file_id

        documents = self.process_llamaindex_documents(documents, pdf_path, file_id)

        VectorStoreIndex.from_documents(
            documents,
            storage_context=StorageContext.from_defaults(
                vector_store=self.vector_store
            ),
        )

        self.on_pdf_ingested(pdf_path, file_id)

    def on_finish(self) -> None:
        """A method to wrap up the pipeline if needed"""
        pass

    def on_pdf_ingested(self, pdf_path, file_id) -> None:
        """A method for allowing logic after every pdf document ingestion"""
        pass

    def process_llamaindex_documents(
        self,
        documents: list[Document],
        pdf_path: str,
        file_id: UUID,
    ) -> list[Document]:
        """Method to handle custom document parsing logic

        Args:
            documents (list[Document]): llamaindex documents

        Returns:
            list[Document]: llamaindex documents after modifications/custom logic
        """

        return documents

    def run(self, return_ids: bool = False, *args, **kwargs) -> UUID | None:
        """Run the pipeline

        Args:
            return_ids (bool, optional): should this method return the ids of the ingested files. Defaults to False.

        Returns:
            (UUID | None): ids of the newly ingested files
        """
        ingested_ids = []

        pdfs = self.acquire_pdfs(*args, **kwargs)

        for pdf in pdfs:
            vector_store_id = self.ingest_pdf(pdf)
            ingested_ids.append(vector_store_id)

        self.logger.info(f"Successfully ingested {len(ingested_ids)} documents!")

        self.on_finish()

        if return_ids:
            return ingested_ids
