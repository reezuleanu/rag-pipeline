mkdir -p ./opensearch

export APP_USERNAME="admin"
export APP_PASSWORD=""

export OPENAI_API_KEY=""
export OPENAI_MODEL="gpt-4o-mini"
export LLM_TEMPERATURE="0.1"

export OPENSEARCH_ENDPOINT="https://opensearch-rag-pipeline:9200"
export OPENSEARCH_USERNAME="admin"
export OPENSEARCH_PASSWORD=""
export OPENSEARCH_INDEX="rag-example-index"

docker-compose up -d