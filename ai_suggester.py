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

Review the following code and provide 2–3 high-impact suggestions.

CODE:
{code_string}

FORMAT YOUR RESPONSE EXACTLY LIKE THIS:

Robustness:
- point with short example

Readability:
- point with short example

Optimization:
- point with short example
"""

    try:
        response = model.invoke([
            HumanMessage(content=prompt)
        ])

        return response.content.strip()

    except Exception as e:
        return f"AI Error: {str(e)}"
