#!/usr/bin/env python3
"""
Version management system with file hashing
Automatically tracks file changes and manages version numbers
"""

import os
import json
import hashlib
import logging
from pathlib import Path
from typing import Dict, List, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VersionManager:
    """Manages application versioning based on file hashes"""
    
    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root) if project_root else Path(__file__).parent
        self.version_file = self.project_root / 'version.json'
        self.tracked_files = [
            '*.py',
            'pyproject.toml',
            'README.md',
            'PRD.md'
        ]
        
    def _get_file_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of a file"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            logger.warning(f"Could not hash {file_path}: {e}")
            return ""
    
    def _get_all_tracked_files(self) -> List[Path]:
        """Get all files matching the tracked patterns"""
        all_files = []
        
        for pattern in self.tracked_files:
            if '**' in pattern:
                # Recursive glob
                files = list(self.project_root.glob(pattern))
            else:
                # Simple glob
                files = list(self.project_root.glob(pattern))
            
            # Filter out dist/, build/, __pycache__ directories
            filtered_files = []
            for f in files:
                if f.is_file():
                    rel_path = f.relative_to(self.project_root)
                    if not any(part.startswith('.') or part in ['dist', 'build', '__pycache__', 'instance'] 
                             for part in rel_path.parts):
                        filtered_files.append(f)
            
            all_files.extend(filtered_files)
        
        return sorted(set(all_files))
    
    def _calculate_file_hashes(self) -> Dict[str, str]:
        """Calculate hashes for all tracked files"""
        hashes = {}
        tracked_files = self._get_all_tracked_files()
        
        for file_path in tracked_files:
            rel_path = str(file_path.relative_to(self.project_root))
            hashes[rel_path] = self._get_file_hash(file_path)
        
        return hashes
    
    def _load_version_data(self) -> Dict:
        """Load version data from file"""
        default_data = {
            "major": 1,
            "minor": 0,
            "patch": 0,
            "file_hashes": {}
        }
        
        if not self.version_file.exists():
            return default_data
        
        try:
            with open(self.version_file, 'r') as f:
                data = json.load(f)
                # Ensure all required fields exist
                for key in default_data:
                    if key not in data:
                        data[key] = default_data[key]
                return data
        except Exception as e:
            logger.error(f"Error loading version file: {e}")
            return default_data
    
    def _save_version_data(self, data: Dict) -> None:
        """Save version data to file"""
        try:
            with open(self.version_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving version file: {e}")
    
    def get_current_version(self) -> Tuple[int, int, int]:
        """Get current version without checking for changes"""
        data = self._load_version_data()
        return data["major"], data["minor"], data["patch"]
    
    def check_and_update_version(self) -> Tuple[int, int, int, bool]:
        """Check for file changes and update version if needed"""
        data = self._load_version_data()
        current_hashes = self._calculate_file_hashes()
        previous_hashes = data.get("file_hashes", {})
        
        # Check if any files have changed
        files_changed = False
        changed_files = []
        
        # Check for modified files
        for file_path, current_hash in current_hashes.items():
            if file_path in previous_hashes:
                if previous_hashes[file_path] != current_hash:
                    files_changed = True
                    changed_files.append(f"Modified: {file_path}")
            else:
                files_changed = True
                changed_files.append(f"Added: {file_path}")
        
        # Check for removed files
        for file_path in previous_hashes:
            if file_path not in current_hashes:
                files_changed = True
                changed_files.append(f"Removed: {file_path}")
        
        if files_changed:
            # Increment patch version
            data["patch"] += 1
            data["file_hashes"] = current_hashes
            self._save_version_data(data)
            
            logger.info(f"Version updated to {data['major']}.{data['minor']}.{data['patch']}")
            for change in changed_files:
                logger.info(f"  {change}")
        
        return data["major"], data["minor"], data["patch"], files_changed
    
    def increment_major_version(self) -> Tuple[int, int, int]:
        """Manually increment major version and reset minor and patch to 0"""
        data = self._load_version_data()
        data["major"] += 1
        data["minor"] = 0
        data["patch"] = 0
        data["file_hashes"] = self._calculate_file_hashes()
        self._save_version_data(data)
        
        logger.info(f"Major version incremented to {data['major']}.{data['minor']}.{data['patch']}")
        return data["major"], data["minor"], data["patch"]
    
    def get_version_string(self) -> str:
        """Get formatted version string"""
        major, minor, patch, _ = self.check_and_update_version()
        return f"v{major}.{minor}.{patch}"
    
    def reset_version(self, major: int = 1, minor: int = 0, patch: int = 0) -> Tuple[int, int, int]:
        """Reset version to specified values"""
        data = {
            "major": major,
            "minor": minor,
            "patch": patch,
            "file_hashes": self._calculate_file_hashes()
        }
        self._save_version_data(data)
        
        logger.info(f"Version reset to {major}.{minor}.{patch}")
        return major, minor, patch

# Global version manager instance
version_manager = VersionManager()

def get_version_string() -> str:
    """Convenience function to get version string"""
    return version_manager.get_version_string()

def increment_major() -> str:
    """Convenience function to increment major version"""
    major, minor, patch = version_manager.increment_major_version()
    return f"v{major}.{minor}.{patch}"

# Simple standalone usage for development
if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == 'status':
            major, minor, patch = version_manager.get_current_version()
            print(f"Current version: v{major}.{minor}.{patch}")

        elif command == 'check':
            major, minor, patch, changed = version_manager.check_and_update_version()
            if changed:
                print(f"Version updated to v{major}.{minor}.{patch}")
            else:
                print(f"No changes detected. Version remains v{major}.{minor}.{patch}")

        elif command == 'major':
            major, minor, patch = version_manager.increment_major_version()
            print(f"Major version incremented to v{major}.{minor}.{patch}")

        elif command == 'reset':
            if len(sys.argv) == 5:
                try:
                    maj = int(sys.argv[2])
                    min = int(sys.argv[3])
                    pat = int(sys.argv[4])
                    major, minor, patch = version_manager.reset_version(maj, min, pat)
                    print(f"Version reset to v{major}.{minor}.{patch}")
                except ValueError:
                    print("Error: Version numbers must be integers")
                    sys.exit(1)
            else:
                major, minor, patch = version_manager.reset_version()
                print(f"Version reset to v{major}.{minor}.{patch}")

        else:
            print(f"Unknown command: {command}")
            print("Available commands: status, check, major, reset")
            sys.exit(1)
    else:
        major, minor, patch = version_manager.get_current_version()
        print(f"v{major}.{minor}.{patch}")