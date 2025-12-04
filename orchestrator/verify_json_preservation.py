#!/usr/bin/env python3
"""
Verification script for JSON preservation.

This script verifies that update_pack_lifecycle preserves JSON structure.
Run this after installing dependencies: pip install -r requirements.txt
"""

import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from orchestrator.config import update_pack_lifecycle

def main():
    """Run verification test."""
    print("=" * 60)
    print("JSON Preservation Verification")
    print("=" * 60)
    print()
    
    packs_path = Path(__file__).resolve().parent.parent / "pack-crm" / "data" / "packs.json"
    
    # Save original
    print("1. Loading original packs.json...")
    original_bytes = packs_path.read_bytes()
    original_str = original_bytes.decode('utf-8')
    original_data = json.loads(original_str)
    
    # Find tax-assist
    tax_assist_original = None
    for pack in original_data:
        if pack.get("slug") == "tax-assist":
            tax_assist_original = pack
            break
    
    if not tax_assist_original:
        print("❌ tax-assist pack not found")
        return False
    
    print(f"   Found: {tax_assist_original.get('name')}")
    print()
    
    # Call update_pack_lifecycle with no-op
    print("2. Calling update_pack_lifecycle with no-op updater...")
    
    def no_op_updater(pack: dict) -> dict:
        """No-op: return pack unchanged."""
        return pack
    
    try:
        result = update_pack_lifecycle("tax-assist", no_op_updater)
        print("   ✅ Completed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print()
    
    # Load updated
    print("3. Comparing before/after...")
    updated_bytes = packs_path.read_bytes()
    updated_str = updated_bytes.decode('utf-8')
    updated_data = json.loads(updated_str)
    
    # Find tax-assist again
    tax_assist_updated = None
    for pack in updated_data:
        if pack.get("slug") == "tax-assist":
            tax_assist_updated = pack
            break
    
    if not tax_assist_updated:
        print("❌ tax-assist pack not found after update")
        return False
    
    # Compare JSON strings (exact match)
    if original_str == updated_str:
        print("✅ PASS: JSON is identical (exact match)")
        return True
    
    # Check if only trailing whitespace differs
    orig_stripped = original_str.rstrip()
    upd_stripped = updated_str.rstrip()
    
    if orig_stripped == upd_stripped:
        print("✅ PASS: Content is identical (only trailing whitespace differs)")
        print("   This is acceptable - json.dump normalizes trailing newlines")
        return True
    
    # Deep comparison
    print("⚠️  JSON strings differ. Performing deep comparison...")
    print()
    
    # Compare keys
    orig_keys = list(tax_assist_original.keys())
    upd_keys = list(tax_assist_updated.keys())
    
    if orig_keys != upd_keys:
        print("❌ FAIL: Key order changed")
        print(f"   Original: {orig_keys}")
        print(f"   Updated:  {upd_keys}")
        return False
    print("✅ Key order preserved")
    
    # Compare nested structures
    structures = ["crm", "stages", "deployment", "metadata", "research"]
    all_match = True
    
    for struct_name in structures:
        orig_struct = tax_assist_original.get(struct_name, {})
        upd_struct = tax_assist_updated.get(struct_name, {})
        
        orig_json = json.dumps(orig_struct, indent=2, sort_keys=False, ensure_ascii=False)
        upd_json = json.dumps(upd_struct, indent=2, sort_keys=False, ensure_ascii=False)
        
        if orig_json != upd_json:
            print(f"❌ FAIL: {struct_name} structure changed")
            all_match = False
        else:
            print(f"✅ {struct_name} structure preserved")
    
    if all_match:
        print()
        print("✅ PASS: All structures preserved")
        print("   (Minor formatting differences are acceptable)")
        return True
    
    return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

