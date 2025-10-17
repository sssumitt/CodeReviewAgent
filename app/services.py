# app/services.py
import google.generativeai as genai
from .config import GEMINI_API_KEY, DEFAULT_PROMPT

if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY is not set in the .env file. API calls will fail.")
else:
    genai.configure(api_key=GEMINI_API_KEY)

def call_gemini_review(code: str, filename: str, model_name: str = 'gemini-2.5-pro') -> str:
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY has not been configured.")

    prompt = (
        f"{DEFAULT_PROMPT}\n---\nFilename: {filename}\n---\nCode:\n```\n{code}\n```\n"
    )

    model = genai.GenerativeModel(model_name)
    try:
        response = model.generate_content(prompt)
        return response.text.strip() if response.text else "(No review text returned)"
    except Exception as e:
        # It's good practice to log the error here
        print(f"Gemini API call failed: {e}")
        raise RuntimeError(f"Gemini API call failed: {e}")