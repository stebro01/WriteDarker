from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def ai_root():
    return {"message": "AI placeholder"}
