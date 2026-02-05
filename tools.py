import os
import time
import logging
from typing import List
from urllib.parse import urlparse
from dotenv import load_dotenv
from google.adk.tools import FunctionTool
from tavily import TavilyClient
from exa_py import Exa

load_dotenv()
tool_logger = logging.getLogger("ResearchTools")

def extract_domain(url: str) -> str:
    """Extract and clean domain from URL"""
    try:
        if "://" not in url: 
            url = "http://" + url
        parsed = urlparse(url)
        domain = parsed.netloc
        return domain[4:] if domain.startswith('www.') else domain
    except:
        return url

def search_tavily(query: str, search_depth: str = "advanced", max_results: int = 10) -> str:
    """Search using Tavily for structured web results"""
    tool_logger.info(f"Tavily searching: {query}")
    try:
        tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        response = tavily.search(
            query=query, 
            search_depth=search_depth, 
            max_results=max_results, 
            include_answer=True
        )
        
        if not response.get('results'):
            return f"Notice: No Tavily results for '{query}'."

        formatted = f"**Tavily Data:**\n"
        if response.get('answer'): 
            formatted += f"Quick Summary: {response['answer']}\n"
        
        for i, r in enumerate(response['results'], 1):
            formatted += f"{i}. {r['title']} - {r['url']}\nSnippet: {r['content'][:200]}\n"
        
        return formatted
    except Exception as e:
        tool_logger.error(f"Tavily Error: {e}")
        return f"Error: Tavily failed ({str(e)})"

def search_exa(query: str, num_results: int = 10, use_autoprompt: bool = True) -> str:
    """Search using Exa for neural/semantic results"""
    tool_logger.info(f"Exa searching: {query}")
    try:
        exa = Exa(api_key=os.getenv("EXA_API_KEY"))
        response = exa.search_and_contents(
            query=query, 
            num_results=num_results, 
            use_autoprompt=use_autoprompt, 
            text={"max_characters": 800}
        )
        
        if not response.results:
            return f"Notice: No Exa results for '{query}'."

        formatted = f"**Exa Neural Data:**\n"
        for i, r in enumerate(response.results, 1):
            formatted += f"{i}. {r.title} - {r.url}\nText: {r.text[:200]}...\n"
        
        return formatted
    except Exception as e:
        tool_logger.error(f"Exa Error: {e}")
        return f"Error: Exa failed ({str(e)})"

def search_with_urls(query: str, urls: List[str], use_tool: str = "auto", max_results: int = 10) -> str:
    """Search within specific URLs/domains only"""
    tool_logger.info(f"Specific URL search in: {urls}")
    domains = [extract_domain(u) for u in urls]
    
    try:
        tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        response = tavily.search(
            query=query, 
            include_domains=domains, 
            max_results=max_results
        )
        
        if not response.get('results'):
            return f"Notice: No data found within domains {domains}."

        formatted = f"**Targeted Domain Results:**\n"
        for r in response['results']:
            formatted += f"- {r['title']} ({r['url']}): {r['content'][:200]}\n"
        
        return formatted
    except Exception as e:
        tool_logger.error(f"Domain search error: {e}")
        return f"Error: Domain search failed ({str(e)})"

# Register tools
search_tavily_tool = FunctionTool(func=search_tavily)
search_exa_tool = FunctionTool(func=search_exa)
search_with_urls_tool = FunctionTool(func=search_with_urls)

__all__ = ['search_tavily_tool', 'search_exa_tool', 'search_with_urls_tool']