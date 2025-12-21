"""
JSON HolyGrail - Trading Plan JSON to Markdown Converter
Converts structured trading plan JSON into formatted markdown documents
"""

import json
from pathlib import Path

# Load version from version.json
_version_file = Path(__file__).parent / 'version.json'
if _version_file.exists():
    with open(_version_file, 'r') as f:
        _version_data = json.load(f)
        __version__ = f"{_version_data['major']}.{_version_data['minor']}.{_version_data['patch']}"
else:
    __version__ = "0.1.9"

__all__ = ['__version__']
