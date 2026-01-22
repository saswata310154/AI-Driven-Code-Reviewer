from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-7B-Instruct",
    temperature=0.3,
    max_new_tokens=512
)

model = ChatHuggingFace(llm=llm)


def get_ai_suggestions(code_string):
    prompt = f"""
You are an expert Python code reviewer.

Analyze the following code and give:
1. Errors
2. Improvements
3. Best practices

Code:
{code_string}
"""

    response = model.invoke([
        HumanMessage(content=prompt)
    ])

    return response.content
