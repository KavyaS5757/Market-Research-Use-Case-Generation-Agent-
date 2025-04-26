# agents/knowledge_base_agent.py

import fitz  # PyMuPDF
from transformers import pipeline

# Step 1: Extract Text from PDF
def extract_text_from_pdf(file_path):
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"[Error] Failed to extract text from PDF: {e}")
        return None

# Step 2: Summarize Text
def summarize_text(text):
    try:
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]  # BART has token limit
        summary = ""
        for chunk in chunks:
            result = summarizer(chunk, max_length=150, min_length=40, do_sample=False)
            summary += result[0]['summary_text'] + " "
        return summary
    except Exception as e:
        print(f"[Error] Failed during summarization: {e}")
        return None

# Step 3: Full Knowledge Base Agent
def knowledge_base_summary(file_path):
    print(f"🔍 Reading and summarizing: {file_path}")
    
    text = extract_text_from_pdf(file_path)
    if not text:
        return "❌ No text extracted from PDF."

    summary = summarize_text(text)
    if not summary:
        return "❌ Summarization failed."

    return summary

# (Optional) Save summary to a file
def save_summary_to_file(summary_text, output_path="reports/company_strategy_summary.md"):
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("# 📄 Company Strategy Summary\n\n")
            f.write(summary_text)
        print(f"✅ Summary saved to {output_path}")
    except Exception as e:
        print(f"[Error] Failed to save summary: {e}")
