"""
Orchestrator state model for LangGraph workflow.

Defines the state structure for a single orchestrator run.
"""

import json
import uuid
from pathlib import Path
from typing import TypedDict, Optional

from pydantic import BaseModel, Field


class Scores(BaseModel):
    """Scoring metrics for pack validation."""
    viability: Optional[int] = Field(None, ge=0, le=100)
    data_availability: Optional[int] = Field(None, ge=0, le=100)
    icp_clarity: Optional[int] = Field(None, ge=0, le=100)


class Gate(BaseModel):
    """Gate decisions for workflow control."""
    validation: Optional[str] = Field(None, pattern="^(pass|fail)$")
    scoring: Optional[str] = Field(None, pattern="^(pass|soft_fail_retry|hard_fail)$")


class Artifacts(BaseModel):
    """Artifacts generated during the run."""
    deep_dive_report_path: Optional[str] = None


class Notes(BaseModel):
    """Notes and rationales generated during the run."""
    validation_rationale: Optional[str] = None
    scoring_rationale: Optional[str] = None
    deep_dive_summary: Optional[str] = None


class State(TypedDict):
    """LangGraph state for orchestrator run."""
    run_id: str
    pack_slug: str
    pack_snapshot: dict
    scores: dict
    gate: dict
    artifacts: dict
    notes: dict


def new_run_state(pack_slug: str, pack_snapshot: dict) -> State:
    """
    Create a new run state with initial values.
    
    Args:
        pack_slug: The pack slug identifier
        pack_snapshot: Snapshot of PackLifecycle dict at start
        
    Returns:
        Initial State dict
    """
    run_id = str(uuid.uuid4())
    
    return {
        "run_id": run_id,
        "pack_slug": pack_slug,
        "pack_snapshot": pack_snapshot,
        "scores": {
            "viability": None,
            "data_availability": None,
            "icp_clarity": None,
        },
        "gate": {
            "validation": None,
            "scoring": None,
        },
        "artifacts": {
            "deep_dive_report_path": None,
        },
        "notes": {
            "validation_rationale": None,
            "scoring_rationale": None,
            "deep_dive_summary": None,
        },
    }


def save_run_state(state: State, runs_dir: Optional[Path] = None) -> None:
    """
    Save run state to JSON file.
    
    Args:
        state: The state dict to save
        runs_dir: Optional directory for runs (defaults to orchestrator/data/runs)
    """
    if runs_dir is None:
        # Default to orchestrator/data/runs relative to this file
        runs_dir = Path(__file__).resolve().parent / "data" / "runs"
    
    runs_dir.mkdir(parents=True, exist_ok=True)
    
    run_id = state["run_id"]
    output_file = runs_dir / f"{run_id}.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Run state saved to: {output_file}")

