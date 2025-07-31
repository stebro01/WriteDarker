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

# ---------------------------------------------------------------------------
# Lightweight auto-migration helpers (only for SQLite dev database)
# ---------------------------------------------------------------------------

def _ensure_columns_exist():
    """For simple development setups make sure new columns exist.

    This avoids having to reset the database every time a model changes.
    It is *not* a replacement for proper Alembic migrations, but good
    enough during rapid prototyping.
    """

    from sqlalchemy import text

    required = {
        "references": {
            "pdf": "BLOB",  
            "filename": "TEXT",
            "filetype": "TEXT",
            "file_hash": "TEXT",
        }
    }

    with engine.connect() as conn:
        for table, cols in required.items():
            existing = {
                row[1] for row in conn.execute(text(f"PRAGMA table_info('{table}')"))
            }
            for col, sqltype in cols.items():
                if col not in existing:
                    conn.execute(text(f"ALTER TABLE \"{table}\" ADD COLUMN \"{col}\" {sqltype}"))
                    print(f"[DB] Added missing column '{col}' to '{table}' table")

# Run auto-migrations as soon as the module is imported (after engine exists)
try:
    _ensure_columns_exist()
except Exception as exc:
    # Don't crash the app if something goes wrong – just log and continue
    import traceback, sys
    traceback.print_exception(exc, file=sys.stderr)

