from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from .api.crud import router as crud_router
from .api.ai import router as ai_router
from .api.users import router as users_router
from .api.documents import router as docs_router
from .api.projects import router as projects_router
from .api.references import router as references_router
from .api.settings import router as settings_router
from .db import Base, engine

load_dotenv()

# Configure CORS
origins_env = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
origins = [origin.strip() for origin in origins_env.split(",") if origin.strip()]

# Ensure database exists
Base.metadata.create_all(bind=engine)

app = FastAPI()

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

