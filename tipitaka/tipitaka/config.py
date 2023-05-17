from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(dotenv_path=Path(__file__).parent.parent / '.env')

DB_HOST = os.getenv('DB_HOST', '127.0.0.1') 
DB_USER = os.getenv('DB_USER', 'metanoia')
DB_PWD = os.getenv('DB_PWD', '')
DB_NAME = os.getenv('DB_NAME', 'ai')

POSTGRES_URI = f'dbname={DB_NAME} user={DB_USER} password={DB_PWD} host={DB_HOST}'