"""
State adapter for converting between Harbor pack lifecycle and generic TaskState.

This module provides Harbor-specific adapters that convert between:
- Harbor pack lifecycle dicts (from pack-crm/data/packs.json)
- Generic TaskState (used by Puppeteer core)

The core Puppeteer modules should not import Harbor-specific models directly.
"""

from typing import Any
from pydantic import BaseModel, Field


class TaskState(BaseModel):
    """
    Generic task state model for Puppeteer orchestration.
    
    This is a portable state representation that can be adapted to any project
    by implementing project-specific adapters (like harbor_pack_to_task_state).
    """
    run_id: str
    pack_slug: str
    current_stage: str
    has_research: bool = False
    has_icp: bool = False
    gates_passed: list[str] = Field(default_factory=list)
    steps_taken: int = 0
    tokens_used: int = 0
    metadata: dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        """Pydantic config."""
        extra = "allow"  # Allow extra fields for extensibility


def harbor_pack_to_task_state(pack_lifecycle: dict, run_context: dict) -> TaskState:
    """
    Convert Harbor pack lifecycle dict to generic TaskState.
    
    Extracts relevant fields from the pack lifecycle structure:
    - currentStage -> current_stage
    - research.researchCompleted -> has_research
    - crm.icpSummary -> has_icp (if non-empty)
    - gates_passed from stage statuses or gate decisions
    - steps_taken and tokens_used from run_context
    
    Args:
        pack_lifecycle: Pack lifecycle dict from pack-crm/data/packs.json
        run_context: Run context dict with steps_taken, tokens_used, etc.
        
    Returns:
        TaskState instance
    """
    # Extract current stage
    current_stage = pack_lifecycle.get("currentStage", "idea")
    
    # Check if research is completed
    research = pack_lifecycle.get("research", {})
    has_research = research.get("researchCompleted", False)
    
    # Check if ICP analysis exists
    crm = pack_lifecycle.get("crm", {})
    icp_summary = crm.get("icpSummary", "")
    has_icp = bool(icp_summary and icp_summary.strip())
    
    # Extract gates passed from stages or gate decision notes
    gates_passed = []
    stages = pack_lifecycle.get("stages", {})
    for stage_name, stage_data in stages.items():
        if isinstance(stage_data, dict) and stage_data.get("status") == "completed":
            gates_passed.append(stage_name)
    
    # Also check gate decision notes
    gate_notes = crm.get("gateDecisionNotes", {})
    for gate_name in gate_notes.keys():
        if gate_name not in gates_passed:
            gates_passed.append(gate_name)
    
    # Extract steps and tokens from run_context
    steps_taken = run_context.get("steps_taken", 0)
    tokens_used = run_context.get("tokens_used", 0)
    
    # Store extra Harbor-specific info in metadata
    metadata = {
        "pack_number": pack_lifecycle.get("packNumber"),
        "pack_name": pack_lifecycle.get("name"),
        "regulation_name": pack_lifecycle.get("metadata", {}).get("regulationName"),
        "target_audience": pack_lifecycle.get("metadata", {}).get("targetAudience", []),
        "stages": stages,
        "crm": crm,
        "research": research,
    }
    
    return TaskState(
        run_id=run_context.get("run_id", ""),
        pack_slug=pack_lifecycle.get("slug", ""),
        current_stage=current_stage,
        has_research=has_research,
        has_icp=has_icp,
        gates_passed=gates_passed,
        steps_taken=steps_taken,
        tokens_used=tokens_used,
        metadata=metadata,
    )


def update_states_from_action(
    prev_state: TaskState,
    new_pack_lifecycle: dict,
    new_run_context: dict
) -> TaskState:
    """
    Update TaskState after executing an action.
    
    Creates a new TaskState reflecting changes from the action execution.
    
    Args:
        prev_state: Previous TaskState
        new_pack_lifecycle: Updated pack lifecycle dict
        new_run_context: Updated run context dict
        
    Returns:
        Updated TaskState
    """
    # Rebuild state from updated pack lifecycle
    new_state = harbor_pack_to_task_state(new_pack_lifecycle, new_run_context)
    
    # Preserve run_id and pack_slug from previous state if not in new context
    if not new_state.run_id:
        new_state.run_id = prev_state.run_id
    if not new_state.pack_slug:
        new_state.pack_slug = prev_state.pack_slug
    
    # Increment steps_taken
    new_state.steps_taken = prev_state.steps_taken + 1
    
    # Accumulate tokens
    new_state.tokens_used = prev_state.tokens_used + new_run_context.get("tokens_used", 0)
    
    return new_state

