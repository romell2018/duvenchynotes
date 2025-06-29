import fitz  # PyMuPDF
from fpdf import FPDF
import os
import requests
import time

AZURE_KEY = os.getenv("AZURE_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")

def extract_text_from_pdf(filepath):
    doc = fitz.open(filepath)
    return "\n".join([page.get_text() for page in doc])

def summarize_text(text):
    if not AZURE_KEY or not AZURE_ENDPOINT or "your-resource" in AZURE_ENDPOINT:
        return (
            "⚠️ Dummy summary:\n"
            "This is a placeholder summary used when no Azure credentials are configured."
        )

    # Uncomment this block when Azure is ready
    """
    url = f"{AZURE_ENDPOINT}/language/analyze-text/jobs?api-version=2022-10-01-preview"
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "displayName": "Summarize Notes",
        "analysisInput": {
            "documents": [{"id": "1", "language": "en", "text": text}]
        },
        "tasks": [{"kind": "AbstractiveSummarization"}]
    }

    response = requests.post(url, headers=headers, json=data)
    job_url = response.headers["operation-location"]
    time.sleep(5)
    result = requests.get(job_url, headers=headers).json()

    return result["tasks"]["items"][0]["results"]["documents"][0]["summaries"][0]["text"]
    """

def generate_pdf(text, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        safe_line = line.encode("latin-1", "replace").decode("latin-1")
        pdf.multi_cell(0, 10, safe_line)
    path = os.path.join("notes", filename)
    pdf.output(path)
    return path


def generate_quiz(text):
    # If no Azure subscription configured, return dummy quiz
    if not AZURE_KEY or not AZURE_ENDPOINT or "your-resource" in AZURE_ENDPOINT:
        return f"""Q1: What is this document mainly about?
A. Placeholder content
B. Summary generation
C. PDF reading
D. randon
Answer: D

Q2: Which service is suggested for summarization in this project?
A. ChatGPT
B. Google Translate
C. Azure Language Service
D. Not mentioned
Answer: C

Q3: What does the fallback quiz provide when Azure is unavailable?
A. Nothing
B. Dummy quiz
C. Image preview
D. Random questions
Answer: B
"""

    # --- Azure AI quiz generation (commented out until ready) ---
    """
    url = f"{AZURE_ENDPOINT}/language/generation?api-version=2023-05-15"
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY,
        "Content-Type": "application/json"
    }
    prompt = (
        f"Generate 3 multiple choice questions with answers based on the following summary:\n\n{text}\n\n"
        "Format each question with 4 options labeled A-D and specify the correct answer."
    )
    data = {
        "prompt": prompt,
        "maxTokens": 200,
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()
    # Extract generated quiz text from Azure response depending on API shape
    quiz_text = response_json.get("generatedText", "Error generating quiz.")
    return quiz_text
    """