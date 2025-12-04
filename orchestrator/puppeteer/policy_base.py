"""
Base policy interface and factory for Puppeteer orchestration.

Defines the Policy protocol and factory function for creating policy instances.
"""

from typing import Protocol, Literal
from orchestrator.puppeteer.actions import AgentAction
from orchestrator.puppeteer.state_adapter import TaskState


PolicyMode = Literal["static", "rule", "rl"]


class PuppeteerPolicy(Protocol):
    """
    Protocol for Puppeteer policy implementations.
    
    Policies decide which agent action to take next based on the current task state.
    """
    
    def select_next_agent(self, state: TaskState) -> AgentAction:
        """
        Select the next agent action based on the current state.
        
        Args:
            state: Current task state
            
        Returns:
            Next agent action to execute
        """
        ...


def make_policy(mode: PolicyMode, config: dict | None = None) -> PuppeteerPolicy:
    """
    Factory function to create a policy instance.
    
    Args:
        mode: Policy mode ("static", "rule", or "rl")
        config: Optional configuration dict for the policy
        
    Returns:
        Policy instance implementing PuppeteerPolicy
        
    Raises:
        ValueError: If mode is not recognized
    """
    if mode == "static":
        from orchestrator.puppeteer.policy_static import StaticPolicy
        return StaticPolicy(config or {})
    elif mode == "rule":
        from orchestrator.puppeteer.policy_rule_based import RuleBasedPolicy
        return RuleBasedPolicy(config or {})
    elif mode == "rl":
        from orchestrator.puppeteer.policy_rl import RLPolicy
        return RLPolicy(config or {})
    else:
        raise ValueError(f"Unknown policy mode: {mode}")

