#!/usr/bin/env python3
"""
Parse extracted DOCX content and split into structured paid pack files
"""
import re
import os
from pathlib import Path

def extract_section(text, start_pattern, end_pattern=None, include_start=True):
    """Extract a section of text between patterns"""
    start_match = re.search(start_pattern, text, re.IGNORECASE | re.MULTILINE)
    if not start_match:
        return None
    
    start_idx = start_match.start() if include_start else start_match.end()
    
    if end_pattern:
        end_match = re.search(end_pattern, text[start_idx:], re.IGNORECASE | re.MULTILINE)
        if end_match:
            return text[start_idx:start_idx + end_match.start()].strip()
    else:
        # No end pattern, return everything from start
        return text[start_idx:].strip()
    
    return text[start_idx:].strip()

def clean_markdown(text):
    """Clean up markdown formatting issues"""
    # Remove excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Fix spacing around headers
    text = re.sub(r'([^\n])\n([#])', r'\1\n\n\2', text)
    # Remove trailing spaces
    text = '\n'.join(line.rstrip() for line in text.split('\n'))
    return text.strip()

def split_content(content):
    """Split content into sections based on known patterns"""
    sections = {}
    
    # README.md
    readme_pattern = r'README\.md|Harbor Agent Genesis Paid Pack – README'
    sections['README.md'] = extract_section(content, readme_pattern, r'LICENSE-HARBOR-AGENT|Differentiation|Stripe_Product')
    
    # LICENSE
    license_pattern = r'LICENSE-HARBOR-AGENT\.md|Harbor Agent Paid Pack License'
    sections['LICENSE-HARBOR-AGENT.md'] = extract_section(content, license_pattern, r'Stripe_Product|Differentiation|README')
    
    # Genesis Readiness Checklist
    checklist_pattern = r'Genesis_Readiness_Checklist\.md|Genesis Readiness Checklist.*Expanded|This checklist covers.*Data.*Models'
    sections['checklist/genesis-checklist-full.md'] = extract_section(content, checklist_pattern, r'Internal_Proposal|Executive_Briefing|AI_Copilot')
    
    # Internal Proposal Kit
    proposal_pattern = r'Internal_Proposal_Kit\.md|Internal Proposal|Partner Proposal Template'
    sections['proposal-kit/proposal-template.md'] = extract_section(content, proposal_pattern, r'Executive_Briefing|Governance_Binder|AI_Copilot')
    
    # Executive Briefing
    exec_pattern = r'Executive_Briefing_Template\.md|Executive Briefing Template'
    sections['proposal-kit/executive-brief-template.md'] = extract_section(content, exec_pattern, r'Governance_Binder|AI_Copilot|Schema')
    
    # Governance Binder sections
    gov_patterns = [
        (r'AI_Use_Policy|AI Use Policy Template', 'governance-binder/data-policy.md'),
        (r'Data_Handling_Policy|Data Handling Policy', 'governance-binder/data-policy.md'),
        (r'Risk_Management_Policy|Risk Management Policy', 'governance-binder/risk-management-plan.md'),
        (r'Access_Control|Access Control.*Procedure', 'governance-binder/access-controls.md'),
        (r'Internal_SOP|Standard Operating Procedure', 'governance-binder/sop-index.md'),
    ]
    
    for pattern, filename in gov_patterns:
        if filename not in sections:
            sections[filename] = extract_section(content, pattern, r'(?:AI_Copilot|Schema|Rollout)')
    
    # AI Copilot Playbook sections
    ai_patterns = [
        (r'IDE_Prompts\.md|Harbor Agent – AI Coding Assistant Prompts|30\+ Prompts for Copilot', 'ai-copilot-playbooks/general-playbook.md'),
        (r'QA_Audit_SelfHealing|QA, Audit, and Self-Healing Guidance', 'ai-copilot-playbooks/qa-prompts.md'),
        (r'self-healing|Self-Healing.*Guidance', 'ai-copilot-playbooks/self-healing.md'),
        (r'Prompt_Pack_DevSecOps|Team Prompt Pack – DevSecOps', 'ai-copilot-playbooks/prompts-devsecops.md'),
        (r'Prompt_Pack_Data_Engineering|Team Prompt Pack – Data Engineering', 'ai-copilot-playbooks/prompts-data-eng.md'),
        (r'Prompt_Pack_ML|Team Prompt Pack – ML Engineering|ML Engineering Focus', 'ai-copilot-playbooks/prompts-ml.md'),
    ]
    
    for pattern, filename in ai_patterns:
        content_section = extract_section(content, pattern, r'(?:Prompt_Pack|Schema|Rollout|README)')
        if content_section:
            if filename in sections:
                sections[filename] += '\n\n' + content_section
            else:
                sections[filename] = content_section
    
    # Schema Tooling
    schema_pattern = r'validate_genesis_metadata\.py|Schema_Tooling|Schema Validation Scripts'
    sections['automation-scripts/schema-validate.py'] = extract_section(content, schema_pattern, r'Rollout|README')
    
    # Rollout Guide
    rollout_pattern = r'Rollout_Guide|Rollout Guide.*Training|Step-by-step rollout'
    sections['rollout/org-rollout-guide.md'] = extract_section(content, rollout_pattern, r'README|LICENSE|Differentiation')
    
    # Model Card Template (may be in governance)
    model_card_pattern = r'Model.*Card.*Template|model card'
    if re.search(model_card_pattern, content, re.IGNORECASE):
        sections['governance-binder/model-card-template.md'] = extract_section(content, model_card_pattern, r'Access_Control|Risk_Management')
    
    # Compliance Readiness
    compliance_pattern = r'Compliance.*Readiness|compliance.*audit'
    if re.search(compliance_pattern, content, re.IGNORECASE):
        sections['governance-binder/compliance-readiness.md'] = extract_section(content, compliance_pattern, r'Model.*Card|Access_Control')
    
    return sections

def main():
    """Main parsing function"""
    # Read extracted content
    with open('private_source/extracted_content.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into sections
    sections = split_content(content)
    
    # Create output directory
    output_dir = Path('dist/paid-pack')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Write sections to files
    for filepath, filecontent in sections.items():
        if not filecontent or len(filecontent.strip()) < 50:
            continue  # Skip empty or too-short sections
        
        full_path = output_dir / filepath
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        cleaned = clean_markdown(filecontent)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(cleaned)
        
        print(f"Created: {filepath} ({len(cleaned)} chars)")
    
    print(f"\nParsed {len(sections)} files")

if __name__ == '__main__':
    main()

