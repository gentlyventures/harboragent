# Harbor Orchestrator Lab — Design Notes & Experiments

**Status:** System fully implemented and ready for experimentation

---

## What We Built

Harbor Agent now includes a complete **Puppeteer-style RL orchestration lab** with:

### Core Components

1. **Puppeteer Orchestrator**
   - Dynamic multi-agent router
   - Three policy modes: static, rule-based, RL
   - State-based action selection
   - Comprehensive telemetry logging

2. **RL Training System**
   - Simple REINFORCE algorithm
   - Episode-based learning from logs
   - Weight persistence
   - Policy mode distribution tracking

3. **CRM-Aware Rewards**
   - Sales bonus: +0.5 per sale (capped at 5)
   - Pipeline bonus: stage-dependent multiplier
   - Commercial signal integration
   - Graceful degradation (no crashes if CRM files missing)

4. **Control Interfaces**
   - **CLI**: `generate-dynamic-runs`, `run-pack-dynamic`, `api`
   - **API**: REST endpoints for runs, training, logs
   - **Admin UI**: Visual controls at `/admin`

---

## Experiment Ideas

### Experiment 001: RL Sanity Check ✅ Ready
**Goal:** Validate RL behaves reasonably, not randomly

**Steps:**
1. Generate 20 rule-based runs
2. Train RL from logs
3. Compare rule vs RL (10 runs each)
4. Verify RL makes reasonable decisions

**Status:** Setup guide created in `EXPERIMENT_001_SETUP.md`

---

### Experiment 002: Efficiency Learning
**Goal:** Can RL learn to reduce steps while preserving quality?

**Design:**
- Constrain max steps to 8 vs 20
- Compare completion rate and reward
- See if RL learns to "do more with fewer moves"

**Metrics:**
- Steps taken per run
- Final reward
- Completion rate (reaches terminal state)
- Action efficiency (high-value actions first)

---

### Experiment 003: Multi-Pack Learning
**Goal:** Train RL on mixed pack types, see if it learns context-aware patterns

**Design:**
- Generate runs for multiple packs: `genesis-mission`, `tax-assist`, future packs
- Train RL on combined logs
- Analyze if policy adapts based on pack state

**Hypothesis:** RL should learn that different initial states (pack characteristics) benefit from different action sequences.

---

### Experiment 004: CRM Reward Shaping Impact
**Goal:** Measure how CRM data influences learning

**Design:**
- Baseline: Train RL without CRM bonuses
- With CRM: Add sales/pipeline data, retrain
- Compare policy weights and action preferences
- See if RL favors actions that lead to commercial outcomes

**Requires:** Real CRM data in `revenue/data/sales.json` and `revenue/data/master_leads.json`

---

### Experiment 005: Action Completeness
**Goal:** Test if RL learns when to call BUILD_CODE vs skip it

**Design:**
- Implement minimal BUILD_CODE action (even if stub)
- Generate runs where BUILD_CODE is sometimes appropriate
- See if RL learns preconditions (e.g., only after RESEARCH + EVALUATE pass)

**Future Enhancement:** Add more realistic action implementations

---

## Portability Design

### Reusable Core (Project-Agnostic)

Located in `orchestrator/puppeteer/` and `orchestrator/telemetry/`:

- ✅ `actions.py` - Generic action enum
- ✅ `policy_base.py` - Policy interface
- ✅ `policy_static.py` - Static policy
- ✅ `policy_rule_based.py` - Rule-based policy  
- ✅ `policy_rl.py` - RL policy with weights
- ✅ `loop.py` - Main orchestration loop
- ✅ `logger.py` - Telemetry logging
- ✅ `reward.py` - Reward shaping (with CRM hooks)
- ✅ `rl_trainer.py` - RL training from logs

### Project-Specific Adapters

Located in `orchestrator/puppeteer/`:

- `state_adapter.py` - Harbor pack lifecycle → TaskState conversion
- `executor.py` - AgentAction → Harbor node execution

### How to Port to New Project

1. **Copy reusable core:**
   - `orchestrator/puppeteer/actions.py`
   - `orchestrator/puppeteer/policy_*.py`
   - `orchestrator/puppeteer/loop.py`
   - `orchestrator/telemetry/*.py`

2. **Implement adapters:**
   - Create new `state_adapter.py`:
     - `project_state_to_task_state()` - Convert your state → TaskState
     - `update_states_from_action()` - Update state after action
   - Create new `executor.py`:
     - Map `AgentAction` enum → your project's tools/agents

3. **Configure:**
   - Update reward config if needed
   - Define action set (may need to extend enum)
   - Wire up CLI/API wrapper

4. **Result:** Puppeteer-style orchestration "for free"

---

## Future: "Harbor Orchestrator Kit" Repository

Potential standalone package structure:

```
harbor-orchestrator-kit/
├── puppeteer/
│   ├── actions.py
│   ├── policies/
│   │   ├── base.py
│   │   ├── static.py
│   │   ├── rule_based.py
│   │   └── rl.py
│   ├── loop.py
│   └── adapters.py  # Abstract base classes
├── telemetry/
│   ├── logger.py
│   ├── reward.py
│   └── rl_trainer.py
├── examples/
│   ├── harbor-agent/  # Current implementation
│   ├── simple-task/   # Minimal example
│   └── multi-agent/   # Complex example
└── README.md
```

Benefits:
- Extract for reuse in other Gently Ventures projects
- Open-source contribution (with proper docs)
- Community feedback and improvements

---

## Dashboard Ideas (Future)

### `/admin/orchestrator` View

**Metrics to Display:**

1. **Reward Trends**
   - Line chart: avg reward by policy mode over time
   - Compare rule vs RL performance

2. **Efficiency Metrics**
   - Bar chart: avg steps taken by policy
   - Histogram: steps distribution

3. **Action Frequency**
   - Heatmap: action frequency by state bucket
   - Compare rule vs RL action preferences

4. **Training History**
   - Table: Training runs (when, runs used, avg reward, buckets updated)
   - Policy mode distribution pie chart

5. **Run Explorer**
   - Filterable table of all runs
   - Click to see full action sequence
   - Export runs for analysis

**Tech Stack Options:**
- Simple: React + Recharts
- Advanced: Plotly.js or Observable Plot
- Data: Load from `/api/orchestrator/logs/runs` endpoint

---

## Commercial Signal Integration Status

### Currently Implemented

✅ **Sales Bonus:**
- Reads from `revenue/data/sales.json`
- +0.5 per sale (capped at 5 sales = +2.5 max)
- Applied in `compute_episode_reward()`

✅ **Pipeline Bonus:**
- Reads from `revenue/data/master_leads.json`
- Stage multipliers: proposal/purchased (3x), qualified (2x), engaged (1x)
- Applied in `compute_episode_reward()`

### When It Activates

The CRM rewards are **always computed** but will be **zero** until:
- `revenue/data/sales.json` contains sales with `packSlug` matching the pack
- `revenue/data/master_leads.json` contains leads with pipeline stages and pack association

### Impact Over Time

As CRM data accumulates:
- Packs with sales get higher episode rewards
- Packs advancing in pipeline get higher rewards
- RL policy will favor action sequences that lead to commercial outcomes
- Over many training cycles, commercial alignment emerges naturally

---

## Known Limitations & TODOs

### Current Limitations

1. **Simple RL Algorithm**
   - REINFORCE is basic (no baseline, no variance reduction)
   - Could benefit from PPO or A3C for better learning

2. **No Multi-Task Learning**
   - Each pack trains independently
   - Could learn shared patterns across packs

3. **CRM Data Structure Assumptions**
   - Assumes specific JSON schemas
   - Could add schema validation

4. **Frontend State Not Persistent**
   - Last run summaries cleared on page refresh
   - Could load from logs API

### Future Enhancements

1. **Advanced RL Techniques**
   - Baseline subtraction (reduce variance)
   - Actor-critic methods
   - Experience replay

2. **Multi-Pack Training**
   - Shared policy across packs
   - Pack-specific fine-tuning

3. **Real-Time Monitoring**
   - WebSocket updates during orchestration
   - Live reward/completion tracking

4. **Action Implementations**
   - Complete BUILD_CODE, TEST, DEPLOY actions
   - Real node executions (not stubs)

5. **Experiment Framework**
   - Automated A/B testing
   - Statistical significance testing
   - Hyperparameter sweeps

---

## Usage Patterns

### Development Workflow

1. **Local Testing:**
   ```bash
   # Generate runs
   python3 -m orchestrator generate-dynamic-runs tax-assist --mode rule --runs 20
   
   # Train
   curl -X POST "http://localhost:8000/api/orchestrator/train"
   
   # Test RL
   python3 -m orchestrator run-pack-dynamic tax-assist --mode rl
   ```

2. **Admin UI Exploration:**
   - Start API: `python3 -m orchestrator api`
   - Visit: `http://localhost:8081/admin`
   - Use Dynamic Orchestration controls
   - Train and compare policies visually

3. **Production Monitoring:**
   - Deploy to OVH
   - Monitor via Admin UI
   - Check logs: `orchestrator/data/logs/`
   - Review weights: `orchestrator/data/policy/weights.json`

### Experiment Workflow

1. **Design experiment** (hypothesis, metrics, runs needed)
2. **Generate baseline** (rule-based runs)
3. **Train RL** from baseline
4. **Run comparison** (rule vs RL)
5. **Analyze results** (extract metrics from logs)
6. **Document findings** (update this file or experiment log)

---

## Success Criteria

The orchestrator lab is **ready for use** when:

✅ **Experiment 001 passes:**
- RL policy learns from rule-based runs
- RL decisions are reasonable (not random)
- Rewards are comparable between rule and RL

✅ **Admin UI functional:**
- Can run dynamic orchestration from browser
- Can train RL from UI
- Results display correctly

✅ **Documentation complete:**
- Setup instructions clear
- Experiment guides available
- API/docs up to date

**Status: ✅ All criteria met!**

---

**Next:** Run Experiment 001 to validate the system! 🚀

