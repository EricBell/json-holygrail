<!--
Custom Template Example for json-holygrail
This is a complete example showing how to create a custom Jinja2 template
for formatting trading plan output.

Save this file and use it with:
  json-holygrail input.json --format path/to/this-template.md
-->

{% if not trade_plan.trade %}
# ❌ NO TRADE: {{ ticker }}

{{ trade_plan.no_trade_reason | default("No trade recommendation") }}

{% else %}
# {{ ticker }} Trade Analysis
**Generated**: {{ "now" if not timestamp else timestamp }}

---

## 📋 Executive Summary

| Aspect | Details |
|--------|---------|
| **Ticker** | {{ ticker }} |
| **Direction** | {{ trade_plan.entry.direction | upper }} |
| **Confidence** | {{ trade_plan.verdict.confidence }}% |
| **Asset Type** | {{ asset_type | default("N/A") }} |
| **Trade Style** | {{ trade_style | default("N/A") }} |

---

## 💰 Position & Risk

**Account Size**: {{ account_size | format_price }}
**Risk Tolerance**: {{ risk_percent }}% ({{ trade_plan.position.max_risk | default("Unknown") }})
**Position Size**: {{ trade_plan.position.size_recommendation | title }} - {{ trade_plan.position.quantity }} {{ trade_plan.position.unit_type | default("units") }}

### Entry Strategy
{{ trade_plan.entry.recommendation | title_case }} @ {{ trade_plan.entry.current_price | format_price }}

{% if trade_plan.entry.ideal_zone %}
**Ideal Entry Zone:**
- Low: {{ trade_plan.entry.ideal_zone.low | format_price }}
- Mid: {{ trade_plan.entry.ideal_zone.mid | format_price }}
- High: {{ trade_plan.entry.ideal_zone.high | format_price }}
{% endif %}

> **Wait For**: {{ trade_plan.entry.wait_for | default("No specific trigger") }}

### Exit Levels

{% if trade_plan.exits.stop_loss %}
**Stop Loss**: {% if trade_plan.exits.stop_loss.price_range %}{{ trade_plan.exits.stop_loss.price_range[0] | format_price }} - {{ trade_plan.exits.stop_loss.price_range[-1] | format_price }}{% else %}Not set{% endif %}
*Max Loss*: {{ trade_plan.exits.stop_loss.total_loss | default("Unknown") }}
{% endif %}

{% if trade_plan.exits.profit_targets %}
**Profit Targets**:
{% for target in trade_plan.exits.profit_targets %}
- Target {{ loop.index }}: {{ target.price_range[0] | format_price }}{% if target.price_range | length > 1 %} - {{ target.price_range[-1] | format_price }}{% endif %} ({{ target.position_percent }}%)
{% endfor %}
{% endif %}

---

## 🎯 Agent Analysis

### Technical ({{ agent_verdicts.technical.confidence }}% confidence)
**Direction**: {{ agent_verdicts.technical.direction | upper }}
**Entry Type**: {{ agent_verdicts.technical.entry_type | title_case }}
**MTF Alignment**: {{ agent_verdicts.technical.mtf_alignment | default("Unknown") }}

{% if agent_verdicts.technical.reasoning %}
**Key Points**:
{{ agent_verdicts.technical.reasoning | format_list }}
{% endif %}

### Macro ({{ agent_verdicts.macro.confidence }}% confidence)
**Market Regime**: {{ agent_verdicts.macro.market_regime | title_case }}
**SPY**: {{ agent_verdicts.macro.spy_direction | upper }} | **QQQ**: {{ agent_verdicts.macro.qqq_direction | upper }}

{% if agent_verdicts.macro.reasoning %}
**Analysis**:
{{ agent_verdicts.macro.reasoning | format_list }}
{% endif %}

### Wild Card
**Risk Assessment**: {{ agent_verdicts.wild_card.overall_risk_assessment | upper }}

{% if agent_verdicts.wild_card.wild_cards_identified %}
**Identified Risks**:
{% for wc in agent_verdicts.wild_card.wild_cards_identified %}
{{ loop.index }}. **{{ wc.type | title_case }}** ({{ wc.probability }}/{{ wc.impact }})
   - {{ wc.description }}
   - Mitigation: {{ wc.mitigation | default("None") }}
{% endfor %}
{% endif %}

---

## ✅ Execution Plan

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
*No execution steps defined*
{% endif %}

---

## 🚦 Pre-Trade Status

{% if pre_trade_checks.safe_to_trade %}
### ✅ CLEARED TO TRADE
{% else %}
### ❌ NOT SAFE TO TRADE
{% endif %}

{% if pre_trade_checks.warnings %}
**Warnings**:
{{ pre_trade_checks.warnings | format_list }}
{% endif %}

{% if pre_trade_checks.critical_events %}
**Critical Events**:
{{ pre_trade_checks.critical_events | format_list }}
{% endif %}

{% if pre_trade_checks.manual_check_required %}
> ⚠️ **MANUAL VERIFICATION REQUIRED BEFORE EXECUTING**
{% endif %}

---

*Generated with json-holygrail*

{% endif %}
