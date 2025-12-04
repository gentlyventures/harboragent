"""
Rule-based policy: Heuristic routing based on task state.

This is the default safe "Puppeteer-style" router - dynamic but deterministic,
with no learning component. It uses simple heuristics to decide which agent
action to take next.
"""

from orchestrator.puppeteer.actions import AgentAction
from orchestrator.puppeteer.policy_base import PuppeteerPolicy
from orchestrator.puppeteer.state_adapter import TaskState


class RuleBasedPolicy:
    """
    Rule-based policy using simple heuristics.
    
    This policy is purely synchronous and deterministic. It makes decisions
    based on the current state of the task, following a logical progression
    through the pack lifecycle.
    """
    
    def __init__(self, config: dict):
        """
        Initialize rule-based policy.
        
        Args:
            config: Configuration dict (unused for rule-based policy)
        """
        self.config = config
    
    def select_next_agent(self, state: TaskState) -> AgentAction:
        """
        Select next action using heuristic rules.
        
        Rules (in priority order):
        1. If not has_research -> RESEARCH
        2. Else if not has_icp -> ICP_ANALYSIS
        3. Else if current_stage in ["idea", "validation"] and research is done -> EVALUATE
        4. Else if code not present (hint from metadata) -> BUILD_CODE
        5. Else if tests not run -> TEST
        6. Else if ready_for_publish -> PUBLISH
        7. Else -> STOP
        
        Args:
            state: Current task state
            
        Returns:
            Next agent action
        """
        # Rule 1: Research is fundamental, do it first if not done
        if not state.has_research:
            return AgentAction.RESEARCH
        
        # Rule 2: ICP analysis needed if not present
        if not state.has_icp:
            return AgentAction.ICP_ANALYSIS
        
        # Rule 3: Evaluation after research and ICP are done
        if state.current_stage in ["idea", "validation"] and state.has_research:
            return AgentAction.EVALUATE
        
        # Rule 4: Check if code needs to be built
        # Check metadata for deployment status or code presence
        metadata = state.metadata
        deployment = metadata.get("deployment", {})
        stages = metadata.get("stages", {})
        build_stage = stages.get("build", {})
        
        # If build stage is not completed, we need to build
        if build_stage.get("status") != "completed":
            # Check if we're in the build stage or past evaluation
            if state.current_stage in ["build", "scoring", "deep_dive"]:
                return AgentAction.BUILD_CODE
        
        # Rule 5: Testing (if build is done but tests not run)
        if build_stage.get("status") == "completed":
            # Check if tests have been run (could be in metadata)
            if not metadata.get("tests_run", False):
                return AgentAction.TEST
        
        # Rule 6: Ready to publish
        if state.current_stage == "build" and build_stage.get("status") == "completed":
            # Check if deployment is ready
            if deployment.get("frontendDeployed") or deployment.get("workerDeployed"):
                return AgentAction.PUBLISH
        
        # Rule 7: Default to stop if we don't know what to do
        return AgentAction.STOP

