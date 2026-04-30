from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

GROQ_API_KEY = "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"

@app.route("/", methods=["GET"])
def home():
    return "JARVIS SERVER OK"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_text = data.get("text", "")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": user_text}
        ]
    }

    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload
    )

    result = r.json()

    reply = result["choices"][0]["message"]["content"]

    return jsonify({
        "reply": reply
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
