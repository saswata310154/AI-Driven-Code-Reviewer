from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

# Load environment variables (.env)
load_dotenv()

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
You are a senior Python software engineer.

TASK:
- If the code contains SYNTAX ERRORS, clearly explain each error
  and show how to fix it.
- If the code is VALID, provide 2–3 high-impact improvements.

CODE:
{code_string}

RESPONSE RULES:
- Be precise and professional
- Avoid generic advice
- Include short corrected code snippets where relevant
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
