from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_db_root():
    return {"message": "CRUD placeholder"}
