from langgraph.graph import StateGraph, END
from typing import Dict
from .state import AgentState
from .search_node import search_node
from .fetch_node import fetch_node
from .summarize_node import summarize_node
from .analyze_node import analyze_node
from .decision_node import decision_node
from .extract_node import extract_node
from .report_node import report_node

def run_agent_workflow():
    """
    Constructs the LangGraph workflow for the Research Assistant.
    """
    # 1. Initialize the Graph
    workflow = StateGraph(AgentState)

    # 2. Add Nodes
    workflow.add_node("search", search_node)
    workflow.add_node("fetch", fetch_node)
    workflow.add_node("summarize", summarize_node)
    workflow.add_node("analyze", analyze_node)
    workflow.add_node("extract", extract_node)
    workflow.add_node("report", report_node)

    # 3. Define the Edges
    workflow.set_entry_point("search")
    
    workflow.add_edge("search", "fetch")
    workflow.add_edge("fetch", "summarize")
    workflow.add_edge("summarize", "analyze")

    # 4. Add the Conditional Edge (The "Intelligence" Loop)
    workflow.add_conditional_edges(
        "analyze",
        decision_node,
        {
            "search": "search",    # Loop back for more research
            "report": "extract"    # Go to extraction before reporting
        }
    )

    workflow.add_edge("extract", "report")
    workflow.add_edge("report", END)

    # 5. Compile the app
    app = workflow.compile()
    return app

def run_research(query: str, extract_facts: bool = False):
    """
    Entry point to run the compiled LangGraph agent.
    """
    agent = run_agent_workflow()
    
    # Initial State
    initial_state = {
        "query": query,
        "search_results": [],
        "documents": [],
        "summaries": [],
        "analysis": "",
        "extract_facts": extract_facts,
        "facts_table": "",
        "final_report": "",
        "sources": [],
        "steps": [],
        "loop_count": 0,
        "is_sufficient": False
    }
    
    print(f"🚀 Initializing Research Agent for query: '{query}'")
    final_state = agent.invoke(initial_state)
    return final_state
