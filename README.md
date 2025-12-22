# json-holyGrail

A Python tool that converts trading plan JSON files into formatted markdown documents using customizable Jinja2 templates.

## Features

- **Multiple Output Formats**: Choose from embedded formats or create your own custom templates
- **Jinja2 Template Engine**: Full control over markdown output formatting
- **Configurable Defaults**: Set your preferred format in a config file
- Converts comprehensive trading analysis JSON to readable markdown
- Supports all trading plan sections: Technical, Macro, Wild Cards, Entry/Exit strategies
- Handles futures, stocks, and other asset types
- Automatic formatting of prices, percentages, and risk levels
- Clean, well-structured output perfect for review and documentation

## Installation

```bash
# Clone the repository
cd json-holygrail

# Install using the install script
./install.sh
```

**Requirements:**
- Python 3.11+
- Dependencies: `typer`, `jinja2` (installed automatically)

## Usage

### Basic Usage

```bash
json-holygrail <input.json>
```

This will create a markdown file with the same name as your input file using the default format.

**Example:**
```bash
json-holygrail trade-plan-MES-2025-12-14.json
# Creates: trade-plan-MES-2025-12-14.md
```

### Specify Output File

```bash
json-holygrail <input.json> -o <output.md>
```

**Example:**
```bash
json-holygrail input.json -o my-trade-plan.md
```

### Using Different Formats

List available embedded formats:
```bash
json-holygrail --list-formats
# Output:
# Available embedded formats:
#   - compact
#   - default
```

Use a specific embedded format:
```bash
json-holygrail input.json --format compact
```

Use a custom external template:
```bash
json-holygrail input.json --format /path/to/custom-template.md
```

### Configuration File

Create a `.json-holygrail.toml` file in your project directory or home directory to set default preferences:

```toml
[format]
default = "compact"  # or "default" or "/path/to/custom.md"
```

Now when you run `json-holygrail input.json` without `--format`, it will use your configured default.

## Input Format

The tool expects a JSON file with the following structure:

```json
{
  "status": "success",
  "ticker": "MES",
  "asset_type": "FUTURES",
  "trade_style": "SCALP",
  "account_size": 2000,
  "risk_percent": 1,
  "agent_verdicts": {
    "technical": { ... },
    "macro": { ... },
    "wild_card": { ... }
  },
  "trade_plan": {
    "trade": true,
    "verdict": { ... },
    "entry": { ... },
    "position": { ... },
    "exits": { ... },
    "execution_plan": { ... }
  },
  "pre_trade_checks": { ... }
}
```

See the PRD.md file for complete schema details.

## Output Formats

### Default Format
The default format generates comprehensive markdown with all sections:

1. **Header** - Ticker, action (SHORT/LONG), confidence
2. **Key Metrics** - Account size, risk %, max risk, current price
3. **Agent Verdicts** - Technical, Macro, and Wild Card analysis
4. **Trade Details** - Entry zones and position sizing
5. **Exit Strategy** - Stop loss, profit targets, time stops
6. **Wild Cards & Warnings** - Risk assessment and contingencies
7. **Execution Checklist** - Step-by-step execution plan
8. **Pre-Trading Checklist** - Safety checks and warnings

### Compact Format
A condensed format with:
- Quick stats and levels in one line
- Emoji icons for visual clarity
- Key information only
- Perfect for quick reference

## Creating Custom Templates

You can create your own Jinja2 templates to customize the output format.

### Template Basics

Templates are written in Jinja2 syntax with access to all JSON data:

```jinja2
# {{ ticker }} {{ trade_plan.entry.direction | upper }}

**Confidence**: {{ trade_plan.verdict.confidence }}%

## Entry
{{ trade_plan.entry.wait_for }}

## Levels
- Stop: {{ trade_plan.exits.stop_loss.price_range[0] | format_price }}
- Target: {{ trade_plan.exits.profit_targets[0].price_range[0] | format_price }}
```

### Available Variables

Your templates have access to the entire JSON structure:

**Top-level:**
- `ticker`, `status`, `asset_type`, `trade_style`
- `account_size`, `risk_percent`
- `agent_verdicts` (technical, macro, wild_card)
- `trade_plan` (verdict, entry, position, exits, execution_plan)
- `pre_trade_checks`

**Examples:**
```jinja2
{{ ticker }}                                    # "AAPL"
{{ trade_plan.entry.direction }}                # "long"
{{ agent_verdicts.technical.confidence }}       # 85
{{ trade_plan.exits.profit_targets[0].price_range[0] }}  # 150.50
```

### Available Filters

Custom Jinja2 filters for formatting:

| Filter | Usage | Example Output |
|--------|-------|----------------|
| `format_price` | `{{ 99.99 \| format_price }}` | `$99.99` |
| `format_list` | `{{ items \| format_list }}` | Markdown bullets |
| `title_case` | `{{ "snake_case" \| title_case }}` | `Snake Case` |
| `join_list` | `{{ items \| join_list(", ") }}` | `A, B, C` |
| `safe_get` | `{{ data \| safe_get("key", default="N/A") }}` | Safe nested access |

### Template Example

See `examples/custom-template-example.md` for a complete custom template example.

## Examples

### Convert a trading plan
```bash
json-holygrail examples/trade-plan-FCEL-2025-12-18.json
```

**Output:** `examples/trade-plan-FCEL-2025-12-18.md` (using default format)

### Use compact format
```bash
json-holygrail examples/trade-plan-FCEL-2025-12-18.json --format compact
```

### Create and use custom template
```bash
# Create your template
cat > my-template.md << 'EOF'
# {{ ticker }} Trade Plan
**Direction**: {{ trade_plan.entry.direction | upper }}
**Target**: {{ trade_plan.exits.profit_targets[0].price_range[0] | format_price }}
EOF

# Use it
json-holygrail input.json --format my-template.md
```

### View the generated markdown
```bash
cat examples/trade-plan-FCEL-2025-12-18.md
# Or open in your favorite markdown viewer
```

## Error Handling

The tool handles:
- Missing optional fields (uses defaults)
- Invalid JSON (shows clear error message)
- File not found errors
- File I/O errors

## Project Structure

```
json-holygrail/
├── json_holygrail/           # Main package
│   ├── __init__.py          # Package initialization
│   ├── main.py              # CLI and main logic
│   ├── renderer.py          # Template rendering engine
│   ├── filters.py           # Jinja2 custom filters
│   ├── config.py            # Configuration management
│   ├── version_manager.py   # Version tracking
│   └── formats/             # Embedded templates
│       ├── default.md       # Default format
│       └── compact.md       # Compact format
├── examples/                 # Example files
│   ├── trade-plan-*.json    # Example trading plans
│   └── custom-template-example.md  # Custom template example
├── PRD.md                   # Product Requirements Document
├── README.md                # This file
├── pyproject.toml           # Project configuration
├── setup.py                 # Build configuration
└── install.sh               # Installation script
```

## Development

See `PRD.md` for:
- Detailed requirements
- Formatting specifications
- Testing strategy
- Future enhancements

## License

MIT License

## Support

For issues or questions, please refer to the PRD.md documentation.
