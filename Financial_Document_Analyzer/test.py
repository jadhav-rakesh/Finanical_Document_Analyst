import os
from dotenv import load_dotenv
from crewai import LLM

# Load .env
load_dotenv()

# Initialize LLM (same setup as in your agents.py)
llm = LLM(
    model="openai/gpt-oss-20b:free",   # or "openai/gpt-oss-20b:free"
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0.7
)

def test_llm():
    try:
        response = llm.call("Hello, can you confirm this LLM call works?")
        print("✅ LLM response received:")
        print(response)
    except Exception as e:
        print("❌ LLM call failed:")
        print(e)

if __name__ == "__main__":
    test_llm()
