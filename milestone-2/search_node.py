from duckduckgo_search import DDGS
import arxiv
import os
from typing import List, Dict
from dotenv import load_dotenv
from tavily import TavilyClient
from .state import AgentState


load_dotenv()

def search_node(state: AgentState) -> Dict:
    """
    Hybrid Search node that prioritizes Tavily for results,
    falling back to DuckDuckGo/ArXiv for zero-key free search.
    """
    query = state["query"]
    tavily_key = os.getenv("TAVILY_API_KEY")
    results = []
    
    if tavily_key:
        print(f"Node: Search | Querying Tavily for: {query}")
        try:
            tavily = TavilyClient(api_key=tavily_key)
            # Use advanced search depth to get better snippets and raw content
            search_response = tavily.search(query=query, search_depth="advanced", max_results=3, include_raw_content=True)
            results = search_response.get("results", [])
        except Exception as e:
            print(f"Tavily search failed: {e}. Falling back to DuckDuckGo.")
            tavily_key = None # Trigger fallback

    if not tavily_key:
        print(f"Node: Search | Querying DuckDuckGo for: {query}")
        try:
            with DDGS() as ddgs:
                ddg_results = list(ddgs.text(query, max_results=3))
                results = [{"title": r["title"], "url": r["href"], "content": r["body"]} for r in ddg_results]
        except Exception as e:
            print(f"DuckDuckGo search failed: {e}")

    # Fallback to ArXiv for academic queries if no results yet
    if not results:
        print("Node: Search | No results from web. Querying ArXiv...")
        try:
            search = arxiv.Search(query=query, max_results=2)
            for res in search.results():
                results.append({"title": res.title, "url": res.pdf_url, "content": res.summary})
        except Exception as e:
            print(f"ArXiv search failed: {e}")

    return {
        "search_results": results,
        "steps": [f"Discovery: Found {len(results)} initial sources"]
    }
