from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int = 5432
    PROJECT_NAME: str

    @field_validator("DB_USER", "DB_PASSWORD", "DB_NAME", "DB_HOST", mode="before")
    @classmethod
    def strip_spaces(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding='utf-8',
        extra='ignore'
    )

    @property
    def DATABASE_URL(self) -> str:
        url = f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
      
        return url.strip()
        

settings = Settings()