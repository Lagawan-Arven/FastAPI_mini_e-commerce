from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.database.models import Base
from app.core.config import ENV

import os

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

db_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(db_url)

local_session = sessionmaker(autoflush=False,bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)