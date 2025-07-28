import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

APPDATA_PATH = "/AppData"
DB_NAME = "writedarker.db"
DB_PATH = os.path.join(APPDATA_PATH, DB_NAME)

os.makedirs(APPDATA_PATH, exist_ok=True)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
