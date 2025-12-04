"""
CLI entrypoint for orchestrator.

Usage:
    python -m orchestrator run-pack <pack-slug>
    python -m orchestrator api
"""

import sys
import typer
from orchestrator.graph import run_pack_research

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


if __name__ == "__main__":
    app()

