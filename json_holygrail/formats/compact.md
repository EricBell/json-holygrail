{% if not trade_plan.trade %}
# ❌ NO TRADE: {{ ticker | default("UNKNOWN") }}
{{ trade_plan.no_trade_reason | default("No trade recommendation") }}
{% else %}
# {{ ticker | default("UNKNOWN") }} {{ trade_plan.entry.direction | default("?") | upper }} • {{ trade_plan.verdict.confidence | default("?") }}% confidence

## 📊 Quick Stats
**Entry**: {{ trade_plan.entry.recommendation | default("?") | title_case }} @ {{ trade_plan.entry.current_price | format_price }} | **Size**: {{ trade_plan.position.size_recommendation | default("?") | upper }} ({{ trade_plan.position.quantity | default(0) }} units) | **Risk**: {{ risk_percent | default(0) }}%

## 🎯 Levels
**Stop**: {% if trade_plan.exits.stop_loss.price_range %}${{ "%.2f" | format(trade_plan.exits.stop_loss.price_range[0]) }}{% else %}Not set{% endif %} | **Target**: {% if trade_plan.exits.profit_targets and trade_plan.exits.profit_targets[0].price_range %}${{ "%.2f" | format(trade_plan.exits.profit_targets[0].price_range[0]) }}{% else %}Not set{% endif %} | **Entry Zone**: {% if trade_plan.entry.ideal_zone %}${{ "%.2f" | format(trade_plan.entry.ideal_zone.low) }}-${{ "%.2f" | format(trade_plan.entry.ideal_zone.high) }}{% else %}N/A{% endif %}

## 🔍 Agent Consensus
- **Technical**: {{ agent_verdicts.technical.direction | default("?") | upper }} ({{ agent_verdicts.technical.confidence | default(0) }}%) • {{ agent_verdicts.technical.entry_type | default("?") | title_case }}
- **Macro**: {{ agent_verdicts.macro.market_regime | default("?") | title_case }} ({{ agent_verdicts.macro.confidence | default(0) }}%)
- **Wild Card**: {{ agent_verdicts.wild_card.overall_risk_assessment | default("?") | upper }}

## ⚡ Trigger
{{ trade_plan.entry.wait_for | default("No specific entry instructions") }}

## ⚠️ Key Risks
{% if trade_plan.wild_cards.identified_risks %}
{% for risk in trade_plan.wild_cards.identified_risks %}
- {{ risk.risk | default("Unknown") }} ({{ risk.probability | default("?") }}/{{ risk.impact | default("?") }})
{% endfor %}
{% else %}
- No specific risks identified
{% endif %}

## ✅ Execution
{% set execution_steps = [] %}
{% for key in trade_plan.execution_plan.keys() %}
{% if key.startswith("step_") %}
{% set _ = execution_steps.append(key) %}
{% endif %}
{% endfor %}
{% if execution_steps %}
{% for step_key in execution_steps | sort %}
{{ loop.index }}. {{ trade_plan.execution_plan[step_key] }}
{% endfor %}
{% else %}
No execution plan defined
{% endif %}

## 🚦 Pre-Trade Status
{% if pre_trade_checks.safe_to_trade %}✅ SAFE TO TRADE{% else %}❌ NOT SAFE{% endif %}{% if pre_trade_checks.warnings %} • {{ pre_trade_checks.warnings | length }} warning(s){% endif %}{% if pre_trade_checks.manual_check_required %} • ⚠️ MANUAL CHECK REQUIRED{% endif %}

{% endif %}
