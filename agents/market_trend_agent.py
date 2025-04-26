# agents/market_trend_agent.py
from serpapi import GoogleSearch
import os
from dotenv import load_dotenv
# Load the .env file
load_dotenv()
# agents/market_trend_agent.py

import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_market_trends(industry_name):
    """Fetch industry-specific AI and ML trends by referencing reports."""
    
    prompt = f"""
    Search insights from McKinsey, Deloitte, Nexocode, and other leading consultancies.
    Give a brief summary (max 3 lines) about:
    - How AI/ML/GenAI are transforming the '{industry_name}' industry.
    - Mention one or two emerging use cases or trends.
    
    Respond clearly without needing exact references.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        trends = response['choices'][0]['message']['content']
        return trends

    except Exception as e:
        print(f"[Error] Analyzing trends failed: {e}")
        return "Trends information not available."
