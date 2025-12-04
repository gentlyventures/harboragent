"""
Configuration and pack-crm integration helpers.

Provides safe read/write access to pack-crm/data/packs.json.
"""

import json
import os
from pathlib import Path
from typing import Callable, Optional

from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Path to pack-crm/data/packs.json relative to orchestrator folder
PACK_CRM_PATH = Path(__file__).resolve().parent.parent / "pack-crm" / "data" / "packs.json"

# OpenAI API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY environment variable is not set. "
        "Please set it in your .env file or environment."
    )


def load_packs_json() -> list[dict]:
    """
    Load packs.json and return list of PackLifecycle dicts.
    
    Returns:
        List of pack dictionaries
        
    Raises:
        FileNotFoundError: If packs.json doesn't exist
        json.JSONDecodeError: If JSON is invalid
    """
    if not PACK_CRM_PATH.exists():
        raise FileNotFoundError(
            f"Pack CRM file not found: {PACK_CRM_PATH}\n"
            "Please ensure pack-crm/data/packs.json exists."
        )
    
    with open(PACK_CRM_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    if not isinstance(data, list):
        raise ValueError(f"Expected list in packs.json, got {type(data)}")
    
    return data


def save_packs_json(packs: list[dict]) -> None:
    """
    Save packs list back to packs.json.
    
    Preserves JSON structure and key order (Python 3.7+ maintains dict insertion order).
    Note: May normalize trailing whitespace (e.g., trailing newline), but all data
    structures and key orders are preserved.
    
    Args:
        packs: List of pack dictionaries to save
        
    Raises:
        IOError: If file cannot be written
    """
    # Ensure directory exists
    PACK_CRM_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # Write JSON with consistent formatting
    # Using indent=2 and ensure_ascii=False to match typical JSON formatting
    # sort_keys=False preserves dictionary key order (Python 3.7+)
    with open(PACK_CRM_PATH, "w", encoding="utf-8") as f:
        json.dump(packs, f, indent=2, ensure_ascii=False, sort_keys=False)
        # Add trailing newline for consistency with typical file formatting
        f.write("\n")
    
    print(f"✅ Updated pack CRM: {PACK_CRM_PATH}")


def get_pack_lifecycle(slug: str) -> Optional[dict]:
    """
    Get a pack lifecycle dict by slug.
    
    Args:
        slug: Pack slug identifier
        
    Returns:
        Pack dict if found, None otherwise
    """
    packs = load_packs_json()
    
    for pack in packs:
        if pack.get("slug") == slug:
            # Return a copy to avoid accidental mutations
            return pack.copy()
    
    return None


def update_pack_lifecycle(slug: str, updater_fn: Callable[[dict], dict]) -> dict:
    """
    Update a pack lifecycle using an updater function.
    
    CRITICAL: This function must preserve all unknown keys and maintain JSON structure
    because pack-crm/data/packs.json is the TypeScript domain's source of truth. The
    orchestrator should only perform surgical, in-place mutations of specific fields
    (e.g., stages, crm.gateDecisionNotes, research artifacts) without dropping or
    reordering any existing fields.
    
    This function:
    1. Loads all packs
    2. Finds the pack with the given slug
    3. Calls updater_fn(pack_dict) which returns an updated pack_dict
    4. Replaces that entry in the list
    5. Saves back to packs.json
    6. Returns the updated pack dict
    
    IMPORTANT: updater_fn must preserve unknown keys. It should only
    mutate relevant fields, preserving existing crm, stages, deployment, etc.
    Use dict.copy() and update specific nested structures rather than rebuilding
    the entire dict.
    
    Args:
        slug: Pack slug identifier
        updater_fn: Function that takes a pack dict and returns an updated pack dict.
                   Must preserve all existing keys and nested structures.
        
    Returns:
        Updated pack dict
        
    Raises:
        ValueError: If pack with slug not found
    """
    packs = load_packs_json()
    
    # Find the pack
    pack_index = None
    for i, pack in enumerate(packs):
        if pack.get("slug") == slug:
            pack_index = i
            break
    
    if pack_index is None:
        raise ValueError(f"Pack with slug '{slug}' not found in packs.json")
    
    # Get the pack and update it
    original_pack = packs[pack_index]
    updated_pack = updater_fn(original_pack.copy())
    
    # Replace in list
    packs[pack_index] = updated_pack
    
    # Save back
    save_packs_json(packs)
    
    return updated_pack

