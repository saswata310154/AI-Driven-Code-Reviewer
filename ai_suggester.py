import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

# Initialize HF client
client = InferenceClient(
    model="Qwen/Qwen2.5-7B-Instruct",
    token=os.getenv("HUGGINGFACE_ACCESS_TOKEN")
)

def analyze_code_with_ai(source_code: str):

    review_prompt = f"""
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

    try:
        response = client.text_generation(
            prompt=review_prompt,
            max_new_tokens=800,
            temperature=0.3
        )

        return [{
            "type": "AI_REVIEW",
            "message": response.strip(),
            "severity": "INFO"
        }]

    except Exception as err:
        return [{
            "type": "SYSTEM_ERROR",
            "message": str(err),
            "severity": "ERROR"
        }]
