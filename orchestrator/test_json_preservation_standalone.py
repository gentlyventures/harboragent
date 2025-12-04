"""
Standalone test to verify JSON preservation in update_pack_lifecycle logic.

This simulates what update_pack_lifecycle does and checks for preservation.
"""

import json
from pathlib import Path
from copy import deepcopy

# Path to packs.json
PACKS_JSON_PATH = Path(__file__).resolve().parent.parent / "pack-crm" / "data" / "packs.json"

def test_json_preservation():
    """Test that update_pack_lifecycle preserves JSON structure."""
    
    print("=" * 60)
    print("Testing JSON Preservation in update_pack_lifecycle()")
    print("=" * 60)
    print()
    
    # Step 1: Load original JSON as bytes to preserve exact formatting
    print("1. Loading original packs.json...")
    original_json_bytes = PACKS_JSON_PATH.read_bytes()
    original_json_str = original_json_bytes.decode('utf-8')
    original_data = json.loads(original_json_str)
    
    # Find tax-assist pack
    tax_assist_original = None
    tax_assist_index = None
    for i, pack in enumerate(original_data):
        if pack.get("slug") == "tax-assist":
            tax_assist_original = pack
            tax_assist_index = i
            break
    
    if not tax_assist_original:
        print("❌ tax-assist pack not found")
        return False
    
    print(f"   Found pack: {tax_assist_original.get('name')} at index {tax_assist_index}")
    print()
    
    # Step 2: Simulate update_pack_lifecycle with no-op updater
    print("2. Simulating update_pack_lifecycle with no-op updater...")
    
    # This is what update_pack_lifecycle does:
    # 1. Load packs
    packs = deepcopy(original_data)
    
    # 2. Find pack
    pack_index = tax_assist_index
    
    # 3. Get pack and "update" it (no-op)
    original_pack = packs[pack_index]
    updated_pack = original_pack.copy()  # No-op updater just returns copy
    
    # 4. Replace in list
    packs[pack_index] = updated_pack
    
    # 5. Save back (this is what save_packs_json does)
    updated_json_str = json.dumps(packs, indent=2, ensure_ascii=False)
    
    print("   ✅ Simulated update completed")
    print()
    
    # Step 3: Compare
    print("3. Comparing before/after...")
    print()
    
    # Compare the full JSON strings
    if original_json_str == updated_json_str:
        print("✅ PASS: JSON structure preserved (exact match)")
        print()
        return True
    
    # If not exact match, do deeper comparison
    print("⚠️  JSON strings differ. Performing deep comparison...")
    print()
    
    # Reload to get parsed data
    updated_data = json.loads(updated_json_str)
    tax_assist_updated = updated_data[tax_assist_index]
    
    # Compare keys order
    original_keys = list(tax_assist_original.keys())
    updated_keys = list(tax_assist_updated.keys())
    
    if original_keys != updated_keys:
        print("❌ FAIL: Key order changed")
        print(f"   Original keys: {original_keys}")
        print(f"   Updated keys: {updated_keys}")
        missing = set(original_keys) - set(updated_keys)
        extra = set(updated_keys) - set(original_keys)
        if missing:
            print(f"   Missing keys: {missing}")
        if extra:
            print(f"   Extra keys: {extra}")
        return False
    else:
        print("✅ Key order preserved")
    
    # Compare nested structures deeply
    nested_structures = ["crm", "stages", "deployment", "metadata", "research"]
    
    all_preserved = True
    for struct_name in nested_structures:
        original_struct = tax_assist_original.get(struct_name, {})
        updated_struct = tax_assist_updated.get(struct_name, {})
        
        original_struct_str = json.dumps(original_struct, indent=2, sort_keys=False, ensure_ascii=False)
        updated_struct_str = json.dumps(updated_struct, indent=2, sort_keys=False, ensure_ascii=False)
        
        if original_struct_str != updated_struct_str:
            print(f"❌ FAIL: {struct_name} structure changed")
            print(f"   Original {struct_name} keys: {list(original_struct.keys()) if isinstance(original_struct, dict) else 'N/A'}")
            print(f"   Updated {struct_name} keys: {list(updated_struct.keys()) if isinstance(updated_struct, dict) else 'N/A'}")
            
            # Show diff
            if isinstance(original_struct, dict) and isinstance(updated_struct, dict):
                orig_keys_set = set(original_struct.keys())
                upd_keys_set = set(updated_struct.keys())
                if orig_keys_set != upd_keys_set:
                    print(f"   Missing: {orig_keys_set - upd_keys_set}")
                    print(f"   Extra: {upd_keys_set - orig_keys_set}")
            
            all_preserved = False
        else:
            print(f"✅ {struct_name} structure preserved")
    
    if not all_preserved:
        return False
    
    # If structures match but strings differ, it's likely just formatting
    print()
    print("⚠️  Structures match but JSON strings differ (likely formatting/whitespace)")
    print("   This may be acceptable, but let's check the differences...")
    print()
    
    # Show first difference
    for i, (orig_char, upd_char) in enumerate(zip(original_json_str, updated_json_str)):
        if orig_char != upd_char:
            start = max(0, i - 50)
            end = min(len(original_json_str), i + 50)
            print(f"First difference at position {i}:")
            print(f"  Original: ...{original_json_str[start:end]}...")
            print(f"  Updated:  ...{updated_json_str[start:end]}...")
            break
    
    print()
    print("Note: json.dump() may reorder dictionary keys in Python < 3.7")
    print("      or if sort_keys is used. We use sort_keys=False, so order")
    print("      should be preserved in Python 3.7+.")
    
    return False

if __name__ == "__main__":
    success = test_json_preservation()
    exit(0 if success else 1)

