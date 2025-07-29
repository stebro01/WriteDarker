import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Store application data inside the repository to avoid permission issues
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPDATA_PATH = os.path.join(ROOT_DIR, "AppData")
DB_NAME = "writedarker.db"
DB_PATH = os.path.join(APPDATA_PATH, DB_NAME)

os.makedirs(APPDATA_PATH, exist_ok=True)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
