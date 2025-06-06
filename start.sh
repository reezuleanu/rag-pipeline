mkdir -p ./opensearch

export APP_USERNAME="admin"
export APP_PASSWORD=""

export OPENAI_API_KEY=""
export OPENAI_MODEL="gpt-4o-mini"
export LLM_TEMPERATURE="0.1"
export LLM_SYSTEM_PROMPT="You are a tax expert specializing in providing clear, accurate, \
        and up-to-date information for expatriates living in Germany, Spain, \
        and the United Kingdom. You understand the tax laws, residency rules, \
        double taxation treaties, and filing requirements in these countries. \
        Answer all questions in a professional, friendly, and easy-to-understand manner, \
        focusing on the needs of expats navigating foreign tax systems."

export OPENSEARCH_ENDPOINT="https://opensearch-rag-pipeline:9200"
export OPENSEARCH_USERNAME="admin"
export OPENSEARCH_PASSWORD=""
export OPENSEARCH_INDEX="rag-example-index"

docker-compose up -d