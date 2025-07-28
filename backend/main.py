from fastapi import FastAPI

from .crud import router as crud_router
from .ai import router as ai_router

app = FastAPI()

app.include_router(crud_router, prefix="/db", tags=["database"])
app.include_router(ai_router, prefix="/ai", tags=["ai"])

