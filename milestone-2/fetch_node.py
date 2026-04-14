import requests
from bs4 import BeautifulSoup
from typing import Dict, List
from .state import AgentState

def fetch_node(state: AgentState) -> Dict:
    """
    Fetches raw content from search URLs and extracts text.
    Uses BeautifulSoup for clean parsing.
    """
    search_results = state.get("search_results", [])
    if not search_results:
        return {"documents": [], "steps": ["Skipped fetching (no search results)"]}

    print(f"Node: Fetch | Fetching content from {len(search_results)} sources...")
    
    documents = []
    
    for res in search_results:
        url = res.get("url")
        content = res.get("content")
        
        if content:
            # If content is already present (from Tavily advanced), skip fetching
            documents.append({
                "url": url,
                "title": res.get("title", "No Title"),
                "content": content
            })
            continue
            
        print(f"  -> Fetching: {url}")
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
                
            # Get text
            text = soup.get_text()
    
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            clean_text = '\n'.join(chunk for chunk in chunks if chunk)
            
            documents.append({
                "url": url,
                "title": res.get("title", "No Title"),
                "content": clean_text[:5000]
            })
            
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
            
    return {
        "documents": documents,
        "steps": [f"Fetched content from {len(documents)} sources"]
    }
