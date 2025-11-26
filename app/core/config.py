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
    ANY_DEAL_BASE_URL: str
    
    EMAIL_HOST: str = "smtp.gmail.com"
    EMAIL_PORT: int = 587
    EMAIL_USER: str | None = None
    EMAIL_PASSWORD: str | None = None
    
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",  
    )

settings = Settings()
