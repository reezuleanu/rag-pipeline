from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    USERNAME: str = "admin"
    PASSWORD: str = ""

    OPENSEARCH_ENDPOINT: str = "https://localhost:9200"
    OPENSEARCH_USERNAME: str = "admin"
    OPENSEARCH_PASSWORD: str = ""
    OPENSEARCH_INDEX: str = "rag_example_index"


settings = Settings()
