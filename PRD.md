# Product Requirements Document: Trading Plan JSON-to-Markdown Converter

## Project Overview

**Project Name**: json-holyGrail
**Purpose**: Convert structured trading plan JSON data into formatted markdown documents for easy readability and review.
**Input**: JSON file containing comprehensive trading analysis (technical, macro, wild cards, trade plan)
**Output**: Markdown file formatted as a professional trading plan document

---

## Requirements

### Functional Requirements

1. **JSON Parsing**: Parse the complete trading plan JSON structure
2. **Markdown Generation**: Generate a well-formatted markdown document matching the reference layout
3. **Data Validation**: Validate required fields exist in the JSON
4. **File I/O**: Read JSON from file, write markdown to file
5. **Error Handling**: Handle missing fields gracefully with appropriate defaults or warnings

### Output Format Specifications

The generated markdown should include the following sections in order:

#### 1. Header Section
- **Title**: Display trade action (e.g., "SHORT STOCK", "LONG STOCK") prominently
- **Confidence**: Show confidence percentage from verdict
- **Ticker & Asset Type**: Display ticker symbol and asset type (FUTURES, STOCKS, etc.)
- **Trade Style**: Show trade style (SCALP, SWING, etc.)

#### 2. Key Metrics Summary
Display in a box/callout format:
- Account Size
- Risk Percent
- Max Risk (dollar amount)
- Current Price

#### 3. Agent Verdicts
Three subsections with consistent formatting:

**Technical Agent**:
- Direction & Confidence
- Entry Type
- Support Levels (minor, major, key references)
- Resistance Levels (minor, major, key references)
- Chart Patterns
- MTF Alignment & Volatility
- Reasoning (bullet points)

**Macro Agent**:
- Market Regime & Confidence
- SPY/QQQ Direction
- Cross Asset Alignment
- Session Context
- Economic Assessment
- News Sentiment
- International Assessment
- Reasoning (bullet points)

**Wild Card Agent**:
- Wild Cards Identified (type, description, probability, impact, mitigation)
- Overall Risk Assessment
- Recommended Contingencies
- Timing Considerations
- Honest Uncertainty

#### 4. Trade Details

**Entry Zone**:
- Direction (SHORT/LONG)
- Recommendation
- Ideal Zone (low, mid, high with confidence)
- Current Price
- Wait For instructions

**Position Sizing**:
- Size Recommendation
- Rationale
- Quantity & Unit Type
- Total Cost/Margin Requirement
- Max Risk

#### 5. Exit Strategy

**Stop Loss**:
- Price Range
- Total Loss (dollar amount)
- Rationale

**Profit Targets**:
- Target 1: Price range, position %, probability
- Target 2: Price range, position %, probability (if applicable)

**Time Stop**:
- Duration or specific time
- Rationale

#### 6. Wild Cards & Warnings

**Identified Risks**:
For each risk:
- Risk description
- Probability (high/medium/low)
- Impact (severe/moderate/minor)
- Contingency plan

**Manual Checks Required**:
- List all pre-trade manual verification items

**Honest Uncertainty**:
- Display the uncertainty statement

#### 7. Execution Checklist

**Step-by-step execution plan**:
- Step 1: Order placement details
- Step 2: Bracket/OCO setup
- Step 3: Monitoring instructions

#### 8. Pre-Trading Checklist

**Safety Checks**:
- Safe to Trade status
- Warnings
- Critical Events
- News Summary
- Earnings Upcoming
- Major Events
- Manual Check Required status

---

## Formatting Guidelines

### Visual Hierarchy
- Use `#` for main sections
- Use `##` for subsections
- Use `###` for sub-subsections
- Use **bold** for labels and emphasis
- Use *italic* for notes
- Use `code blocks` for prices and numerical values

### Data Presentation
- **Lists**: Use bullet points for reasoning, warnings, and contingencies
- **Tables**: Consider using tables for support/resistance levels
- **Callouts**: Use blockquotes (>) for important warnings
- **Color Coding** (if supported):
  - Green text for profit targets
  - Red text for stop losses
  - Yellow/Amber for warnings

### Numerical Formatting
- **Prices**: Display with appropriate decimal places (e.g., 6831.50)
- **Percentages**: Include % symbol (e.g., 70%)
- **Dollar Amounts**: Include $ symbol (e.g., $20.00)
- **Probability**: Use text format (e.g., "high", "medium", "low")

---

## Technical Specifications

### Input Requirements
- **Format**: Valid JSON file
- **Structure**: Must match the schema from sample file
- **Required Fields**:
  - `status`
  - `ticker`
  - `asset_type`
  - `trade_style`
  - `agent_verdicts` (technical, macro, wild_card)
  - `trade_plan`
  - `pre_trade_checks`

### Output Requirements
- **Format**: Markdown (.md) file
- **Encoding**: UTF-8
- **Line Endings**: Unix-style (LF)
- **File Naming**: `trade-plan-{TICKER}-{DATE}.md`

### Error Handling
- Missing optional fields: Skip section or use default text
- Missing required fields: Display warning and use placeholder
- Invalid JSON: Return clear error message
- File I/O errors: Return appropriate error with details

---

## Implementation Notes

### Python Implementation
- Use `json` module for parsing
- Use f-strings for markdown formatting
- Consider using Jinja2 templates for complex layouts
- Add logging for debugging

### Testing Strategy
1. Test with complete JSON (all fields present)
2. Test with minimal JSON (only required fields)
3. Test with malformed JSON
4. Test with edge cases (empty arrays, null values)
5. Verify markdown renders correctly in viewers

### Future Enhancements
- Add support for multiple trade plans in one document
- Generate HTML output option
- Add charts/graphs using matplotlib
- CLI tool with arguments for input/output paths
- Watch mode for automatic regeneration

---

## Success Criteria

1. Correctly parses all fields from sample JSON
2. Generates markdown matching reference layout
3. Handles missing optional fields gracefully
4. Produces readable, well-formatted output
5. Executes without errors on valid input
6. Provides clear error messages on invalid input

---

## Sample Usage

```bash
# Basic usage
python main.py trade-plan-MES-2025-12-14.json

# Specify output file
python main.py input.json -o output.md

# Verbose mode
python main.py input.json --verbose
```

---

## File Structure

```
json-holyGrail/
├── main.py              # Entry point and CLI
├── converter.py         # Core conversion logic
├── templates/           # Markdown templates (if using templating)
├── tests/              # Unit tests
├── examples/           # Sample input/output files
├── README.md           # User documentation
├── PRD.md              # This document
└── pyproject.toml      # Project configuration
```
