"""
Template rendering engine for JSON HolyGrail
Handles Jinja2 template loading and rendering
"""

import os
from pathlib import Path
from typing import Dict, Any
from jinja2 import Environment, ChoiceLoader, PackageLoader, FileSystemLoader, TemplateNotFound

from .filters import register_filters


class TemplateRenderer:
    """Renders markdown templates using Jinja2"""

    def __init__(self):
        """Initialize the Jinja2 environment with loaders"""
        # Create loaders
        # 1. PackageLoader for embedded templates in formats/ directory
        package_loader = PackageLoader('json_holygrail', 'formats')

        # 2. FileSystemLoader for external templates (searches from cwd)
        fs_loader = FileSystemLoader(searchpath=[Path.cwd(), '/'])

        # ChoiceLoader tries each loader in order
        loader = ChoiceLoader([package_loader, fs_loader])

        # Create Jinja2 environment
        self.env = Environment(
            loader=loader,
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True
        )

        # Register custom filters
        register_filters(self.env)

    def _resolve_template_name(self, format_name: str) -> str:
        """
        Resolve template name to actual template path

        Args:
            format_name: Either a simple name (e.g., 'default', 'compact')
                        or a full file path (e.g., '/path/to/template.md')

        Returns:
            Template name/path to use with Jinja2

        Logic:
            - If contains path separator: treat as external file path
            - Otherwise: treat as embedded template name in formats/ directory
            - Auto-append .md extension if not present
        """
        # Check if this looks like a file path (contains / or \)
        if '/' in format_name or '\\' in format_name:
            # External file path
            template_path = Path(format_name)

            # Add .md extension if not present
            if not template_path.suffix:
                template_path = template_path.with_suffix('.md')

            return str(template_path)
        else:
            # Embedded template name
            # Add .md extension if not present
            if not format_name.endswith('.md'):
                format_name = f"{format_name}.md"

            return format_name

    def get_template(self, format_name: str):
        """
        Get a Jinja2 template by name or path

        Args:
            format_name: Template name or file path

        Returns:
            Jinja2 Template object

        Raises:
            TemplateNotFound: If template cannot be found
        """
        template_name = self._resolve_template_name(format_name)
        return self.env.get_template(template_name)

    def render(self, format_name: str, context: Dict[str, Any]) -> str:
        """
        Render a template with the given context

        Args:
            format_name: Template name or file path
            context: Dictionary of variables to pass to template

        Returns:
            Rendered markdown string

        Raises:
            TemplateNotFound: If template cannot be found
        """
        template = self.get_template(format_name)
        return template.render(**context)

    def list_embedded_formats(self):
        """
        List all embedded template formats available

        Returns:
            List of format names (without .md extension)
        """
        try:
            # Get the package loader (first in ChoiceLoader)
            package_loader = self.env.loader.loaders[0]

            # List all templates
            templates = package_loader.list_templates()

            # Filter for .md files and remove extension
            formats = [
                t[:-3] for t in templates
                if t.endswith('.md')
            ]

            return sorted(formats)
        except Exception:
            return []
