from fastapi import FastAPI

from .crud import router as crud_router
from .ai import router as ai_router
from .users import router as users_router
from .documents import router as docs_router
from .db import Base, engine

# Ensure database exists
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users_router, prefix="/auth", tags=["auth"])
app.include_router(docs_router, prefix="/documents", tags=["documents"])
app.include_router(crud_router, prefix="/db", tags=["database"])
app.include_router(ai_router, prefix="/ai", tags=["ai"])
