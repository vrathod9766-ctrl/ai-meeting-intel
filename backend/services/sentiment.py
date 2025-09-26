import subprocess

def analyze_sentiment(transcript: str, model_name="gemma:2b"):
    prompt = (
        "Analyze the emotional tone of this meeting transcript.\n"
        "Return:\n- Overall sentiment\n- Key emotional moments\n- Positive/negative highlights\n\n"
        f"{transcript}"
    )
    cmd = ["ollama", "run", model_name]
    result = subprocess.run(cmd, input=prompt, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Ollama failed: {result.stderr}")
    return result.stdout.strip()
