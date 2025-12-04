"""
Harbor Ops API - FastAPI backend for pack management and orchestration.

Provides REST endpoints for:
- Pack lifecycle management (CRUD)
- CRM data updates
- Research pipeline execution
- Revenue/sales data access
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, List

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

from orchestrator.graph import run_pack_research
from orchestrator.config import (
    load_packs_json,
    save_packs_json,
    get_pack_lifecycle,
    update_pack_lifecycle,
    OPENAI_API_KEY,
)
from orchestrator.state import save_run_state
from orchestrator.puppeteer.loop import run_dynamic_orchestration
from orchestrator.puppeteer.policy_base import PolicyMode
from orchestrator.telemetry.rl_trainer import SimpleRLTrainer

# Initialize OpenAI client
openai_client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI(title="Harbor Ops API", version="0.1.0")

# Enable CORS for local dev and production
# Dev: frontend on localhost:8081, API on 127.0.0.1:8000
# Prod: frontend on harboragent.dev, API on api.harboragent.dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8081",
        "http://127.0.0.1:8081",
        "https://harboragent.dev",
        "https://api.harboragent.dev",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path to revenue data
REVENUE_DATA_PATH = Path(__file__).resolve().parent.parent / "revenue" / "data"
MASTER_LEADS_JSON = REVENUE_DATA_PATH / "master_leads.json"
MASTER_LEADS_CSV = REVENUE_DATA_PATH / "master_leads.csv"
SALES_JSON = REVENUE_DATA_PATH / "sales.json"

# Path to runs directory
RUNS_DIR = Path(__file__).resolve().parent / "data" / "runs"


# ============================================================================
# Pydantic Models
# ============================================================================


class PackCreateRequest(BaseModel):
    """Request model for creating a new pack."""
    slug: str
    name: str
    packNumber: Optional[int] = None
    ideaNotes: Optional[str] = None
    icpSummary: Optional[str] = None
    primaryPainPoints: Optional[List[str]] = None
    valueHypothesis: Optional[str] = None
    pricingNotes: Optional[str] = None
    competitionNotes: Optional[str] = None


class PackCRMUpdateRequest(BaseModel):
    """Request model for updating pack CRM data."""
    ideaNotes: Optional[str] = None
    icpSummary: Optional[str] = None
    primaryPainPoints: Optional[List[str]] = None
    valueHypothesis: Optional[str] = None
    pricingNotes: Optional[str] = None
    competitionNotes: Optional[str] = None


class ResearchRunResponse(BaseModel):
    """Response model for research run execution."""
    runId: str
    packSlug: str
    gate: dict
    artifacts: dict


class RevenueSummaryResponse(BaseModel):
    """Response model for revenue summary."""
    totalLeads: int
    totalSales: Optional[int] = None
    packs: List[dict]
    note: Optional[str] = None


class SaleRecordRequest(BaseModel):
    """Request model for recording a Stripe sale."""
    sessionId: str
    packSlug: str
    customerEmail: str
    amountTotal: int  # in cents
    currency: str = "usd"
    customerName: Optional[str] = None
    organization: Optional[str] = None


class LeadDiscoveryRequest(BaseModel):
    """Request model for lead discovery runs."""
    packSlug: str
    limit: Optional[int] = 25


# ============================================================================
# Pack & CRM Endpoints
# ============================================================================


@app.get("/api/packs")
async def list_packs():
    """
    Get a list of all packs with summary information.
    
    Returns:
        List of pack summaries including slug, name, packNumber, currentStage,
        CRM fields, and research status.
    """
    try:
        packs = load_packs_json()
        
        summaries = []
        for pack in packs:
            summary = {
                "slug": pack.get("slug"),
                "name": pack.get("name"),
                "packNumber": pack.get("packNumber"),
                "currentStage": pack.get("currentStage"),
                "crm": {
                    "ideaNotes": pack.get("crm", {}).get("ideaNotes"),
                    "icpSummary": pack.get("crm", {}).get("icpSummary"),
                    "primaryPainPoints": pack.get("crm", {}).get("primaryPainPoints", []),
                    "valueHypothesis": pack.get("crm", {}).get("valueHypothesis"),
                    "pricingNotes": pack.get("crm", {}).get("pricingNotes"),
                    "competitionNotes": pack.get("crm", {}).get("competitionNotes"),
                    "gateDecisionNotes": pack.get("crm", {}).get("gateDecisionNotes", {}),
                },
                "research": {
                    "researchCompleted": pack.get("research", {}).get("researchCompleted", False),
                },
            }
            summaries.append(summary)
        
        return summaries
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=f"Pack CRM file not found: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading packs: {str(e)}")


@app.get("/api/packs/{slug}")
async def get_pack(slug: str):
    """
    Get the full pack lifecycle data for a specific pack.
    
    Args:
        slug: Pack slug identifier
        
    Returns:
        Complete PackLifecycle dict
        
    Raises:
        404: If pack not found
    """
    pack = get_pack_lifecycle(slug)
    if pack is None:
        raise HTTPException(status_code=404, detail=f"Pack with slug '{slug}' not found")
    return pack


@app.post("/api/packs")
async def create_pack(request: PackCreateRequest):
    """
    Create a new pack in the CRM.
    
    Args:
        request: Pack creation request with required slug and name
        
    Returns:
        Created pack dict
        
    Raises:
        400: If slug already exists
    """
    packs = load_packs_json()
    
    # Check if slug already exists
    for pack in packs:
        if pack.get("slug") == request.slug:
            raise HTTPException(
                status_code=400,
                detail=f"Pack with slug '{request.slug}' already exists"
            )
    
    # Determine pack number
    if request.packNumber is not None:
        pack_number = request.packNumber
    else:
        # Generate next pack number
        max_number = 0
        for pack in packs:
            num = pack.get("packNumber", 0)
            if isinstance(num, int) and num > max_number:
                max_number = num
        pack_number = max_number + 1
    
    # Create timestamp
    now = datetime.utcnow().isoformat() + "Z"
    
    # Build new pack dict
    new_pack = {
        "slug": request.slug,
        "name": request.name,
        "packNumber": pack_number,
        "currentStage": "idea",
        "stages": {
            "idea": {"status": "not_started"},
            "validation": {"status": "not_started"},
            "scoring": {"status": "not_started"},
            "deep_dive": {"status": "not_started"},
            "build": {"status": "not_started"},
            "published": {"status": "not_started"},
        },
        "metadata": {
            "createdAt": now,
            "updatedAt": now,
        },
        "crm": {
            "ideaNotes": request.ideaNotes or "",
            "icpSummary": request.icpSummary or "",
            "primaryPainPoints": request.primaryPainPoints or [],
            "valueHypothesis": request.valueHypothesis or "",
            "pricingNotes": request.pricingNotes or "",
            "competitionNotes": request.competitionNotes or "",
            "gateDecisionNotes": {},
        },
        "research": {
            "researchCompleted": False,
            "researchArtifacts": [],
            "researchNotes": "",
        },
        "deployment": {
            "frontendDeployed": False,
            "workerDeployed": False,
            "stripeConfigured": False,
            "r2Uploaded": False,
        },
    }
    
    # Append and save
    packs.append(new_pack)
    save_packs_json(packs)
    
    return new_pack


@app.patch("/api/packs/{slug}/crm")
async def update_pack_crm(slug: str, request: PackCRMUpdateRequest):
    """
    Update CRM fields for a pack.
    
    Args:
        slug: Pack slug identifier
        request: CRM update request with optional fields
        
    Returns:
        Updated CRM dict
        
    Raises:
        404: If pack not found
    """
    def updater(pack: dict) -> dict:
        """Updater function that merges CRM fields."""
        if "crm" not in pack:
            pack["crm"] = {}
        
        # Update only provided fields
        if request.ideaNotes is not None:
            pack["crm"]["ideaNotes"] = request.ideaNotes
        if request.icpSummary is not None:
            pack["crm"]["icpSummary"] = request.icpSummary
        if request.primaryPainPoints is not None:
            pack["crm"]["primaryPainPoints"] = request.primaryPainPoints
        if request.valueHypothesis is not None:
            pack["crm"]["valueHypothesis"] = request.valueHypothesis
        if request.pricingNotes is not None:
            pack["crm"]["pricingNotes"] = request.pricingNotes
        if request.competitionNotes is not None:
            pack["crm"]["competitionNotes"] = request.competitionNotes
        
        # Update metadata timestamp
        if "metadata" not in pack:
            pack["metadata"] = {}
        pack["metadata"]["updatedAt"] = datetime.utcnow().isoformat() + "Z"
        
        return pack
    
    try:
        updated_pack = update_pack_lifecycle(slug, updater)
        return updated_pack.get("crm", {})
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ============================================================================
# Orchestration Run Endpoints
# ============================================================================


@app.post("/api/packs/{slug}/check-updates")
async def check_pack_updates(slug: str):
    """
    Check for updates to a published pack (regulations, market, users).
    
    This endpoint is designed to be called weekly via cron for published packs.
    It checks for:
    - Regulation/standard changes
    - Market updates
    - User feedback patterns
    - Competitive landscape shifts
    
    Args:
        slug: Pack slug identifier
        
    Returns:
        Update check results with any changes found
        
    Raises:
        404: If pack not found
    """
    # Verify pack exists
    pack = get_pack_lifecycle(slug)
    if pack is None:
        raise HTTPException(status_code=404, detail=f"Pack with slug '{slug}' not found")
    
    # Only check updates for published or build-stage packs
    if pack.get("currentStage") not in ["published", "build"]:
        return {
            "packSlug": slug,
            "status": "skipped",
            "reason": f"Pack is in '{pack.get('currentStage')}' stage. Updates only checked for published/build packs.",
            "updates": [],
        }
    
    # TODO: Implement actual update checks:
    # 1. Check regulation/standard sources for changes
    # 2. Monitor market trends (could use OpenAI to analyze recent news)
    # 3. Aggregate user feedback (if we have a feedback mechanism)
    # 4. Check competitive landscape
    
    # For now, return a placeholder structure
    return {
        "packSlug": slug,
        "status": "checked",
        "checkedAt": datetime.utcnow().isoformat() + "Z",
        "updates": [
            {
                "type": "regulation",
                "status": "no_changes",
                "note": "Regulation check not yet implemented. Will check official sources.",
            },
            {
                "type": "market",
                "status": "no_changes",
                "note": "Market trend analysis not yet implemented.",
            },
        ],
        "note": "Update checking is a placeholder. Implement with actual sources (regulation sites, news APIs, etc.)",
    }


@app.post("/api/packs/{slug}/runs/research", response_model=ResearchRunResponse)
async def run_research_pipeline(slug: str):
    """
    Run the research pipeline for a pack.
    
    Args:
        slug: Pack slug identifier
        
    Returns:
        Research run response with runId, gate, and artifacts
        
    Raises:
        404: If pack not found
        500: If pipeline execution fails
    """
    # Verify pack exists
    pack = get_pack_lifecycle(slug)
    if pack is None:
        raise HTTPException(status_code=404, detail=f"Pack with slug '{slug}' not found")
    
    try:
        # Run the research pipeline (synchronous for v0)
        final_state = run_pack_research(slug)
        
        return ResearchRunResponse(
            runId=final_state["run_id"],
            packSlug=slug,
            gate=final_state.get("gate", {}),
            artifacts=final_state.get("artifacts", {}),
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error running research pipeline: {str(e)}"
        )


@app.get("/api/packs/{slug}/runs")
async def list_pack_runs(slug: str):
    """
    List all research runs for a pack.
    
    Args:
        slug: Pack slug identifier
        
    Returns:
        List of run summaries
    """
    if not RUNS_DIR.exists():
        return []
    
    runs = []
    for run_file in RUNS_DIR.glob("*.json"):
        try:
            with open(run_file, "r", encoding="utf-8") as f:
                state = json.load(f)
            
            # Filter by pack_slug
            if state.get("pack_slug") == slug:
                runs.append({
                    "runId": state.get("run_id"),
                    "gate": state.get("gate", {}),
                    "artifacts": state.get("artifacts", {}),
                    "scores": state.get("scores", {}),
                    # Include timestamps if present
                    "createdAt": state.get("metadata", {}).get("createdAt") if "metadata" in state else None,
                })
        except (json.JSONDecodeError, KeyError):
            # Skip invalid files
            continue
    
    # Sort by runId (most recent first, if we had timestamps we'd use those)
    runs.sort(key=lambda x: x.get("runId", ""), reverse=True)
    
    return runs


@app.get("/api/runs/{run_id}")
async def get_run(run_id: str):
    """
    Get a specific run by run ID.
    
    Args:
        run_id: Run identifier (UUID)
        
    Returns:
        Complete run state dict
        
    Raises:
        404: If run not found
    """
    run_file = RUNS_DIR / f"{run_id}.json"
    
    if not run_file.exists():
        raise HTTPException(status_code=404, detail=f"Run with ID '{run_id}' not found")
    
    try:
        with open(run_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Error reading run file: {str(e)}")


# ============================================================================
# Revenue Endpoints
# ============================================================================


@app.get("/api/revenue/summary", response_model=RevenueSummaryResponse)
async def get_revenue_summary():
    """
    Get revenue/sales summary.
    
    Returns:
        Summary with total leads, sales, and per-pack breakdown
    """
    # Try to load from JSON first, then CSV
    leads_data = None
    
    if MASTER_LEADS_JSON.exists():
        try:
            with open(MASTER_LEADS_JSON, "r", encoding="utf-8") as f:
                leads_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    
    if leads_data is None and MASTER_LEADS_CSV.exists():
        # For now, just count lines (skip header)
        try:
            with open(MASTER_LEADS_CSV, "r", encoding="utf-8") as f:
                lines = f.readlines()
                # Subtract 1 for header, count non-empty lines
                total_leads = sum(1 for line in lines[1:] if line.strip())
                leads_data = {"total": total_leads, "leads": []}
        except Exception:
            pass
    
    if leads_data is None:
        return RevenueSummaryResponse(
            totalLeads=0,
            totalSales=None,
            packs=[],
            note="No leads data found yet. Revenue data structure TBD.",
        )
    
    # If it's a dict with a list of leads
    if isinstance(leads_data, dict):
        leads_list = leads_data.get("leads", [])
        if not leads_list and "total" in leads_data:
            # Simple count structure
            return RevenueSummaryResponse(
                totalLeads=leads_data.get("total", 0),
                totalSales=None,
                packs=[],
                note="Leads data structure is TBD. Summary not fully implemented.",
            )
    elif isinstance(leads_data, list):
        leads_list = leads_data
    else:
        leads_list = []
    
    # Count total leads
    total_leads = len(leads_list)
    
    # Load sales data
    total_sales = None
    sales_data = []
    if SALES_JSON.exists():
        try:
            with open(SALES_JSON, "r", encoding="utf-8") as f:
                sales_data = json.load(f).get("sales", [])
                total_sales = len(sales_data)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    
    # Group by pack (if there's a packSlug or similar field)
    pack_counts = {}
    for lead in leads_list:
        if isinstance(lead, dict):
            # Try to find pack association
            pack_slug = lead.get("packSlug") or lead.get("pack_slug") or lead.get("pack")
            if pack_slug:
                if pack_slug not in pack_counts:
                    pack_counts[pack_slug] = {"leads": 0, "sales": 0, "revenue": 0}
                pack_counts[pack_slug]["leads"] += 1
    
    # Add sales data to pack counts
    for sale in sales_data:
        if isinstance(sale, dict):
            pack_slug = sale.get("packSlug")
            if pack_slug:
                if pack_slug not in pack_counts:
                    pack_counts[pack_slug] = {"leads": 0, "sales": 0, "revenue": 0}
                pack_counts[pack_slug]["sales"] += 1
                pack_counts[pack_slug]["revenue"] += sale.get("amountTotal", 0)
    
    packs = [
        {
            "slug": slug,
            "leads": counts["leads"],
            "sales": counts["sales"],
            "revenue": counts.get("revenue", 0) / 100.0,  # Convert cents to dollars
        }
        for slug, counts in pack_counts.items()
    ]
    
    return RevenueSummaryResponse(
        totalLeads=total_leads,
        totalSales=total_sales,
        packs=packs,
        note=None if total_leads > 0 else "Leads data structure is TBD. Summary not fully implemented.",
    )


@app.post("/api/revenue/sales")
async def record_sale(request: SaleRecordRequest):
    """
    Record a Stripe sale to revenue data.
    
    Called by Stripe webhook handler to track sales.
    
    Args:
        request: Sale record with session ID, pack slug, customer info, and amount
        
    Returns:
        Confirmation message
    """
    # Load existing sales or create new list
    sales = []
    if SALES_JSON.exists():
        try:
            with open(SALES_JSON, "r", encoding="utf-8") as f:
                data = json.load(f)
                sales = data.get("sales", []) if isinstance(data, dict) else data
        except (json.JSONDecodeError, FileNotFoundError):
            sales = []
    
    # Create sale record
    sale_record = {
        "sessionId": request.sessionId,
        "packSlug": request.packSlug,
        "customerEmail": request.customerEmail,
        "customerName": request.customerName,
        "organization": request.organization,
        "amountTotal": request.amountTotal,
        "currency": request.currency,
        "purchasedAt": datetime.utcnow().isoformat() + "Z",
    }
    
    # Check if sale already exists (idempotent)
    existing = next((s for s in sales if s.get("sessionId") == request.sessionId), None)
    if existing:
        return {"status": "already_recorded", "sale": existing}
    
    # Add to sales list
    sales.append(sale_record)
    
    # Save to JSON file
    SALES_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(SALES_JSON, "w", encoding="utf-8") as f:
        json.dump({"sales": sales, "lastUpdated": datetime.utcnow().isoformat() + "Z"}, f, indent=2)
    
    return {"status": "recorded", "sale": sale_record}


@app.get("/api/revenue/leads")
async def get_revenue_leads(limit: Optional[int] = None):
    """
    Get raw leads data.
    
    Args:
        limit: Optional limit on number of leads to return
        
    Returns:
        List of leads (or empty list if data not found)
    """
    leads_data = None
    
    if MASTER_LEADS_JSON.exists():
        try:
            with open(MASTER_LEADS_JSON, "r", encoding="utf-8") as f:
                leads_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    
    if leads_data is None and MASTER_LEADS_CSV.exists():
        # For CSV, return a note that JSON is preferred
        return {
            "leads": [],
            "note": "Leads data exists as CSV. JSON format preferred for API access.",
        }
    
    if leads_data is None:
        return {
            "leads": [],
            "note": "No leads data found yet.",
        }
    
    # Extract leads list
    if isinstance(leads_data, dict):
        leads_list = leads_data.get("leads", [])
    elif isinstance(leads_data, list):
        leads_list = leads_data
    else:
        leads_list = []
    
    # Apply limit if specified
    if limit is not None and limit > 0:
        leads_list = leads_list[:limit]
    
    return {"leads": leads_list}


@app.post("/api/revenue/lead-discovery-runs")
async def create_lead_discovery_run(request: LeadDiscoveryRequest):
    """
    Stub endpoint for LinkedIn ICP discovery agent integration.
    
    Args:
        request: Lead discovery request with packSlug and limit
        
    Returns:
        Status message indicating not implemented
    """
    return {
        "status": "not_implemented",
        "message": "LinkedIn ICP discovery agent integration is TBD",
        "packSlug": request.packSlug,
        "limit": request.limit,
    }


# ============================================================================
# Health Check
# ============================================================================


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "service": "Harbor Ops API",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


# ============================================================================
# Audio Transcription Endpoint
# ============================================================================


@app.post("/api/transcribe")
async def transcribe_audio(audio_file: UploadFile = File(...)):
    """
    Transcribe audio using OpenAI Whisper API.
    
    Accepts audio files (mp3, mp4, mpeg, mpga, m4a, wav, webm) and returns
    transcribed text using OpenAI's Whisper model.
    
    Args:
        audio_file: Audio file to transcribe
        
    Returns:
        JSON with transcribed text
        
    Raises:
        400: If file format is not supported
        500: If transcription fails
    """
    # Whisper supports: mp3, mp4, mpeg, mpga, m4a, wav, webm
    # We'll be lenient with content-type since browsers vary
    # and let OpenAI handle format validation
    
    try:
        # Read audio file content
        audio_content = await audio_file.read()
        
        # Create a temporary file-like object for OpenAI
        import io
        
        # OpenAI SDK expects a file-like object with a name attribute
        # Create a BytesIO object and set the name
        audio_file_obj = io.BytesIO(audio_content)
        # Determine file extension from content type or filename
        filename = audio_file.filename or "audio.webm"
        if not filename.endswith(('.mp3', '.mp4', '.mpeg', '.mpga', '.m4a', '.wav', '.webm')):
            # Default to webm if extension unclear
            filename = "audio.webm"
        audio_file_obj.name = filename
        
        # Transcribe using OpenAI Whisper
        transcript = openai_client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file_obj,
            language="en",  # Optional: specify language for better accuracy
        )
        
        return {
            "text": transcript.text,
            "language": getattr(transcript, "language", "en"),
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Transcription failed: {str(e)}"
        )

