"""
Intake node: Load pack lifecycle and initialize state.
"""

from orchestrator.config import get_pack_lifecycle
from orchestrator.state import State


def intake_node(state: State) -> State:
    """
    Intake node: Ensure state has run_id and pack_slug, load pack lifecycle.
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with pack_snapshot
        
    Raises:
        ValueError: If pack not found
    """
    pack_slug = state.get("pack_slug")
    
    if not pack_slug:
        raise ValueError("pack_slug is required in state")
    
    # Load pack lifecycle
    pack_lifecycle = get_pack_lifecycle(pack_slug)
    
    if pack_lifecycle is None:
        raise ValueError(
            f"Pack with slug '{pack_slug}' not found in pack-crm/data/packs.json"
        )
    
    # Attach pack snapshot to state
    state["pack_snapshot"] = pack_lifecycle
    
    print(f"✅ Intake: Loaded pack '{pack_slug}' (Pack #{pack_lifecycle.get('packNumber', '?')})")
    
    return state

