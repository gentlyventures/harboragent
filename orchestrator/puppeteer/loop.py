"""
Orchestration loop: Main runner for dynamic Puppeteer-style orchestration.

This module coordinates the execution of the dynamic orchestration loop,
integrating policy, executor, telemetry, and state management.
"""

import uuid
from orchestrator.puppeteer.actions import AgentAction, is_terminal
from orchestrator.puppeteer.state_adapter import harbor_pack_to_task_state, update_states_from_action
from orchestrator.puppeteer.policy_base import PolicyMode, make_policy
from orchestrator.puppeteer.executor import StepExecutor
from orchestrator.config import get_pack_lifecycle, update_pack_lifecycle
from orchestrator.telemetry.logger import OrchestratorLogger
from orchestrator.telemetry.reward import compute_step_reward, compute_episode_reward, default_reward_config


def run_dynamic_orchestration(
    pack_slug: str,
    policy_mode: PolicyMode = "rule",
    max_steps: int = 20
) -> dict:
    """
    Run dynamic orchestration for a pack.
    
    This is the main entry point for Puppeteer-style orchestration. It:
    1. Loads pack lifecycle
    2. Initializes state, policy, executor, and logger
    3. Runs the orchestration loop
    4. Logs all steps and computes rewards
    5. Persists updated pack lifecycle
    
    Args:
        pack_slug: Pack slug identifier
        policy_mode: Policy mode ("static", "rule", or "rl")
        max_steps: Maximum number of steps to execute
        
    Returns:
        Run summary dict with:
        - run_id
        - pack_slug
        - policy_mode
        - actions: list of action names
        - final_reward
        - steps_taken
        - success: bool
        - error: str (if failed)
    """
    # Initialize run
    run_id = str(uuid.uuid4())
    
    # Load pack lifecycle
    pack_lifecycle = get_pack_lifecycle(pack_slug)
    if pack_lifecycle is None:
        return {
            "run_id": run_id,
            "pack_slug": pack_slug,
            "policy_mode": policy_mode,
            "actions": [],
            "final_reward": 0.0,
            "steps_taken": 0,
            "success": False,
            "error": f"Pack with slug '{pack_slug}' not found",
        }
    
    # Initialize run context
    run_context = {
        "run_id": run_id,
        "steps_taken": 0,
        "tokens_used": 0,
        "scores": {},
        "gate": {},
        "artifacts": {},
        "notes": {},
    }
    
    # Initialize state
    state = harbor_pack_to_task_state(pack_lifecycle, run_context)
    
    # Initialize components
    logger = OrchestratorLogger()
    policy = make_policy(policy_mode)
    executor = StepExecutor()
    reward_config = default_reward_config()
    
    # Track actions taken
    actions_taken: list[str] = []
    
    try:
        # Start run logging
        logger.start_run(run_id, pack_slug, policy_mode)
        
        # Orchestration loop
        for step_index in range(max_steps):
            # Select next action
            action = policy.select_next_agent(state)
            actions_taken.append(action.value)
            
            print(f"Step {step_index + 1}/{max_steps}: {action.value}")
            
            # Check if terminal
            if is_terminal(action):
                print(f"✅ Terminal action reached: {action.value}")
                break
            
            # Execute action
            state_before = state
            try:
                updated_pack, updated_run_context, tokens_used = executor.execute(
                    action, pack_lifecycle, run_context
                )
            except Exception as e:
                print(f"❌ Error executing action {action.value}: {e}")
                # Log error and break
                logger.log_step(
                    run_id,
                    step_index,
                    action,
                    state,
                    tokens_used=0,
                    local_reward=-1.0,  # Penalty for error
                )
                raise
            
            # Update state
            state_after = update_states_from_action(
                state_before,
                updated_pack,
                updated_run_context
            )
            
            # Compute step reward
            step_reward = compute_step_reward(
                state_before,
                state_after,
                tokens_used,
                reward_config
            )
            
            # Log step
            logger.log_step(
                run_id,
                step_index,
                action,
                state_after,
                tokens_used,
                step_reward,
            )
            
            # Update for next iteration
            pack_lifecycle = updated_pack
            run_context = updated_run_context
            state = state_after
        
        # Compute final reward
        run_summary = {
            "run_id": run_id,
            "pack_slug": pack_slug,
            "policy_mode": policy_mode,
            "actions": actions_taken,
            "steps_taken": len(actions_taken),
            "tokens_used": run_context.get("tokens_used", 0),
            "final_state": {
                "current_stage": state.current_stage,
                "has_research": state.has_research,
                "has_icp": state.has_icp,
                "gates_passed": state.gates_passed,
            },
        }
        
        final_reward = compute_episode_reward(run_summary, reward_config)
        run_summary["final_reward"] = final_reward
        
        # Determine success (pack is ready to publish or has completed key stages)
        success = (
            state.current_stage == "published"
            or len(state.gates_passed) >= 3
            or (state.has_research and state.has_icp)
        )
        run_summary["success"] = success
        
        # End run logging
        logger.end_run(run_id, final_reward, success, len(actions_taken))
        
        # Persist updated pack lifecycle
        # Use update_pack_lifecycle to preserve structure
        def updater(pack: dict) -> dict:
            # Merge updated fields into pack
            # This preserves all existing keys
            for key, value in pack_lifecycle.items():
                if key not in ["slug", "packNumber"]:  # Don't overwrite identifiers
                    pack[key] = value
            return pack
        
        try:
            update_pack_lifecycle(pack_slug, updater)
        except Exception as e:
            print(f"⚠️  Warning: Failed to persist pack lifecycle: {e}")
        
        return run_summary
    
    except Exception as e:
        # Error occurred during orchestration
        error_msg = str(e)
        print(f"❌ Orchestration failed: {error_msg}")
        
        # Log error
        logger.end_run(
            run_id,
            final_reward=-1.0,
            success=False,
            steps_taken=len(actions_taken),
            extra={"error": error_msg},
        )
        
        return {
            "run_id": run_id,
            "pack_slug": pack_slug,
            "policy_mode": policy_mode,
            "actions": actions_taken,
            "final_reward": -1.0,
            "steps_taken": len(actions_taken),
            "success": False,
            "error": error_msg,
        }

