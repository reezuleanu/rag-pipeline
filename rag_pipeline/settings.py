from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    LLM_TEMPERATURE: float = 0.1

    APP_USERNAME: str = "admin"
    APP_PASSWORD: str = ""

    OPENSEARCH_ENDPOINT: str = "https://localhost:9200"
    OPENSEARCH_USERNAME: str = "admin"
    OPENSEARCH_PASSWORD: str = ""
    OPENSEARCH_INDEX: str = "rag-example-index"


settings = Settings()
