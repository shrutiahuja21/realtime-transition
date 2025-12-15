from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import upload, process, media

app = FastAPI(title="Real-Time Translation + LipSync Pipeline")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/upload")
app.include_router(process.router, prefix="/process")
app.include_router(media.router, prefix="/media")
