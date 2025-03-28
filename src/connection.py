from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from model.tarefa_model import create_tables

load_dotenv()

class Config:
    DB_USER = os.getenv('DB_USER') 
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')
    DB_PORT = os.getenv('DB_PORT', 3306)

    DATABASE_URL = f'mysql+pymysql://{DB_USER}:@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(Config.DATABASE_URL)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

try:
    with engine.connect() as connection:
        print('Conexão bem sucedida')
        create_tables(engine)
except Exception as e:
    print(f'Erro ao conectar: {e}')