#!/usr/bin/env python3
"""
Static audit script for Genesis Mission fidelity checks.
Ensures content doesn't overclaim compliance, uses correct terminology, and includes required disclaimers.
"""
import json
import os
import sys
from typing import List, Dict
from pathlib import Path

CONFIG_PATH = os.path.join("config", "genesis_fidelity_rules.json")


def load_config(path: str) -> Dict:
    """Load the fidelity rules configuration."""
    if not os.path.exists(path):
        print(f"[ERROR] Config file not found at {path}")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def should_scan_file(path: str, extensions: List[str]) -> bool:
    """Check if file should be scanned based on extension."""
    return any(path.endswith(ext) for ext in extensions)


def read_file(path: str) -> str:
    """Read file content."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"[WARNING] Could not read {path}: {e}")
        return ""


def check_forbidden_phrases(content: str, phrases: List[str], rel_path: str, report: List[str]) -> None:
    """Check for forbidden phrases that overclaim compliance."""
    lowered = content.lower()
    for phrase in phrases:
        if phrase.lower() in lowered:
            report.append(
                f"[FORBIDDEN PHRASE] '{phrase}' found in {rel_path}"
            )


def check_project_name_misuse(content: str, misuses: List[str], official_name: str, rel_path: str, report: List[str]) -> None:
    """Check for incorrect project name usage."""
    lowered = content.lower()
    for bad in misuses:
        if bad.lower() in lowered:
            report.append(
                f"[NAMING] Found '{bad}' in {rel_path}. Use the official term '{official_name}' instead."
            )


def check_disclaimer_required(
    rel_path: str,
    abs_path: str,
    required_files: List[str],
    disclaimer: str,
    report: List[str]
) -> None:
    """Check if required disclaimer is present in specified files."""
    normalized_required = [os.path.normpath(p) for p in required_files]
    normalized_rel_path = os.path.normpath(rel_path)
    
    if normalized_rel_path not in normalized_required:
        return

    if not os.path.exists(abs_path):
        report.append(f"[DISCLAIMER] Required file {rel_path} not found")
        return

    content = read_file(abs_path)
    if disclaimer not in content:
        report.append(
            f"[DISCLAIMER] Required disclaimer not found in {rel_path}"
        )


def main():
    """Main audit function."""
    config = load_config(CONFIG_PATH)

    scan_root = config.get("scan_root", "dist/paid-pack")
    scan_extensions = config.get("scan_extensions", [".md"])
    forbidden_phrases = config.get("forbidden_phrases", [])
    misuses = config.get("project_name_misuses", [])
    official_name = config.get("official_terms", {}).get("program_name", "Genesis Mission")
    disclaimer = config.get("required_disclaimer", "")
    required_files = config.get("files_requiring_disclaimer", [])

    # Get repo root (assume script is in tools/, go up one level)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    target_root = os.path.join(repo_root, scan_root)

    if not os.path.exists(target_root):
        print(f"[ERROR] Scan root does not exist: {target_root}")
        sys.exit(1)

    report: List[str] = []

    for root, _, files in os.walk(target_root):
        for fname in files:
            abs_path = os.path.join(root, fname)
            rel_path = os.path.relpath(abs_path, repo_root)

            if not should_scan_file(abs_path, scan_extensions):
                continue

            content = read_file(abs_path)
            if not content:
                continue

            # Run checks
            check_forbidden_phrases(content, forbidden_phrases, rel_path, report)
            check_project_name_misuse(content, misuses, official_name, rel_path, report)
            check_disclaimer_required(rel_path, abs_path, required_files, disclaimer, report)

    # Output results
    if not report:
        print("[OK] Genesis Mission fidelity checks passed. No issues found.")
        sys.exit(0)

    print("[FAIL] Genesis Mission fidelity checks found issues:\n")
    for item in report:
        print("  - " + item)
    print()

    sys.exit(1)


if __name__ == "__main__":
    main()

