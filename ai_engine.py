from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from model.llm_engine import load_llm, generate_reply
import sys
import os
sys.path.append(os.path.dirname(__file__))


app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "allow_headers": ["Content-Type"],
        "methods": ["GET", "POST", "OPTIONS"]
    }
})

llm = load_llm()


@app.route("/")
def index():
    return send_from_directory(".", "new.html")

@app.route("/new.html")
def new_page():
    return send_from_directory(".", "new.html")

@app.route("/new2.html")
def chat_page():
    return send_from_directory(".", "new2.html")

@app.route("/ask", methods=["POST", "OPTIONS"])
def ask():
    if request.method == "OPTIONS":
        return "", 204
    
    data = request.get_json()
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"reply": "Enter question to ask"})
    
    print(f"you: {prompt}")
    reply = generate_reply(llm, prompt)
    print(f"ai: {reply}")
    return jsonify({"reply": reply})

def start_ai_engine():
    app.run(
        host="127.0.0.1",
        port=5137,
        debug=False,
        use_reloader=False
    )

if __name__ == "__main__":
    start_ai_engine()