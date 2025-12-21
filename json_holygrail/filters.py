"""
Jinja2 filters for template rendering
Provides formatting functions as Jinja2 filters
"""

from typing import Any, List, Dict


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


def title_case(text: str) -> str:
    """Convert snake_case to Title Case"""
    return text.replace("_", " ").title()


def join_list(items: List[Any], separator: str = ", ") -> str:
    """Join list items with a separator"""
    if not items:
        return ""
    return separator.join(map(str, items))


def safe_get(data: Dict[str, Any], *keys, default=None) -> Any:
    """
    Safely access nested dictionary values
    Usage in template: {{ data | safe_get('key1', 'key2', default='fallback') }}
    """
    result = data
    for key in keys:
        if isinstance(result, dict):
            result = result.get(key)
            if result is None:
                return default
        else:
            return default
    return result if result is not None else default


def register_filters(env):
    """Register all custom filters with a Jinja2 environment"""
    env.filters['format_price'] = format_price
    env.filters['format_list'] = format_list
    env.filters['format_dict_as_list'] = format_dict_as_list
    env.filters['title_case'] = title_case
    env.filters['join_list'] = join_list
    env.filters['safe_get'] = safe_get
    return env
