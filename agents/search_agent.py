from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

def search_agent(topic: str, num_results: int = 7) -> list[dict]:
    """
    Takes a research topic, searches the web using Tavily,
    returns a list of sources with title, URL, and content snippet.
    """
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    
    print(f"🔎Search Agent: Searching for '{topic}'...")
    
    response = client.search(
        query=topic,
        search_depth="advanced",
        max_results=num_results,
        include_raw_content=True
    )
    
    sources = []
    for result in response["results"]:
        sources.append({
            "title": result.get("title", "No title"),
            "url": result.get("url", ""),
            "snippet": result.get("content", ""),
            "raw_content": result.get("raw_content", "")[:3000]  
        })
    
    print(f"Search Agent: Found {len(sources)} sources")
    return sources