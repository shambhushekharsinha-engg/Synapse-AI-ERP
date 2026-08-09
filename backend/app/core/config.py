from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Synapse AI ERP"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/synapse_erp"

    class Config:
        env_file = ".env"

settings = Settings()
