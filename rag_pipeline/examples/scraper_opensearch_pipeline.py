"""Example script using the SimplePipeline class to convert urls to llm knowledge"""

from llama_index.vector_stores.opensearch import (
    OpensearchVectorClient,
    OpensearchVectorStore,
)

from rag_pipeline.pipelines.simple import SimplePipeline
from rag_pipeline.settings import settings

opensearch_client = OpensearchVectorClient(
    endpoint=settings.OPENSEARCH_ENDPOINT,
    index=settings.OPENSEARCH_INDEX,
    dim=1536,
    verify_certs=False,  # ignore self signed certs
    ssl_show_warn=False,
    http_auth=(settings.OPENSEARCH_USERNAME, settings.OPENSEARCH_PASSWORD),
)
vector_store = OpensearchVectorStore(opensearch_client)

urls = [
    "https://www.expat.hsbc.com/expat-explorer/expat-guides/spain/tax-in-spain/",
]

SimplePipeline(vector_store, urls).run()
