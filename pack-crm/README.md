# Pack CRM Module

A file-based Pack CRM (Customer Relationship Management) module for tracking pack lifecycle, research, deployment status, and idea pipeline.

## Overview

The Pack CRM module provides:

- **Lifecycle Management**: Track packs through stages (idea → validation → scoring → deep_dive → build → published)
- **CRM Fields**: Track ideas, ICP, pain points, value hypothesis, pricing, competition, and gate decisions
- **File-Based Storage**: JSON-based storage matching the project's file-based approach
- **Research Integration**: OpenAI-powered deep-dive research automation
- **Admin Dashboard**: Read-only React UI for viewing pack status and CRM data (with password gate)
- **CLI Tools**: Scripts for pack management and research

## Directory Structure

```
pack-crm/
├── src/
│   ├── models.ts              # Data models (PackLifecycle, stages, etc.)
│   ├── store.ts               # File-based storage (read/write packs.json)
│   ├── lifecycle.ts           # Stage advancement logic
│   ├── openai-client.ts       # OpenAI API client
│   └── prompts/
│       └── deepDive.ts        # Deep-dive research prompt builder
├── scripts/
│   ├── init-pack.ts           # Create a new pack
│   ├── advance-stage.ts       # Advance pack to a stage
│   ├── export-packs-for-frontend.ts  # Export packs for React UI
│   └── run-deep-dive.ts       # Run OpenAI research
├── data/
│   └── packs.json             # Master pack registry (JSON)
├── research/
│   └── {slug}-deep-dive.md    # Research reports (generated)
└── README.md                  # This file
```

## Data Model

### PackLifecycle

The core data structure for a pack:

```typescript
interface PackLifecycle {
  slug: string;                    // URL-friendly ID (e.g., "genesis-mission")
  name: string;                     // Display name
  packNumber: number;               // Sequential number (1, 2, 3, ...)
  currentStage: PackStage;          // Current lifecycle stage
  stages: PackStages;               // Stage states with timestamps
  metadata: PackMetadata;           // Regulation name, audience, price
  research: PackResearch;           // Research completion status
  deployment: PackDeployment;       // Deployment status flags
  crm: PackCRM;                     // CRM fields for idea + research + pipeline
}
```

### PackCRM

CRM fields for tracking ideas, research, and pipeline decisions:

```typescript
interface PackCRM {
  ideaNotes: string | null;         // Initial stream-of-consciousness idea dump
  icpSummary: string | null;        // Who this is for
  primaryPainPoints: string[];      // Bullet list of pains
  valueHypothesis: string | null;   // How the pack helps
  pricingNotes: string | null;      // Thoughts on price points / packages
  competitionNotes: string | null; // Notes on the market landscape / competitors
  gateDecisionNotes: {
    validation?: string;            // Why it passed/failed validation
    scoring?: string;               // Justification for scores
    deep_dive?: string;             // Summary of research conclusions
  };
}
```

**Important:** The CRM does NOT store actual credentials, API keys, or secrets. Only high-level references (e.g., "Stripe credentials in Cloudflare env") are acceptable.

### Pack Stages

1. **idea** - Initial concept
2. **validation** - Validate concept
3. **scoring** - Score and gate (pass/fail)
4. **deep_dive** - Research phase
5. **build** - Implementation
6. **published** - Live and deployed

Each stage has:
- `status`: 'not_started' | 'in_progress' | 'completed'
- `startedAt`: ISO 8601 timestamp
- `completedAt`: ISO 8601 timestamp
- Optional fields: `score`, `gate`, `researchArtifacts`, `publishedAt`

## Usage

### Creating a New Pack

```bash
pnpm tsx pack-crm/scripts/init-pack.ts <slug> <name> [--price <price>]
```

Example:
```bash
pnpm tsx pack-crm/scripts/init-pack.ts new-pack "New Pack Name" --price 499
```

This creates a new pack with:
- Stage: `idea`
- All stages set to `not_started`
- Default price: $199 (or specified price)

### Advancing a Pack Stage

```bash
pnpm tsx pack-crm/scripts/advance-stage.ts <slug> <stage> [--score <score>] [--gate <pass|fail>] [--note <note>]
```

Examples:
```bash
# Advance to deep_dive stage
pnpm tsx pack-crm/scripts/advance-stage.ts tax-assist deep_dive

# Advance to scoring stage with score and gate
pnpm tsx pack-crm/scripts/advance-stage.ts tax-assist scoring --score 85 --gate pass
```

### Running Deep-Dive Research

```bash
export OPENAI_API_KEY=your-api-key-here
pnpm tsx pack-crm/scripts/run-deep-dive.ts <slug>
```

Example:
```bash
export OPENAI_API_KEY=sk-...
pnpm tsx pack-crm/scripts/run-deep-dive.ts tax-assist
```

This script:
1. Loads the pack
2. Reads `pack-process/CHATGPT_RESEARCH_TEMPLATE.md`
3. Builds a research prompt
4. Calls OpenAI API
5. Saves report to `pack-crm/research/{slug}-deep-dive.md`
6. Updates pack with research completion status
7. Advances pack to `deep_dive` stage

### Exporting Packs for Frontend

```bash
pnpm tsx pack-crm/scripts/export-packs-for-frontend.ts
```

This exports `pack-crm/data/packs.json` to `src/data/packs.local.json` for the React admin dashboard.

## Admin Dashboard

### URLs

- **Dev admin URL:** `http://localhost:8081/admin` (when running `pnpm dev`)
- **Prod admin URL (expected):** `https://harboragent.dev/admin`

### Password Gate

The admin dashboard is protected by a lightweight password gate:

- **Environment Variable:** `VITE_HARBOR_ADMIN_PASSWORD`
- **How it works:**
  - If `VITE_HARBOR_ADMIN_PASSWORD` is set, users must enter the password to access the dashboard
  - Password is stored in `localStorage` as `harbor_admin_authed` after successful authentication
  - If `VITE_HARBOR_ADMIN_PASSWORD` is NOT set, the page is accessible without authentication (dev mode only, with console warning)

**Important:** This is a lightweight UI gate, NOT full authentication. For production, consider implementing proper authentication.

### Dashboard Features

The dashboard shows:
- **Sales Summary:** Revenue and leads summary (requires Harbor Ops API)
- **New Idea Form:** Create new packs via the UI (requires Harbor Ops API)
- **Pack List:** All packs with full lifecycle details
- **Run Research Pipeline:** Execute research pipeline for any pack (requires Harbor Ops API)
- **Core Details:** Pack number, name, slug, current stage, price, updated timestamp
- **CRM Overview:**
  - Idea notes (truncated to first ~200 chars)
  - ICP summary
  - Primary pain points (as bullet list)
  - Value hypothesis
  - Pricing notes
  - Competition notes
- **Lifecycle:**
  - Current stage
  - Research completion status
  - Research artifacts (filenames)
- **Gate Decisions:**
  - Validation gate decision notes
  - Scoring gate decision notes
  - Deep dive research conclusions
- **Deployment Status:** Frontend, Worker, Stripe, R2

### Harbor Ops API Integration

The admin dashboard now integrates with the **Harbor Ops API** (FastAPI backend) for interactive features:

- **API Base URL:** Configurable via `VITE_HARBOR_OPS_API_URL` environment variable
  - **Dev:** Defaults to `http://127.0.0.1:8000` (if env var not set)
  - **Prod:** Set to `https://api.harboragent.dev` (or your deployed API URL)
- **Start API (local):** `python -m orchestrator api`
- **API Docs:** http://127.0.0.1:8000/docs (local) or https://api.harboragent.dev/docs (prod)

**Environment Variable Configuration:**

- **Local Development:**
  - `VITE_HARBOR_OPS_API_URL` can be left unset; defaults to `http://127.0.0.1:8000`
  - Or set in `.env` file: `VITE_HARBOR_OPS_API_URL=http://127.0.0.1:8000`

- **Production (Cloudflare Pages):**
  - Set `VITE_HARBOR_OPS_API_URL=https://api.harboragent.dev` in Cloudflare Pages environment variables
  - Redeploy the frontend after setting the variable

**Interactive Features (require API):**
- **New Idea Form:** Create packs directly from the UI
- **Run Research Pipeline:** Execute research pipeline with one click
- **Sales Summary:** View revenue/leads data

**Note:** If the API is not running, the dashboard will show an error banner with instructions. The dashboard can still display packs from the API if it was previously running, but interactive features will be disabled.

**Important:** `pack-crm/data/packs.json` remains the TypeScript domain's source of truth. All backend updates via the API preserve unknown keys and maintain JSON structure.

## For AI Agents (Cursor, etc.)

AI agents can use this module by:

1. **Reading pack data**: Import and use `loadPacks()`, `getPack()` from `pack-crm/src/store.ts`
2. **Updating packs**: Use `updatePack()` or `advancePackStage()` functions
3. **Running research**: Call `run-deep-dive.ts` script
4. **Creating packs**: Call `init-pack.ts` script

Example TypeScript usage:
```typescript
import { getPack, updatePack } from './pack-crm/src/store';
import { advancePackStage } from './pack-crm/src/lifecycle';

// Get a pack
const pack = getPack('tax-assist');

// Update deployment status
updatePack('tax-assist', {
  deployment: {
    ...pack.deployment,
    frontendDeployed: true,
  },
});

// Advance stage
advancePackStage('tax-assist', 'build');
```

## File Locations

- **Pack Data**: `pack-crm/data/packs.json`
- **Research Reports**: `pack-crm/research/{slug}-deep-dive.md`
- **Frontend Export**: `src/data/packs.local.json` (generated)
- **Research Template**: `pack-process/CHATGPT_RESEARCH_TEMPLATE.md`

## Environment Variables

- `OPENAI_API_KEY` (required for research scripts): Your OpenAI API key
- `VITE_HARBOR_ADMIN_PASSWORD` (optional): Password for admin dashboard access. If not set, dashboard is accessible without authentication (dev mode only).

## Usage Workflow

### Daily Workflow

1. **Create a new pack idea:**
   ```bash
   pnpm tsx pack-crm/scripts/init-pack.ts new-pack "New Pack Name" --price 499
   ```

2. **Edit CRM fields in `pack-crm/data/packs.json`:**
   - Add `ideaNotes`, `icpSummary`, `primaryPainPoints`, `valueHypothesis`, etc.
   - Use your editor to update the JSON file directly

3. **Visualize in admin dashboard:**
   - Navigate to `/admin` (with password if `VITE_HARBOR_ADMIN_PASSWORD` is set)
   - View all CRM fields, lifecycle status, and gate decisions

4. **Advance through stages:**
   ```bash
   pnpm tsx pack-crm/scripts/advance-stage.ts new-pack validation
   pnpm tsx pack-crm/scripts/advance-stage.ts new-pack scoring --score 85 --gate pass
   ```

5. **Run deep-dive research:**
   ```bash
   export OPENAI_API_KEY=sk-...
   pnpm tsx pack-crm/scripts/run-deep-dive.ts new-pack
   ```

6. **Update gate decision notes:**
   - Edit `crm.gateDecisionNotes` in `pack-crm/data/packs.json` after each gate

### Best Practices

- **Use `init-pack.ts` and CLI scripts** to create/advance packs
- **Use `/admin`** to visualize lifecycle + CRM fields
- **Do NOT store real secrets** in the CRM (no API keys, passwords, or credentials)
- **Keep gate decision notes** updated after each stage gate
- **Export packs for frontend** after making changes: `pnpm tsx pack-crm/scripts/export-packs-for-frontend.ts`

## Integration Points

### With Existing Pack Structure

Packs are stored in `packs/{slug}/` directories. The CRM tracks metadata and lifecycle, but pack content (docs, schemas, etc.) remains in the pack directories.

### With Frontend

The admin dashboard reads from `src/data/packs.local.json`, which is generated by `export-packs-for-frontend.ts`. This is a manual export step (not wired into build yet).

### With Worker

The Worker (`workers/personalized-download/`) currently hardcodes pack mappings. Future integration could read from the CRM to dynamically configure packs.

## Harbor Ops API

The Harbor Ops API (FastAPI) provides REST endpoints for pack management:

- **Location:** `orchestrator/api.py`
- **Start:** `python -m orchestrator api`
- **Base URL:** http://127.0.0.1:8000
- **Documentation:** See `orchestrator/README.md` for full API documentation

**Key Endpoints:**
- `POST /api/packs` - Create new pack
- `PATCH /api/packs/{slug}/crm` - Update CRM fields
- `POST /api/packs/{slug}/runs/research` - Run research pipeline
- `GET /api/revenue/summary` - Get sales summary

**Note:** The API is currently dev/local only. Production deployment is planned for a future release.

## Future Enhancements

- [ ] Wire export into build process
- [x] Add API endpoints for pack operations (Harbor Ops API)
- [ ] Add authentication for admin dashboard
- [x] Add pack editing UI (New Idea form, Run Research button)
- [ ] Integrate with Worker for dynamic pack configuration
- [ ] Add audit trail / change history
- [ ] Add pack validation rules

## Troubleshooting

### "OPENAI_API_KEY is not set"
Set the environment variable:
```bash
export OPENAI_API_KEY=sk-...
```

### "Pack not found"
Ensure the pack exists in `pack-crm/data/packs.json`. You can create it with `init-pack.ts`.

### "Research template not found"
Ensure `pack-process/CHATGPT_RESEARCH_TEMPLATE.md` exists.

### JSON parse errors
Check `pack-crm/data/packs.json` for valid JSON. The file is auto-formatted, but manual edits might introduce errors.

## See Also

- `DEV_AUDIT_harbor_agent.md` - Full project audit
- `pack-process/` - Pack creation process documentation
- `packs/` - Pack content directories

