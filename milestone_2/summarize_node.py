import os
import time
import re
from typing import Dict, List
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from .state import AgentState

def local_summarize_filter(content: str, query: str, max_chars: int = 1500) -> str:
    """
    Local NLP filter to reduce input tokens before the API call.
    Uses basic keyword-based sentence selection.
    """
    if not content or len(content) <= max_chars:
        return content
    
    # Extract query keywords for picking relevant lines
    query_words = set(re.findall(r'\w+', query.lower()))
    sentences = content.split('. ')
    
    # Score sentences based on query match
    scored_sentences = []
    for s in sentences:
        score = sum(1 for word in query_words if word in s.lower())
        scored_sentences.append((score, s))
    
    # Sort by score and take top sentences
    scored_sentences.sort(key=lambda x: x[0], reverse=True)
    
    # Reassemble up to max_chars
    selected = []
    current_len = 0
    for score, s in scored_sentences:
        if current_len + len(s) < max_chars:
            selected.append(s)
            current_len += len(s)
        else:
            break
            
    return ". ".join(selected)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type(Exception),
    reraise=True
)
def _call_summarize_llm(chain, content):
    """
    Robust call to LLM for summarization.
    """
    return chain.invoke({
        "content": content
    })

def summarize_node(state: AgentState) -> Dict:
    """
    Summarization node.
    Focuses on fact-based 3-4 point summaries with robust error handling.
    """
    documents = state.get("documents", [])
    query = state.get("query", "")
    
    if not documents:
        print("Note: No documents to summarize.")
        return {"summaries": [], "steps": ["Skipped summarization (no documents found)"]}

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY missing in environment.")
        return {"steps": ["Failed summarization (missing API key)"]}

    print(f"Node: Summarize | Summarizing {len(documents)} sources...")

    # Using the faster, cheaper 8B model for extraction
    llm = ChatGroq(
        groq_api_key=api_key,
        model_name="llama-3.1-8b-instant",
        temperature=0.1
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", """
        You are a Fact Extraction Agent. Your goal is to provide a concise, 3-4 point summary of the text provided.
        Focus ONLY on facts, research findings, and technical details.
        NO conversational text. NO 'Here is a summary'.
        """),
        ("user", "SOURCE TEXT:\n{content}")
    ])

    chain = prompt | llm
    summaries = []
    
    for doc in documents:
        # LOCAL FILTERING: Reduce token usage before sending to API
        clean_content = local_summarize_filter(doc["content"], query)
        
        try:
            response = _call_summarize_llm(chain, clean_content)
            summaries.append(response.content.strip())
            time.sleep(0.5) 
        except Exception as e:
            print(f"Failed to summarize source: {e}")
            
    return {
        "summaries": summaries,
        "steps": [f"Synthesized summaries for {len(summaries)} sources"]
    }
