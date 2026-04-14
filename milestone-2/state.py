from typing import Annotated, List, TypedDict, Dict
import operator

class AgentState(TypedDict):
    """
    State definition for the Agentic AI Research Assistant.
    """
    query: str
    search_results: List[dict]  # List of {title, url, snippet}
    documents: List[dict]       # List of {url, content}
    summaries: List[str]
    analysis: str               # Synthesized analysis
    extract_facts: bool         # Toggle for fact-sheet extraction
    facts_table: str            # Extracted technical facts in Markdown
    final_report: str
    sources: List[str]
    steps: Annotated[List[str], operator.add]
    loop_count: int             # Track iterations to prevent infinite loops
    is_sufficient: bool         # Logic flag for decision node
