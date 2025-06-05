from pydantic_settings import PydanticBaseSettingsSource


class Settings(PydanticBaseSettingsSource):
    OPENAI_API_KEY: str = ""
    USERNAME: str = "admin"
    PASSWORD: str = ""

    OPENSEARCH_ENDPOINT: str = "https://localhost:9200"
    OPENSEARCH_USERNAME: str = "admin"
    OPENSEARCH_PASSWORD: str = ""


settings = Settings()
