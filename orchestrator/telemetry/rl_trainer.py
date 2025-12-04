"""
Simple REINFORCE-style RL trainer for Puppeteer policies.

Loads logs, computes returns, and updates policy weights.
"""

import json
from pathlib import Path
from typing import Any
from orchestrator.telemetry.logger import OrchestratorLogger
from orchestrator.telemetry.reward import compute_episode_reward, default_reward_config
from orchestrator.puppeteer.policy_rl import RLPolicy, featurize_state, state_to_bucket_key
from orchestrator.puppeteer.state_adapter import TaskState


class RunRecord:
    """Record from runs.jsonl."""
    def __init__(self, data: dict):
        self.event = data.get("event")
        self.run_id = data.get("run_id")
        self.pack_slug = data.get("pack_slug")
        self.policy_mode = data.get("policy_mode")
        self.timestamp = data.get("timestamp")
        self.final_reward = data.get("final_reward")
        self.success = data.get("success")
        self.steps_taken = data.get("steps_taken")
        self.metadata = data.get("metadata", {})


class StepRecord:
    """Record from steps.jsonl."""
    def __init__(self, data: dict):
        self.event = data.get("event")
        self.run_id = data.get("run_id")
        self.step_index = data.get("step_index")
        self.action = data.get("action")
        self.state = data.get("state", {})
        self.tokens_used = data.get("tokens_used", 0)
        self.local_reward = data.get("local_reward", 0.0)
        self.timestamp = data.get("timestamp")


def load_run_and_step_logs(
    runs_log_path: Path | None = None,
    steps_log_path: Path | None = None
) -> tuple[list[RunRecord], list[StepRecord]]:
    """
    Load run and step logs from JSONL files.
    
    Args:
        runs_log_path: Path to runs.jsonl
        steps_log_path: Path to steps.jsonl
        
    Returns:
        Tuple of (list of RunRecord, list of StepRecord)
    """
    if runs_log_path is None:
        runs_log_path = (
            Path(__file__).resolve().parent.parent / "data" / "logs" / "runs.jsonl"
        )
    if steps_log_path is None:
        steps_log_path = (
            Path(__file__).resolve().parent.parent / "data" / "logs" / "steps.jsonl"
        )
    
    runs_log_path = Path(runs_log_path)
    steps_log_path = Path(steps_log_path)
    
    run_records = []
    step_records = []
    
    # Load runs
    if runs_log_path.exists():
        with open(runs_log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        data = json.loads(line)
                        run_records.append(RunRecord(data))
                    except json.JSONDecodeError:
                        continue
    
    # Load steps
    if steps_log_path.exists():
        with open(steps_log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        data = json.loads(line)
                        step_records.append(StepRecord(data))
                    except json.JSONDecodeError:
                        continue
    
    return run_records, step_records


class SimpleRLTrainer:
    """
    Simple REINFORCE-style RL trainer.
    
    Trains policy weights by:
    1. Loading logs
    2. Computing episode rewards
    3. Updating action preferences based on returns
    """
    
    def __init__(
        self,
        learning_rate: float = 0.01,
        weights_path: Path | None = None
    ):
        """
        Initialize RL trainer.
        
        Args:
            learning_rate: Learning rate for weight updates
            weights_path: Path to weights.json (default: orchestrator/data/policy/weights.json)
        """
        self.learning_rate = learning_rate
        
        if weights_path is None:
            weights_path = (
                Path(__file__).resolve().parent.parent / "data" / "policy" / "weights.json"
            )
        self.weights_path = Path(weights_path)
        
        # Initialize policy to access weights
        self.policy = RLPolicy({"weights_path": str(self.weights_path)})
        self.reward_config = default_reward_config()
    
    def train_from_logs(self, max_runs: int | None = None) -> dict:
        """
        Train policy from logs.
        
        Args:
            max_runs: Maximum number of runs to process (None = all)
            
        Returns:
            Training summary dict with:
            - total_runs: int
            - avg_reward: float
            - updated_buckets: int
        """
        # Load logs
        run_records, step_records = load_run_and_step_logs()
        
        # Filter to run_end events only
        completed_runs = [
            r for r in run_records
            if r.event == "run_end" and r.final_reward is not None
        ]
        
        # Sort by timestamp (most recent first)
        completed_runs.sort(key=lambda x: x.timestamp or "", reverse=True)
        
        # Limit runs
        if max_runs is not None:
            completed_runs = completed_runs[:max_runs]
        
        total_runs = len(completed_runs)
        if total_runs == 0:
            return {
                "total_runs": 0,
                "avg_reward": 0.0,
                "updated_buckets": 0,
                "message": "No completed runs found in logs",
            }
        
        # Group steps by run_id
        steps_by_run: dict[str, list[StepRecord]] = {}
        for step in step_records:
            if step.event == "step":
                run_id = step.run_id
                if run_id not in steps_by_run:
                    steps_by_run[run_id] = []
                steps_by_run[run_id].append(step)
        
        # Sort steps within each run by step_index
        for run_id in steps_by_run:
            steps_by_run[run_id].sort(key=lambda x: x.step_index)
        
        # Process each run
        total_reward = 0.0
        updated_buckets = set()
        
        for run_record in completed_runs:
            run_id = run_record.run_id
            episode_reward = run_record.final_reward
            
            total_reward += episode_reward
            
            # Get steps for this run
            steps = steps_by_run.get(run_id, [])
            
            # Update weights for each step
            for step in steps:
                # Reconstruct state from step record
                state_data = step.state
                state = TaskState(
                    run_id=run_id,
                    pack_slug="",  # Not needed for featurization
                    current_stage=state_data.get("current_stage", "idea"),
                    has_research=state_data.get("has_research", False),
                    has_icp=state_data.get("has_icp", False),
                    gates_passed=state_data.get("gates_passed", []),
                    steps_taken=state_data.get("steps_taken", 0),
                    tokens_used=state_data.get("tokens_used", 0),
                )
                
                # Featurize and get bucket
                features = featurize_state(state)
                bucket_key = state_to_bucket_key(features)
                
                # Get action
                action_name = step.action
                
                # Update weight for this action in this bucket
                bucket_weights = self.policy._get_bucket_weights(bucket_key)
                old_weight = bucket_weights.get(action_name, 0.0)
                new_weight = old_weight + self.learning_rate * episode_reward
                bucket_weights[action_name] = new_weight
                
                # Store in policy weights
                self.policy.weights[bucket_key] = bucket_weights
                updated_buckets.add(bucket_key)
        
        # Save updated weights
        self.policy.save_weights()
        
        avg_reward = total_reward / total_runs if total_runs > 0 else 0.0
        
        return {
            "total_runs": total_runs,
            "avg_reward": avg_reward,
            "updated_buckets": len(updated_buckets),
            "message": f"Trained on {total_runs} runs, updated {len(updated_buckets)} buckets",
        }

