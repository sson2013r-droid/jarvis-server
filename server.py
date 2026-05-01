from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ---------- GROQ CONFIG ----------
GROQ_API_KEY = "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"

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


# ---------- MAIN JARVIS ENDPOINT ----------
@app.route("/ask", methods=["POST"])
def ask():

    try:
        data = request.get_json()

        # ESP sends: {"text":"hello jarvis"}
        user_text = data.get("text", "")

        if not user_text:
            return jsonify({"reply": "No input received"}), 400

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
           "model": "llama-3.1-8b-instant",
            "messages": [
                {
                    "role": "system",
                    "content": "You are Jarvis, an AI assistant for ESP32 IoT system."
                },
                {
                    "role": "user",
                    "content": user_text
                }
            ],
            "temperature": 0.7
        }

        response = requests.post(GROQ_URL, json=payload, headers=headers)

        # ---------- SAFE JSON PARSE ----------
        try:
            result = response.json()
        except:
            return jsonify({"reply": "Invalid response from Groq"}), 500

        # ---------- SAFE CHECK (FIX FOR YOUR 500 ERROR) ----------
        if "choices" not in result:
            error_msg = result.get("error", "Unknown Groq error")
            return jsonify({"reply": f"Groq Error: {error_msg}"}), 500

        reply = result["choices"][0]["message"]["content"]

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"Server Error: {str(e)}"}), 500


# ---------- HEALTH CHECK ----------
@app.route("/", methods=["GET"])
def home():
    return "Jarvis Server Running"


# ---------- RUN SERVER ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
