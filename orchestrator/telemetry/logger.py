"""
Orchestration logger: Logs runs and steps to JSONL files.

Logs are written to:
- orchestrator/data/logs/runs.jsonl (run-level events)
- orchestrator/data/logs/steps.jsonl (step-level events)
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from orchestrator.puppeteer.actions import AgentAction
    from orchestrator.puppeteer.state_adapter import TaskState


class OrchestratorLogger:
    """
    Logger for orchestration runs and steps.
    
    Writes structured logs to JSONL files for later analysis and training.
    """
    
    def __init__(
        self,
        runs_log_path: str | Path | None = None,
        steps_log_path: str | Path | None = None
    ):
        """
        Initialize logger with log file paths.
        
        Args:
            runs_log_path: Path to runs.jsonl (default: orchestrator/data/logs/runs.jsonl)
            steps_log_path: Path to steps.jsonl (default: orchestrator/data/logs/steps.jsonl)
        """
        if runs_log_path is None:
            runs_log_path = (
                Path(__file__).resolve().parent.parent / "data" / "logs" / "runs.jsonl"
            )
        if steps_log_path is None:
            steps_log_path = (
                Path(__file__).resolve().parent.parent / "data" / "logs" / "steps.jsonl"
            )
        
        self.runs_log_path = Path(runs_log_path)
        self.steps_log_path = Path(steps_log_path)
        
        # Ensure directories exist
        self.runs_log_path.parent.mkdir(parents=True, exist_ok=True)
        self.steps_log_path.parent.mkdir(parents=True, exist_ok=True)
    
    def start_run(
        self,
        run_id: str,
        pack_slug: str,
        policy_mode: str,
        extra: dict[str, Any] | None = None
    ) -> None:
        """
        Log the start of a run.
        
        Args:
            run_id: Run identifier
            pack_slug: Pack slug
            policy_mode: Policy mode used
            extra: Optional extra metadata
        """
        record = {
            "event": "run_start",
            "run_id": run_id,
            "pack_slug": pack_slug,
            "policy_mode": policy_mode,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "metadata": extra or {},
        }
        
        self._append_jsonl(self.runs_log_path, record)
    
    def log_step(
        self,
        run_id: str,
        step_index: int,
        action: "AgentAction",
        state: "TaskState",
        tokens_used: int,
        local_reward: float
    ) -> None:
        """
        Log a step execution.
        
        Args:
            run_id: Run identifier
            step_index: Step index (0-based)
            action: Action taken
            state: State after action
            tokens_used: Tokens used in this step
            local_reward: Reward for this step
        """
        # Import here to avoid circular dependency
        from orchestrator.puppeteer.actions import AgentAction
        from orchestrator.puppeteer.state_adapter import TaskState
        
        record = {
            "event": "step",
            "run_id": run_id,
            "step_index": step_index,
            "action": action.value,
            "state": {
                "current_stage": state.current_stage,
                "has_research": state.has_research,
                "has_icp": state.has_icp,
                "gates_passed": state.gates_passed,
                "steps_taken": state.steps_taken,
                "tokens_used": state.tokens_used,
            },
            "tokens_used": tokens_used,
            "local_reward": local_reward,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
        
        self._append_jsonl(self.steps_log_path, record)
    
    def end_run(
        self,
        run_id: str,
        final_reward: float,
        success: bool,
        steps_taken: int,
        extra: dict[str, Any] | None = None
    ) -> None:
        """
        Log the end of a run.
        
        Args:
            run_id: Run identifier
            final_reward: Final episode reward
            success: Whether run was successful
            steps_taken: Total steps taken
            extra: Optional extra metadata
        """
        record = {
            "event": "run_end",
            "run_id": run_id,
            "final_reward": final_reward,
            "success": success,
            "steps_taken": steps_taken,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "metadata": extra or {},
        }
        
        self._append_jsonl(self.runs_log_path, record)
    
    def _append_jsonl(self, path: Path, record: dict) -> None:
        """
        Append a JSON record to a JSONL file.
        
        Args:
            path: Path to JSONL file
            record: Record dict to append
        """
        with open(path, "a", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False)
            f.write("\n")

