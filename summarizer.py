# summarizer.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-1.5-pro")

def basic_fallback_summary(content):
    """Fallback when API quota is exceeded."""
    if not content:
        return "No content to summarize."
    return content[:150] + "..." if len(content) > 150 else content

def summarize_email(content):
    if not content:
        return "No content to summarize."

    prompt = f"Summarize the following email in 1-2 sentences:\n\n{content}"
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
         print(f"[Gemini API] Error: {e}")
         return f"{basic_fallback_summary(content)}"
