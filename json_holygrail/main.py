#!/usr/bin/env python3
"""
Trading Plan JSON to Markdown Converter
Converts structured trading plan JSON into formatted markdown documents
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
import typer
from .version_manager import version_manager
from .renderer import TemplateRenderer
from .config import Config


def format_price(value: Any) -> str:
    """Format price values consistently"""
    if isinstance(value, (int, float)):
        return f"${value:,.2f}" if value < 100 else f"{value:,.2f}"
    return str(value)


def format_list(items: List[Any], prefix: str = "-") -> str:
    """Format a list into markdown bullet points"""
    if not items:
        return "- None"
    return "\n".join([f"{prefix} {item}" for item in items])


def format_dict_as_list(data: Dict[str, Any], label_suffix: str = "") -> str:
    """Format dictionary items as a list"""
    if not data:
        return "- None"
    lines = []
    for key, value in data.items():
        formatted_key = key.replace("_", " ").title()
        if isinstance(value, list):
            formatted_value = ", ".join(map(str, value))
        else:
            formatted_value = str(value)
        lines.append(f"- **{formatted_key}**: {formatted_value}")
    return "\n".join(lines)



def convert_json_to_markdown(json_data: Dict[str, Any], format_name: str = "default") -> str:
    """Convert trading plan JSON to markdown format using templates

    Args:
        json_data: Trading plan data dictionary
        format_name: Template name (embedded) or path (external)

    Returns:
        Formatted markdown string
    """
    # Check if trade should be executed
    trade_plan = json_data.get("trade_plan", {})
    if not trade_plan.get("trade", False):
        no_trade_reason = trade_plan.get("no_trade_reason", "No trade recommendation")
        return f"# No Trade Recommended\n\n**Reason**: {no_trade_reason}\n"

    # Render using template
    renderer = TemplateRenderer()
    return renderer.render(format_name, json_data)


def version_callback(value: bool):
    """Show version and exit"""
    if value:
        major, minor, patch = version_manager.get_current_version()
        typer.echo(f"v{major}.{minor}.{patch}")
        raise typer.Exit()


def cli_main(
    input_file: Optional[Path] = typer.Argument(
        None,
        help="Input JSON file containing trading plan data",
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output markdown file path (must include .md extension)",
        file_okay=True,
        dir_okay=False,
    ),
    format_name: Optional[str] = typer.Option(
        None,
        "--format",
        "-f",
        help="Output format template (name or path). Use --list-formats to see available formats.",
    ),
    list_formats: bool = typer.Option(
        False,
        "--list-formats",
        help="List available embedded format templates and exit",
        is_eager=True,
    ),
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version and exit",
        callback=version_callback,
        is_eager=True,
    )
):
    """
    Trading Plan JSON to Markdown Converter

    Convert trading plan JSON file to formatted markdown document.
    Output file defaults to same location and name as input with .md extension.

    Examples:
      json-holygrail trade-plan-MES-2025-12-14.json
      json-holygrail input.json -o /path/to/output.md
      json-holygrail input.json --format compact
      json-holygrail input.json --format /path/to/custom.md
    """
    # Handle --list-formats flag
    if list_formats:
        renderer = TemplateRenderer()
        formats = renderer.list_embedded_formats()
        if formats:
            typer.echo("Available embedded formats:")
            for fmt in formats:
                typer.echo(f"  - {fmt}")
        else:
            typer.echo("No embedded formats found.")
        raise typer.Exit()

    # Check if input file was provided
    if input_file is None:
        typer.echo("Error: Missing required argument INPUT_FILE", err=True)
        typer.echo("\nUsage: json-holygrail [OPTIONS] INPUT_FILE", err=True)
        typer.echo("\nTry 'json-holygrail --help' for help.", err=True)
        raise typer.Exit(1)

    # Validate input file exists
    if not input_file.exists():
        typer.echo(f"Error: File not found: {input_file}", err=True)
        raise typer.Exit(1)

    # Determine output file
    if output:
        output_file = output
    else:
        # Auto-generate output filename in same directory as input
        output_file = input_file.with_suffix(".md")

    # Determine format to use
    if format_name:
        selected_format = format_name
    else:
        # Load from config, fallback to "default"
        config = Config()
        selected_format = config.get_default_format()

    # Read JSON file
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            json_data = json.load(f)
    except json.JSONDecodeError as e:
        typer.echo(f"Error: Invalid JSON in {input_file}: {e}", err=True)
        raise typer.Exit(1)

    # Convert to markdown
    markdown_content = convert_json_to_markdown(json_data, selected_format)

    # Write output file
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        typer.echo(f"✅ Successfully converted {input_file} to {output_file}")
    except IOError as e:
        typer.echo(f"Error: Could not write to {output_file}: {e}", err=True)
        raise typer.Exit(1)


def main():
    """Entry point for console script"""
    typer.run(cli_main)


if __name__ == "__main__":
    typer.run(cli_main)
