import requests
import os
from kaggle.api.kaggle_api_extended import KaggleApi
from dotenv import load_dotenv

# Load .env file for Kaggle API token (assuming you have the file)
load_dotenv()

def search_datasets_platforms(use_case):
    """Search for datasets related to a specific use case on multiple platforms."""
    datasets = []

    # Search on Kaggle
    try:
        api = KaggleApi()
        api.authenticate()  # Make sure to authenticate the Kaggle API
        search_results = api.dataset_list(search=use_case)
        
        # Limiting results manually by slicing the list
        search_results = search_results[:5]  # Get only the first 5 results
        
        for dataset in search_results:
            datasets.append({
                "platform": "Kaggle",
                "name": dataset.title,
                "url": f"https://www.kaggle.com/datasets/{dataset.ref}"
            })
        print(f"Kaggle Results for {use_case}: {datasets}")  # Debug log
    except Exception as e:
        print(f"Error fetching Kaggle datasets: {e}")

    # Search on HuggingFace
    try:
        huggingface_url = f"https://huggingface.co/api/datasets?search={use_case.replace(' ', '+')}"
        response = requests.get(huggingface_url)
        
        if response.status_code == 200:
            huggingface_datasets = response.json()
            for dataset in huggingface_datasets:
                datasets.append({
                    "platform": "HuggingFace",
                    "name": dataset.get("name", "No Name"),
                    "url": f"https://huggingface.co/datasets/{dataset['id']}"
                })
        print(f"HuggingFace Results for {use_case}: {datasets}")  # Debug log
    except Exception as e:
        print(f"Error fetching HuggingFace datasets: {e}")

    # Search on GitHub
    try:
        github_search_url = f"https://api.github.com/search/repositories?q={use_case.replace(' ', '+')}+dataset"
        github_datasets = requests.get(github_search_url).json()
        
        for repo in github_datasets.get("items", []):
            datasets.append({
                "platform": "GitHub",
                "name": repo["name"],
                "url": repo["html_url"]
            })
        print(f"GitHub Results for {use_case}: {datasets}")  # Debug log
    except Exception as e:
        print(f"Error fetching GitHub datasets: {e}")

    return datasets



def find_resources_for_usecases(use_cases):
    """Find datasets related to the proposed use cases."""
    print("[Resource Finder Agent] Finding datasets...")

    all_resources = {}

    for use_case in use_cases:
        datasets = search_datasets_platforms(use_case)
        if datasets:
            all_resources[use_case] = datasets
        else:
            all_resources[use_case] = "No datasets found."

    return all_resources
