from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()


llm_endpoint = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-7B-Instruct",
    temperature=0.3,
    max_new_tokens=800
)

chat_model = ChatHuggingFace(llm=llm_endpoint)


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
        result = chat_model.invoke(
            [HumanMessage(content=review_prompt)]
        )

        message = result.content if hasattr(result, "content") else ""

        return [{
            "type": "AI_REVIEW",
            "message": message.strip(),
            "severity": "INFO"
        }]

    except Exception as err:
        return [{
            "type": "SYSTEM_ERROR",
            "message": str(err),
            "severity": "ERROR"
        }]
