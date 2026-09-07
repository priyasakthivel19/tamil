"""
app.py

Flask backend for a single-topic study chatbot powered by the Gemini API.
The allowed topic and the behaviour rules live in chatbot_config.py.
"""

import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
from google.genai import types

from chatbot_config import CHATBOT_TITLE, SYSTEM_PROMPT

# Load GEMINI_API_KEY from the .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-3.1-flash-lite"

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Add it to your .env file before running the app."
    )

client = genai.Client(api_key=GEMINI_API_KEY)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html", chatbot_title=CHATBOT_TITLE)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()

    if not user_message:
        return jsonify({"reply": "Please type a question to get started."}), 400

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
            ),
        )
        reply = response.text or "Sorry, I couldn't generate a response. Please try again."
    except Exception:
        reply = "Something went wrong while contacting the AI service. Please try again shortly."

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)
