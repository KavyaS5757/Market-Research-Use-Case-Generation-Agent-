import streamlit as st
from agents.research_agent import research_company
from agents.market_trend_agent import analyze_market_trends
from agents.usecase_agent import generate_use_cases
from agents.resource_finder_agent import find_resources_for_usecases

st.set_page_config(page_title="AI/ML Use Case Generator", page_icon="🤖", layout="centered")

st.title("🤖 AI/ML/GenAI Use Case Advisor")
st.markdown("Type a company or industry name, and I'll generate AI use cases, trends, and resources!")

# Session State to store conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

# User input
user_input = st.chat_input("Enter company or industry name...")

if user_input:
    # Store user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Run your agents
    company_name = user_input
    company_info = research_company(company_name)
    
    # Check if company_info was retrieved successfully
    if company_info and 'Company' not in company_info:
        company_info['Company'] = company_name
    
    if company_info:    
        industry = company_info.get('Industry', '') 
        # Fetch trends for the given industry
        trends = analyze_market_trends(industry)

        # Generate use cases based on company info and trends
        use_cases = generate_use_cases(company_info, trends)

        # Find resources based on use cases
        resources = find_resources_for_usecases(use_cases)

        # 🛠 Normalize nested list if needed
        for uc in resources:
            if isinstance(resources[uc], list) and len(resources[uc]) > 0 and isinstance(resources[uc][0], list):
                resources[uc] = resources[uc][0]

        # Format AI reply
        ai_reply = f"""
## 🏢 Company Overview
- **Industry**: {company_info.get('Industry', 'Unknown')}
- **Key Offerings**: {', '.join(company_info.get('Key Offerings', []))}
- **Strategic Focus Areas**: {', '.join(company_info.get('Strategic Focus Areas', []))}
- **Vision**: {company_info.get('Vision', 'Not available.')}

## 💡 Proposed Use Cases
"""
        for uc in use_cases:
            ai_reply += f"- {uc}\n"

        ai_reply += "\n## 📚 Resources (Datasets)\n"

        for uc in use_cases:
            ai_reply += f"\n**{uc}**:\n"
            resource_links = resources.get(uc, [])
            # Handle nested list if needed
            if isinstance(resource_links, list) and len(resource_links) > 0 and isinstance(resource_links[0], list):
                resource_links = resource_links[0]
                
            # Filter only valid datasets (having non-empty URL)
            valid_resources = []
            for r in resource_links:
                if isinstance(r, dict) and r.get('url'):
                    valid_resources.append(r)

            if not valid_resources:
                ai_reply += "\n_No datasets found._\n"
            else:
                for r in valid_resources:
                    ai_reply += f"- [{r['name']}]({r['url']}) ({r['platform']})\n"


        # Store assistant reply
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})

    else:
        # If company info is not found, provide an error message
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "❌ Error: Unable to fetch company information. Please try again later."
        })

# Display conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            st.markdown(message["content"])
            
            # After showing assistant overview & use cases — show Resources Expanders
            if message["content"].startswith("## 🏢 Company Overview"):
                st.markdown("## 📚 Resources (Datasets)")

                for uc in use_cases:
                    with st.expander(f"📚 Resources for {uc}"):
                        resource_links = resources.get(uc, [])

                        if not resource_links:
                            st.markdown("<span style='color: #FF6B6B;'>❌ No datasets found.</span>", unsafe_allow_html=True)
                        else:
                            # Handle nested lists if needed
                            if isinstance(resource_links[0], list):
                                resource_links = resource_links[0]

                            valid_resources = []
                            for r in resource_links:
                                if isinstance(r, dict) and r.get('url'):
                                    valid_resources.append(r)

                            if not valid_resources:
                                st.markdown("<span style='color: #FF6B6B;'>❌ No datasets found.</span>", unsafe_allow_html=True)
                            else:
                                for r in valid_resources:
                                    st.markdown(
                                        f"<div style='padding:5px 0;'>"
                                        f"🔗 <a href='{r['url']}' target='_blank' style='color:#1f77b4; text-decoration:none;'>{r['name']}</a> "
                                        f"<span style='color: #6c757d;'>({r['platform']})</span>"
                                        f"</div>",
                                        unsafe_allow_html=True
                                    )
        else:
            st.markdown(message["content"])


# # app.py

# # frontend.py
# import streamlit as st
# import requests

# st.title("Frontend Streamlit App")

# # User input
# input_text = st.text_input("Enter text for prediction:")

# # Button to send data to Flask
# if st.button("Predict"):
#     if input_text:
#         # Send to Flask backend
#         response = requests.post(
#             "http://localhost:5000/predict",
#             json={"input_text": input_text}
#         )
        
#         if response.status_code == 200:
#             prediction = response.json().get("result")
#             st.success(f"Prediction: {prediction}")
#         else:
#             st.error("Failed to get prediction from backend")
