from tempfile import NamedTemporaryFile
import os

from rag_pipeline.pipelines.base import BasePipeline
from rag_pipeline.scrapers.generic import GenericScraper, BaseScraper


class SimplePipeline(BasePipeline):
    """Really simple pipeline that scrapes a website"""

    def __init__(self, vector_store, urls: list[str] = [], scraper: BaseScraper = None):
        super().__init__(vector_store)
        self.scraper = scraper or GenericScraper()
        self.urls = urls
        self.temps_to_urls = {}  # map uuids to original urls

    def acquire_pdfs(self, *args, **kwargs) -> list[str]:
        pdf_paths = []

        # this could be easily reworked to make use of a thread pool or an async loop
        for url in self.urls:
            with NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                self.logger.info(f"Scraping url: {url}")
                path = self.scraper.scrape(url, tmp.name)
                pdf_paths.append(path)
                self.temps_to_urls[tmp.name] = url

        return pdf_paths

    def on_pdf_ingested(self, pdf_path, file_id):
        # delete the temporary pdfs after everything was indexed
        os.unlink(pdf_path)

    def process_llamaindex_documents(self, documents, pdf_path, file_id):
        for d in documents:
            d.metadata["original_url"] = self.temps_to_urls.get(pdf_path, "")

        return documents
