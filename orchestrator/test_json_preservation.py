"""
Test script to verify update_pack_lifecycle preserves JSON structure.

This script:
1. Loads packs.json
2. Calls update_pack_lifecycle with a no-op updater
3. Compares before/after JSON
4. Reports any differences
"""

import json
from pathlib import Path
from orchestrator.config import load_packs_json, save_packs_json, update_pack_lifecycle

# Path to packs.json
PACKS_JSON_PATH = Path(__file__).resolve().parent.parent / "pack-crm" / "data" / "packs.json"

def test_json_preservation():
    """Test that update_pack_lifecycle preserves JSON structure."""
    
    print("=" * 60)
    print("Testing JSON Preservation in update_pack_lifecycle()")
    print("=" * 60)
    print()
    
    # Step 1: Load original JSON
    print("1. Loading original packs.json...")
    original_json_bytes = PACKS_JSON_PATH.read_bytes()
    original_json_str = original_json_bytes.decode('utf-8')
    original_data = json.loads(original_json_str)
    
    # Find tax-assist pack
    tax_assist_original = None
    for pack in original_data:
        if pack.get("slug") == "tax-assist":
            tax_assist_original = pack
            break
    
    if not tax_assist_original:
        print("❌ tax-assist pack not found")
        return False
    
    print(f"   Found pack: {tax_assist_original.get('name')}")
    print()
    
    # Step 2: Call update_pack_lifecycle with no-op updater
    print("2. Calling update_pack_lifecycle with no-op updater...")
    
    def no_op_updater(pack: dict) -> dict:
        """No-op updater that returns pack unchanged."""
        return pack
    
    try:
        updated_pack = update_pack_lifecycle("tax-assist", no_op_updater)
        print("   ✅ update_pack_lifecycle completed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    print()
    
    # Step 3: Load JSON again and compare
    print("3. Loading updated packs.json...")
    updated_json_bytes = PACKS_JSON_PATH.read_bytes()
    updated_json_str = updated_json_bytes.decode('utf-8')
    updated_data = json.loads(updated_json_str)
    
    # Find tax-assist pack again
    tax_assist_updated = None
    for pack in updated_data:
        if pack.get("slug") == "tax-assist":
            tax_assist_updated = pack
            break
    
    if not tax_assist_updated:
        print("❌ tax-assist pack not found after update")
        return False
    
    print()
    
    # Step 4: Compare
    print("4. Comparing before/after...")
    print()
    
    # Compare JSON strings (preserves order)
    original_pack_str = json.dumps(tax_assist_original, indent=2, sort_keys=False, ensure_ascii=False)
    updated_pack_str = json.dumps(tax_assist_updated, indent=2, sort_keys=False, ensure_ascii=False)
    
    if original_pack_str == updated_pack_str:
        print("✅ PASS: JSON structure preserved (exact match)")
        print()
        return True
    
    # If not exact match, do deeper comparison
    print("⚠️  JSON strings differ. Performing deep comparison...")
    print()
    
    # Compare keys
    original_keys = list(tax_assist_original.keys())
    updated_keys = list(tax_assist_updated.keys())
    
    if original_keys != updated_keys:
        print("❌ FAIL: Key order changed")
        print(f"   Original keys: {original_keys}")
        print(f"   Updated keys: {updated_keys}")
        return False
    else:
        print("✅ Key order preserved")
    
    # Compare nested structures
    nested_structures = ["crm", "stages", "deployment", "metadata", "research"]
    
    for struct_name in nested_structures:
        original_struct = tax_assist_original.get(struct_name, {})
        updated_struct = tax_assist_updated.get(struct_name, {})
        
        original_struct_str = json.dumps(original_struct, indent=2, sort_keys=False, ensure_ascii=False)
        updated_struct_str = json.dumps(updated_struct, indent=2, sort_keys=False, ensure_ascii=False)
        
        if original_struct_str != updated_struct_str:
            print(f"❌ FAIL: {struct_name} structure changed")
            print(f"   Original {struct_name}:")
            print(original_struct_str[:200] + "..." if len(original_struct_str) > 200 else original_struct_str)
            print(f"   Updated {struct_name}:")
            print(updated_struct_str[:200] + "..." if len(updated_struct_str) > 200 else updated_struct_str)
            return False
        else:
            print(f"✅ {struct_name} structure preserved")
    
    # If we get here, structures match but strings differ (likely formatting)
    print()
    print("⚠️  Structures match but JSON strings differ (likely formatting)")
    print("   This may be acceptable if only whitespace/formatting changed")
    print()
    print("First 500 chars of original:")
    print(original_pack_str[:500])
    print()
    print("First 500 chars of updated:")
    print(updated_pack_str[:500])
    
    return False

if __name__ == "__main__":
    success = test_json_preservation()
    exit(0 if success else 1)

