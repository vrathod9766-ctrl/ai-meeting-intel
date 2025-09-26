import subprocess
import os
import shutil

# === Hardcoded paths ===
WHISPER_EXE = r"C:\Users\Admin\whisper.cpp\build\bin\Release\whisper-cli.exe"
MODEL_PATH = r"C:\Users\Admin\whisper.cpp\models\ggml-medium.en.bin"
FFMPEG_EXE = r"C:\Project\ffmpeg-2025-09-25-git-9970dc32bf-essentials_build\ffmpeg-2025-09-25-git-9970dc32bf-essentials_build\bin\ffmpeg.exe"

# Directories
UPLOAD_DIR = "Data/uploads"
TRANSCRIPT_DIR = "Data/transcripts"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)


def extract_audio(video_path: str) -> str:
    """
    Extract audio from MP4 using ffmpeg -> WAV (16kHz, mono).
    Returns the generated WAV file path.
    """
    wav_path = os.path.splitext(video_path)[0] + ".wav"
    cmd = [
        FFMPEG_EXE,
        "-y",
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        wav_path,
    ]
    subprocess.run(cmd, capture_output=True, text=True, check=True)
    return wav_path


def transcribe(file_path: str) -> str:
    """
    Transcribes an audio/video file using whisper.cpp.
    Supports .mp3, .wav, and .mp4.
    """
    ext = os.path.splitext(file_path)[1].lower()

    # If MP4, extract audio first
    is_temp_wav = False
    if ext == ".mp4":
        file_path = extract_audio(file_path)
        is_temp_wav = True

    # Run Whisper.cpp
    result = subprocess.run(
        [WHISPER_EXE, "-m", MODEL_PATH, "-f", file_path, "-otxt"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Whisper failed: {result.stderr}")

    # Whisper generates transcript file
    transcript_file = file_path + ".txt"
    if not os.path.exists(transcript_file):
        raise FileNotFoundError(f"Transcript file not found: {transcript_file}")

    # Save transcript into TRANSCRIPT_DIR
    final_path = os.path.join(
        TRANSCRIPT_DIR, os.path.basename(file_path) + ".txt"
    )
    shutil.move(transcript_file, final_path)

    # Read and return text
    with open(final_path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    # Clean up temp wav if created from mp4
    if is_temp_wav and os.path.exists(file_path):
        os.remove(file_path)

    return text
