# app/config.py
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./code_reviews.db")

DEFAULT_PROMPT = (
    "You are a senior software engineer and code reviewer.\n"
    "Review the provided code for: readability, modularity, correctness, potential bugs, performance, security issues, and maintainability.\n"
    "Provide: 1) a short summary (2-3 sentences), 2) categorized findings (Bugs, Security, Performance, Style/Readability, Architecture/Design), and 3) actionable suggestions and examples or small diffs when possible.\n"
    "Be concise and include line references if you can.\n"
)