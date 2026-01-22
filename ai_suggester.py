from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

# Initialize HuggingFace LLM
hf_endpoint = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-7B-Instruct",
    temperature=0.3,
    max_new_tokens=1000
)

chat_model = ChatHuggingFace(llm=hf_endpoint)


def get_ai_suggestions(code_string: str):
    """
    Generates AI-based review suggestions for Python code.
    Focuses on robustness, readability, and optimization.
    """

    review_prompt = f"""
    You are an experienced Python code reviewer.

    TASK:
    Analyze the Python code below and suggest improvements.

    CODE SNIPPET:
    {code_string}

    GUIDELINES:
    - Give 2 to 3 concise suggestions only
    - Categorize suggestions into:
        • Robustness
        • Readability
        • Optimization
    - Keep explanations short and practical
    - Include minimal code examples where helpful
    """

    try:
        response = chat_model.invoke(
            [HumanMessage(content=review_prompt)]
        )

        return [{
            "type": "AISuggestion",
            "message": response.content,
            "severity": "Info"
        }]

    except Exception as err:
        return [{
            "type": "Error",
            "message": str(err),
            "severity": "Info"
        }]
