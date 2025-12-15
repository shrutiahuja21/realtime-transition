import os, subprocess

def run_pipeline(upload_id, job_id, lang, jobs):
    jobs[job_id] = "processing"

    input_video = None
    for f in os.listdir("data/uploads"):
        if f.startswith(upload_id):
            input_video = f"data/uploads/{f}"

    output_path = f"data/outputs/{job_id}.mp4"

   
    subprocess.run([
        "ffmpeg", "-y",
        "-i", input_video,
        "-c", "copy",
        output_path
    ])

    jobs[job_id] = "completed"
