from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/{file_name}")
def media(file_name: str):
    return FileResponse(f"data/outputs/{file_name}", media_type="video/mp4")