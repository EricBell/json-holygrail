{% if not trade_plan.trade %}
# No Trade Recommended

**Reason**: {{ trade_plan.no_trade_reason | default("No trade recommendation") }}
{% else %}
{# Header Section #}
# {{ ticker | default("UNKNOWN") }} {{ trade_plan.entry.direction | default("UNKNOWN") | upper }}

**Confidence**: {{ trade_plan.verdict.confidence | default("Unknown") }}

## Trigger
> {{ trade_plan.entry.wait_for | default("No specific entry instructions provided") }}

## Trade Parameters

| **Position Size** | **Stop Loss** | **Target** | **Risk Note** |
|-------------------|---------------|------------|---------------|
| {{ trade_plan.position.size_recommendation | default("Unknown") | upper }} | {% if trade_plan.exits.stop_loss.price_range %}{% if trade_plan.exits.stop_loss.price_range | length == 1 %}${{ "%.2f" | format(trade_plan.exits.stop_loss.price_range[0]) }}{% else %}${{ "%.2f" | format(trade_plan.exits.stop_loss.price_range[0]) }} – ${{ "%.2f" | format(trade_plan.exits.stop_loss.price_range[-1]) }}{% endif %}{% else %}Not set{% endif %} | {% if trade_plan.exits.profit_targets %}{% if trade_plan.exits.profit_targets[0].price_range %}{% if trade_plan.exits.profit_targets[0].price_range | length == 1 %}${{ "%.2f" | format(trade_plan.exits.profit_targets[0].price_range[0]) }}{% else %}${{ "%.2f" | format(trade_plan.exits.profit_targets[0].price_range[0]) }} – ${{ "%.2f" | format(trade_plan.exits.profit_targets[0].price_range[-1]) }}{% endif %}{% else %}Not set{% endif %}{% else %}Not set{% endif %} | Risk {{ risk_percent | default(0) }}% of account ({{ trade_plan.position.max_risk | default("Unknown") }}) |

## Technical Alignment
{% if agent_verdicts.technical.reasoning %}{{ agent_verdicts.technical.reasoning[:2] | join_list(" ") }}{% else %}No technical summary available{% endif %}

---

**{% if trade_plan.verdict.action %}{{ trade_plan.verdict.action.split()[0] }}{% else %}TRADE{% endif %} {% if "STOCK" in (asset_type | default("ASSET") | upper) %}STOCK{% elif "FUTURES" in (asset_type | default("ASSET") | upper) or "FUTURE" in (asset_type | default("ASSET") | upper) %}FUTURES{% elif "OPTION" in (asset_type | default("ASSET") | upper) %}OPTIONS{% else %}ASSET{% endif %}     {% if "STOCK" in (asset_type | default("ASSET") | upper) %}STOCK{% elif "FUTURES" in (asset_type | default("ASSET") | upper) or "FUTURE" in (asset_type | default("ASSET") | upper) %}FUTURES{% elif "OPTION" in (asset_type | default("ASSET") | upper) %}OPTIONS{% else %}ASSET{% endif %}     {{ trade_style | default("TRADE") }}**

---

## Agent Verdicts

| **TECHNICAL** | **MACRO** | **WILD CARD** |
|---------------|-----------|---------------|
| **{{ agent_verdicts.technical.direction | default("Unknown") | upper }}** ({{ agent_verdicts.technical.confidence | default(0) }}%) | **{{ agent_verdicts.macro.market_regime | default("Unknown") | replace("_", " ") | upper }}** ({{ agent_verdicts.macro.confidence | default(0) }}%) | **{{ agent_verdicts.wild_card.overall_risk_assessment | default("Unknown") | upper }}** |

### Technical Agent

**Direction**: {{ agent_verdicts.technical.direction | default("Unknown") | upper }} | **Confidence**: {{ agent_verdicts.technical.confidence | default(0) }}%

**Entry Type**: {{ agent_verdicts.technical.entry_type | default("Unknown") | title_case }}

{% if agent_verdicts.technical.support_levels %}
**Support Levels**:
{% if agent_verdicts.technical.support_levels.minor %}
- Minor: {{ agent_verdicts.technical.support_levels.minor | join_list(", ") }}
{% endif %}
{% if agent_verdicts.technical.support_levels.major %}
- Major: {{ agent_verdicts.technical.support_levels.major | join_list(", ") }}
{% endif %}
{% if agent_verdicts.technical.support_levels.key_references %}
- Key References:
{% for key, val in agent_verdicts.technical.support_levels.key_references.items() %}
  - {{ key | replace("_", " ") | upper }}: {{ val }}
{% endfor %}
{% endif %}

{% endif %}
{% if agent_verdicts.technical.resistance_levels %}
**Resistance Levels**:
{% if agent_verdicts.technical.resistance_levels.minor %}
- Minor: {{ agent_verdicts.technical.resistance_levels.minor | join_list(", ") }}
{% endif %}
{% if agent_verdicts.technical.resistance_levels.major %}
- Major: {{ agent_verdicts.technical.resistance_levels.major | join_list(", ") }}
{% endif %}
{% if agent_verdicts.technical.resistance_levels.key_references %}
- Key References:
{% for key, val in agent_verdicts.technical.resistance_levels.key_references.items() %}
  - {{ key | replace("_", " ") | upper }}: {{ val }}
{% endfor %}
{% endif %}

{% endif %}
{% if agent_verdicts.technical.chart_patterns %}
**Chart Patterns**:
{{ agent_verdicts.technical.chart_patterns | format_list }}

{% endif %}
**MTF Alignment**: {{ agent_verdicts.technical.mtf_alignment | default("Unknown") }} | **Volatility**: {{ agent_verdicts.technical.volatility | default("Unknown") }}

{% if agent_verdicts.technical.reasoning %}
**Technical Reasoning**:
{{ agent_verdicts.technical.reasoning | format_list }}

{% endif %}
---

### Macro Agent

**Market Regime**: {{ agent_verdicts.macro.market_regime | default("Unknown") | title_case }} | **Confidence**: {{ agent_verdicts.macro.confidence | default(0) }}%

**SPY Direction**: {{ agent_verdicts.macro.spy_direction | default("Unknown") | upper }} | **QQQ Direction**: {{ agent_verdicts.macro.qqq_direction | default("Unknown") | upper }}

**Cross Asset Alignment**: {{ agent_verdicts.macro.cross_asset_alignment | default("Unknown") | title }}

{% if agent_verdicts.macro.session_context %}
**Session Context**:
- Type: {{ agent_verdicts.macro.session_context.type | default("Unknown") | title_case }}
{% if agent_verdicts.macro.session_context.risk_note %}
- Risk Note: {{ agent_verdicts.macro.session_context.risk_note }}
{% endif %}

{% endif %}
{% if agent_verdicts.macro.economic_assessment %}
**Economic Assessment**:
{% if agent_verdicts.macro.economic_assessment.macro_headwinds %}
- Headwinds:
{% for hw in agent_verdicts.macro.economic_assessment.macro_headwinds %}
  - {{ hw }}
{% endfor %}
{% endif %}
{% if agent_verdicts.macro.economic_assessment.macro_tailwinds %}
- Tailwinds:
{% for tw in agent_verdicts.macro.economic_assessment.macro_tailwinds %}
  - {{ tw }}
{% endfor %}
{% endif %}

{% endif %}
{% if agent_verdicts.macro.news_sentiment %}
**News Sentiment**:
- Overall: {{ agent_verdicts.macro.news_sentiment.overall | default("Unknown") | title }}
{% if agent_verdicts.macro.news_sentiment.key_themes %}
- Key Themes: {{ agent_verdicts.macro.news_sentiment.key_themes | join_list(", ") }}
{% endif %}

{% endif %}
{% if agent_verdicts.macro.reasoning %}
**Macro Reasoning**:
{{ agent_verdicts.macro.reasoning | format_list }}

{% endif %}
---

### Wild Card Agent

**Overall Risk Assessment**: {{ agent_verdicts.wild_card.overall_risk_assessment | default("Unknown") | upper }}

{% if agent_verdicts.wild_card.wild_cards_identified %}
**Identified Wild Cards**:

{% for wc in agent_verdicts.wild_card.wild_cards_identified %}
{{ loop.index }}. **{{ wc.type | default("Unknown") | title_case }}**: {{ wc.description | default("N/A") }}
   - **Probability**: {{ wc.probability | default("Unknown") | title }}
   - **Impact**: {{ wc.impact | default("Unknown") | title }}
   - **Mitigation**: {{ wc.mitigation | default("None") }}

{% endfor %}
{% endif %}
{% if agent_verdicts.wild_card.recommended_contingencies %}
**Recommended Contingencies**:
{{ agent_verdicts.wild_card.recommended_contingencies | format_list }}

{% endif %}
{% if agent_verdicts.wild_card.timing_considerations %}
**Timing Considerations**:
{{ agent_verdicts.wild_card.timing_considerations | format_list }}

{% endif %}
{% if agent_verdicts.wild_card.honest_uncertainty %}
> **Honest Uncertainty**: {{ agent_verdicts.wild_card.honest_uncertainty }}

{% endif %}
---

## Key Metrics

| Metric | Value |
|--------|-------|
| **Account Size** | {{ account_size | format_price }} |
| **Risk Percent** | {{ risk_percent | default(0) }}% |
| **Max Risk** | {{ trade_plan.position.max_risk | default("Unknown") }} |
| **Current Price** | {{ trade_plan.entry.current_price | format_price }} |

---
## Trade Details

### Entry Zone

**Direction**: {{ trade_plan.entry.direction | default("Unknown") }}

**Recommendation**: {{ trade_plan.entry.recommendation | default("Unknown") | title_case }}

{% if trade_plan.entry.ideal_zone %}
**Ideal Entry Zone**:
- Low: {{ trade_plan.entry.ideal_zone.low | format_price }}
- Mid: {{ trade_plan.entry.ideal_zone.mid | format_price }}
- High: {{ trade_plan.entry.ideal_zone.high | format_price }}
- Confidence: {{ trade_plan.entry.ideal_zone.confidence | default("Unknown") }}

{% endif %}
{% if trade_plan.entry.wait_for %}
> **Wait For**: {{ trade_plan.entry.wait_for }}

{% endif %}
---

### Position Sizing

**Size Recommendation**: {{ trade_plan.position.size_recommendation | default("Unknown") | title }}

**Quantity**: {{ trade_plan.position.quantity | default(0) }} {{ trade_plan.position.unit_type | default("units") }}

**Total Cost**: {{ trade_plan.position.total_cost | default("Unknown") }}

**Max Risk**: {{ trade_plan.position.max_risk | default("Unknown") }}

{% if trade_plan.position.rationale %}
**Rationale**: {{ trade_plan.position.rationale }}

{% endif %}
---

## Exit Strategy

{% if trade_plan.exits.stop_loss %}
### Stop Loss

{% if trade_plan.exits.stop_loss.price_range %}
**Price Range**: {{ trade_plan.exits.stop_loss.price_range[0] | format_price }} - {{ trade_plan.exits.stop_loss.price_range[-1] | format_price }}

{% endif %}
**Total Loss**: {{ trade_plan.exits.stop_loss.total_loss | default("Unknown") }}

{% if trade_plan.exits.stop_loss.rationale %}
**Rationale**: {{ trade_plan.exits.stop_loss.rationale }}

{% endif %}
{% endif %}
{% if trade_plan.exits.profit_targets %}
### Profit Targets

{% for target in trade_plan.exits.profit_targets %}
**Target {{ target.target | default(loop.index) }}**:
{% if target.price_range %}
- Price Range: {{ target.price_range[0] | format_price }} - {{ target.price_range[-1] | format_price }}
{% endif %}
- Position %: {{ target.position_percent | default(0) }}%
- Probability: {{ target.probability | default("Unknown") }}

{% endfor %}
{% endif %}
{% if trade_plan.exits.time_stop %}
### Time Stop

**Duration**: {{ trade_plan.exits.time_stop.date_or_duration | default("Unknown") }}

{% if trade_plan.exits.time_stop.rationale %}
**Rationale**: {{ trade_plan.exits.time_stop.rationale }}

{% endif %}
{% endif %}
---

## Wild Cards & Warnings

{% if trade_plan.wild_cards.identified_risks %}
### Identified Risks

{% for risk in trade_plan.wild_cards.identified_risks %}
- **{{ risk.risk | default("Unknown") }}**
  - Probability: {{ risk.probability | default("Unknown") | title }}
  - Impact: {{ risk.impact | default("Unknown") | title }}
  - Contingency: {{ risk.contingency | default("None") }}

{% endfor %}
{% endif %}
{% if trade_plan.wild_cards.manual_checks_required %}
### Manual Checks Required

{{ trade_plan.wild_cards.manual_checks_required | format_list }}

{% endif %}
{% if trade_plan.wild_cards.honest_uncertainty %}
> **Honest Uncertainty**: {{ trade_plan.wild_cards.honest_uncertainty }}

{% endif %}
---

## Execution Checklist

{% set execution_steps = [] %}
{% for key in trade_plan.execution_plan.keys() %}
{% if key.startswith("step_") %}
{% set _ = execution_steps.append(key) %}
{% endif %}
{% endfor %}
{% if execution_steps %}
{% for step_key in execution_steps | sort %}
{{ step_key.split("_")[1] }}. {{ trade_plan.execution_plan[step_key] }}
{% endfor %}

{% else %}
- No execution steps defined

{% endif %}
---

## Pre-Trading Checklist

**Safe to Trade**: {% if pre_trade_checks.safe_to_trade %}✅ YES{% else %}❌ NO{% endif %}

{% if pre_trade_checks.warnings %}
### Warnings

{{ pre_trade_checks.warnings | format_list }}

{% endif %}
{% if pre_trade_checks.critical_events %}
### Critical Events

{{ pre_trade_checks.critical_events | format_list }}

{% endif %}
{% if pre_trade_checks.news_summary %}
**News Summary**: {{ pre_trade_checks.news_summary }}

{% endif %}
{% if pre_trade_checks.manual_check_required %}
> ⚠️ **MANUAL CHECK REQUIRED BEFORE TRADING**

{% endif %}
---

{% endif %}
