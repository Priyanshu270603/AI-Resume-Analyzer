from flask import Flask, request, jsonify, render_template
import fitz  # PyMuPDF for extracting text from PDFs
import os

# Ensure Flask knows where to find templates and static files
app = Flask(__name__, template_folder="templates", static_folder="static")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text.strip()

@app.route("/")
def index():
    return render_template("index.html")  # Load the frontend

@app.route("/analyze_resume", methods=["POST"])
def analyze_resume():
    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["resume"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith(".pdf"):
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        # Extract text from PDF
        resume_text = extract_text_from_pdf(filepath)

        response = {
            "message": "Resume analyzed successfully!",
            "extracted_text": resume_text[:500]  # Show first 500 chars
        }
        return jsonify(response)

    return jsonify({"error": "Invalid file format. Only PDFs are allowed."}), 400

if __name__ == "__main__":
    app.run(debug=True)
