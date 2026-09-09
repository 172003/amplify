"""
conftest.py
Ensures the project root (containing the backend package) is importable
when pytest is run from any working directory.
"""

import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if project_root not in sys.path:
    sys.path.insert(0, project_root)
