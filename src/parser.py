from PyPDF2 import PdfReader
from docx import Document

def parse_resume(file):
    text = ""

    if file.name.endswith(".pdf"):
        pdf = PdfReader(file)
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted

    elif file.name.endswith(".docx"):
        doc = Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"

    return text