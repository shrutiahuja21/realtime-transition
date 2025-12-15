import os
import subprocess
import uuid
import torch
from transformers import MarianMTModel, MarianTokenizer
import whisper
from TTS.api import TTS

UPLOAD_DIR = "data/uploads"
OUTPUT_DIR = "data/outputs"
WAV2LIP_DIR = "app/models/wav2lip"

def find_uploaded_file(upload_id):
    for f in os.listdir(UPLOAD_DIR):
        if f.startswith(upload_id):
            return os.path.join(UPLOAD_DIR, f)
    raise FileNotFoundError("Uploaded file not found")

def extract_audio(video_path, audio_path):
    subprocess.run([
        "ffmpeg", "-y",
        "-i", video_path,
        "-ar", "16000",
        "-ac", "1",
        audio_path
    ], check=True)

def transcribe(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"]

def translate(text, target_lang="fr"):
    model_name = f"Helsinki-NLP/opus-mt-en-{target_lang}"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)

    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    translated = model.generate(**inputs)
    return tokenizer.decode(translated[0], skip_special_tokens=True)

def text_to_speech(text, out_wav):
    tts = TTS(model_name="tts_models/en/vctk/vits")
    tts.tts_to_file(text=text, file_path=out_wav)

def lip_sync(video_path, audio_path, output_path):
    subprocess.run([
        "python",
        f"{WAV2LIP_DIR}/inference.py",
        "--checkpoint_path", f"{WAV2LIP_DIR}/wav2lip_gan.pth",
        "--face", video_path,
        "--audio", audio_path,
        "--outfile", output_path
    ], check=True)

def run_pipeline(upload_id, job_id, target_language, jobs):
    try:
        jobs[job_id] = "extracting_audio"

        input_video = find_uploaded_file(upload_id)
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        extracted_audio = f"{OUTPUT_DIR}/{job_id}_orig.wav"
        extract_audio(input_video, extracted_audio)

        jobs[job_id] = "transcribing"
        transcript = transcribe(extracted_audio)

        jobs[job_id] = "translating"
        translated_text = translate(transcript, target_language)

        jobs[job_id] = "tts"
        tts_audio = f"{OUTPUT_DIR}/{job_id}_tts.wav"
        text_to_speech(translated_text, tts_audio)

        jobs[job_id] = "lip_sync"
        final_video = f"{OUTPUT_DIR}/{job_id}.mp4"
        lip_sync(input_video, tts_audio, final_video)

        jobs[job_id] = "completed"

    except Exception as e:
        jobs[job_id] = f"failed: {str(e)}"
