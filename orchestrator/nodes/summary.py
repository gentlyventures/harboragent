"""
Summary node: Save run state and generate final summary.
"""

from orchestrator.state import State, save_run_state


def summary_node(state: State) -> State:
    """
    Summary node: Save run state to JSON file.
    
    Args:
        state: Current graph state
        
    Returns:
        State (unchanged, but persisted)
    """
    save_run_state(state)
    
    print(f"✅ Summary: Run {state['run_id']} completed")
    
    return state

