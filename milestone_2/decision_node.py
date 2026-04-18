from typing import Literal
from .state import AgentState

def decision_node(state: AgentState) -> Literal["search", "report"]:
    """
    Router function that determines the next step based on analysis verdict and loop count.
    """
    is_sufficient = state.get("is_sufficient", False)
    loop_count = state.get("loop_count", 0)
    
    # Safety break to prevent infinite loops (Limit of 2 research loops)
    if loop_count >= 2:
        print(f"Node: Decision | Loop limit reached ({loop_count}). Proceeding to report.")
        return "report"

    if is_sufficient:
        print("Node: Decision | Information is sufficient. Proceeding to report.")
        return "report"
    else:
        print(f"Node: Decision | Information is insufficient. Loop count: {loop_count}. Searching again...")
        return "search"
