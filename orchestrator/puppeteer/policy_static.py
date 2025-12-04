"""
Static policy: Fixed sequence based on current stage.

This policy mimics the existing fixed graph behavior by advancing through
a predefined sequence based on the current_stage field.
"""

from orchestrator.puppeteer.actions import AgentAction
from orchestrator.puppeteer.policy_base import PuppeteerPolicy
from orchestrator.puppeteer.state_adapter import TaskState


class StaticPolicy:
    """
    Static policy that follows a fixed sequence based on current stage.
    
    This is a minimal stub that provides baseline behavior for comparison
    with dynamic policies. It maps current_stage to the next action in a
    fixed sequence.
    """
    
    # Stage to action mapping (fixed sequence)
    STAGE_TO_ACTION = {
        "idea": AgentAction.INTAKE,
        "validation": AgentAction.EVALUATE,
        "scoring": AgentAction.EVALUATE,
        "deep_dive": AgentAction.RESEARCH,
        "build": AgentAction.BUILD_CODE,
        "published": AgentAction.PUBLISH,
    }
    
    def __init__(self, config: dict):
        """
        Initialize static policy.
        
        Args:
            config: Configuration dict (unused for static policy)
        """
        self.config = config
    
    def select_next_agent(self, state: TaskState) -> AgentAction:
        """
        Select next action based on current stage (fixed sequence).
        
        Args:
            state: Current task state
            
        Returns:
            Next agent action
        """
        current_stage = state.current_stage
        
        # If we have a direct mapping, use it
        if current_stage in self.STAGE_TO_ACTION:
            return self.STAGE_TO_ACTION[current_stage]
        
        # Default progression logic
        if current_stage == "idea":
            return AgentAction.INTAKE
        elif current_stage == "validation":
            return AgentAction.EVALUATE
        elif current_stage == "scoring":
            return AgentAction.EVALUATE
        elif current_stage == "deep_dive":
            if not state.has_research:
                return AgentAction.RESEARCH
            else:
                return AgentAction.STOP
        elif current_stage == "build":
            return AgentAction.BUILD_CODE
        elif current_stage == "published":
            return AgentAction.STOP
        else:
            # Unknown stage, stop
            return AgentAction.STOP

