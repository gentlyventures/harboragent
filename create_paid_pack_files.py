#!/usr/bin/env python3
"""
Create paid pack files by extracting and organizing content from DOCX
"""
import re
from pathlib import Path

def find_and_extract(text, start_markers, end_markers=None, max_chars=50000):
    """Find content between markers"""
    for marker in start_markers:
        match = re.search(marker, text, re.IGNORECASE | re.DOTALL)
        if match:
            start = match.end()
            
            # Find end marker
            end = len(text)
            if end_markers:
                for end_marker in end_markers:
                    end_match = re.search(end_marker, text[start:], re.IGNORECASE)
                    if end_match:
                        end = min(end, start + end_match.start())
                        break
            
            content = text[start:end].strip()
            # Limit size
            if len(content) > max_chars:
                content = content[:max_chars] + "\n\n[... content truncated ...]"
            return content
    return None

# Read full content
with open('private_source/extracted_content.txt', 'r', encoding='utf-8') as f:
    full_content = f.read()

output_base = Path('dist/paid-pack')
output_base.mkdir(parents=True, exist_ok=True)

# Extract and save README.md
readme_content = find_and_extract(
    full_content,
    [r'README\.md', r'Harbor Agent Genesis Paid Pack – README'],
    [r'LICENSE-HARBOR-AGENT', r'Differentiation']
)
if readme_content:
    (output_base / 'README.md').write_text(readme_content[:30000], encoding='utf-8')
    print("✓ README.md")

# Extract LICENSE
license_content = find_and_extract(
    full_content,
    [r'LICENSE-HARBOR-AGENT', r'Harbor Agent Paid Pack License'],
    [r'Stripe_Product', r'Differentiation']
)
if license_content:
    (output_base / 'LICENSE-HARBOR-AGENT.md').write_text(license_content[:20000], encoding='utf-8')
    print("✓ LICENSE-HARBOR-AGENT.md")

# Extract Checklist
checklist_content = find_and_extract(
    full_content,
    [r'Genesis_Readiness_Checklist', r'Genesis Readiness Checklist.*Expanded'],
    [r'Internal_Proposal', r'Executive_Briefing']
)
if checklist_content:
    (output_base / 'checklist' / 'genesis-checklist-full.md').write_text(
        checklist_content[:50000], encoding='utf-8'
    )
    print("✓ checklist/genesis-checklist-full.md")

# Extract Proposal Kit
proposal_content = find_and_extract(
    full_content,
    [r'Internal_Proposal_Kit', r'Partner Proposal Template'],
    [r'Executive_Briefing', r'Governance_Binder']
)
if proposal_content:
    (output_base / 'proposal-kit' / 'proposal-template.md').write_text(
        proposal_content[:40000], encoding='utf-8'
    )
    print("✓ proposal-kit/proposal-template.md")

# Extract Executive Briefing
exec_content = find_and_extract(
    full_content,
    [r'Executive_Briefing_Template', r'Executive Briefing Template'],
    [r'Governance_Binder', r'AI_Copilot']
)
if exec_content:
    (output_base / 'proposal-kit' / 'executive-brief-template.md').write_text(
        exec_content[:30000], encoding='utf-8'
    )
    print("✓ proposal-kit/executive-brief-template.md")

# Extract AI Copilot Playbook - General
ai_gen_content = find_and_extract(
    full_content,
    [r'IDE_Prompts\.md', r'Harbor Agent – AI Coding Assistant Prompts', r'30\+ Prompts'],
    [r'QA_Audit', r'Prompt_Pack_DevSecOps']
)
if ai_gen_content:
    (output_base / 'ai-copilot-playbooks' / 'general-playbook.md').write_text(
        ai_gen_content[:60000], encoding='utf-8'
    )
    print("✓ ai-copilot-playbooks/general-playbook.md")

# Extract QA Prompts
qa_content = find_and_extract(
    full_content,
    [r'QA_Audit_SelfHealing', r'QA, Audit, and Self-Healing Guidance'],
    [r'Prompt_Pack_DevSecOps', r'Schema_Tooling']
)
if qa_content:
    (output_base / 'ai-copilot-playbooks' / 'qa-prompts.md').write_text(
        qa_content[:40000], encoding='utf-8'
    )
    print("✓ ai-copilot-playbooks/qa-prompts.md")

# Extract DevSecOps Prompts
devsecops_content = find_and_extract(
    full_content,
    [r'Prompt_Pack_DevSecOps', r'Team Prompt Pack – DevSecOps'],
    [r'Prompt_Pack_Data', r'Schema_Tooling']
)
if devsecops_content:
    (output_base / 'ai-copilot-playbooks' / 'prompts-devsecops.md').write_text(
        devsecops_content[:40000], encoding='utf-8'
    )
    print("✓ ai-copilot-playbooks/prompts-devsecops.md")

# Extract Data Engineering Prompts
dataeng_content = find_and_extract(
    full_content,
    [r'Prompt_Pack_Data_Engineering', r'Team Prompt Pack – Data Engineering'],
    [r'Prompt_Pack_ML', r'Schema_Tooling']
)
if dataeng_content:
    (output_base / 'ai-copilot-playbooks' / 'prompts-data-eng.md').write_text(
        dataeng_content[:40000], encoding='utf-8'
    )
    print("✓ ai-copilot-playbooks/prompts-data-eng.md")

# Extract ML Engineering Prompts  
ml_content = find_and_extract(
    full_content,
    [r'Prompt_Pack_ML', r'Team Prompt Pack – ML Engineering'],
    [r'Schema_Tooling', r'Rollout']
)
if ml_content:
    (output_base / 'ai-copilot-playbooks' / 'prompts-ml.md').write_text(
        ml_content[:40000], encoding='utf-8'
    )
    print("✓ ai-copilot-playbooks/prompts-ml.md")

# Extract Self-Healing (may overlap with QA)
selfheal_content = find_and_extract(
    full_content,
    [r'self-healing', r'Self-Healing.*Guidance', r'Repository Drift Detection'],
    [r'Prompt_Pack', r'Schema_Tooling']
)
if selfheal_content and len(selfheal_content) > 1000:
    (output_base / 'ai-copilot-playbooks' / 'self-healing.md').write_text(
        selfheal_content[:40000], encoding='utf-8'
    )
    print("✓ ai-copilot-playbooks/self-healing.md")

# Extract Rollout Guide
rollout_content = find_and_extract(
    full_content,
    [r'Rollout_Guide', r'Rollout Guide.*Training', r'Step-by-step rollout'],
    [r'README', r'LICENSE', r'Differentiation']
)
if rollout_content:
    (output_base / 'rollout' / 'org-rollout-guide.md').write_text(
        rollout_content[:50000], encoding='utf-8'
    )
    print("✓ rollout/org-rollout-guide.md")

# Extract Governance sections
gov_patterns = [
    (r'AI_Use_Policy|AI Use Policy Template', 'governance-binder/data-policy.md'),
    (r'Data_Handling_Policy|Data Handling Policy Template', 'governance-binder/data-policy.md'),
    (r'Risk_Management_Policy|Risk Management Policy Template', 'governance-binder/risk-management-plan.md'),
    (r'Access_Control.*Procedure|Access Control.*Documentation', 'governance-binder/access-controls.md'),
    (r'Internal_SOP|Standard Operating Procedure', 'governance-binder/sop-index.md'),
]

for pattern, filepath in gov_patterns:
    content = find_and_extract(full_content, [pattern], [r'AI_Use|Data_Handling|Risk_Management|Access_Control|Internal_SOP|AI_Copilot'])
    if content and len(content) > 500:
        (output_base / filepath).write_text(content[:30000], encoding='utf-8')
        print(f"✓ {filepath}")

print("\n✓ File extraction complete!")

