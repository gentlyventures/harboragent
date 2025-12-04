"""
Puppeteer-style dynamic multi-agent router for Harbor Orchestrator.

This package provides:
- Dynamic agent routing based on policy (static, rule-based, or RL)
- Portable orchestration core that can be adapted to other projects
- Integration with Harbor-specific nodes via adapters
"""

from orchestrator.puppeteer.actions import AgentAction, list_all_actions, is_terminal
from orchestrator.puppeteer.state_adapter import TaskState, harbor_pack_to_task_state, update_states_from_action
from orchestrator.puppeteer.policy_base import PuppeteerPolicy, PolicyMode, make_policy
from orchestrator.puppeteer.executor import StepExecutor
from orchestrator.puppeteer.loop import run_dynamic_orchestration

__all__ = [
    "AgentAction",
    "list_all_actions",
    "is_terminal",
    "TaskState",
    "harbor_pack_to_task_state",
    "update_states_from_action",
    "PuppeteerPolicy",
    "PolicyMode",
    "make_policy",
    "StepExecutor",
    "run_dynamic_orchestration",
]

