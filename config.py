import os

import psycopg2
from dotenv import load_dotenv
from pathlib import Path

# Определяем корневую папку приложения
BASE_DIR = Path(__file__).parent

load_dotenv(BASE_DIR / '.env')

# Настройки базы данных
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

DB_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@localhost/{DB_NAME}'
