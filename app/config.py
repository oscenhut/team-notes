from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "TeamNotes API"
    VERSION: str = "1.0.0"
    
    # Database Configuration (Defaults to local SQLite)
    DATABASE_URL: str = "sqlite:///./team_notes.db"
    
    # Security & JWT Configuration
    SECRET_KEY: str = "SUPER_SECRET_KEY_CHANGE_ME_IN_PROD_3f9b2a1c"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()