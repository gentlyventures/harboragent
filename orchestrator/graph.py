"""
LangGraph workflow definition for pack research pipeline.

Defines the graph: intake -> validation -> scoring_gate -> deep_research -> summary
with conditional branching for deep_research (only if scoring gate passes).
"""

from langgraph.graph import StateGraph, END
from orchestrator.state import State, new_run_state
from orchestrator.config import get_pack_lifecycle
from orchestrator.nodes import (
    intake_node,
    validation_node,
    scoring_gate_node,
    deep_research_node,
    summary_node,
)


def should_run_deep_research(state: State) -> str:
    """
    Conditional function: determine if deep_research should run.
    
    Args:
        state: Current graph state
        
    Returns:
        "continue" if scoring gate passed, "skip" otherwise
    """
    gate_scoring = state.get("gate", {}).get("scoring")
    
    if gate_scoring == "pass":
        return "continue"
    else:
        return "skip"


def build_graph() -> StateGraph:
    """
    Build the LangGraph workflow graph.
    
    Graph structure:
    - intake_node
    - validation_node
    - scoring_gate_node
    - conditional: should_run_deep_research
      - if "continue": deep_research_node -> summary_node
      - if "skip": summary_node (direct)
    - summary_node
    
    Returns:
        Configured StateGraph
    """
    # Create graph
    workflow = StateGraph(State)
    
    # Add nodes
    workflow.add_node("intake", intake_node)
    workflow.add_node("validation", validation_node)
    workflow.add_node("scoring_gate", scoring_gate_node)
    workflow.add_node("deep_research", deep_research_node)
    workflow.add_node("summary", summary_node)
    
    # Define edges
    workflow.set_entry_point("intake")
    workflow.add_edge("intake", "validation")
    workflow.add_edge("validation", "scoring_gate")
    
    # Conditional edge: only run deep_research if scoring gate passes
    workflow.add_conditional_edges(
        "scoring_gate",
        should_run_deep_research,
        {
            "continue": "deep_research",
            "skip": "summary",
        }
    )
    
    # Deep research leads to summary
    workflow.add_edge("deep_research", "summary")
    
    # Summary is the end
    workflow.add_edge("summary", END)
    
    return workflow


def run_pack_research(pack_slug: str) -> State:
    """
    Run the complete pack research pipeline for a given pack.
    
    Steps:
    1. Load pack lifecycle to build initial snapshot
    2. Create initial state
    3. Run the graph
    4. Return final state
    
    Args:
        pack_slug: Pack slug identifier
        
    Returns:
        Final state after graph execution
        
    Raises:
        ValueError: If pack not found
    """
    # Load pack lifecycle once to build snapshot
    pack_lifecycle = get_pack_lifecycle(pack_slug)
    
    if pack_lifecycle is None:
        raise ValueError(
            f"Pack with slug '{pack_slug}' not found in pack-crm/data/packs.json"
        )
    
    # Create initial state
    initial_state = new_run_state(pack_slug, pack_lifecycle)
    
    print(f"🚀 Starting research pipeline for pack: {pack_slug}")
    print(f"   Run ID: {initial_state['run_id']}")
    print()
    
    # Build and compile graph
    graph = build_graph()
    app = graph.compile()
    
    # Run the graph
    final_state = app.invoke(initial_state)
    
    print()
    print("=" * 60)
    print("Pipeline Complete")
    print("=" * 60)
    print(f"Run ID: {final_state['run_id']}")
    print(f"Pack: {pack_slug}")
    print(f"Scoring Gate: {final_state['gate'].get('scoring', 'N/A')}")
    
    if final_state["artifacts"].get("deep_dive_report_path"):
        print(f"Report: {final_state['artifacts']['deep_dive_report_path']}")
    
    print()
    
    return final_state

