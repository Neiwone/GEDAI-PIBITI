import os
from dotenv import load_dotenv

load_dotenv() # Carrega as variáveis do .env

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
settings = Settings()