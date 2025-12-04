"""
Step executor: Maps AgentAction to Harbor node execution.

This module is the ONLY place that knows about actual Harbor nodes.
The Puppeteer core depends on StepExecutor, not on Harbor directly.
"""

from orchestrator.puppeteer.actions import AgentAction
from orchestrator.nodes.intake import intake_node
from orchestrator.nodes.validation import validation_node
from orchestrator.nodes.scoring_gate import scoring_gate_node
from orchestrator.nodes.deep_research import deep_research_node
from orchestrator.state import State, new_run_state


class StepExecutor:
    """
    Executes agent actions by calling corresponding Harbor nodes.
    
    Maps AgentAction enum values to actual Harbor node functions.
    Returns updated pack lifecycle, run context, and tokens used.
    """
    
    def __init__(self):
        """Initialize step executor."""
        pass
    
    def execute(
        self,
        action: AgentAction,
        pack_lifecycle: dict,
        run_context: dict
    ) -> tuple[dict, dict, int]:
        """
        Execute an agent action.
        
        Args:
            action: Agent action to execute
            pack_lifecycle: Current pack lifecycle dict
            run_context: Current run context dict
            
        Returns:
            Tuple of (updated_pack_lifecycle, updated_run_context, tokens_used)
        """
        pack_slug = pack_lifecycle.get("slug", "")
        run_id = run_context.get("run_id", "")
        
        # Create a minimal state for Harbor nodes
        # Harbor nodes expect a State dict with specific structure
        harbor_state: State = {
            "run_id": run_id,
            "pack_slug": pack_slug,
            "pack_snapshot": pack_lifecycle.copy(),
            "scores": run_context.get("scores", {}),
            "gate": run_context.get("gate", {}),
            "artifacts": run_context.get("artifacts", {}),
            "notes": run_context.get("notes", {}),
        }
        
        tokens_used = 0
        
        # Map action to Harbor node
        if action == AgentAction.INTAKE:
            # Intake just loads the pack, which we already have
            # But we can call it to ensure state is properly initialized
            harbor_state = intake_node(harbor_state)
            updated_pack = harbor_state["pack_snapshot"]
        
        elif action == AgentAction.RESEARCH:
            # Research = deep research node
            harbor_state = deep_research_node(harbor_state)
            updated_pack = harbor_state["pack_snapshot"]
            # Estimate tokens (deep research uses GPT-4 with max_tokens=8000)
            tokens_used = 8000  # Rough estimate
        
        elif action == AgentAction.EVALUATE:
            # Evaluate = validation + scoring gate
            harbor_state = validation_node(harbor_state)
            tokens_used += 2000  # Rough estimate for validation
            harbor_state = scoring_gate_node(harbor_state)
            updated_pack = harbor_state["pack_snapshot"]
        
        elif action == AgentAction.ICP_ANALYSIS:
            # ICP analysis - stub for now
            # Could be a future node that analyzes ICP from research
            print(f"⏭️  ICP Analysis: Stub implementation (no-op)")
            updated_pack = pack_lifecycle.copy()
            tokens_used = 0
        
        elif action == AgentAction.DESIGN_SPEC:
            # Design spec - stub for now
            print(f"⏭️  Design Spec: Stub implementation (no-op)")
            updated_pack = pack_lifecycle.copy()
            tokens_used = 0
        
        elif action == AgentAction.BUILD_CODE:
            # Build code - stub for now
            print(f"⏭️  Build Code: Stub implementation (no-op)")
            updated_pack = pack_lifecycle.copy()
            # Mark in metadata that build was attempted
            if "metadata" not in updated_pack:
                updated_pack["metadata"] = {}
            updated_pack["metadata"]["build_attempted"] = True
            tokens_used = 0
        
        elif action == AgentAction.TEST:
            # Test - stub for now
            print(f"⏭️  Test: Stub implementation (no-op)")
            updated_pack = pack_lifecycle.copy()
            if "metadata" not in updated_pack:
                updated_pack["metadata"] = {}
            updated_pack["metadata"]["tests_run"] = True
            tokens_used = 0
        
        elif action == AgentAction.DEPLOY:
            # Deploy - stub for now
            print(f"⏭️  Deploy: Stub implementation (no-op)")
            updated_pack = pack_lifecycle.copy()
            if "deployment" not in updated_pack:
                updated_pack["deployment"] = {}
            updated_pack["deployment"]["frontendDeployed"] = True
            tokens_used = 0
        
        elif action == AgentAction.PUBLISH:
            # Publish - stub for now
            print(f"⏭️  Publish: Stub implementation (no-op)")
            updated_pack = pack_lifecycle.copy()
            if "stages" not in updated_pack:
                updated_pack["stages"] = {}
            if "published" not in updated_pack["stages"]:
                updated_pack["stages"]["published"] = {}
            updated_pack["stages"]["published"]["status"] = "completed"
            updated_pack["currentStage"] = "published"
            tokens_used = 0
        
        elif action == AgentAction.STOP:
            # Stop - no-op
            updated_pack = pack_lifecycle.copy()
            tokens_used = 0
        
        else:
            # Unknown action - no-op
            print(f"⚠️  Unknown action: {action}, skipping")
            updated_pack = pack_lifecycle.copy()
            tokens_used = 0
        
        # Update run context with new state
        updated_run_context = run_context.copy()
        updated_run_context.update({
            "scores": harbor_state.get("scores", {}),
            "gate": harbor_state.get("gate", {}),
            "artifacts": harbor_state.get("artifacts", {}),
            "notes": harbor_state.get("notes", {}),
            "tokens_used": run_context.get("tokens_used", 0) + tokens_used,
        })
        
        return updated_pack, updated_run_context, tokens_used

