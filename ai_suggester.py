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
You are a senior Python software engineer performing a professional code review.

IMPORTANT RULES:
- If the code is already clean, small, and idiomatic, explicitly say:
  "This code is already well-written and does not require changes."
- Do NOT give generic advice unless it clearly improves the code.
- Be honest and realistic, like a real senior reviewer.

TASK:
1. If SYNTAX ERRORS exist:
   - Explain each error clearly
   - Show corrected code

2. If the code is VALID:
   - First state whether the code is already optimal or not
   - Only then suggest 1–3 **meaningful** improvements (if any)

CODE:
{code_string}

OUTPUT FORMAT:
- Short bullet points
- Include code snippets only if they add value
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
