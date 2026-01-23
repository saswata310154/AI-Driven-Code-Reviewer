# ai_suggester.py
import streamlit as st


def get_ai_suggestions(code_string: str) -> str:
    """
    Generates AI-powered code review suggestions.

    RETURNS:
    - Plain text (string) suitable for direct display in Streamlit
    """

    # --- 1. Read token safely (Cloud + Local) ---
    HF_TOKEN = st.secrets.get("HUGGINGFACEHUB_API_TOKEN", None)

    if not HF_TOKEN:
        return (
            "⚠️ AI suggestions are unavailable.\n\n"
            "Reason: Hugging Face API token is not configured on the server.\n\n"
            "Static analysis and style checks are still available."
        )

    try:
        # --- 2. Lazy imports (VERY important) ---
        from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
        from langchain_core.messages import HumanMessage

        # --- 3. Initialize model ONLY when needed ---
        llm = HuggingFaceEndpoint(
            repo_id="Qwen/Qwen2.5-7B-Instruct",
            huggingfacehub_api_token=HF_TOKEN,
            temperature=0.3,
            max_new_tokens=700
        )

        model = ChatHuggingFace(llm=llm)

        # --- 4. Prompt (UNCHANGED) ---
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

        response = model.invoke([HumanMessage(content=prompt)])

        return response.content.strip()

    except Exception as e:
        return (
            "⚠️ AI could not generate suggestions at this time.\n\n"
            f"Reason: {str(e)}"
        )
