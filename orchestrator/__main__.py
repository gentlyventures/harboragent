"""
CLI entrypoint for orchestrator.

Usage:
    python -m orchestrator run-pack <pack-slug>
    python -m orchestrator api
"""

import sys
import typer
from orchestrator.graph import run_pack_research
from orchestrator.puppeteer.loop import run_dynamic_orchestration
from orchestrator.puppeteer.policy_base import PolicyMode

app = typer.Typer(help="Harbor Agent Pack Research Orchestrator")


@app.command()
def run_pack(
    slug: str = typer.Argument(..., help="Pack slug (e.g., 'tax-assist')"),
):
    """
    Run the research pipeline for a pack.
    
    Example:
        python -m orchestrator run-pack tax-assist
    """
    try:
        final_state = run_pack_research(slug)
        
        # Print summary
        print("\n" + "=" * 60)
        print("Run Summary")
        print("=" * 60)
        print(f"Run ID: {final_state['run_id']}")
        print(f"Pack Slug: {final_state['pack_slug']}")
        print(f"\nScores:")
        scores = final_state.get("scores", {})
        print(f"  - Viability: {scores.get('viability', 'N/A')}")
        print(f"  - Data Availability: {scores.get('data_availability', 'N/A')}")
        print(f"  - ICP Clarity: {scores.get('icp_clarity', 'N/A')}")
        print(f"\nGates:")
        gate = final_state.get("gate", {})
        print(f"  - Validation: {gate.get('validation', 'N/A')}")
        print(f"  - Scoring: {gate.get('scoring', 'N/A')}")
        
        artifacts = final_state.get("artifacts", {})
        report_path = artifacts.get("deep_dive_report_path")
        if report_path:
            print(f"\nDeep Dive Report: {report_path}")
        else:
            print("\nDeep Dive Report: Not generated (scoring gate did not pass)")
        
        print(f"\nRun State: orchestrator/data/runs/{final_state['run_id']}.json")
        print()
        
    except ValueError as e:
        typer.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        typer.echo(f"❌ Unexpected error: {e}", err=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)


@app.command()
def run_pack_dynamic(
    slug: str = typer.Argument(..., help="Pack slug (e.g., 'tax-assist')"),
    mode: str = typer.Option("rule", help="Policy mode: 'static', 'rule', or 'rl'"),
    max_steps: int = typer.Option(20, help="Maximum number of steps"),
):
    """
    Run dynamic Puppeteer-style orchestration for a pack.
    
    Example:
        python -m orchestrator run-pack-dynamic tax-assist --mode=rule
        python -m orchestrator run-pack-dynamic tax-assist --mode=rl --max-steps=30
    """
    if mode not in ["static", "rule", "rl"]:
        typer.echo(f"❌ Error: Invalid mode '{mode}'. Must be 'static', 'rule', or 'rl'", err=True)
        sys.exit(1)
    
    try:
        result = run_dynamic_orchestration(
            pack_slug=slug,
            policy_mode=mode,  # type: ignore
            max_steps=max_steps
        )
        
        # Print summary
        print("\n" + "=" * 60)
        print("Dynamic Orchestration Summary")
        print("=" * 60)
        print(f"Run ID: {result['run_id']}")
        print(f"Pack Slug: {result['pack_slug']}")
        print(f"Policy Mode: {result['policy_mode']}")
        print(f"Steps Taken: {result['steps_taken']}")
        print(f"Final Reward: {result['final_reward']:.4f}")
        print(f"Success: {result['success']}")
        print(f"\nActions Taken:")
        for i, action in enumerate(result['actions'], 1):
            print(f"  {i}. {action}")
        
        if result.get("error"):
            print(f"\nError: {result['error']}")
        
        print()
        
    except ValueError as e:
        typer.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        typer.echo(f"❌ Unexpected error: {e}", err=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)


@app.command()
def api(
    host: str = typer.Option("127.0.0.1", help="Host to bind to"),
    port: int = typer.Option(8000, help="Port to bind to"),
    reload: bool = typer.Option(True, help="Enable auto-reload for development"),
):
    """
    Start the Harbor Ops API server.
    
    Example:
        python -m orchestrator api
        python -m orchestrator api --port 8001
    """
    import uvicorn
    
    typer.echo(f"🚀 Starting Harbor Ops API on http://{host}:{port}")
    typer.echo(f"   API docs: http://{host}:{port}/docs")
    typer.echo()
    
    uvicorn.run(
        "orchestrator.api:app",
        host=host,
        port=port,
        reload=reload,
    )


@app.command()
def generate_dynamic_runs(
    pack_slug: str = typer.Argument(..., help="Pack slug (e.g., 'tax-assist')"),
    mode: str = typer.Option("rule", help="Policy mode: 'static', 'rule', or 'rl'"),
    runs: int = typer.Option(20, help="Number of runs to generate"),
    max_steps: int = typer.Option(20, help="Maximum steps per run"),
):
    """
    Generate multiple dynamic orchestration runs to seed logs for RL training.
    
    This is useful for quickly generating training data without manual loops.
    
    Example:
        python -m orchestrator generate-dynamic-runs tax-assist --mode rule --runs 20 --max-steps 20
    """
    if mode not in ["static", "rule", "rl"]:
        typer.echo(f"❌ Error: Invalid mode '{mode}'. Must be 'static', 'rule', or 'rl'", err=True)
        sys.exit(1)
    
    typer.echo(f"Generating {runs} dynamic orchestration runs for pack '{pack_slug}'...")
    typer.echo(f"Mode: {mode}, Max steps per run: {max_steps}")
    typer.echo()
    
    successful_runs = 0
    failed_runs = 0
    
    for i in range(runs):
        try:
            result = run_dynamic_orchestration(
                pack_slug=pack_slug,
                policy_mode=mode,  # type: ignore
                max_steps=max_steps
            )
            
            if result.get("error"):
                failed_runs += 1
                typer.echo(f"  Run {i + 1}/{runs}: ❌ Failed - {result.get('error')}")
            else:
                successful_runs += 1
                typer.echo(
                    f"  Run {i + 1}/{runs}: ✓ Steps={result.get('steps_taken', 0)}, "
                    f"Reward={result.get('final_reward', 0):.3f}"
                )
        except Exception as e:
            failed_runs += 1
            typer.echo(f"  Run {i + 1}/{runs}: ❌ Exception - {str(e)}")
    
    typer.echo()
    typer.echo(f"✅ Completed: {successful_runs} successful, {failed_runs} failed")
    typer.echo(f"   Logs saved to orchestrator/data/logs/")


if __name__ == "__main__":
    app()

