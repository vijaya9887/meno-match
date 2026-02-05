import os
from typing import Optional

class Settings:
    database_url: str = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/meno_match")
    api_port: int = int(os.getenv("API_PORT", "3001"))
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    
settings = Settings()
