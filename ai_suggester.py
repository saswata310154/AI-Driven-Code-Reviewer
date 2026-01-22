from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-7B-Instruct",
    temperature=0.3,
    max_new_tokens=700
)

model = ChatHuggingFace(llm=llm)


def get_ai_suggestions(code_string: str) -> str:
    """
    Asks AI for improvement suggestions and RETURNS PLAIN TEXT
    """

    prompt = f"""
You are a senior Python software engineer.

TASK:
- If the code has SYNTAX ERRORS, explain them clearly and show how to fix them.
- If the code is VALID, give 2–3 high-impact improvements.

CODE:
{code_string}

FORMAT RULES:
- Be precise
- Do NOT give generic advice
- Show corrected code snippets where applicable
"""


    try:
        response = model.invoke([
            HumanMessage(content=prompt)
        ])

        return response.content.strip()

    except Exception as e:
        return f"AI Error: {str(e)}"
