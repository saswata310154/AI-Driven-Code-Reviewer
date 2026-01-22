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


def get_ai_suggestions(code_string):
    """
    WHAT IT DOES: Asks AI improvements ideas
    """
    prompt = f"""
    Act as an expert Python Senior Software Engineer. 
    Review the following code for logic, efficiency, and best practices:

    CODE:
    {code_string}

    INSTRUCTIONS:
    Provide exactly 2-3 high-impact suggestions. 
    Structure your response using these specific categories:
    1. **Robustness**: How to prevent crashes or handle edge cases.
    2. **Readability**: How to make the code more "Pythonic" (PEP 8).
    3. **Optimization**: How to improve performance or simplify logic.

    Keep each point brief, professional, and include a small code example of the fix.
    """

    try: 
        response = model.invoke(
            [HumanMessage(content=prompt)]
        )

        ai_message = response.content
        print(ai_message)

        return [{
            "type": "AISuggestion",
            "message": ai_message,
            "severity": "Info"
        }]
    except Exception as e:
        return [{
            "type": "Error",
            "message": e,
            "severity": "Info"
        }]