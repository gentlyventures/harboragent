"""
Deep research node: Generate comprehensive research report using OpenAI.
"""

from datetime import datetime
from pathlib import Path
from orchestrator.config import OPENAI_API_KEY, get_pack_lifecycle, update_pack_lifecycle
from orchestrator.state import State
from openai import OpenAI


def deep_research_node(state: State) -> State:
    """
    Deep research node: Generate comprehensive research report.
    
    Only runs if gate.scoring == "pass".
    
    Reads:
    - pack-process/CHATGPT_RESEARCH_TEMPLATE.md
    - Pack lifecycle for metadata
    
    Generates:
    - Deep dive report saved to pack-crm/research/{pack_slug}-{run_id}-deep-dive.md
    - Updates pack lifecycle with research completion status
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with artifacts.deep_dive_report_path and notes.deep_dive_summary
    """
    gate_scoring = state["gate"].get("scoring")
    
    # Only proceed if scoring gate passed
    if gate_scoring != "pass":
        print(f"⏭️  Deep Research: Skipping (scoring gate: {gate_scoring})")
        return state
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    pack_slug = state["pack_slug"]
    run_id = state["run_id"]
    pack_snapshot = state["pack_snapshot"]
    
    # Load fresh pack lifecycle to get latest state
    pack_lifecycle = get_pack_lifecycle(pack_slug)
    if not pack_lifecycle:
        raise ValueError(f"Pack '{pack_slug}' not found")
    
    # Read research template
    template_path = (
        Path(__file__).resolve().parent.parent.parent
        / "pack-process"
        / "CHATGPT_RESEARCH_TEMPLATE.md"
    )
    
    if not template_path.exists():
        raise FileNotFoundError(
            f"Research template not found: {template_path}\n"
            "Please ensure pack-process/CHATGPT_RESEARCH_TEMPLATE.md exists."
        )
    
    with open(template_path, "r", encoding="utf-8") as f:
        template_text = f.read()
    
    # Extract pack metadata
    metadata = pack_lifecycle.get("metadata", {})
    crm = pack_lifecycle.get("crm", {})
    
    regulation_name = metadata.get("regulationName", "Unknown regulation")
    target_audience = metadata.get("targetAudience", [])
    price = metadata.get("price", 0)
    price_dollars = price / 100 if price else 0
    
    icp_summary = crm.get("icpSummary", "No ICP summary provided")
    pack_name = pack_lifecycle.get("name", "Unknown Pack")
    pack_number = pack_lifecycle.get("packNumber", "?")
    
    # Build deep dive prompt
    prompt = f"""You are an AI research assistant for Harbor Agent, creating comprehensive compliance and readiness documentation.

# Pack Metadata
```json
{{
  "packSlug": "{pack_slug}",
  "packName": "{pack_name}",
  "packNumber": {pack_number},
  "regulationName": "{regulation_name}",
  "targetAudience": {target_audience},
  "currentStage": "{pack_lifecycle.get('currentStage', 'unknown')}",
  "price": "${price_dollars:.2f}"
}}
```

# Research Context
You are conducting deep-dive research for the **{pack_name}** (Pack #{pack_number}).

**Regulation/Standard:** {regulation_name}

**Target Audience:**
{chr(10).join(f"- {audience}" for audience in target_audience) if target_audience else "- Not specified"}

**ICP Summary:**
{icp_summary}

# Instructions
Please use the following research template to conduct comprehensive research and produce all necessary content for this pack. Replace all placeholders in the template with specific information about **{regulation_name}**.

---

{template_text}

---

# Additional Notes
- This research will be used to create a Harbor Agent compliance pack
- Focus on engineering and developer-ready content
- Make content AI-copilot friendly (for Cursor, GitHub Copilot, etc.)
- Provide actionable, practical guidance
- Include code examples and templates where relevant

Please provide complete output for all 16 sections of the template, tailored specifically to **{regulation_name}**.

After the full report, please provide a 1-2 paragraph executive summary that can be used as a deep_dive_summary."""

    print("🤖 Deep Research: Calling OpenAI for comprehensive research report...")
    
    # Call OpenAI
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert research assistant specializing in compliance, regulations, "
                    "and engineering toolkits. Provide comprehensive, accurate, and actionable content."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=8000  # Allow for long research reports
    )
    
    report_content = response.choices[0].message.content
    
    # Extract summary if it's at the end (look for "executive summary" or similar)
    # For now, we'll use a simple approach: ask for summary in a follow-up if needed
    # Or extract from the report content
    summary = "Deep dive research completed. See full report for details."
    
    # Try to extract summary from report if it contains one
    if "executive summary" in report_content.lower() or "summary" in report_content.lower():
        # Look for summary section
        lines = report_content.split("\n")
        summary_lines = []
        in_summary = False
        for line in lines:
            if "summary" in line.lower() and ("executive" in line.lower() or "deep_dive" in line.lower()):
                in_summary = True
                continue
            if in_summary and line.strip():
                summary_lines.append(line.strip())
                if len(summary_lines) >= 5:  # Limit summary length
                    break
        
        if summary_lines:
            summary = " ".join(summary_lines)
    
    # Save report
    research_dir = Path(__file__).resolve().parent.parent.parent / "pack-crm" / "research"
    research_dir.mkdir(parents=True, exist_ok=True)
    
    report_filename = f"{pack_slug}-{run_id}-deep-dive.md"
    report_path = research_dir / report_filename
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
    
    # Update state
    state["artifacts"]["deep_dive_report_path"] = str(report_path)
    state["notes"]["deep_dive_summary"] = summary
    
    # Update pack lifecycle
    now = datetime.utcnow().isoformat() + "Z"
    
    def update_pack(pack: dict) -> dict:
        # Update research
        research = pack.get("research", {})
        research["researchCompleted"] = True
        
        # Add report to artifacts
        artifacts = research.get("researchArtifacts", [])
        if str(report_path) not in artifacts:
            artifacts.append(str(report_path))
        research["researchArtifacts"] = artifacts
        pack["research"] = research
        
        # Update deep_dive stage
        stages = pack.get("stages", {})
        deep_dive_stage = stages.get("deep_dive", {})
        deep_dive_stage["status"] = "completed"
        if not deep_dive_stage.get("startedAt"):
            deep_dive_stage["startedAt"] = now
        deep_dive_stage["completedAt"] = now
        
        # Add report to stage artifacts
        stage_artifacts = deep_dive_stage.get("researchArtifacts", [])
        if str(report_path) not in stage_artifacts:
            stage_artifacts.append(str(report_path))
        deep_dive_stage["researchArtifacts"] = stage_artifacts
        stages["deep_dive"] = deep_dive_stage
        pack["stages"] = stages
        
        # Update current stage if needed
        if pack.get("currentStage") != "deep_dive":
            pack["currentStage"] = "deep_dive"
        
        # Update CRM gate decision notes
        crm = pack.get("crm", {})
        gate_notes = crm.get("gateDecisionNotes", {})
        gate_notes["deep_dive"] = summary
        crm["gateDecisionNotes"] = gate_notes
        pack["crm"] = crm
        
        # Update metadata timestamp
        metadata = pack.get("metadata", {})
        metadata["updatedAt"] = now
        pack["metadata"] = metadata
        
        return pack
    
    update_pack_lifecycle(pack_slug, update_pack)
    
    print(f"✅ Deep Research: Report saved to {report_path}")
    print(f"   Summary: {summary[:100]}...")
    
    return state

