# Implementation Plan: Multiple Output Format Support with Jinja2 Templates

## Overview
Add support for multiple markdown output formats using Jinja2 templates. Users can select formats via `--format` CLI option, with default format stored in a config file. Templates can be embedded in the package or provided as external files.

## Requirements
- Support Jinja2 templates with variables ({{ ticker }}, {% for %}, etc.)
- Templates stored in `formats/` directory within package
- Support both embedded templates (just filename) and external templates (full path)
- CLI: `--format xyz` where xyz is template name or full path
- Default format read from `.json-holygrail.toml` config file
- All current helper functions available as Jinja2 filters

## Architecture Changes

### Convert from Flat Module to Package Structure
**Current**: Flat py-modules in root (main.py, version_manager.py)
**New**: Proper package structure:
```
json_holygrail/
├── __init__.py
├── main.py (refactored)
├── renderer.py (NEW)
├── filters.py (NEW)
├── config.py (NEW)
├── version_manager.py (moved)
└── formats/
    ├── __init__.py
    ├── default.md (NEW - current output as template)
    └── compact.md (NEW - example alternative)
```

### New Components

#### 1. Template Renderer (`json_holygrail/renderer.py`)
```python
class TemplateRenderer:
    - Uses Jinja2 Environment with ChoiceLoader
    - PackageLoader for embedded templates (formats/ directory)
    - FileSystemLoader for external template paths
    - get_template(format_name) - resolves template by name or path
    - render(template_name, context) - renders template with JSON data
```

**Template Resolution**:
- If format contains `/` or `\`: treat as external file path
- Otherwise: treat as embedded template name, look in formats/ directory
- Auto-append `.md` if not present

#### 2. Jinja2 Filters (`json_holygrail/filters.py`)
Register existing helper functions as filters:
- `format_price` - Currency/numeric formatting
- `format_list` - Convert list to markdown bullets
- `format_dict_as_list` - Convert dict to key-value bullets
- `title_case` - Clean snake_case to Title Case
- `join_list` - Join list items with separator
- `safe_get` - Safe nested dict access

#### 3. Configuration Manager (`json_holygrail/config.py`)
```python
class Config:
    - Loads .json-holygrail.toml from cwd or home directory
    - get_default_format() - returns default format name
    - Fallback to "default" if no config found
```

**Config File Format** (`.json-holygrail.toml`):
```toml
[format]
default = "default"  # or "/path/to/template.md"
```

## Implementation Steps

### Step 1: Create Package Structure
1. Create `json_holygrail/` directory
2. Create `__init__.py` with version info
3. Move `main.py` into package
4. Move `version_manager.py` into package
5. Create `formats/` subdirectory with `__init__.py`

### Step 2: Implement Core Modules
1. **Create `renderer.py`**:
   - TemplateRenderer class
   - Jinja2 environment setup with ChoiceLoader
   - Template resolution logic (embedded vs external)

2. **Create `filters.py`**:
   - Move format_price, format_list, format_dict_as_list from main.py
   - Create register_filters(env) function
   - Add new utility filters (title_case, join_list, safe_get)

3. **Create `config.py`**:
   - Config class with TOML file loading
   - Search cwd → home directory → defaults
   - get_default_format() method

### Step 3: Create Default Template
1. **Create `formats/default.md`**:
   - Convert all 8 `generate_*` functions to Jinja2 template
   - Use Jinja2 syntax: `{{ variable }}`, `{% if %}`, `{% for %}`
   - Apply filters: `{{ value | format_price }}`
   - Must produce identical output to current code (backward compatibility)

2. **Create `formats/compact.md`**:
   - Example alternative format
   - Condensed layout for demonstration

### Step 4: Refactor main.py
1. **Update imports**:
   - Import TemplateRenderer, Config
   - Update import paths for new package structure

2. **Refactor `convert_json_to_markdown()`**:
   ```python
   def convert_json_to_markdown(json_data: Dict[str, Any], format_name: str = "default") -> str:
       # Check trade flag
       if not trade_plan.get("trade", False):
           return no_trade_message

       # Render using template
       renderer = TemplateRenderer()
       return renderer.render(format_name, json_data)
   ```

3. **Update CLI**:
   - Add `--format` option to cli_main()
   - Add `--list-formats` option to list embedded templates
   - Load config to get default format
   - Pass format_name to convert_json_to_markdown()

4. **Remove old generate_* functions**:
   - Keep helper functions (they become filters)
   - Remove generate_header, generate_agent_verdicts, etc.

### Step 5: Update Build Configuration

1. **Update `pyproject.toml`**:
   ```toml
   [project]
   dependencies = [
       "typer>=0.9.0",
       "jinja2>=3.1.0",  # NEW
       "toml>=0.10.2",   # NEW
   ]

   [project.scripts]
   json-holygrail = "json_holygrail.main:main"  # Updated path

   [tool.setuptools]
   packages = ["json_holygrail"]  # Changed from py-modules

   [tool.setuptools.package-data]
   json_holygrail = ["formats/*.md"]  # Include templates
   ```

2. **Update `setup.py`**:
   ```python
   setup(
       packages=find_packages(),
       package_data={'json_holygrail': ['formats/*.md', 'version.json']},
       cmdclass={'build_py': CustomBuildPy},
   )
   ```
   - Update CustomBuildPy to copy version.json to json_holygrail/ directory

3. **Update `MANIFEST.in`**:
   ```
   include json_holygrail/formats/*.md
   include json_holygrail/version.json
   ```

### Step 6: Update Version Manager
1. Update import paths in version_manager.py for new location
2. Update tracked_files patterns to match new structure
3. Update version.json path resolution

### Step 7: Testing
1. Create test templates in formats/
2. Test template loading (embedded vs external)
3. Test filter registration and usage
4. Test config file loading
5. Regression test: default template produces identical output
6. Test CLI --format option with different formats
7. Test --list-formats option

### Step 8: Documentation
1. Update README with:
   - How to use --format option
   - How to list available formats
   - How to create custom templates
   - Template variable reference
2. Create example custom template
3. Document config file format

## Critical Files to Modify

### New Files
- `/home/eric/workspace/original/json-holygrail/json_holygrail/__init__.py`
- `/home/eric/workspace/original/json-holygrail/json_holygrail/renderer.py`
- `/home/eric/workspace/original/json-holygrail/json_holygrail/filters.py`
- `/home/eric/workspace/original/json-holygrail/json_holygrail/config.py`
- `/home/eric/workspace/original/json-holygrail/json_holygrail/formats/__init__.py`
- `/home/eric/workspace/original/json-holygrail/json_holygrail/formats/default.md`
- `/home/eric/workspace/original/json-holygrail/json_holygrail/formats/compact.md`

### Modified Files
- `/home/eric/workspace/original/json-holygrail/json_holygrail/main.py` (moved and refactored)
- `/home/eric/workspace/original/json-holygrail/json_holygrail/version_manager.py` (moved)
- `/home/eric/workspace/original/json-holygrail/pyproject.toml`
- `/home/eric/workspace/original/json-holygrail/setup.py`
- `/home/eric/workspace/original/json-holygrail/MANIFEST.in`

## Template Variable Reference

Templates have access to entire JSON structure:

**Top-level**:
- `ticker`, `status`, `asset_type`, `trade_style`
- `account_size`, `risk_percent`
- `agent_verdicts` (dict with technical, macro, wild_card)
- `trade_plan` (dict with verdict, entry, position, exits, execution_plan)
- `pre_trade_checks`

**Nested structures**:
- `trade_plan.verdict.*` - action, confidence
- `trade_plan.entry.*` - direction, recommendation, ideal_zone, wait_for
- `trade_plan.position.*` - size_recommendation, quantity, max_risk
- `trade_plan.exits.*` - stop_loss, profit_targets, time_stop
- `agent_verdicts.technical.*`, `agent_verdicts.macro.*`, `agent_verdicts.wild_card.*`

**Available filters**:
- `{{ value | format_price }}` - Format currency
- `{{ list | format_list }}` - Markdown bullets
- `{{ dict | format_dict_as_list }}` - Key-value bullets
- `{{ string | title_case }}` - Clean snake_case
- `{{ list | join_list }}` - Join with commas
- `{{ value | default("fallback") }}` - Default value

## Backward Compatibility

- Default template produces **identical** output to current code
- No breaking changes to CLI (--format is optional)
- Config file is optional (falls back to "default")
- Version bump: 0.1.x → 0.2.0 (minor version for new feature)

## Example Usage

```bash
# Use default format (from config or "default")
json-holygrail trade-plan.json

# Use specific embedded format
json-holygrail trade-plan.json --format compact

# Use external template
json-holygrail trade-plan.json --format /path/to/custom.md

# List available formats
json-holygrail --list-formats

# Set default format in config
echo '[format]\ndefault = "compact"' > .json-holygrail.toml
```

## Rollout Strategy

1. Implement in feature branch
2. Run regression tests (default template matches current output)
3. Test installation in clean environment
4. Update documentation
5. Bump version to 0.2.0
6. Merge to main
7. Update install.sh for new package structure
