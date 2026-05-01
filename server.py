from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ---------- CONFIG ----------
GROQ_API_KEY = "YOUR_GROQ_KEY"

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


# ---------- MAIN JARVIS ENDPOINT ----------
@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()

    # ESP sends:
    # {"text": "hello jarvis"}
    user_text = data.get("text", "")

    if not user_text:
        return jsonify({"reply": "No input received"}), 400

    # ---------- CALL GROQ ----------
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {
                "role": "system",
                "content": "You are Jarvis, a smart AI assistant for ESP32 IoT system."
            },
            {
                "role": "user",
                "content": user_text
            }
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(GROQ_URL, json=payload, headers=headers)
        result = response.json()

        reply = result["choices"][0]["message"]["content"]

        # ---------- RETURN TO ESP ----------
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"}), 500


# ---------- HEALTH CHECK ----------
@app.route("/", methods=["GET"])
def home():
    return "Jarvis Server Running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
