# Real-Time Voice Translation + Lip-Synced Video

## Stack
FastAPI, Docker, Kubernetes, Whisper, MarianMT, Coqui TTS, Wav2Lip

## Flow
Upload → ASR → Translate → TTS → Lip Sync → Output Video

## Run
docker-compose up --build

## Endpoints
POST /upload  
POST /process  
GET /process/{job_id}/status  
GET /media/{job_id}.mp4

# TO RUN
http://localhost:8000/docs
