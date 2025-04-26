from serpapi import GoogleSearch
import os
from dotenv import load_dotenv
from agents.market_trend_agent import analyze_market_trends

# Load the .env file
load_dotenv()

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

def research_company(company_name):
    params = {
        "q": f"{company_name} industry key products vision",
        "api_key": os.getenv("SERPAPI_API_KEY"),
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()

        if not results:
            raise ValueError(f"No results found for {company_name}")

        organic_results = results.get("organic_results", [])
        
        if not organic_results:
            return {
                "Industry": "Unknown",
                "Key Offerings": [],
                "Strategic Focus Areas": [],
                "Vision": "No data found."
            }

        combined_text = " ".join([res.get("snippet", "") for res in organic_results])

        industry = classify_industry(combined_text)

        # Extract Key Offerings
        keywords_offerings = ["product", "platform", "service", "solution", "technology", "software", "EV", "battery", "cloud services"]
        key_offerings = [kw.capitalize() for kw in keywords_offerings if kw in combined_text.lower()]

        # Define a mapping between offerings and focus areas
        offering_to_focus = {
            "Cloud services": ["Digital Transformation", "Automation"],
            "Battery": ["Sustainability"],
            "Ev": ["Sustainability"],
            "Software": ["Automation", "Customer Experience"],
            "Technology": ["Digital Transformation"],
            "Service": ["Customer Experience"],
            "Platform": ["Digital Transformation", "Analytics"],
            "Product": ["Operations", "Supply Chain"],
            "Solution": ["Operations", "Analytics"],
        }

        # Generate Strategic Focus Areas based on detected key offerings
        strategic_focus = set()
        for offering in key_offerings:
            focuses = offering_to_focus.get(offering, [])
            strategic_focus.update(focuses)

        # Extract Vision
        vision = "Vision not clearly mentioned."
        for res in organic_results:
            snippet = res.get("snippet", "")
            if "vision" in snippet.lower() and len(snippet.split()) > 5:
                vision = snippet
                break

        return {
            "Industry": industry,
            "Key Offerings": key_offerings,
            "Strategic Focus Areas": list(strategic_focus),
            "Vision": vision
        }

    except Exception as e:
        print(f"[Error] An error occurred during the API request: {e}")
        return None


# Main logic
company_name = input("Enter the company or industry name: ")
company_info = research_company(company_name)

if company_info is None:
    print("Error: Unable to fetch company information. Please try again later.")
else:
    print(f"Company Info: {company_info}")



# Main logic
if __name__ == "__main__":
    company_name = input("Enter the company or industry name: ")
    company_info = research_company(company_name)

    if company_info is None:
        print("Error: Unable to fetch company information. Please try again later.")
    else:
        print(f"Company Info: {company_info}")
        # Continue processing only if company_info is valid
        trends = analyze_market_trends(company_info.get('Industry', ''))
