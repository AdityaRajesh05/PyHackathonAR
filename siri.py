from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from transformers import pipeline, set_seed

# ✅ Define Flask app before using it
app = Flask(__name__, template_folder=".")
CORS(app)

# ✅ Initialize AI Model
set_seed(42)
generator = pipeline("text-generation", model="gpt2")

@app.route("/")
def home():
    return render_template("Chatgpt Voice Webapp.html")  # Ensure this matches your HTML file name

@app.route("/voice", methods=["POST"])
def voice_command():
    data = request.get_json()

    if not data or "command" not in data:
        return jsonify({"response": "Invalid request"}), 400

    command = data["command"]

    try:
        response = generator(command, max_length=100, num_return_sequences=1, truncation=True)
        ai_response = response[0]["generated_text"]
        print("AI Response:", ai_response)  # Debugging output
    except Exception as e:
        print("Error generating AI response:", e)
        ai_response = "Sorry, I couldn't process that."

    return jsonify({"response": ai_response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
