import os
from typing import Dict
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from .state import AgentState

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type(Exception),
    reraise=True
)
def _call_report_llm(chain, query, summaries_text):
    """
    Robust call to LLM for final report synthesis.
    """
    return chain.invoke({
        "query": query,
        "summaries_text": summaries_text
    })

def report_node(state: AgentState) -> Dict:
    """
    Produces a professional, cross-referenced Markdown research report.
    """
    summaries = state.get("summaries", [])
    query = state.get("query", "Unknown Topic")
    
    if not summaries:
        print("Note: Insufficient data to generate a report.")
        return {
            "final_report": f"# Research Report: {query}\n\n*Error: Could not generate findings as no source summaries were available.*",
            "steps": ["Report generation failed (insufficient summaries)"]
        }

    print(f"Node: Report | Synthesizing final report for: {query}...")
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return {"final_report": "Error: Missing GROQ_API_KEY.", "steps": ["Report generation failed (missing key)"]}

    llm = ChatGroq(
        groq_api_key=api_key,
        model_name=os.getenv("MODEL_NAME", "llama-3.3-70b-versatile"),
        temperature=0.3
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", """
        You are a Senior Research Analyst. Synthesize the provided summaries into a professional Markdown report.
        CRITICAL: No conversational filler, no 'Here is your report', no 'I hope this helps'. 
        Start directly with the # TITLE. Be factual, dense, and structured.
        """),
        ("user", """
        TOPIC: {query}
        
        SOURCE SUMMARIES:
        {summaries_text}
        
        Please generate the report using this exact structure:
        
        # RESEARCH REPORT: [Descriptive Title]
        
        ## Executive Summary
        [A 2-3 sentence overview of the research findings and current state of the field]
        
        ---
        
        ## Key Research Findings
        [Group the information into 3-4 thematic areas. Use bolding for emphasis.]
        
        ## Regional/Contextual Nuances (If Applicable)
        [Note any differences in findings across sources]
        
        ## Strategic Conclusion
        [Final synthesis and future outlook]
        
        ---
        
        ## Appendix: Sources & Citations
        [List the URLs and Titles of all sources used]
        """)
    ])

    summaries_text = "\n\n---\n\n".join(summaries)
    chain = prompt | llm

    try:
        response = _call_report_llm(chain, query, summaries_text)
        
        # Combine Fact Table (if exists) with the report
        facts_table = state.get("facts_table", "")
        if facts_table and "NO SIGNIFICANT TECHNICAL METRICS" not in facts_table.upper():
            final_content = f"# RESEARCH AT A GLANCE\n\n{facts_table}\n\n---\n\n{response.content}"
        else:
            final_content = response.content

        return {
            "final_report": final_content,
            "steps": ["Professionally synthesized final research report"]
        }
    except Exception as e:
        print(f"Failed to generate final report: {e}")
        return {
            "final_report": f"# Research Report: {query}\n\n*Technical Error during synthesis: {e}*",
            "steps": ["Report synthesis failed due to API error"]
        }
