import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict
from .state import AgentState

def extract_node(state: AgentState) -> Dict:
    """
    Optional Hard-Fact Extraction Node.
    Isolates technical data, numbers, and key entities into a Markdown table.
    """
    if not state.get("extract_facts", False):
        return {"facts_table": "", "steps": ["Skipped Hard-Fact extraction"]}

    summaries = state.get("summaries", [])
    if not summaries:
        return {"facts_table": "", "steps": ["Skipped extraction (no data)"]}

    print("Node: Extract | Isolating technical facts and statistics...")
    
    api_key = os.getenv("GROQ_API_KEY")
    llm = ChatGroq(
        groq_api_key=api_key,
        model_name=os.getenv("MODEL_NAME", "llama-3.3-70b-versatile"),
        temperature=0.0
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", """
        You are a Technical Data Extractor. Your task is to extract hard data from the provided research summaries.
        Focus ONLY on:
        - Numbers, Percentages, and Statistics
        - Specific Dates and Timelines
        - Key Companies or Organizations
        - Technical Metrics (e.g., 50km/h, 5nm process)
        
        OUTPUT FORMAT:
        Return ONLY a Markdown Table with the following columns:
        | Entity/Metric | Value/Observation | Source |
        
        If no hard data is found, return "No significant technical metrics found."
        Do not provide any conversational text or preamble.
        """),
        ("user", "RESEARCH SUMMARIES:\n" + "\n---\n".join(summaries))
    ])

    chain = prompt | llm
    try:
        response = chain.invoke({})
        return {
            "facts_table": response.content.strip(),
            "steps": ["Member 2: Generated technical fact-sheet table"]
        }
    except Exception as e:
        print(f"Fact extraction failed: {e}")
        return {"facts_table": "", "steps": ["Failed fact extraction"]}
    
