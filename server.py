import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

# Load .env
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

API_KEY = os.getenv("GROQ_API_KEY")
PORT = int(os.getenv("PORT", 5051))

print("API KEY LOADED:", API_KEY)

@app.route("/", methods=["GET"])
def home():
    return "Jarvis server (Groq) running"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_input = data.get("question", "").lower()

    if not user_input:
        return jsonify({"error": "No question"}), 400

    # 🔥 COMMAND SYSTEM
    if "play" in user_input:
        return jsonify({
            "type": "command",
            "action": "play_music",
            "song": user_input.replace("play", "").strip()
        })

    if "time" in user_input:
        return jsonify({
            "type": "response",
            "reply": datetime.now().strftime("%H:%M")
        })

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-8b-instant",  # ✅ FIXED MODEL
                "messages": [
                    {
                        "role": "system",
                        "content": (
    "You are Jarvis, a smart assistant. "
    "Reply in under 10 words. "
    "No roleplay, no Tony Stark, no drama. "
    "Be direct, calm, and slightly robotic."
)
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ],
                "max_tokens": 50,
                "temperature": 0.3
            }
        )

        print("STATUS:", response.status_code)
        print("RAW:", response.text)

        result = response.json()

        if "choices" not in result:
            return jsonify({
                "error": "AI error",
                "details": result
            }), 500

        reply = result["choices"][0]["message"]["content"]

        return jsonify({
            "type": "response",
            "reply": reply
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": "AI failed"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)