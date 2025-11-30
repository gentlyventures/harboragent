#!/usr/bin/env python3

"""
Utility script to load .env file for Python scripts
Usage: python scripts/load-env.py your-script.py
"""

import os
import sys
import subprocess
from pathlib import Path

# Check if .env exists
env_path = Path('.env')
if not env_path.exists():
    print('Error: .env file not found', file=sys.stderr)
    print('Please copy .env.example to .env and fill in your values', file=sys.stderr)
    sys.exit(1)

# Try to load dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print('Warning: python-dotenv not installed. Install with: pip install python-dotenv', file=sys.stderr)

# Get the script to run
if len(sys.argv) < 2:
    print('Usage: python scripts/load-env.py <script.py>', file=sys.stderr)
    sys.exit(1)

script = sys.argv[1]

# Run the script with env loaded
try:
    subprocess.run([sys.executable, script] + sys.argv[2:], env=os.environ, check=True)
except subprocess.CalledProcessError as e:
    sys.exit(e.returncode)

