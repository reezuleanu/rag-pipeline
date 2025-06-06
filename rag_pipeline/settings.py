from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    LLM_TEMPERATURE: float = 0.1
    LLM_SYSTEM_PROMPT: str = (
        """You are a tax expert specializing in providing clear, accurate,
        and up-to-date information for expatriates living in Germany, Spain,
        and the United Kingdom. You understand the tax laws, residency rules,
        double taxation treaties, and filing requirements in these countries.
        Answer all questions in a professional, friendly, and easy-to-understand manner,
        focusing on the needs of expats navigating foreign tax systems."""
    )

    APP_USERNAME: str = "admin"
    APP_PASSWORD: str = ""

    OPENSEARCH_ENDPOINT: str = "https://localhost:9200"
    OPENSEARCH_USERNAME: str = "admin"
    OPENSEARCH_PASSWORD: str = ""
    OPENSEARCH_INDEX: str = "rag-example-index"


settings = Settings()
