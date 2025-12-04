"""
RL-backed policy: Reinforcement learning policy that learns from experience.

This policy uses a simple feature-based approach with preference scores
stored in weights.json. The actual learning is done by the RL trainer.
"""

import json
from pathlib import Path
from typing import Any
from orchestrator.puppeteer.actions import AgentAction, list_all_actions
from orchestrator.puppeteer.policy_base import PuppeteerPolicy
from orchestrator.puppeteer.policy_rule_based import RuleBasedPolicy
from orchestrator.puppeteer.state_adapter import TaskState


def featurize_state(state: TaskState) -> dict[str, Any]:
    """
    Extract features from task state for RL policy.
    
    Features:
    - current_stage (string)
    - has_research (0/1)
    - has_icp (0/1)
    - steps_taken_bucket (low/mid/high)
    - gates_passed_count
    
    Args:
        state: Task state to featurize
        
    Returns:
        Dict of feature values
    """
    # Bucket steps_taken
    steps = state.steps_taken
    if steps <= 3:
        steps_bucket = "low"
    elif steps <= 7:
        steps_bucket = "mid"
    else:
        steps_bucket = "high"
    
    return {
        "current_stage": state.current_stage,
        "has_research": 1 if state.has_research else 0,
        "has_icp": 1 if state.has_icp else 0,
        "steps_taken_bucket": steps_bucket,
        "gates_passed_count": len(state.gates_passed),
    }


def state_to_bucket_key(features: dict[str, Any]) -> str:
    """
    Convert feature dict to a bucket key string.
    
    Args:
        features: Feature dict from featurize_state
        
    Returns:
        Bucket key string (e.g., "stage=deep_research|has_research=1|steps=low")
    """
    parts = [
        f"stage={features['current_stage']}",
        f"has_research={features['has_research']}",
        f"has_icp={features['has_icp']}",
        f"steps={features['steps_taken_bucket']}",
        f"gates={features['gates_passed_count']}",
    ]
    return "|".join(parts)


class RLPolicy:
    """
    RL-backed policy that uses learned preference scores.
    
    Loads weights from orchestrator/data/policy/weights.json and uses them
    to select actions. Falls back to RuleBasedPolicy if weights are missing
    or bucket is unknown.
    """
    
    def __init__(self, config: dict):
        """
        Initialize RL policy.
        
        Args:
            config: Configuration dict with optional:
                - weights_path: Path to weights.json (default: orchestrator/data/policy/weights.json)
                - use_softmax: Whether to use softmax sampling (default: False, use argmax)
        """
        self.config = config
        self.weights_path = Path(config.get(
            "weights_path",
            Path(__file__).resolve().parent.parent / "data" / "policy" / "weights.json"
        ))
        self.use_softmax = config.get("use_softmax", False)
        self.weights = self._load_weights()
        self.fallback_policy = RuleBasedPolicy({})
    
    def _load_weights(self) -> dict[str, dict[str, float]]:
        """
        Load weights from JSON file, or initialize default uniform weights.
        
        Returns:
            Dict mapping bucket_key -> action -> preference_score
        """
        if not self.weights_path.exists():
            # Initialize default uniform weights
            return self._initialize_default_weights()
        
        try:
            with open(self.weights_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Validate structure
            if not isinstance(data, dict):
                return self._initialize_default_weights()
            
            # Ensure all actions are present for each bucket
            all_actions = [action.value for action in list_all_actions()]
            weights = {}
            for bucket_key, action_scores in data.items():
                if not isinstance(action_scores, dict):
                    continue
                # Fill in missing actions with default score
                weights[bucket_key] = {}
                for action_name in all_actions:
                    weights[bucket_key][action_name] = action_scores.get(action_name, 0.0)
            
            return weights
        except (json.JSONDecodeError, IOError):
            return self._initialize_default_weights()
    
    def _initialize_default_weights(self) -> dict[str, dict[str, float]]:
        """
        Initialize default uniform weights (all actions have equal preference).
        
        Returns:
            Empty dict (will be populated on-demand)
        """
        return {}
    
    def _get_bucket_weights(self, bucket_key: str) -> dict[str, float]:
        """
        Get action weights for a bucket, initializing if needed.
        
        Args:
            bucket_key: Bucket key string
            
        Returns:
            Dict mapping action name -> preference score
        """
        if bucket_key not in self.weights:
            # Initialize with uniform weights
            all_actions = list_all_actions()
            self.weights[bucket_key] = {
                action.value: 0.0 for action in all_actions
            }
        
        return self.weights[bucket_key]
    
    def select_next_agent(self, state: TaskState) -> AgentAction:
        """
        Select next action using RL weights.
        
        Args:
            state: Current task state
            
        Returns:
            Next agent action
        """
        # Featurize state
        features = featurize_state(state)
        bucket_key = state_to_bucket_key(features)
        
        # Get weights for this bucket
        action_weights = self._get_bucket_weights(bucket_key)
        
        # If no weights or all zero, fall back to rule-based
        if not action_weights or all(score == 0.0 for score in action_weights.values()):
            return self.fallback_policy.select_next_agent(state)
        
        # Select action
        if self.use_softmax:
            # Softmax sampling (for exploration)
            import math
            exp_scores = {k: math.exp(v) for k, v in action_weights.items()}
            total = sum(exp_scores.values())
            if total > 0:
                probs = {k: v / total for k, v in exp_scores.items()}
                # Sample based on probabilities
                import random
                actions = list(probs.keys())
                probs_list = list(probs.values())
                selected = random.choices(actions, weights=probs_list)[0]
                return AgentAction(selected)
            else:
                # Fallback if all exp scores are zero
                return self.fallback_policy.select_next_agent(state)
        else:
            # Argmax (greedy selection)
            best_action = max(action_weights.items(), key=lambda x: x[1])
            if best_action[1] > 0.0:
                return AgentAction(best_action[0])
            else:
                # All scores are zero or negative, fall back
                return self.fallback_policy.select_next_agent(state)
    
    def save_weights(self) -> None:
        """
        Save current weights to JSON file.
        
        Creates directory if it doesn't exist.
        """
        self.weights_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.weights_path, "w", encoding="utf-8") as f:
            json.dump(self.weights, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved RL weights to {self.weights_path}")

