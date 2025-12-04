"""
Reward shaping functions for Puppeteer orchestration.

Defines reward computation for steps and episodes to guide RL training.
"""

import json
from dataclasses import dataclass
from pathlib import Path
from orchestrator.puppeteer.state_adapter import TaskState


@dataclass
class RewardConfig:
    """Configuration for reward computation."""
    success_weight: float = 1.0
    token_penalty: float = 0.0001
    step_penalty: float = 0.01
    gate_bonus: float = 0.1
    crm_sale_bonus: float = 0.5
    crm_pipeline_bonus: float = 0.1


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


def load_sales_for_pack(pack_slug: str) -> int:
    """
    Load sales count for a pack from revenue/data/sales.json.
    
    Args:
        pack_slug: Pack slug identifier
        
    Returns:
        Number of sales for this pack (0 if file doesn't exist or no sales)
    """
    # Path to sales.json (relative to project root)
    revenue_data_path = Path(__file__).resolve().parent.parent.parent / "revenue" / "data"
    sales_json = revenue_data_path / "sales.json"
    
    if not sales_json.exists():
        return 0
    
    try:
        with open(sales_json, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Handle both {"sales": [...]} and just a list
        sales_list = data.get("sales", []) if isinstance(data, dict) else data
        
        if not isinstance(sales_list, list):
            return 0
        
        # Count sales matching this pack_slug
        count = 0
        for sale in sales_list:
            if isinstance(sale, dict):
                # Try multiple possible field names
                sale_pack = sale.get("packSlug") or sale.get("pack_slug") or sale.get("pack")
                if sale_pack == pack_slug:
                    count += 1
        
        return count
    except (json.JSONDecodeError, FileNotFoundError, KeyError, AttributeError):
        # Fail gracefully - treat as 0 sales
        return 0


def load_pipeline_stage_for_pack(pack_slug: str) -> str | None:
    """
    Load the most advanced pipeline stage for a pack from revenue/data/master_leads.json.
    
    Args:
        pack_slug: Pack slug identifier
        
    Returns:
        Pipeline stage string ("prospect", "engaged", "qualified", "proposal", "purchased")
        or None if not found or file doesn't exist
    """
    # Path to master_leads.json (relative to project root)
    revenue_data_path = Path(__file__).resolve().parent.parent.parent / "revenue" / "data"
    leads_json = revenue_data_path / "master_leads.json"
    
    if not leads_json.exists():
        return None
    
    try:
        with open(leads_json, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Handle both {"leads": [...]} and just a list
        leads_list = data.get("leads", []) if isinstance(data, dict) else data
        
        if not isinstance(leads_list, list):
            return None
        
        # Stage priority mapping (higher = more advanced)
        stage_priority = {
            "purchased": 5,
            "proposal": 4,
            "qualified": 3,
            "engaged": 2,
            "prospect": 1,
        }
        
        # Find most advanced stage
        max_priority = 0
        most_advanced_stage = None
        
        for lead in leads_list:
            if not isinstance(lead, dict):
                continue
            
            # Try to find pack association
            lead_pack = lead.get("packSlug") or lead.get("pack_slug") or lead.get("pack")
            
            # If no explicit pack field, try to infer from ICP or skip
            if not lead_pack:
                # Could try inferring from ICP or other fields, but for now skip
                continue
            
            if lead_pack != pack_slug:
                continue
            
            # Try to extract stage from various possible field names
            stage = (
                lead.get("stage")
                or lead.get("pipelineStage")
                or lead.get("pipeline_stage")
                or lead.get("status")
                or lead.get("leadStatus")
            )
            
            if not stage:
                continue
            
            # Normalize stage name to lowercase
            stage_lower = str(stage).lower()
            
            # Check if it matches known stages
            for known_stage, priority in stage_priority.items():
                if known_stage in stage_lower or stage_lower == known_stage:
                    if priority > max_priority:
                        max_priority = priority
                        most_advanced_stage = known_stage
                    break
        
        return most_advanced_stage
    except (json.JSONDecodeError, FileNotFoundError, KeyError, AttributeError):
        # Fail gracefully - treat as None
        return None


def compute_episode_reward(
    run_summary: dict,
    config: RewardConfig
) -> float:
    """
    Compute final reward for an episode (run).
    
    Args:
        run_summary: Run summary dict with:
            - pack_slug: str
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
    
    # CRM-aware rewards
    pack_slug = run_summary.get("pack_slug")
    if pack_slug:
        # Sales bonus
        sale_count = load_sales_for_pack(pack_slug)
        if sale_count > 0:
            reward += config.crm_sale_bonus * min(sale_count, 5)  # Cap at 5x bonus
        
        # Pipeline stage bonus
        stage = load_pipeline_stage_for_pack(pack_slug)
        if stage:
            stage_multipliers = {
                "proposal": 3,
                "purchased": 3,
                "qualified": 2,
                "engaged": 1,
            }
            multiplier = stage_multipliers.get(stage, 0)
            reward += config.crm_pipeline_bonus * multiplier
    
    return reward

