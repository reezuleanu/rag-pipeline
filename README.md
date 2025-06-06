# RAG Pipeline POC
An example implementation of a RAG pipeline using LlamaIndex. This also uses Streamlit for a demo.

## Actual implementation
### Data acquisition
The data is scraped from 3 websites containing tax info for expats for Spain, Great Britain and Germany (more websites can easily be added). This data is then cleaned and saved as a pdf for RAG ingestion

### Indexing
The acquired pdfs are then indexed in a vector store (in this implementation, I am using `Opensearch`) using LlamaIndex. The embedding model used is OpenAI's `ada-002`. It is multilingual, so the data can be queried in any language.

### RAG
A user can get up-to-date answers from the scraped websites using an OpenAI LLM with LlamaIndex. I used a ReAct agent approach, enabling the LLM to query the vector store multiple times if it deems it necessary to answer the user's question, then generates an answer with the acquired context.

### Demo
There is a demo available, built using Streamlit. There is also a deployed version [here](http://172.104.142.244/).

### Checking the data
You can see the indexed data, extracted metadatas, and embeddings by accessing `Opensearch Dashboards`, at port `5601` ([Deployed Version](http://172.104.142.244/)).

## Disclaimer
This is a simple pipeline. It does not address versioning, or smart crawling for the scrapers, but even so it delivers in creating a multilingual system able to provide tax advice to expats.

The deployed version required credentials to access. If you don't have them, ask the creator.
