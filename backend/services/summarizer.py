import subprocess

def generate_summary(transcript: str, model_name="gemma:2b"):
    prompt = f"Summarize the following meeting transcript:\n\n{transcript}"
    cmd = ["ollama", "run", model_name]
    result = subprocess.run(cmd, input=prompt, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Ollama failed: {result.stderr}")
    return result.stdout.strip()
