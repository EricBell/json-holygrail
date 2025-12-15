# json-holyGrail

A Python tool that converts trading plan JSON files into formatted markdown documents.

## Features

- Converts comprehensive trading analysis JSON to readable markdown
- Supports all trading plan sections: Technical, Macro, Wild Cards, Entry/Exit strategies
- Handles futures, stocks, and other asset types
- Automatic formatting of prices, percentages, and risk levels
- Clean, well-structured output perfect for review and documentation

## Installation

```bash
# Clone or navigate to the repository
cd json-holyGrail

# Ensure Python 3.12+ is installed
python --version
```

No additional dependencies required - uses only Python standard library.

## Usage

### Basic Usage

```bash
python main.py <input.json>
```

This will create a markdown file with the same name as your input file.

**Example:**
```bash
python main.py trade-plan-MES-2025-12-14.json
# Creates: trade-plan-MES-2025-12-14.md
```

### Specify Output File

```bash
python main.py <input.json> -o <output.md>
```

**Example:**
```bash
python main.py input.json -o my-trade-plan.md
```

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

## Output Format

The generated markdown includes:

1. **Header** - Ticker, action (SHORT/LONG), confidence
2. **Key Metrics** - Account size, risk %, max risk, current price
3. **Agent Verdicts** - Technical, Macro, and Wild Card analysis
4. **Trade Details** - Entry zones and position sizing
5. **Exit Strategy** - Stop loss, profit targets, time stops
6. **Wild Cards & Warnings** - Risk assessment and contingencies
7. **Execution Checklist** - Step-by-step execution plan
8. **Pre-Trading Checklist** - Safety checks and warnings

## Examples

### Convert a trading plan
```bash
python main.py trade-plan-MES-2025-12-14.json
```

**Output:** `trade-plan-MES-2025-12-14.md`

### View the generated markdown
```bash
cat trade-plan-MES-2025-12-14.md
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
json-holyGrail/
├── main.py              # Converter implementation
├── PRD.md              # Product Requirements Document
├── README.md           # This file
├── pyproject.toml      # Project configuration
└── .python-version     # Python version specification
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
