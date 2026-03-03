from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configurações da aplicação"""
    app_name: str = "My FastAPI App"
    app_version: str = "1.0.0"
    debug: bool = True
    
    class Config:
        env_file = ".env"


settings = Settings()
