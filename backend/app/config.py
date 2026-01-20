import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Vault Configuration
    VAULT_ADDR: str = os.getenv("VAULT_ADDR", "http://localhost:8200")
    VAULT_TOKEN: str = os.getenv("VAULT_TOKEN", "")
    VAULT_SECRET_PATH: str = os.getenv("VAULT_SECRET_PATH", "secret/data/namecom")
    
    # name.com API Configuration
    NAMECOM_API_KEY: str = os.getenv("NAMECOM_API_KEY", "")
    NAMECOM_API_TOKEN: str = os.getenv("NAMECOM_API_TOKEN", "")
    NAMECOM_USERNAME: str = os.getenv("NAMECOM_USERNAME", "")
    
    # FastAPI Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", 8000))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    
    # JWT Configuration
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

settings = Settings()
