"""
Validation node: Use OpenAI to assess pack viability.
"""

import json
from datetime import datetime
from orchestrator.config import OPENAI_API_KEY, update_pack_lifecycle
from orchestrator.state import State
from openai import OpenAI


def validation_node(state: State) -> State:
    """
    Validation node: Use OpenAI to produce viability assessment.
    
    Sets:
    - scores.viability (0-100)
    - scores.data_availability (0-100)
    - scores.icp_clarity (0-100)
    - notes.validation_rationale
    
    Updates pack lifecycle:
    - stages.validation.status = "completed"
    - crm.gateDecisionNotes.validation
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with scores and notes
    """
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    pack_snapshot = state["pack_snapshot"]
    pack_slug = state["pack_slug"]
    
    # Extract relevant fields
    crm = pack_snapshot.get("crm", {})
    metadata = pack_snapshot.get("metadata", {})
    
    idea_notes = crm.get("ideaNotes") or "No idea notes provided"
    icp_summary = crm.get("icpSummary") or "No ICP summary provided"
    regulation_name = metadata.get("regulationName", "Unknown regulation")
    target_audience = metadata.get("targetAudience", [])
    
    # Build validation prompt
    prompt = f"""You are an AI research assistant evaluating a Harbor Agent compliance pack idea.

Pack Information:
- Regulation/Standard: {regulation_name}
- Target Audience: {', '.join(target_audience) if target_audience else 'Not specified'}

Idea Notes:
{idea_notes}

ICP Summary:
{icp_summary}

Please evaluate this pack idea and provide:
1. Viability Score (0-100): How viable is this pack idea? Consider market need, clarity of value proposition, and feasibility.
2. Data Availability Score (0-100): How readily available is the information needed to create this pack? Consider regulation documentation, research sources, and existing knowledge.
3. ICP Clarity Score (0-100): How clear and well-defined is the target audience? Consider specificity, accessibility, and market size.

Provide your response in the following JSON format:
{{
  "viability": <0-100 integer>,
  "data_availability": <0-100 integer>,
  "icp_clarity": <0-100 integer>,
  "rationale": "<2-3 sentence explanation of the scores>"
}}"""

    print("🤖 Validation: Calling OpenAI for viability assessment...")
    
    # Call OpenAI
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are an expert at evaluating business ideas and compliance pack concepts. Provide accurate, thoughtful assessments with clear reasoning."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        response_format={"type": "json_object"}
    )
    
    # Parse response
    result = json.loads(response.choices[0].message.content)
    
    viability = int(result.get("viability", 0))
    data_availability = int(result.get("data_availability", 0))
    icp_clarity = int(result.get("icp_clarity", 0))
    rationale = result.get("rationale", "No rationale provided")
    
    # Update state
    state["scores"]["viability"] = viability
    state["scores"]["data_availability"] = data_availability
    state["scores"]["icp_clarity"] = icp_clarity
    state["notes"]["validation_rationale"] = rationale
    
    # Determine validation gate
    # Simple rule: pass if viability >= 60
    validation_gate = "pass" if viability >= 60 else "fail"
    state["gate"]["validation"] = validation_gate
    
    # Update pack lifecycle
    now = datetime.utcnow().isoformat() + "Z"
    
    def update_pack(pack: dict) -> dict:
        # Update validation stage
        stages = pack.get("stages", {})
        validation_stage = stages.get("validation", {})
        validation_stage["status"] = "completed"
        if not validation_stage.get("startedAt"):
            validation_stage["startedAt"] = now
        validation_stage["completedAt"] = now
        stages["validation"] = validation_stage
        pack["stages"] = stages
        
        # Update CRM gate decision notes
        crm = pack.get("crm", {})
        gate_notes = crm.get("gateDecisionNotes", {})
        gate_notes["validation"] = (
            f"Validation {'passed' if validation_gate == 'pass' else 'failed'}. "
            f"Scores: Viability={viability}, Data Availability={data_availability}, "
            f"ICP Clarity={icp_clarity}. {rationale}"
        )
        crm["gateDecisionNotes"] = gate_notes
        pack["crm"] = crm
        
        # Update metadata timestamp
        metadata = pack.get("metadata", {})
        metadata["updatedAt"] = now
        pack["metadata"] = metadata
        
        return pack
    
    update_pack_lifecycle(pack_slug, update_pack)
    
    print(f"✅ Validation: Scores - Viability={viability}, Data={data_availability}, ICP={icp_clarity}")
    print(f"   Gate: {validation_gate.upper()}")
    
    return state

