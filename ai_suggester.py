from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

# Load environment variables (.env)
import os

load_dotenv()

HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")


if not os.getenv("HUGGINGFACEHUB_API_TOKEN"):
    raise RuntimeError("HuggingFace API token not found")


# Initialize HuggingFace LLM endpoint
llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-7B-Instruct",
    temperature=0.3,
    max_new_tokens=700
)

# Wrap with ChatHuggingFace
model = ChatHuggingFace(llm=llm)


def get_ai_suggestions(code_string: str) -> str:

    """
    Generates AI-powered code review suggestions.

    RETURNS:
    - Plain text (string) suitable for direct display in Streamlit
    """

    prompt = f"""
You are a senior Python software engineer doing a realistic code review.

VERY IMPORTANT RULES:
- If the code is already clean, simple, and idiomatic, explicitly say:
  "This code is already well-written and does not require changes."
- Do NOT give generic advice like docstrings or variable naming
  unless it truly improves the code.
- Be honest, concise, and practical.

REVIEW TASK:
1. If there are SYNTAX ERRORS:
   - Explain each error clearly
   - Show corrected code

2. If the code is VALID:
   - First state whether the code is already optimal
   - Only then suggest few meaningful improvements (if any)

CODE:
{code_string}

OUTPUT FORMAT:
- Short bullet points
- Code snippets only if they add real value
"""




    try:
        response = model.invoke(
            [HumanMessage(content=prompt)]
        )

        # Always return plain text
        return response.content.strip()

    except Exception as e:
        # Fail safely with readable message
        return (
            "⚠️ AI could not generate suggestions at this time.\n\n"
            f"Reason: {str(e)}"
        )
