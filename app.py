from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Load knowledge base
with open("data/knowledge.json", "r") as f:
    knowledge = json.load(f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").lower()
    
    # Simple keyword matching
    for key, item in knowledge.items():
        for keyword in item["keywords"]:
            if keyword.lower() in user_message:
                return jsonify({"reply": item["response"]})
    
    # Fallback response
    return jsonify({"reply": "Sorry, I did not understand that. Can you rephrase?"})

if __name__ == "__main__":
    app.run(debug=True)
