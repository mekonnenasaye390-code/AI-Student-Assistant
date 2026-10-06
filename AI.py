from flask import Flask, request, jsonify, send_from_directory
from google import genai
import os
import traceback

app = Flask(__name__)

# Get Gemini API key
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not set.")

# Connect to Gemini
client = genai.Client(api_key=API_KEY)


# Open index.html from the same folder as AI.py
@app.route("/")
def home():
    return send_from_directory(
        os.path.dirname(os.path.abspath(__file__)),
        "index.html"
    )


# Ask Gemini
@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "answer": "No question received."
            })

        question = data.get("question", "").strip()

        if not question:
            return jsonify({
                "answer": "Please enter a question."
            })

        print("Question:", question)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=question
        )

        answer = response.text

        print("Gemini:", answer)

        return jsonify({
            "answer": answer
        })

    except Exception as e:
        print("ERROR:")
        traceback.print_exc()

        return jsonify({
            "answer": "Gemini error: " + str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)