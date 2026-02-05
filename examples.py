import requests
import json

BASE_URL = "https://iecc-research-agent-1013110229500.us-central1.run.app" 
API_KEY = "iecc_ai_developer**983**" 



def test_agent_info():
    print("\n--- Testing Agent Info (GET /a2a/info) ---")
    url = f"{BASE_URL}/a2a/info"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("✅ Success! Agent Capabilities:")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        else:
            print(f"❌ Failed with status: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"💥 Error: {e}")
HEADERS = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY  
}
def test_research_task():
    print("\n--- Testing Research Task (POST /a2a/task) ---")
    url = f"{BASE_URL}/a2a/task"
    
    payload = {
        "query": "How nile university support innovation ?",
        "search_mode": "hybrid", 
        "domains":['nu.edu.eg'],
        "max_results_per_tool": 5
    }
    
    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Research Completed! Session ID: {result.get('session_id')}")
            print("\n--- Research Report ---")
            print(result.get("research_report"))
        elif response.status_code in [401, 403]:
            print(f"🚫 Auth Error ({response.status_code}): تأكد من صحة الـ API_KEY")
        else:
            print(f"❌ Failed with status: {response.status_code}")
            print(response.json())
            
    except Exception as e:
        print(f"💥 Error: {e}")

if __name__ == "__main__":
    test_agent_info()
    
    test_research_task()