"""
Scoring gate node: Apply deterministic rules to determine if pack passes scoring gate.
"""

from datetime import datetime
from orchestrator.config import update_pack_lifecycle
from orchestrator.state import State


def scoring_gate_node(state: State) -> State:
    """
    Scoring gate node: Apply rules to determine scoring gate outcome.
    
    Rules:
    - If viability >= 70 AND data_availability >= 60: gate.scoring = "pass"
    - Else if viability >= 50: gate.scoring = "soft_fail_retry"
    - Else: gate.scoring = "hard_fail"
    
    Updates pack lifecycle:
    - stages.scoring.status = "completed"
    - crm.gateDecisionNotes.scoring
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with gate.scoring set
    """
    scores = state["scores"]
    pack_slug = state["pack_slug"]
    
    viability = scores.get("viability")
    data_availability = scores.get("data_availability")
    
    if viability is None or data_availability is None:
        raise ValueError("Viability and data_availability scores must be set before scoring gate")
    
    # Apply deterministic rules
    if viability >= 70 and data_availability >= 60:
        gate_outcome = "pass"
        rationale = (
            f"Passed scoring gate with viability {viability} and data availability {data_availability}. "
            "Scores meet thresholds for proceeding to deep research."
        )
    elif viability >= 50:
        gate_outcome = "soft_fail_retry"
        rationale = (
            f"Soft fail: Viability {viability} is moderate but data availability {data_availability} "
            "is below threshold. May retry after improving data sources or refining idea."
        )
    else:
        gate_outcome = "hard_fail"
        rationale = (
            f"Hard fail: Viability {viability} is below threshold. "
            "Pack idea needs significant refinement before proceeding."
        )
    
    state["gate"]["scoring"] = gate_outcome
    state["notes"]["scoring_rationale"] = rationale
    
    # Update pack lifecycle
    now = datetime.utcnow().isoformat() + "Z"
    
    def update_pack(pack: dict) -> dict:
        # Update scoring stage
        stages = pack.get("stages", {})
        scoring_stage = stages.get("scoring", {})
        scoring_stage["status"] = "completed"
        scoring_stage["score"] = viability  # Store viability as the primary score
        scoring_stage["gate"] = "pass" if gate_outcome == "pass" else "fail"
        if not scoring_stage.get("startedAt"):
            scoring_stage["startedAt"] = now
        scoring_stage["completedAt"] = now
        stages["scoring"] = scoring_stage
        pack["stages"] = stages
        
        # Update CRM gate decision notes
        crm = pack.get("crm", {})
        gate_notes = crm.get("gateDecisionNotes", {})
        gate_notes["scoring"] = rationale
        crm["gateDecisionNotes"] = gate_notes
        pack["crm"] = crm
        
        # Update metadata timestamp
        metadata = pack.get("metadata", {})
        metadata["updatedAt"] = now
        pack["metadata"] = metadata
        
        return pack
    
    update_pack_lifecycle(pack_slug, update_pack)
    
    print(f"✅ Scoring Gate: {gate_outcome.upper()}")
    print(f"   Rationale: {rationale}")
    
    return state

