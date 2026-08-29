import os

from dotenv import load_dotenv

load_dotenv() # Lê os arquivos do .env

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")

    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    PORT = int(os.getenv("PORT", 5000))