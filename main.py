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
from version_manager import version_manager


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


def generate_header(data: Dict[str, Any]) -> str:
    """Generate the header section"""
    trade_plan = data.get("trade_plan", {})
    verdict = trade_plan.get("verdict", {})

    action = verdict.get("action", "NO ACTION")
    confidence = verdict.get("confidence", "Unknown")
    ticker = data.get("ticker", "UNKNOWN")
    asset_type = data.get("asset_type", "UNKNOWN")
    trade_style = data.get("trade_style", "UNKNOWN")

    header = f"""# Trading Plan: {ticker}

## {action}
**Confidence**: {confidence}
**Asset Type**: {asset_type} | **Trade Style**: {trade_style}

---
"""
    return header


def generate_key_metrics(data: Dict[str, Any]) -> str:
    """Generate key metrics summary"""
    trade_plan = data.get("trade_plan", {})
    entry = trade_plan.get("entry", {})
    position = trade_plan.get("position", {})

    account_size = data.get("account_size", 0)
    risk_percent = data.get("risk_percent", 0)
    max_risk = position.get("max_risk", "Unknown")
    current_price = entry.get("current_price", "Unknown")

    metrics = f"""## Key Metrics

| Metric | Value |
|--------|-------|
| **Account Size** | {format_price(account_size)} |
| **Risk Percent** | {risk_percent}% |
| **Max Risk** | {max_risk} |
| **Current Price** | {format_price(current_price)} |

---
"""
    return metrics


def generate_agent_verdicts(data: Dict[str, Any]) -> str:
    """Generate agent verdicts section"""
    agents = data.get("agent_verdicts", {})
    technical = agents.get("technical", {})
    macro = agents.get("macro", {})
    wild_card = agents.get("wild_card", {})

    output = "## Agent Verdicts\n\n"

    # Technical Agent
    output += "### Technical Agent\n\n"
    output += f"**Direction**: {technical.get('direction', 'Unknown').upper()} | "
    output += f"**Confidence**: {technical.get('confidence', 0)}%\n\n"
    output += f"**Entry Type**: {technical.get('entry_type', 'Unknown').replace('_', ' ').title()}\n\n"

    # Support Levels
    support = technical.get("support_levels", {})
    if support:
        output += "**Support Levels**:\n"
        if support.get("minor"):
            output += f"- Minor: {', '.join(map(str, support['minor']))}\n"
        if support.get("major"):
            output += f"- Major: {', '.join(map(str, support['major']))}\n"
        if support.get("key_references"):
            output += "- Key References:\n"
            for key, val in support["key_references"].items():
                output += f"  - {key.replace('_', ' ').upper()}: {val}\n"
        output += "\n"

    # Resistance Levels
    resistance = technical.get("resistance_levels", {})
    if resistance:
        output += "**Resistance Levels**:\n"
        if resistance.get("minor"):
            output += f"- Minor: {', '.join(map(str, resistance['minor']))}\n"
        if resistance.get("major"):
            output += f"- Major: {', '.join(map(str, resistance['major']))}\n"
        if resistance.get("key_references"):
            output += "- Key References:\n"
            for key, val in resistance["key_references"].items():
                output += f"  - {key.replace('_', ' ').upper()}: {val}\n"
        output += "\n"

    # Chart Patterns
    if technical.get("chart_patterns"):
        output += "**Chart Patterns**:\n"
        output += format_list(technical["chart_patterns"]) + "\n\n"

    # Additional Technical Info
    output += f"**MTF Alignment**: {technical.get('mtf_alignment', 'Unknown')} | "
    output += f"**Volatility**: {technical.get('volatility', 'Unknown')}\n\n"

    # Technical Reasoning
    if technical.get("reasoning"):
        output += "**Technical Reasoning**:\n"
        output += format_list(technical["reasoning"]) + "\n\n"

    output += "---\n\n"

    # Macro Agent
    output += "### Macro Agent\n\n"
    output += f"**Market Regime**: {macro.get('market_regime', 'Unknown').replace('_', ' ').title()} | "
    output += f"**Confidence**: {macro.get('confidence', 0)}%\n\n"
    output += f"**SPY Direction**: {macro.get('spy_direction', 'Unknown').upper()} | "
    output += f"**QQQ Direction**: {macro.get('qqq_direction', 'Unknown').upper()}\n\n"
    output += f"**Cross Asset Alignment**: {macro.get('cross_asset_alignment', 'Unknown').title()}\n\n"

    # Session Context
    session = macro.get("session_context", {})
    if session:
        output += "**Session Context**:\n"
        output += f"- Type: {session.get('type', 'Unknown').replace('_', ' ').title()}\n"
        if session.get("risk_note"):
            output += f"- Risk Note: {session['risk_note']}\n"
        output += "\n"

    # Economic Assessment
    econ = macro.get("economic_assessment", {})
    if econ:
        output += "**Economic Assessment**:\n"
        if econ.get("macro_headwinds"):
            output += "- Headwinds:\n"
            for hw in econ["macro_headwinds"]:
                output += f"  - {hw}\n"
        if econ.get("macro_tailwinds"):
            output += "- Tailwinds:\n"
            for tw in econ["macro_tailwinds"]:
                output += f"  - {tw}\n"
        output += "\n"

    # News Sentiment
    news = macro.get("news_sentiment", {})
    if news:
        output += "**News Sentiment**:\n"
        output += f"- Overall: {news.get('overall', 'Unknown').title()}\n"
        if news.get("key_themes"):
            output += "- Key Themes: " + ", ".join(news["key_themes"]) + "\n"
        output += "\n"

    # Macro Reasoning
    if macro.get("reasoning"):
        output += "**Macro Reasoning**:\n"
        output += format_list(macro["reasoning"]) + "\n\n"

    output += "---\n\n"

    # Wild Card Agent
    output += "### Wild Card Agent\n\n"
    output += f"**Overall Risk Assessment**: {wild_card.get('overall_risk_assessment', 'Unknown').upper()}\n\n"

    # Wild Cards Identified
    wild_cards = wild_card.get("wild_cards_identified", [])
    if wild_cards:
        output += "**Identified Wild Cards**:\n\n"
        for i, wc in enumerate(wild_cards, 1):
            output += f"{i}. **{wc.get('type', 'Unknown').replace('_', ' ').title()}**: {wc.get('description', 'N/A')}\n"
            output += f"   - **Probability**: {wc.get('probability', 'Unknown').title()}\n"
            output += f"   - **Impact**: {wc.get('impact', 'Unknown').title()}\n"
            output += f"   - **Mitigation**: {wc.get('mitigation', 'None')}\n\n"

    # Contingencies
    if wild_card.get("recommended_contingencies"):
        output += "**Recommended Contingencies**:\n"
        output += format_list(wild_card["recommended_contingencies"]) + "\n\n"

    # Timing Considerations
    if wild_card.get("timing_considerations"):
        output += "**Timing Considerations**:\n"
        output += format_list(wild_card["timing_considerations"]) + "\n\n"

    # Honest Uncertainty
    if wild_card.get("honest_uncertainty"):
        output += f"> **Honest Uncertainty**: {wild_card['honest_uncertainty']}\n\n"

    output += "---\n\n"

    return output


def generate_trade_details(data: Dict[str, Any]) -> str:
    """Generate trade details section"""
    trade_plan = data.get("trade_plan", {})
    entry = trade_plan.get("entry", {})
    position = trade_plan.get("position", {})

    output = "## Trade Details\n\n"

    # Entry Zone
    output += "### Entry Zone\n\n"
    output += f"**Direction**: {entry.get('direction', 'Unknown')}\n\n"
    output += f"**Recommendation**: {entry.get('recommendation', 'Unknown').replace('_', ' ').title()}\n\n"

    ideal_zone = entry.get("ideal_zone", {})
    if ideal_zone:
        output += "**Ideal Entry Zone**:\n"
        output += f"- Low: {format_price(ideal_zone.get('low', 'N/A'))}\n"
        output += f"- Mid: {format_price(ideal_zone.get('mid', 'N/A'))}\n"
        output += f"- High: {format_price(ideal_zone.get('high', 'N/A'))}\n"
        output += f"- Confidence: {ideal_zone.get('confidence', 'Unknown')}\n\n"

    if entry.get("wait_for"):
        output += f"> **Wait For**: {entry['wait_for']}\n\n"

    output += "---\n\n"

    # Position Sizing
    output += "### Position Sizing\n\n"
    output += f"**Size Recommendation**: {position.get('size_recommendation', 'Unknown').title()}\n\n"
    output += f"**Quantity**: {position.get('quantity', 0)} {position.get('unit_type', 'units')}\n\n"
    output += f"**Total Cost**: {position.get('total_cost', 'Unknown')}\n\n"
    output += f"**Max Risk**: {position.get('max_risk', 'Unknown')}\n\n"

    if position.get("rationale"):
        output += f"**Rationale**: {position['rationale']}\n\n"

    output += "---\n\n"

    return output


def generate_exit_strategy(data: Dict[str, Any]) -> str:
    """Generate exit strategy section"""
    trade_plan = data.get("trade_plan", {})
    exits = trade_plan.get("exits", {})

    output = "## Exit Strategy\n\n"

    # Stop Loss
    stop_loss = exits.get("stop_loss", {})
    if stop_loss:
        output += "### Stop Loss\n\n"
        price_range = stop_loss.get("price_range", [])
        if price_range:
            output += f"**Price Range**: {format_price(price_range[0])} - {format_price(price_range[-1])}\n\n"
        output += f"**Total Loss**: {stop_loss.get('total_loss', 'Unknown')}\n\n"
        if stop_loss.get("rationale"):
            output += f"**Rationale**: {stop_loss['rationale']}\n\n"

    # Profit Targets
    profit_targets = exits.get("profit_targets", [])
    if profit_targets:
        output += "### Profit Targets\n\n"
        for i, target in enumerate(profit_targets, 1):
            output += f"**Target {target.get('target', i)}**:\n"
            price_range = target.get("price_range", [])
            if price_range:
                output += f"- Price Range: {format_price(price_range[0])} - {format_price(price_range[-1])}\n"
            output += f"- Position %: {target.get('position_percent', 0)}%\n"
            output += f"- Probability: {target.get('probability', 'Unknown')}\n\n"

    # Time Stop
    time_stop = exits.get("time_stop", {})
    if time_stop:
        output += "### Time Stop\n\n"
        output += f"**Duration**: {time_stop.get('date_or_duration', 'Unknown')}\n\n"
        if time_stop.get("rationale"):
            output += f"**Rationale**: {time_stop['rationale']}\n\n"

    output += "---\n\n"

    return output


def generate_wild_cards_warnings(data: Dict[str, Any]) -> str:
    """Generate wild cards and warnings section"""
    trade_plan = data.get("trade_plan", {})
    wild_cards = trade_plan.get("wild_cards", {})

    output = "## Wild Cards & Warnings\n\n"

    # Identified Risks
    risks = wild_cards.get("identified_risks", [])
    if risks:
        output += "### Identified Risks\n\n"
        for risk in risks:
            output += f"- **{risk.get('risk', 'Unknown')}**\n"
            output += f"  - Probability: {risk.get('probability', 'Unknown').title()}\n"
            output += f"  - Impact: {risk.get('impact', 'Unknown').title()}\n"
            output += f"  - Contingency: {risk.get('contingency', 'None')}\n\n"

    # Manual Checks Required
    manual_checks = wild_cards.get("manual_checks_required", [])
    if manual_checks:
        output += "### Manual Checks Required\n\n"
        output += format_list(manual_checks) + "\n\n"

    # Honest Uncertainty
    if wild_cards.get("honest_uncertainty"):
        output += f"> **Honest Uncertainty**: {wild_cards['honest_uncertainty']}\n\n"

    output += "---\n\n"

    return output


def generate_execution_checklist(data: Dict[str, Any]) -> str:
    """Generate execution checklist section"""
    trade_plan = data.get("trade_plan", {})
    execution = trade_plan.get("execution_plan", {})

    output = "## Execution Checklist\n\n"

    # Get all step keys and sort them
    steps = sorted([k for k in execution.keys() if k.startswith("step_")])

    if steps:
        for step_key in steps:
            step_num = step_key.split("_")[1]
            output += f"{step_num}. {execution[step_key]}\n"
        output += "\n"
    else:
        output += "- No execution steps defined\n\n"

    output += "---\n\n"

    return output


def generate_pre_trading_checklist(data: Dict[str, Any]) -> str:
    """Generate pre-trading checklist section"""
    checks = data.get("pre_trade_checks", {})

    output = "## Pre-Trading Checklist\n\n"

    safe_to_trade = checks.get("safe_to_trade", False)
    output += f"**Safe to Trade**: {'✅ YES' if safe_to_trade else '❌ NO'}\n\n"

    # Warnings
    warnings = checks.get("warnings", [])
    if warnings:
        output += "### Warnings\n\n"
        output += format_list(warnings) + "\n\n"

    # Critical Events
    critical = checks.get("critical_events", [])
    if critical:
        output += "### Critical Events\n\n"
        output += format_list(critical) + "\n\n"

    # Additional Info
    if checks.get("news_summary"):
        output += f"**News Summary**: {checks['news_summary']}\n\n"

    if checks.get("manual_check_required"):
        output += "> ⚠️ **MANUAL CHECK REQUIRED BEFORE TRADING**\n\n"

    output += "---\n\n"

    return output


def convert_json_to_markdown(json_data: Dict[str, Any]) -> str:
    """Convert trading plan JSON to markdown format"""

    # Check if trade should be executed
    trade_plan = json_data.get("trade_plan", {})
    if not trade_plan.get("trade", False):
        no_trade_reason = trade_plan.get("no_trade_reason", "No trade recommendation")
        return f"# No Trade Recommended\n\n**Reason**: {no_trade_reason}\n"

    markdown = ""
    markdown += generate_header(json_data)
    markdown += generate_key_metrics(json_data)
    markdown += generate_agent_verdicts(json_data)
    markdown += generate_trade_details(json_data)
    markdown += generate_exit_strategy(json_data)
    markdown += generate_wild_cards_warnings(json_data)
    markdown += generate_execution_checklist(json_data)
    markdown += generate_pre_trading_checklist(json_data)

    return markdown


def version_callback(value: bool):
    """Show version and exit"""
    if value:
        major, minor, patch = version_manager.get_current_version()
        typer.echo(f"v{major}.{minor}.{patch}")
        raise typer.Exit()

def main(
    input_file: Path = typer.Argument(
        ...,
        help="Input JSON file containing trading plan data",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output markdown file path (must include .md extension)",
        file_okay=True,
        dir_okay=False,
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
      python main.py trade-plan-MES-2025-12-14.json
      python main.py input.json -o /path/to/output.md
    """
    # Determine output file
    if output:
        output_file = output
    else:
        # Auto-generate output filename in same directory as input
        output_file = input_file.with_suffix(".md")

    # Read JSON file
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            json_data = json.load(f)
    except FileNotFoundError:
        typer.echo(f"Error: File not found: {input_file}", err=True)
        raise typer.Exit(1)
    except json.JSONDecodeError as e:
        typer.echo(f"Error: Invalid JSON in {input_file}: {e}", err=True)
        raise typer.Exit(1)

    # Convert to markdown
    markdown_content = convert_json_to_markdown(json_data)

    # Write output file
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        typer.echo(f"✅ Successfully converted {input_file} to {output_file}")
    except IOError as e:
        typer.echo(f"Error: Could not write to {output_file}: {e}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    typer.run(main)
