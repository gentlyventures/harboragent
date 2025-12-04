# Harbor Agent Orchestrator

Python-based LangGraph orchestrator for automating the research side of the Harbor Agent pack pipeline.

## Overview

The orchestrator automates the pack research workflow:
1. **Intake**: Load pack lifecycle from pack-crm
2. **Validation**: Use OpenAI to assess pack viability
3. **Scoring Gate**: Apply deterministic rules to determine if pack passes
4. **Deep Research**: Generate comprehensive research report (only if gate passes)
5. **Summary**: Save run state and generate summary

## Installation

### Prerequisites

- Python 3.11 or higher
- `pip` or `uv` package manager

### Install Dependencies

Using pip:
```bash
pip install -r orchestrator/requirements.txt
```

Or using uv:
```bash
uv pip install -r orchestrator/requirements.txt
```

## Environment Variables

### Required

- **`OPENAI_API_KEY`**: Your OpenAI API key
  - For local dev: Set in `.env` file in project root (loaded automatically)
  - For GitHub Actions: Set as GitHub secret named `OPENAI_API_KEY`

The orchestrator will automatically:
- Load from `.env` file if present (using `python-dotenv`)
- Read from environment variable `OPENAI_API_KEY`
- Raise a clear error if the key is missing

## Usage

### Start the Harbor Ops API

The Harbor Ops API provides REST endpoints for pack management, research pipeline execution, and revenue data access.

```bash
python -m orchestrator api
```

This starts the FastAPI server on `http://127.0.0.1:8000` with auto-reload enabled.

**API Documentation:**
- Interactive docs: http://127.0.0.1:8000/docs
- OpenAPI schema: http://127.0.0.1:8000/openapi.json

**Endpoints:**
- `GET /api/packs` - List all packs
- `GET /api/packs/{slug}` - Get pack details
- `POST /api/packs` - Create new pack
- `PATCH /api/packs/{slug}/crm` - Update pack CRM data
- `POST /api/packs/{slug}/runs/research` - Run research pipeline
- `GET /api/packs/{slug}/runs` - List runs for a pack
- `GET /api/runs/{run_id}` - Get run details
- `GET /api/revenue/summary` - Get revenue summary
- `GET /api/revenue/leads` - Get leads data
- `POST /api/revenue/lead-discovery-runs` - Stub for LinkedIn ICP discovery

**Note:** The API must be running for the admin dashboard (`/admin`) to function with interactive features (New Idea form, Run Research button).

### Run Research Pipeline for a Pack

```bash
python -m orchestrator run-pack <pack-slug>
```

Example:
```bash
python -m orchestrator run-pack tax-assist
```

This will:
1. Load the pack from `pack-crm/data/packs.json`
2. Run validation assessment
3. Apply scoring gate rules
4. Generate deep research report (if gate passes)
5. Save run state to `orchestrator/data/runs/{run_id}.json`
6. Update pack lifecycle in `pack-crm/data/packs.json`

### Output Files

After running, you'll find:

1. **Research Report** (if scoring gate passed):
   - Location: `pack-crm/research/{pack_slug}-{run_id}-deep-dive.md`
   - Contains comprehensive research report based on `pack-process/CHATGPT_RESEARCH_TEMPLATE.md`

2. **Run State JSON**:
   - Location: `orchestrator/data/runs/{run_id}.json`
   - Contains complete state of the run including scores, gates, and artifacts

3. **Updated Pack Lifecycle**:
   - Location: `pack-crm/data/packs.json`
   - Pack lifecycle is updated with:
     - Stage statuses (validation, scoring, deep_dive)
     - CRM gate decision notes
     - Research artifacts
     - Research completion status

## How It Works

### Integration with pack-crm

The orchestrator reads and writes to `pack-crm/data/packs.json`:

- **Reads**: Pack lifecycle data including CRM fields (ideaNotes, icpSummary, etc.)
- **Writes**: Updates stage statuses, gate decision notes, research artifacts
- **Preserves**: All existing fields and structure (does not drop unknown keys)

### Workflow Graph

```
intake → validation → scoring_gate → [conditional]
                                      ├─ continue → deep_research → summary
                                      └─ skip → summary
```

**Conditional Logic:**
- If `gate.scoring == "pass"`: Run deep research
- Otherwise: Skip deep research and go directly to summary

### Scoring Gate Rules

Deterministic rules applied in `scoring_gate_node`:

- **Pass**: `viability >= 70 AND data_availability >= 60`
- **Soft Fail Retry**: `viability >= 50` (but data_availability < 60)
- **Hard Fail**: `viability < 50`

### Validation Node

Uses OpenAI GPT-4 to assess:
- **Viability Score** (0-100): Market need, value proposition, feasibility
- **Data Availability Score** (0-100): Information availability, research sources
- **ICP Clarity Score** (0-100): Target audience specificity and accessibility

### Deep Research Node

Generates comprehensive research report by:
1. Reading `pack-process/CHATGPT_RESEARCH_TEMPLATE.md`
2. Building prompt with pack metadata and CRM fields
3. Calling OpenAI GPT-4
4. Saving markdown report to `pack-crm/research/`
5. Updating pack lifecycle with research completion status

## File Structure

```
orchestrator/
├── __init__.py
├── __main__.py              # CLI entrypoint
├── config.py                # Configuration and pack-crm integration
├── state.py                 # State model and helpers
├── graph.py                 # LangGraph workflow definition
├── nodes/
│   ├── __init__.py
│   ├── intake.py            # Load pack lifecycle
│   ├── validation.py        # OpenAI viability assessment
│   ├── scoring_gate.py      # Deterministic gate rules
│   ├── deep_research.py     # Generate research report
│   └── summary.py           # Save run state
├── data/
│   └── runs/                # Run state JSON files
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Example Commands

### Create a new run for an existing pack

```bash
# Run research pipeline for tax-assist pack
python -m orchestrator run-pack tax-assist
```

### Find output files

After running, find the files:

```bash
# Find the research report
ls -la pack-crm/research/tax-assist-*.md

# Find the run state JSON
ls -la orchestrator/data/runs/*.json

# Or use the run_id from the output
# The orchestrator prints the run_id at the end
```

## Troubleshooting

### "OPENAI_API_KEY environment variable is not set"

1. **Local dev**: Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```

2. **GitHub Actions**: Ensure the secret `OPENAI_API_KEY` is set in your repository settings.

### "Pack with slug 'X' not found"

Ensure the pack exists in `pack-crm/data/packs.json`. You can create it using:
```bash
pnpm tsx pack-crm/scripts/init-pack.ts <slug> <name>
```

### "Research template not found"

Ensure `pack-process/CHATGPT_RESEARCH_TEMPLATE.md` exists in the repository.

### JSON parse errors

If `pack-crm/data/packs.json` has invalid JSON, fix it manually or regenerate it using the pack-crm scripts.

## Future Enhancements

- [ ] Add more sophisticated scoring algorithms
- [ ] Support for retry logic on soft failures
- [ ] Integration with design_spec_node and build_node
- [ ] Parallel processing for multiple packs
- [ ] Webhook notifications on completion
- [ ] Metrics and analytics dashboard

## Admin Dashboard

The admin dashboard at `/admin` (dev: http://localhost:8081/admin) provides:

- **Read-only view** of all packs and their lifecycle status
- **New Idea form** - Create new packs via the UI (requires Harbor Ops API)
- **Run Research Pipeline** - Execute research pipeline for any pack (requires Harbor Ops API)
- **Sales Summary** - View revenue/leads summary (requires Harbor Ops API)

**Requirements:**
- `VITE_HARBOR_ADMIN_PASSWORD` environment variable must be set
- Harbor Ops API must be running (`python -m orchestrator api`) for interactive features

**Note:** `pack-crm/data/packs.json` remains the TypeScript domain's source of truth. All backend updates via the API preserve unknown keys and maintain JSON structure.

## Production Deployment

The Harbor Ops API can be deployed to an OVH VM using Docker. See `deploy/README.md` for complete deployment instructions.

**Quick Start:**
1. Run `./deploy/deploy_to_ovh.sh <OVH_HOST> <SSH_USER>`
2. Configure environment variables on the server
3. Point `api.harboragent.dev` DNS to the VM
4. Set `VITE_HARBOR_OPS_API_URL=https://api.harboragent.dev` in Cloudflare Pages

## Puppeteer-style Harbor Orchestrator v1.0

The orchestrator now includes a Puppeteer-style dynamic multi-agent router with logging, reward shaping, and a simple RL loop. This system provides:

- **Dynamic agent routing**: Agents are selected dynamically based on policy (static, rule-based, or RL)
- **Policy modes**: Choose between static (fixed sequence), rule-based (heuristic), or RL (learned) policies
- **Telemetry**: Comprehensive logging of runs and steps for analysis and training
- **Reward shaping**: Configurable rewards to guide RL training
- **Portable core**: The Puppeteer core modules can be adapted to other projects by swapping adapters

### Policy Modes

1. **Static** (`"static"`): Fixed sequence based on current stage (baseline for comparison)
2. **Rule-based** (`"rule"`): Heuristic routing using simple rules (default, safe, deterministic)
3. **RL** (`"rl"`): Reinforcement learning policy that learns from experience

### Data Locations

- **Logs**: `orchestrator/data/logs/`
  - `runs.jsonl`: Run-level events (start, end)
  - `steps.jsonl`: Step-level events (action, state, reward)
- **Policy weights**: `orchestrator/data/policy/weights.json` (for RL policy)

### Running Dynamic Orchestration

#### CLI

```bash
# Run with rule-based policy (default)
python -m orchestrator run-pack-dynamic tax-assist --mode=rule

# Run with RL policy
python -m orchestrator run-pack-dynamic tax-assist --mode=rl --max-steps=30

# Run with static policy
python -m orchestrator run-pack-dynamic tax-assist --mode=static
```

#### API

```bash
# Run dynamic orchestration
curl -X POST http://localhost:8000/api/packs/tax-assist/runs/dynamic \
  -H "Content-Type: application/json" \
  -d '{"policyMode": "rule", "maxSteps": 20}'

# Train RL policy from logs
curl -X POST http://localhost:8000/api/orchestrator/train?max_runs=50

# Get recent logs
curl http://localhost:8000/api/orchestrator/logs/runs?limit=20
```

### API Endpoints

- **POST `/api/packs/{slug}/runs/dynamic`**: Run dynamic orchestration
  - Request body: `{"policyMode": "rule" | "rl" | "static", "maxSteps": 20}`
  - Returns: Run summary with actions, final_reward, steps_taken

- **POST `/api/orchestrator/train`**: Train RL policy from logs
  - Query param: `max_runs` (optional, limits number of runs to process)
  - Returns: Training summary with total_runs, avg_reward, updated_buckets

- **GET `/api/orchestrator/logs/runs`**: Get recent orchestration logs
  - Query param: `limit` (optional, default: 20)
  - Returns: List of run log entries (most recent first)

### Architecture

The Puppeteer system is organized into two main packages:

#### `orchestrator/puppeteer/`

- **`actions.py`**: Agent action definitions (INTAKE, RESEARCH, EVALUATE, etc.)
- **`state_adapter.py`**: Converts between Harbor pack lifecycle and generic TaskState
- **`policy_base.py`**: Policy interface and factory
- **`policy_static.py`**: Static policy (fixed sequence)
- **`policy_rule_based.py`**: Rule-based policy (heuristic routing)
- **`policy_rl.py`**: RL policy (learned preferences)
- **`executor.py`**: Maps actions to Harbor node execution
- **`loop.py`**: Main orchestration loop runner

#### `orchestrator/telemetry/`

- **`logger.py`**: Logs runs and steps to JSONL files
- **`reward.py`**: Reward shaping functions for steps and episodes
- **`rl_trainer.py`**: Simple REINFORCE-style RL trainer

### Training RL Policy

The RL policy learns from logged runs:

1. Run dynamic orchestration with `policyMode: "rule"` to generate logs
2. Review logs to ensure quality
3. Train RL policy: `POST /api/orchestrator/train`
4. Use trained policy: `policyMode: "rl"` in subsequent runs

The trainer uses a simple REINFORCE algorithm:
- Loads run and step logs
- Computes episode rewards
- Updates action preferences based on returns
- Saves weights to `orchestrator/data/policy/weights.json`

### Portability

The Puppeteer core is designed to be portable to other projects:

- **Generic components**: `actions.py`, `policy_base.py`, `loop.py` are project-agnostic
- **Adapters**: Project-specific logic lives in `state_adapter.py` and `executor.py`
- **No circular imports**: Clean dependency structure (puppeteer -> telemetry, adapters at edges)

To adapt to a new project:
1. Implement new state adapters (similar to `harbor_pack_to_task_state`)
2. Implement new executor (map actions to your project's operations)
3. Keep the core Puppeteer modules unchanged

### Legacy Behavior

The existing `run_pack_research` function and fixed graph remain unchanged. The dynamic orchestration runs alongside the legacy system, allowing for gradual migration and comparison.

## See Also

- `pack-crm/README.md` - Pack CRM module documentation
- `pack-process/` - Process documentation
- `deploy/README.md` - Production deployment guide
- `DEV_AUDIT_harbor_agent.md` - Full project audit

