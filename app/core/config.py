from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "FastAPI App"
    environment: str = "development"
    debug: bool = True
    DATABASE_URL: str = "postgresql://rag_user:ilikturtles%4012@localhost:5432  /rag_app"
    class Config:
        env_file = ".env"

settings = Settings()
