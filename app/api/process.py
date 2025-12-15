from fastapi import APIRouter, BackgroundTasks
from app.services.pipeline import run_pipeline
import uuid

router = APIRouter()
jobs = {}

@router.post("/")
def start(upload_id: str, background_tasks: BackgroundTasks, target_language: str = "fr"):
    job_id = str(uuid.uuid4())
    jobs[job_id] = "processing"
    background_tasks.add_task(run_pipeline, upload_id, job_id, target_language, jobs)
    return {"job_id": job_id}

@router.get("/{job_id}/status")
def status(job_id: str):
    return {"job_id": job_id, "status": jobs.get(job_id, "unknown")}