import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables from the repository root
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

# Store application data inside the repository to avoid permission issues
ROOT_DIR = Path(__file__).resolve().parents[1]
APPDATA_PATH = ROOT_DIR / "AppData"
DB_NAME = "writedarker.db"

# Determine the full database path
db_dir = os.getenv("DB_DIR")
if db_dir:
    DB_PATH = Path(os.path.expanduser(db_dir)) / DB_NAME
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
else:
    DB_PATH = APPDATA_PATH / DB_NAME
    APPDATA_PATH.mkdir(parents=True, exist_ok=True)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
