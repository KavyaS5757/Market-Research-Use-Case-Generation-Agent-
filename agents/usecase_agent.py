import pandas as pd

def load_company_industry_mapping(file_path="data.csv"):
    df = pd.read_csv(file_path)
    mapping = dict(zip(df['Company'].str.lower(), df['Industry']))
    return mapping

def get_industry_for_company(company_name, mapping):
    company_name = company_name.lower()
    return mapping.get(company_name, "Unknown")

def generate_use_cases(company_info, industry_trends):
    use_cases = []

    industry_mapping = load_company_industry_mapping()

    # 👇 fix by using .get() instead of direct indexing
    company_name = company_info.get('Company')  # safe way

    if not company_name:
        return ["Error: 'Company' key missing in input."]
    
    industry = get_industry_for_company(company_name, industry_mapping)
    
    # Generate use cases based on industry
    if industry == "Retail":
        use_cases.append("Implement GenAI-powered recommendation engines for personalized shopping experiences.")
        use_cases.append("Use ML for predictive demand forecasting in inventory management.")
        use_cases.append("Leverage AI chatbots to provide 24/7 customer support and improve customer service.")
    
    elif industry == "Healthcare":
        use_cases.append("Leverage LLMs for medical data analysis and AI-driven patient recommendations.")
        use_cases.append("Apply automation for patient scheduling and resource optimization.")
        use_cases.append("Use AI for diagnostic support and personalized treatment plans.")
    
    elif industry == "Automotive":
        use_cases.append("Use ML for predictive maintenance of vehicle components.")
        use_cases.append("Implement AI in autonomous driving systems and customer safety features.")
        use_cases.append("Leverage AI for smart supply chain management in the automotive industry.")

    elif industry == "Technology":
        use_cases.append("Develop intelligent virtual assistants using LLMs.")
        use_cases.append("Implement AI-driven cybersecurity threat detection and prevention systems.")
        use_cases.append("Use AI to enhance software development cycles via code generation and bug prediction.")

    elif industry == "Pharmaceuticals":
        use_cases.append("Use AI for drug discovery and optimization processes.")
        use_cases.append("Implement GenAI models for predictive modeling of clinical trials outcomes.")
        use_cases.append("Use RPA for regulatory compliance documentation.")

    elif industry == "Banking" or industry == "Financial Services":
        use_cases.append("Use ML models for fraud detection in real-time transactions.")
        use_cases.append("Implement GenAI to personalize banking experiences and financial planning.")
        use_cases.append("Automate loan approval processes using predictive analytics.")

    elif industry == "Entertainment":
        use_cases.append("Leverage GenAI to create personalized content recommendations.")
        use_cases.append("Use AI to generate automated scriptwriting and video editing.")
        use_cases.append("Implement deep learning models for real-time audience sentiment analysis.")

    elif industry == "Energy":
        use_cases.append("Predict energy demands with ML models for optimized distribution.")
        use_cases.append("Leverage AI for renewable energy management and efficiency improvement.")
        use_cases.append("Use AI in fault detection in oil and gas pipelines.")

    elif industry == "Education":
        use_cases.append("Use AI-based adaptive learning platforms for personalized education.")
        use_cases.append("Leverage chatbots for 24/7 student query resolution.")
        use_cases.append("Develop intelligent tutoring systems to assist both students and educators.")

    elif industry == "Food & Beverage":
        use_cases.append("Use predictive analytics to optimize food supply chains.")
        use_cases.append("Apply AI in personalized nutrition recommendation systems.")
        use_cases.append("Use computer vision for quality control in food production lines.")

    elif industry == "Agriculture":
        use_cases.append("Leverage AI for precision farming and crop monitoring.")
        use_cases.append("Use drone-based ML models for real-time field analysis.")
        use_cases.append("Apply AI in weather prediction for optimal planting schedules.")

    elif industry == "Logistics":
        use_cases.append("Implement AI for route optimization and last-mile delivery prediction.")
        use_cases.append("Use ML for demand forecasting and inventory management.")
        use_cases.append("Automate warehouse operations with AI-based robotics.")

    elif industry == "Consulting":
        use_cases.append("Use GenAI to automate market research and insights generation.")
        use_cases.append("Leverage AI for client-specific strategic planning recommendations.")
        use_cases.append("Automate proposal generation with AI-powered drafting tools.")

    elif industry == "Real Estate Tech":
        use_cases.append("Implement AI for property price prediction and dynamic valuation.")
        use_cases.append("Use GenAI for automatic property descriptions and marketing content.")
        use_cases.append("Leverage ML models for tenant risk scoring and management.")

    elif industry == "Social Networking":
        use_cases.append("Use AI to enhance content moderation and detect harmful content.")
        use_cases.append("Leverage LLMs to generate engaging posts and user interactions.")
        use_cases.append("Implement recommendation systems for personalized feed curation.")

    elif industry == "Cloud Computing" or industry == "SaaS":
        use_cases.append("Use AI for resource allocation optimization across cloud services.")
        use_cases.append("Leverage GenAI for automated cloud infrastructure management.")
        use_cases.append("Predict and prevent service downtime using ML models.")

    elif industry == "Semiconductors":
        use_cases.append("Use AI to optimize semiconductor manufacturing processes.")
        use_cases.append("Leverage ML models for chip defect detection.")
        use_cases.append("Apply predictive maintenance in semiconductor fabrication plants.")

    elif industry == "Transportation":
        use_cases.append("Implement AI in fleet management and route optimization.")
        use_cases.append("Use ML for predictive maintenance of transportation vehicles.")
        use_cases.append("Develop AI-driven logistics optimization systems.")

    elif industry == "Hospitality":
        use_cases.append("Leverage GenAI to personalize guest experiences and itineraries.")
        use_cases.append("Use ML for dynamic pricing optimization in hotels.")
        use_cases.append("Implement AI chatbots for guest service management.")

    else:
        use_cases.append("Explore GenAI and automation technologies to enhance operational efficiency.")
    
    # Add industry trends if provided
    if industry_trends:
        use_cases.append(f"Industry-specific trends: {industry_trends[:200]}...")

    return use_cases
