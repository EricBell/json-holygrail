"""
Configuration management for JSON HolyGrail
Loads settings from .json-holygrail.toml files
"""

import tomllib
from pathlib import Path
from typing import Optional, Dict, Any


class Config:
    """Manages application configuration from TOML files"""

    CONFIG_FILENAME = ".json-holygrail.toml"

    def __init__(self):
        self._config_data: Optional[Dict[str, Any]] = None
        self._load_config()

    def _find_config_file(self) -> Optional[Path]:
        """
        Search for config file in:
        1. Current working directory
        2. Home directory
        """
        # Check current directory
        cwd_config = Path.cwd() / self.CONFIG_FILENAME
        if cwd_config.exists():
            return cwd_config

        # Check home directory
        home_config = Path.home() / self.CONFIG_FILENAME
        if home_config.exists():
            return home_config

        return None

    def _load_config(self):
        """Load configuration from TOML file"""
        config_file = self._find_config_file()

        if config_file is None:
            self._config_data = {}
            return

        try:
            with open(config_file, 'rb') as f:
                self._config_data = tomllib.load(f)
        except Exception as e:
            # If we can't load the config, just use defaults
            self._config_data = {}

    def get_default_format(self) -> str:
        """
        Get the default format name from config
        Returns 'default' if not specified
        """
        if not self._config_data:
            return "default"

        format_section = self._config_data.get("format", {})
        return format_section.get("default", "default")

    def get(self, section: str, key: str, default=None) -> Any:
        """
        Get a configuration value

        Args:
            section: The TOML section name
            key: The key within that section
            default: Default value if not found
        """
        if not self._config_data:
            return default

        section_data = self._config_data.get(section, {})
        return section_data.get(key, default)
