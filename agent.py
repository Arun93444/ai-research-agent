import os
import requests
from dotenv import load_dotenv
from serpapi import GoogleSearch

load_dotenv()

gemini_key = os.environ.get("GEMINI_API_KEY")
serpapi_key = os.environ.get("SERPAPI_KEY")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"

def search_web(query):
    print(f"Searching: {query}")
    search = GoogleSearch({
        "q": query,
        "api_key": serpapi_key,
        "num": 5
    })
    results = search.get_dict()
    
    snippets = ""
    if "organic_results" in results:
        for r in results["organic_results"][:5]:
            snippets += r.get("snippet", "") + "\n"
    return snippets

def ask_gemini(prompt):
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    response = requests.post(url, json=data)
    result = response.json()
    if "candidates" in result:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    return "Error: " + str(result)

def research_agent(topic):
    print(f"\n🤖 Agent starting research on: {topic}")
    print("="*50)
    
    # Step 1 — Search
    print("\n📡 Step 1: Searching the web...")
    search_results = search_web(topic)
    
    # Step 2 — Analyze
    print("🧠 Step 2: Analyzing results...")
    prompt = f"""You are a research agent. Based on the search results below,
write a comprehensive summary about: {topic}

Search Results:
{search_results}

Write a clear, detailed summary with key points:"""
    
    summary = ask_gemini(prompt)
    
    # Step 3 — Output
    print("\n📝 Step 3: Research Complete!")
    print("="*50)
    print(summary)
    print("="*50)
    
    return summary

print("🤖 AI Research Agent Ready!")
print("Type 'quit' to exit\n")

while True:
    topic = input("What should I research? ")
    if topic == "quit":
        break
    research_agent(topic)
    print()