import os
import requests


HF_API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-7B-Instruct"
HF_TOKEN = os.getenv("HUGGINGFACE_ACCESS_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

def analyze_code_with_ai(source_code: str):

    prompt = f"""
You are a senior Python engineer performing a professional code review.

Analyze the following Python code and suggest improvements related to:
- Code safety and edge cases
- Code clarity and Python best practices
- Performance or logic simplification

CODE SNIPPET:
{source_code}

RESPONSE RULES:
- Provide only 2–3 important suggestions
- Use the following sections:
  * Robustness
  * Readability
  * Optimization
- Keep explanations concise
- Include a short code example for each suggestion
"""

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 800,
            "temperature": 0.3
        }
    }

    try:
        response = requests.post(
            HF_API_URL,
            headers=HEADERS,
            json=payload,
            timeout=60
        )
        response.raise_for_status()

        result = response.json()

        # HF sometimes returns list or dict
        if isinstance(result, list):
            text = result[0].get("generated_text", "")
        else:
            text = result.get("generated_text", "")

        return [{
            "type": "AI_REVIEW",
            "message": text.strip(),
            "severity": "INFO"
        }]

    except Exception as err:
        return [{
            "type": "SYSTEM_ERROR",
            "message": str(err),
            "severity": "ERROR"
        }]
