from fastapi import APIRouter, UploadFile, File
import uuid, os

router = APIRouter()
UPLOAD_DIR = "data/uploads"

@router.post("/")
async def upload(file: UploadFile = File(...)):
    uid = str(uuid.uuid4())
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    path = f"{UPLOAD_DIR}/{uid}_{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())
    return {"upload_id": uid}