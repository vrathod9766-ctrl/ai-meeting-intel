import subprocess
import json

def categorize_meeting(transcript: str, model_name: str = "gemma:2b"):
    """
    Categorize meeting and extract tags using Ollama LLM.
    Returns HTML string for browser display.
    """
    prompt = f"""
    Analyze the following meeting transcript and categorize it. 
    Provide output in JSON format with keys:
    - category: main category of the meeting (e.g., "Team Meeting", "Client Call")
    - tags: list of 2–5 relevant tags
    
    Transcript:
    {transcript}
    """

    cmd = ["ollama", "run", model_name]
    result = subprocess.run(cmd, input=prompt, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Ollama failed: {result.stderr}")

    try:
        output = json.loads(result.stdout.strip())
        category = output.get("category", "Uncategorized")
        tags = output.get("tags", [])

        # ✅ Format as HTML for browser display
        formatted = f"""
        <h3>Category:</h3>
        <p>{category}</p>

        <h3>Tags:</h3>
        <ul>
        {''.join(f"<li>{tag}</li>" for tag in tags)}
        </ul>
        """
        return formatted

    except Exception:
        return "<h3>Category:</h3><p>Uncategorized</p><h3>Tags:</h3><ul><li>None</li></ul>"
