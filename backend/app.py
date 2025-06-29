from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from utils import extract_text_from_pdf, summarize_text, generate_pdf, generate_quiz
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS so React frontend can call

UPLOAD_FOLDER = "uploads"
NOTES_FOLDER = "notes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(NOTES_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    text = extract_text_from_pdf(filepath)
    summary = summarize_text(text)
    quiz = generate_quiz(summary)    # Use summary here, NOT raw text
    pdf_path = generate_pdf(summary + "\n\n---\n\n" + quiz, filename + "_summary.pdf")

    return jsonify({
        "summary": summary,
        "quiz": quiz,
        "pdf": pdf_path
    })

@app.route("/download", methods=["GET"])
def download_pdf():
    path = request.args.get("path")
    if not path or not os.path.isfile(path):
        return "File not found", 404
    return send_file(os.path.abspath(path), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
