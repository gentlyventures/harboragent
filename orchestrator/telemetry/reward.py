"""
Reward shaping functions for Puppeteer orchestration.

Defines reward computation for steps and episodes to guide RL training.
"""

from dataclasses import dataclass
from orchestrator.puppeteer.state_adapter import TaskState


@dataclass
class RewardConfig:
    """Configuration for reward computation."""
    success_weight: float = 1.0
    token_penalty: float = 0.0001
    step_penalty: float = 0.01
    gate_bonus: float = 0.1


def default_reward_config() -> RewardConfig:
    """
    Get default reward configuration.
    
    Returns:
        Default RewardConfig instance
    """
    return RewardConfig()


def compute_step_reward(
    state_before: TaskState,
    state_after: TaskState,
    tokens_used: int,
    config: RewardConfig
) -> float:
    """
    Compute reward for a single step.
    
    Args:
        state_before: State before action
        state_after: State after action
        tokens_used: Tokens used in this step
        config: Reward configuration
        
    Returns:
        Step reward (float)
    """
    reward = 0.0
    
    # Penalty for token usage
    reward -= config.token_penalty * tokens_used
    
    # Small penalty for each step
    reward -= config.step_penalty
    
    # Bonus for milestones reached
    if not state_before.has_research and state_after.has_research:
        reward += 0.2  # Research completed
    
    if not state_before.has_icp and state_after.has_icp:
        reward += 0.1  # ICP analysis completed
    
    # Bonus for gates passed
    new_gates = set(state_after.gates_passed) - set(state_before.gates_passed)
    if new_gates:
        reward += config.gate_bonus * len(new_gates)
    
    return reward


def compute_episode_reward(
    run_summary: dict,
    config: RewardConfig
) -> float:
    """
    Compute final reward for an episode (run).
    
    Args:
        run_summary: Run summary dict with:
            - steps_taken: int
            - tokens_used: int
            - final_state: dict with current_stage, has_research, has_icp, gates_passed
        config: Reward configuration
        
    Returns:
        Episode reward (float)
    """
    reward = 0.0
    
    # Success bonus
    final_state = run_summary.get("final_state", {})
    if final_state.get("current_stage") == "published":
        reward += config.success_weight
    elif len(final_state.get("gates_passed", [])) >= 3:
        reward += config.success_weight * 0.5  # Partial success
    
    # Penalties
    tokens_used = run_summary.get("tokens_used", 0)
    reward -= config.token_penalty * tokens_used
    
    steps_taken = run_summary.get("steps_taken", 0)
    reward -= config.step_penalty * steps_taken
    
    # Gate bonuses
    gates_passed = final_state.get("gates_passed", [])
    reward += config.gate_bonus * len(gates_passed)
    
    return reward

