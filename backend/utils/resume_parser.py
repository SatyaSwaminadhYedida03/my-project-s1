"""
Resume Parser - Stub Version for Deployment
Original functionality disabled due to dependency size constraints
PyPDF2 and python-docx removed to reduce deployment size
"""
import re
import io

# Stub functions - resume parsing disabled for deployment
def _get_nlp():
    """Stub: NLP functionality disabled"""
    return None

def extract_text_from_pdf(file_data):
    """Stub: PDF extraction disabled for deployment"""
    return "Resume parsing temporarily disabled. Please use plain text format."

def extract_text_from_docx(file_data):
    """Stub: DOCX extraction disabled for deployment"""
    return "Resume parsing temporarily disabled. Please use plain text format."

def extract_text_from_file(file_data, filename):
    """Extract text from uploaded file - stub version"""
    name = filename.lower()
    
    if name.endswith(".pdf"):
        return extract_text_from_pdf(file_data)
    elif name.endswith(".docx") or name.endswith(".doc"):
        return extract_text_from_docx(file_data)
    else:
        # Treat as plain text
        try:
            return file_data.decode('utf-8', errors='ignore')
        except Exception:
            return str(file_data)

def anonymize_text(text):
    """Remove PII from text using basic regex - simplified version"""
    if not isinstance(text, str):
        return ""
    
    # Remove emails
    text = re.sub(r'\S+@\S+', ' [EMAIL] ', text)
    
    # Remove phone numbers (various formats)
    text = re.sub(r'\+?\d[\d\-\s()]{6,}\d', ' [PHONE] ', text)
    
    # Remove URLs
    text = re.sub(r'http\S+|www\.\S+', ' [URL] ', text)
    
    # Mask gender words
    text = re.sub(r'\b(Male|Female|male|female|M|F|Man|Woman|man|woman)\b', ' [GENDER] ', text)
    
    # Simple header removal (first line if it looks like a name)
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if lines:
        first = lines[0]
        if 1 <= len(first.split()) <= 4 and first == first.title():
            lines[0] = "[REDACTED HEADER]"
        text = "\n".join(lines)
    
    # Compact whitespace
    text = re.sub(r'\s{2,}', ' ', text)
    return text
