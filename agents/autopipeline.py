# agents/auto_pipeline.py

import os
import requests
import fitz  # PyMuPDF
import pandas as pd
from dotenv import load_dotenv
from kaggle.api.kaggle_api_extended import KaggleApi
from transformers import pipeline
from serpapi import GoogleSearch
import openai

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class AutoPipeline:
    def __init__(self):
        pass

    def predict(self, company_name):
        company_text = research_company(company_name)
        industry = classify_industry(company_text)
        trends = analyze_market_trends(industry)
        return {
            "Company": company_name,
            "Industry": industry,
            "Trends": trends
        }


# Step 1: Extract Text from PDF
def extract_text_from_pdf(file_path):
    try:
        doc = fitz.open(file_path)
        text = "".join(page.get_text() for page in doc)
        return text
    except Exception as e:
        print(f"[Error] PDF extraction failed: {e}")
        return None

# Step 2: Summarize extracted text
def summarize_text(text):
    try:
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
        summary = " ".join(summarizer(chunk, max_length=150, min_length=40, do_sample=False)[0]['summary_text'] for chunk in chunks)
        return summary
    except Exception as e:
        print(f"[Error] Summarization failed: {e}")
        return None

# Step 3: Company Research via SerpAPI
def research_company(company_name):
    params = {
        "q": f"{company_name} industry key products vision",
        "api_key": os.getenv("SERPAPI_API_KEY"),
    }
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results.get("organic_results", [])
        combined_text = " ".join(res.get("snippet", "") for res in organic_results)

        return combined_text
    except Exception as e:
        print(f"[Error] Company research failed: {e}")
        return None

# Step 4: Classify Industry
def classify_industry(text):
    industries = {
        "Automotive": ["automotive", "vehicle", "car", "mobility", "transportation"],
        "Manufacturing": ["manufacturing", "factory", "production", "industrial", "automation"],
        "Finance": ["finance", "banking", "investment", "insurance", "financial services"],
        "Retail": ["retail", "e-commerce", "store", "shopping", "online sales"],
        "Healthcare": ["healthcare", "medical", "pharma", "hospital", "healthcare technology"],
        "Technology": ["technology", "software", "AI", "cloud", "machine learning", "SaaS"],
        "Energy": ["energy", "oil", "gas", "renewable", "solar", "wind energy"],
    }
    text = text.lower()
    for industry, keywords in industries.items():
        if any(keyword in text for keyword in keywords):
            return industry
    return "Other"

# Step 5: Analyze Market Trends via OpenAI
def analyze_market_trends(industry_name):
    prompt = f"""
    Give a brief summary (max 3 lines) about:
    - How AI/ML/GenAI are transforming the '{industry_name}' industry.
    - Mention one or two emerging use cases.
    No references needed.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"[Error] Trend analysis failed: {e}")
        return None

# Step 6: Load Company to Industry Mapping
def load_company_industry_mapping(file_path="data.csv"):
    try:
        df = pd.read_csv(file_path)
        return dict(zip(df['Company'].str.lower(), df['Industry']))
    except Exception as e:
        print(f"[Error] Loading mapping failed: {e}")
        return {}

# Step 7: Generate Use Cases based on Industry
def generate_use_cases(industry):
    industry_use_cases = {
        "Retail": [
            "GenAI-powered personalized shopping engines.",
            "ML-based predictive inventory management.",
            "AI customer support automation."
        ],
        "Healthcare": [
            "LLMs for patient data analysis.",
            "AI-based diagnostic tools.",
            "Automation in hospital management."
        ],
        "Automotive": [
            "AI for predictive vehicle maintenance.",
            "Autonomous driving enhancements.",
            "Smart automotive supply chains."
        ],
        # Add more industries as needed
    }
    return industry_use_cases.get(industry, ["Explore GenAI and automation opportunities."])

# Step 8: Search Datasets from Kaggle, HuggingFace, GitHub
def search_datasets_platforms(use_case):
    datasets = []
    # Kaggle
    try:
        api = KaggleApi()
        api.authenticate()
        kaggle_results = api.dataset_list(search=use_case)[:3]
        for d in kaggle_results:
            datasets.append({"platform": "Kaggle", "name": d.title, "url": f"https://www.kaggle.com/datasets/{d.ref}"})
    except Exception as e:
        print(f"[Error] Kaggle search failed: {e}")

    # HuggingFace
    try:
        response = requests.get(f"https://huggingface.co/api/datasets?search={use_case.replace(' ', '+')}")
        if response.status_code == 200:
            for d in response.json()[:3]:
                datasets.append({"platform": "HuggingFace", "name": d.get("name", ""), "url": f"https://huggingface.co/datasets/{d['id']}"})
    except Exception as e:
        print(f"[Error] HuggingFace search failed: {e}")

    # GitHub
    try:
        response = requests.get(f"https://api.github.com/search/repositories?q={use_case.replace(' ', '+')}+dataset")
        if response.status_code == 200:
            for repo in response.json().get("items", [])[:3]:
                datasets.append({"platform": "GitHub", "name": repo["name"], "url": repo["html_url"]})
    except Exception as e:
        print(f"[Error] GitHub search failed: {e}")

    return datasets

# ✨ The Final Orchestration: Fully Automated Pipeline
def auto_run_pipeline(file_path, company_name):
    print(f"🚀 Starting auto-pipeline for {company_name}...")

    # Step 1: Read PDF and Summarize
    text = extract_text_from_pdf(file_path)
    if not text:
        return "Failed to extract text."
    summary = summarize_text(text)
    print("✅ Text Summarized.")

    # Step 2: Research Company
    company_text = research_company(company_name)
    if not company_text:
        return "Failed to research company."
    print("✅ Company info fetched.")

    # Step 3: Classify Industry
    industry = classify_industry(company_text)
    print(f"✅ Industry classified: {industry}")

    # Step 4: Get Industry Trends
    trends = analyze_market_trends(industry)
    print(f"✅ Industry trends: {trends}")

    # Step 5: Generate Use Cases
    use_cases = generate_use_cases(industry)
    print(f"✅ Use cases generated: {use_cases}")

    # Step 6: Find Datasets for Each Use Case
    datasets_per_use_case = {}
    for use_case in use_cases:
        datasets = search_datasets_platforms(use_case)
        datasets_per_use_case[use_case] = datasets
    print(f"✅ Dataset search complete.")

    # Step 7: Bundle Everything
    return {
        "Summary": summary,
        "Industry": industry,
        "Trends": trends,
        "Use Cases": use_cases,
        "Datasets": datasets_per_use_case
    }

# 👇 Example usage:
if __name__ == "__main__":
    file_path = input("Enter path to company strategy PDF: ")
    company_name = input("Enter company name: ")
    results = auto_run_pipeline(file_path, company_name)
    print(results)
