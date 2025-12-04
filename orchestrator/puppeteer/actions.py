"""
Agent action definitions for Puppeteer-style orchestration.

Defines the set of actions that agents can take in the orchestration loop.
This module is generic and project-agnostic.
"""

from enum import Enum
from typing import Literal


class AgentAction(str, Enum):
    """Enumeration of available agent actions."""
    
    INTAKE = "INTAKE"
    RESEARCH = "RESEARCH"
    ICP_ANALYSIS = "ICP_ANALYSIS"
    EVALUATE = "EVALUATE"
    DESIGN_SPEC = "DESIGN_SPEC"
    BUILD_CODE = "BUILD_CODE"
    TEST = "TEST"
    DEPLOY = "DEPLOY"
    PUBLISH = "PUBLISH"
    STOP = "STOP"
    
    def __str__(self) -> str:
        return self.value


def list_all_actions() -> list[AgentAction]:
    """
    Get a list of all available agent actions.
    
    Returns:
        List of all AgentAction values
    """
    return list(AgentAction)


def is_terminal(action: AgentAction) -> bool:
    """
    Check if an action is terminal (ends the orchestration loop).
    
    Args:
        action: The action to check
        
    Returns:
        True if the action is terminal, False otherwise
    """
    return action == AgentAction.STOP

