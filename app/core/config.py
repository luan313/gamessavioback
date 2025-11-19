from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    ALGORITHM: str = "HS256"
    DATABASE_URL: str
    ANY_DEAL_API_KEY:str
    RAWG_API_KEY:str
    RAWG_BASE_URL:str
    BACKOFFICE_TOKEN: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",  
    )

settings = Settings()
