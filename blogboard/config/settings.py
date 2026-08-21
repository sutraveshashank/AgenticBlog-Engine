import os
from pathlib import Path
from typing import Dict
from dotenv import load_dotenv
from pydantic import BaseModel, Field, AliasChoices
from pydantic_settings import BaseSettings, SettingsConfigDict

# Ensure .env is loaded before Pydantic Settings instantiates
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
env_file = ROOT_DIR / ".env"
if env_file.exists():
    load_dotenv(dotenv_path=env_file)
else:
    load_dotenv()

class LLMSettings(BaseModel):
    API_KEY: str = Field(default="", validation_alias=AliasChoices('API_KEY', 'api_key', 'GROQ_API_KEY', 'groq_api_key', 'LLM__API_KEY', 'llm__api_key'))
    MODEL_NAME: str = "openai/gpt-oss-120b"
    TEMPERATURE: float = 0.7

class TagSettings(BaseModel):
    ml: Dict[str, str] = {"label": "Machine Learning", "shortLabel": "ML"}
    dl: Dict[str, str] = {"label": "Deep Learning", "shortLabel": "DL"}
    statistics: Dict[str, str] = {"label": "Statistics for AI", "shortLabel": "Stats"}
    nlp: Dict[str, str] = {"label": "Natural Language Processing", "shortLabel": "NLP"}
    cv: Dict[str, str] = {"label": "Computer Vision", "shortLabel": "CV"}
    genai: Dict[str, str] = {"label": "Generative AI", "shortLabel": "Gen AI"}
    ainews: Dict[str, str] = {"label": "AI News", "shortLabel": "AI News"}

class R2Settings(BaseModel):
    ACCOUNT_ID: str = "dummy"
    ACCESS_KEY_ID: str = "dummy"
    SECRET_ACCESS_KEY: str = "dummy"
    BUCKET_NAME: str = "dummy"

class ContentAPISettings(BaseModel):
    TAVILY_API_KEY: str = ""
    GUARDIAN_API_KEY: str = ""
    UNSPLASH_API_KEY: str = ""

class Settings(BaseSettings):
    llm: LLMSettings = Field(default_factory=LLMSettings)
    tags: TagSettings = Field(default_factory=TagSettings)
    r2: R2Settings = Field(default_factory=R2Settings)
    content: ContentAPISettings = Field(default_factory=ContentAPISettings)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore"
    )

app_settings = Settings()