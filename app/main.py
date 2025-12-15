from fastapi import FastAPI
from app.api import upload, process, media

app = FastAPI(title="Real-Time Translation + LipSync Pipeline")

app.include_router(upload.router, prefix="/upload")
app.include_router(process.router, prefix="/process")
app.include_router(media.router, prefix="/media")