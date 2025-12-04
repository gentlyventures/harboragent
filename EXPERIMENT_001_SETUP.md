# Experiment 001: RL System Validation

**Goal:** Validate that the Puppeteer RL orchestrator behaves sanely and learns from experience.

---

## Prerequisites

### 1. Install Orchestrator Dependencies

You'll need Python 3.11+ with dependencies installed. Choose one approach:

**Option A: Using pip (recommended for quick testing)**
```bash
cd /Users/dwmini/Documents/1_GV_Builds/1_Active/harbor_agent
python3 -m pip install --user -r orchestrator/requirements.txt
```

**Option B: Using a virtual environment (cleaner isolation)**
```bash
cd /Users/dwmini/Documents/1_GV_Builds/1_Active/harbor_agent
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or: venv\Scripts\activate  # On Windows
pip install -r orchestrator/requirements.txt
```

**Option C: Using uv (fastest)**
```bash
cd /Users/dwmini/Documents/1_GV_Builds/1_Active/harbor_agent
uv pip install -r orchestrator/requirements.txt
```

### 2. Verify Installation

```bash
python3 -m orchestrator --help
```

You should see the CLI help menu.

### 3. Environment Variables

Ensure `.env` file exists in repo root with:
```
OPENAI_API_KEY=sk-your-key-here
```

---

## Experiment 001 Steps

### Step 1: Seed Logs with Rule-Based Runs

Generate baseline runs using the sensible rule-based policy:

```bash
# Start with rule (the sensible baseline)
python3 -m orchestrator generate-dynamic-runs tax-assist --mode rule --runs 20 --max-steps 15
```

**What to expect:**
- 20 orchestration runs will execute
- Each run selects actions based on rule-based policy
- Runs and steps logged to `orchestrator/data/logs/`
- Progress printed to console

**Check logs:**
```bash
tail -5 orchestrator/data/logs/runs.jsonl
tail -20 orchestrator/data/logs/steps.jsonl
```

You should see:
- Runs with `"policy_mode": "rule"`
- Reasonable rewards (typically between -1.0 and 1.0 depending on completion)
- Action sequences logged

---

### Step 2: Train RL Policy from Logs

With the API running in one terminal:

```bash
python3 -m orchestrator api
```

In another terminal:

```bash
curl -X POST "http://localhost:8000/api/orchestrator/train?max_runs=50" | jq
```

**What to expect:**
```json
{
  "total_runs_used": 20,
  "avg_episode_reward": 0.234,
  "avg_reward": 0.234,
  "updated_buckets": 5,
  "number_of_buckets_updated": 5,
  "policy_mode_distribution": {
    "rule": 20
  },
  "message": "Trained on 20 runs, updated 5 buckets"
}
```

**Verify weights saved:**
```bash
cat orchestrator/data/policy/weights.json | jq
```

You should see action preferences by state bucket.

---

### Step 3: Compare Rule vs RL

Run small A/B comparison:

```bash
# Rule-based (baseline)
python3 -m orchestrator generate-dynamic-runs tax-assist --mode rule --runs 10 --max-steps 15

# RL (learned policy)
python3 -m orchestrator generate-dynamic-runs tax-assist --mode rl --runs 10 --max-steps 15
```

**Analyze results:**

Extract metrics from logs:
```bash
# Extract rule-based run metrics
grep '"policy_mode":"rule"' orchestrator/data/logs/runs.jsonl | \
  jq -r '[.final_reward, .steps_taken] | @csv' | \
  awk -F, '{sum_r+=$1; sum_s+=$2; n++} END {print "Rule - Avg Reward:", sum_r/n, "Avg Steps:", sum_s/n}'

# Extract RL run metrics  
grep '"policy_mode":"rl"' orchestrator/data/logs/runs.jsonl | \
  jq -r '[.final_reward, .steps_taken] | @csv' | \
  awk -F, '{sum_r+=$1; sum_s+=$2; n++} END {print "RL - Avg Reward:", sum_r/n, "Avg Steps:", sum_s/n}'
```

**What to look for:**
- ✅ **RL looks reasonable**: Average reward is in same ballpark as rule-based
- ✅ **Not random**: RL runs show consistent patterns (not wildly different each time)
- ✅ **Action sequences make sense**: Check `actions` array in runs.jsonl - should follow logical progression

**Red flags:**
- ❌ RL rewards consistently much worse than rule-based (might need more training)
- ❌ RL actions are completely random/unpredictable
- ❌ RL gets stuck in loops or takes many more steps

---

## Expected Outcomes

After Experiment 001, you should have:

1. ✅ **Baseline established**: Rule-based policy performance metrics
2. ✅ **RL weights trained**: Policy learned from rule-based runs
3. ✅ **A/B comparison**: Direct rule vs RL comparison
4. ✅ **Confidence**: RL system behaves sanely, not randomly

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'typer'"
→ Install dependencies (see Prerequisites above)

### "Pack with slug 'tax-assist' not found"
→ Ensure pack exists in `pack-crm/data/packs.json` or use existing pack slug

### "OPENAI_API_KEY environment variable is not set"
→ Create `.env` file in repo root with your OpenAI API key

### "Connection refused" when calling API
→ Start the API server: `python3 -m orchestrator api`

### No logs generated
→ Check that `orchestrator/data/logs/` directory exists and is writable

---

## Next Steps After Experiment 001

Once validated:

1. **Experiment 002**: Test RL efficiency (can it reduce steps while preserving quality?)
2. **Multi-pack training**: Train on multiple packs simultaneously
3. **CRM integration**: Add real sales/pipeline data and see reward shaping in action
4. **Production deployment**: Deploy to OVH and test via Admin UI

---

## Admin UI Testing (After Local Validation)

Once you're happy locally:

1. Deploy backend: `cd deploy && ./deploy_to_ovh.sh`
2. Deploy frontend: Cloudflare Pages (if Admin UI changed)
3. Visit `https://harboragent.dev/admin`
4. Test Dynamic Orchestration controls:
   - Select policy mode
   - Set max steps
   - Run orchestration
   - View results
5. Train RL policy via "Train RL Policy from Logs" button
6. Compare rule vs RL via UI

---

**Ready to run Experiment 001? Start with Step 1!** 🚀

