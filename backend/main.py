from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from the repository root
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from .api.crud import router as crud_router
from .api.ai import router as ai_router
from .api.users import router as users_router
from .api.documents import router as docs_router
from .api.projects import router as projects_router
from .api.references import router as references_router
from .api.settings import router as settings_router
from .api.pubmed import router as pubmed_router
from .db import Base, engine, SessionLocal
from .models import User
from .services.auth import get_password_hash

# Configure CORS - Allow all origins for development
origins = ["*"]  # Allow all origins


# Ensure database exists
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.on_event("startup")
def ensure_admin_user():
    """Create default admin user if not present."""
    username = os.getenv("ADMIN_USERNAME")
    password = os.getenv("ADMIN_PASSWORD")
    if not username or not password:
        return
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.username == username).first():
            admin = User(
                username=username,
                password_hash=get_password_hash(password),
            )
            db.add(admin)
            db.commit()
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router, prefix="/auth", tags=["auth"])
app.include_router(docs_router, prefix="/documents", tags=["documents"])
app.include_router(projects_router, prefix="/projects", tags=["projects"])
app.include_router(references_router, prefix="/references", tags=["references"])
app.include_router(settings_router, prefix="/settings", tags=["settings"])
app.include_router(crud_router, prefix="/db", tags=["database"])
app.include_router(ai_router, prefix="/ai", tags=["ai"])
app.include_router(pubmed_router, prefix="/pubmed", tags=["pubmed"])

