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

RULES:
- If the code is very small or already optimal, say so explicitly.
- Do NOT repeat generic advice like "add docstrings" unless it truly adds value.
- Be honest and concise.

TASK:
- If syntax errors exist, explain and fix them.
- If the code is valid:
    - Say whether the code is already optimal
    - Suggest improvements ONLY if they are meaningful

CODE:
{code_string}

FORMAT:
- Use short bullet points
- Include code snippets only if needed
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
