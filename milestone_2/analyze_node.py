import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict
from .state import AgentState

def analyze_node(state: AgentState) -> Dict:
    summaries = state.get("summaries", [])
    query = state.get("query", "")
    
    if not summaries:
        return {"analysis": "No data available for analysis.", "is_sufficient": False, "loop_count": 1}

    print(f"Node: Analyze | Processing insights from {len(summaries)} sources...")
    
    api_key = os.getenv("GROQ_API_KEY")
    llm = ChatGroq(
        groq_api_key=api_key,
        model_name=os.getenv("MODEL_NAME", "llama-3.3-70b-versatile"),
        temperature=0.1
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", """
        You are a Research Intelligence Analyst. Your task is to look at multiple source summaries and the original research query.
        
        1. Summarize the collective findings.
        2. Identify any specific details from the original query that are still missing.
        3. Determine if the current information is "SUFFICIENT" to write a full professional report.
        
        Output format:
        Collective Insights: [Your synthesis]
        Missing Info: [What is still unknown]
        Verdict: [SUFFICIENT or INSUFFICIENT]
        """),
        ("user", f"Original Query: {query}\n\nSummaries:\n" + "\n---\n".join(summaries))
    ])

    chain = prompt | llm
    response = chain.invoke({})
    
    analysis_text = response.content
    is_sufficient = "VERDICT: SUFFICIENT" in analysis_text.upper()

    return {
        "analysis": analysis_text,
        "is_sufficient": is_sufficient,
        "loop_count": 1,
        "steps": ["Performed cross-document analysis and gap identification"]
    }
