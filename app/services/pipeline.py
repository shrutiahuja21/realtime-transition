import time, os

def run_pipeline(upload_id, job_id, lang, jobs):
    time.sleep(2)  
    time.sleep(2)  
    time.sleep(2) 
    os.makedirs("data/outputs", exist_ok=True)
    open(f"data/outputs/{job_id}.mp4", "wb").write(b"demo")
    jobs[job_id] = "completed"