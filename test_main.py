#!/usr/bin/env python3
"""
Unit tests for Trading Plan JSON to Markdown Converter
"""

import json
import sys
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open
from main import (
    format_price,
    format_list,
    format_dict_as_list,
    generate_header,
    generate_key_metrics,
    generate_agent_verdicts,
    generate_trade_details,
    generate_exit_strategy,
    generate_wild_cards_warnings,
    generate_execution_checklist,
    generate_pre_trading_checklist,
    convert_json_to_markdown,
    main,
)


class TestFormatPrice:
    """Test cases for format_price function"""

    def test_format_price_integer_under_100(self):
        assert format_price(50) == "$50.00"

    def test_format_price_float_under_100(self):
        assert format_price(99.99) == "$99.99"

    def test_format_price_integer_over_100(self):
        assert format_price(150) == "150.00"

    def test_format_price_float_over_100(self):
        assert format_price(1234.56) == "1,234.56"

    def test_format_price_large_number(self):
        assert format_price(1234567.89) == "1,234,567.89"

    def test_format_price_string(self):
        assert format_price("Unknown") == "Unknown"

    def test_format_price_zero(self):
        assert format_price(0) == "$0.00"

    def test_format_price_exactly_100(self):
        assert format_price(100) == "100.00"


class TestFormatList:
    """Test cases for format_list function"""

    def test_format_list_empty(self):
        assert format_list([]) == "- None"

    def test_format_list_single_item(self):
        assert format_list(["Item 1"]) == "- Item 1"

    def test_format_list_multiple_items(self):
        result = format_list(["Item 1", "Item 2", "Item 3"])
        assert result == "- Item 1\n- Item 2\n- Item 3"

    def test_format_list_custom_prefix(self):
        result = format_list(["Item 1", "Item 2"], prefix="*")
        assert result == "* Item 1\n* Item 2"

    def test_format_list_numbers(self):
        result = format_list([1, 2, 3])
        assert result == "- 1\n- 2\n- 3"


class TestFormatDictAsList:
    """Test cases for format_dict_as_list function"""

    def test_format_dict_as_list_empty(self):
        assert format_dict_as_list({}) == "- None"

    def test_format_dict_as_list_simple(self):
        data = {"key_one": "value1", "key_two": "value2"}
        result = format_dict_as_list(data)
        assert "- **Key One**: value1" in result
        assert "- **Key Two**: value2" in result

    def test_format_dict_as_list_with_list_value(self):
        data = {"items": [1, 2, 3]}
        result = format_dict_as_list(data)
        assert "- **Items**: 1, 2, 3" in result

    def test_format_dict_as_list_with_number_value(self):
        data = {"count": 42}
        result = format_dict_as_list(data)
        assert "- **Count**: 42" in result


class TestGenerateHeader:
    """Test cases for generate_header function"""

    def test_generate_header_complete_data(self):
        data = {
            "ticker": "AAPL",
            "asset_type": "Stock",
            "trade_style": "Swing",
            "trade_plan": {
                "verdict": {
                    "action": "BUY",
                    "confidence": "High"
                }
            }
        }
        result = generate_header(data)
        assert "# Trading Plan: AAPL" in result
        assert "## BUY" in result
        assert "**Confidence**: High" in result
        assert "**Asset Type**: Stock" in result
        assert "**Trade Style**: Swing" in result

    def test_generate_header_missing_data(self):
        data = {}
        result = generate_header(data)
        assert "# Trading Plan: UNKNOWN" in result
        assert "## NO ACTION" in result
        assert "**Confidence**: Unknown" in result


class TestGenerateKeyMetrics:
    """Test cases for generate_key_metrics function"""

    def test_generate_key_metrics_complete_data(self):
        data = {
            "account_size": 10000,
            "risk_percent": 2,
            "trade_plan": {
                "entry": {
                    "current_price": 150.50
                },
                "position": {
                    "max_risk": "$200.00"
                }
            }
        }
        result = generate_key_metrics(data)
        assert "## Key Metrics" in result
        assert "10,000.00" in result  # No $ for values >= 100
        assert "2%" in result
        assert "$200.00" in result
        assert "150.50" in result  # No $ for values >= 100

    def test_generate_key_metrics_missing_data(self):
        data = {}
        result = generate_key_metrics(data)
        assert "## Key Metrics" in result
        assert "Unknown" in result


class TestGenerateAgentVerdicts:
    """Test cases for generate_agent_verdicts function"""

    def test_generate_agent_verdicts_technical_agent(self):
        data = {
            "agent_verdicts": {
                "technical": {
                    "direction": "bullish",
                    "confidence": 85,
                    "entry_type": "breakout_momentum",
                    "mtf_alignment": "Strong",
                    "volatility": "Medium",
                    "reasoning": ["Strong uptrend", "Volume increasing"]
                },
                "macro": {},
                "wild_card": {}
            }
        }
        result = generate_agent_verdicts(data)
        assert "### Technical Agent" in result
        assert "**Direction**: BULLISH" in result
        assert "**Confidence**: 85%" in result
        assert "Breakout Momentum" in result
        assert "Strong uptrend" in result

    def test_generate_agent_verdicts_with_support_resistance(self):
        data = {
            "agent_verdicts": {
                "technical": {
                    "direction": "bullish",
                    "confidence": 80,
                    "entry_type": "pullback",
                    "support_levels": {
                        "minor": [100, 105],
                        "major": [90, 95],
                        "key_references": {"fib_618": 98.5}
                    },
                    "resistance_levels": {
                        "minor": [120, 125],
                        "major": [130, 135]
                    }
                },
                "macro": {},
                "wild_card": {}
            }
        }
        result = generate_agent_verdicts(data)
        assert "**Support Levels**:" in result
        assert "Minor: 100, 105" in result
        assert "Major: 90, 95" in result
        assert "FIB 618: 98.5" in result
        assert "**Resistance Levels**:" in result

    def test_generate_agent_verdicts_macro_agent(self):
        data = {
            "agent_verdicts": {
                "technical": {},
                "macro": {
                    "market_regime": "risk_on",
                    "confidence": 75,
                    "spy_direction": "up",
                    "qqq_direction": "up",
                    "cross_asset_alignment": "strong"
                },
                "wild_card": {}
            }
        }
        result = generate_agent_verdicts(data)
        assert "### Macro Agent" in result
        assert "Risk On" in result
        assert "75%" in result
        assert "UP" in result

    def test_generate_agent_verdicts_wild_card_agent(self):
        data = {
            "agent_verdicts": {
                "technical": {},
                "macro": {},
                "wild_card": {
                    "overall_risk_assessment": "medium",
                    "wild_cards_identified": [
                        {
                            "type": "earnings_release",
                            "description": "Earnings tomorrow",
                            "probability": "high",
                            "impact": "high",
                            "mitigation": "Reduce position size"
                        }
                    ]
                }
            }
        }
        result = generate_agent_verdicts(data)
        assert "### Wild Card Agent" in result
        assert "**Overall Risk Assessment**: MEDIUM" in result
        assert "Earnings Release" in result
        assert "Earnings tomorrow" in result


class TestGenerateTradeDetails:
    """Test cases for generate_trade_details function"""

    def test_generate_trade_details_complete(self):
        data = {
            "trade_plan": {
                "entry": {
                    "direction": "LONG",
                    "recommendation": "market_order",
                    "ideal_zone": {
                        "low": 100,
                        "mid": 105,
                        "high": 110,
                        "confidence": "High"
                    },
                    "wait_for": "Confirmation of support"
                },
                "position": {
                    "size_recommendation": "full",
                    "quantity": 10,
                    "unit_type": "shares",
                    "total_cost": "$1050.00",
                    "max_risk": "$200.00",
                    "rationale": "Strong setup"
                }
            }
        }
        result = generate_trade_details(data)
        assert "## Trade Details" in result
        assert "### Entry Zone" in result
        assert "**Direction**: LONG" in result
        assert "Market Order" in result
        assert "100.00" in result  # No $ for values >= 100
        assert "### Position Sizing" in result
        assert "10 shares" in result


class TestGenerateExitStrategy:
    """Test cases for generate_exit_strategy function"""

    def test_generate_exit_strategy_complete(self):
        data = {
            "trade_plan": {
                "exits": {
                    "stop_loss": {
                        "price_range": [95, 98],
                        "total_loss": "$200.00",
                        "rationale": "Below support"
                    },
                    "profit_targets": [
                        {
                            "target": 1,
                            "price_range": [120, 125],
                            "position_percent": 50,
                            "probability": "High"
                        }
                    ],
                    "time_stop": {
                        "date_or_duration": "7 days",
                        "rationale": "Earnings release"
                    }
                }
            }
        }
        result = generate_exit_strategy(data)
        assert "## Exit Strategy" in result
        assert "### Stop Loss" in result
        assert "$95.00 - $98.00" in result
        assert "### Profit Targets" in result
        assert "### Time Stop" in result


class TestGenerateWildCardsWarnings:
    """Test cases for generate_wild_cards_warnings function"""

    def test_generate_wild_cards_warnings_complete(self):
        data = {
            "trade_plan": {
                "wild_cards": {
                    "identified_risks": [
                        {
                            "risk": "Market crash",
                            "probability": "low",
                            "impact": "high",
                            "contingency": "Exit immediately"
                        }
                    ],
                    "manual_checks_required": [
                        "Check news before market open",
                        "Verify broker connection"
                    ],
                    "honest_uncertainty": "Market could go either way"
                }
            }
        }
        result = generate_wild_cards_warnings(data)
        assert "## Wild Cards & Warnings" in result
        assert "### Identified Risks" in result
        assert "Market crash" in result
        assert "### Manual Checks Required" in result
        assert "Check news before market open" in result


class TestGenerateExecutionChecklist:
    """Test cases for generate_execution_checklist function"""

    def test_generate_execution_checklist_with_steps(self):
        data = {
            "trade_plan": {
                "execution_plan": {
                    "step_1": "Check pre-market data",
                    "step_2": "Place limit order",
                    "step_3": "Monitor execution"
                }
            }
        }
        result = generate_execution_checklist(data)
        assert "## Execution Checklist" in result
        assert "1. Check pre-market data" in result
        assert "2. Place limit order" in result
        assert "3. Monitor execution" in result

    def test_generate_execution_checklist_no_steps(self):
        data = {
            "trade_plan": {
                "execution_plan": {}
            }
        }
        result = generate_execution_checklist(data)
        assert "No execution steps defined" in result


class TestGeneratePreTradingChecklist:
    """Test cases for generate_pre_trading_checklist function"""

    def test_generate_pre_trading_checklist_safe(self):
        data = {
            "pre_trade_checks": {
                "safe_to_trade": True,
                "warnings": ["Volatility elevated"],
                "critical_events": []
            }
        }
        result = generate_pre_trading_checklist(data)
        assert "## Pre-Trading Checklist" in result
        assert "✅ YES" in result
        assert "Volatility elevated" in result

    def test_generate_pre_trading_checklist_not_safe(self):
        data = {
            "pre_trade_checks": {
                "safe_to_trade": False,
                "warnings": [],
                "critical_events": ["FOMC meeting"],
                "manual_check_required": True
            }
        }
        result = generate_pre_trading_checklist(data)
        assert "❌ NO" in result
        assert "FOMC meeting" in result
        assert "MANUAL CHECK REQUIRED" in result


class TestConvertJsonToMarkdown:
    """Test cases for convert_json_to_markdown function"""

    def test_convert_json_to_markdown_no_trade(self):
        data = {
            "trade_plan": {
                "trade": False,
                "no_trade_reason": "Market conditions unfavorable"
            }
        }
        result = convert_json_to_markdown(data)
        assert "# No Trade Recommended" in result
        assert "Market conditions unfavorable" in result

    def test_convert_json_to_markdown_with_trade(self):
        data = {
            "ticker": "AAPL",
            "asset_type": "Stock",
            "trade_style": "Day",
            "account_size": 10000,
            "risk_percent": 1,
            "trade_plan": {
                "trade": True,
                "verdict": {
                    "action": "BUY",
                    "confidence": "High"
                },
                "entry": {
                    "current_price": 150
                },
                "position": {
                    "max_risk": "$100"
                },
                "exits": {},
                "wild_cards": {},
                "execution_plan": {}
            },
            "agent_verdicts": {
                "technical": {},
                "macro": {},
                "wild_card": {}
            },
            "pre_trade_checks": {
                "safe_to_trade": True
            }
        }
        result = convert_json_to_markdown(data)
        assert "# Trading Plan: AAPL" in result
        assert "## BUY" in result
        assert "## Key Metrics" in result
        assert "## Agent Verdicts" in result
        assert "## Trade Details" in result


class TestMain:
    """Test cases for main function"""

    def test_main_no_arguments(self, capsys):
        with patch.object(sys, 'argv', ['main.py']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
            captured = capsys.readouterr()
            assert "Usage:" in captured.out

    def test_main_file_not_found(self, capsys):
        with patch.object(sys, 'argv', ['main.py', 'nonexistent.json']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
            captured = capsys.readouterr()
            assert "File not found" in captured.out

    def test_main_invalid_json(self, capsys, tmp_path):
        # Create a temporary invalid JSON file
        invalid_json = tmp_path / "invalid.json"
        invalid_json.write_text("{ invalid json }")

        with patch.object(sys, 'argv', ['main.py', str(invalid_json)]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
            captured = capsys.readouterr()
            assert "Invalid JSON" in captured.out

    def test_main_success_auto_output(self, capsys, tmp_path):
        # Create a temporary valid JSON file
        input_json = tmp_path / "test.json"
        json_data = {
            "trade_plan": {
                "trade": False,
                "no_trade_reason": "Test reason"
            }
        }
        input_json.write_text(json.dumps(json_data))

        expected_output = tmp_path / "test.md"

        with patch.object(sys, 'argv', ['main.py', str(input_json)]):
            main()
            captured = capsys.readouterr()
            assert "Successfully converted" in captured.out
            assert expected_output.exists()

    def test_main_success_explicit_output(self, capsys, tmp_path):
        # Create a temporary valid JSON file
        input_json = tmp_path / "input.json"
        output_md = tmp_path / "output.md"
        json_data = {
            "trade_plan": {
                "trade": False,
                "no_trade_reason": "Test reason"
            }
        }
        input_json.write_text(json.dumps(json_data))

        with patch.object(sys, 'argv', ['main.py', str(input_json), str(output_md)]):
            main()
            captured = capsys.readouterr()
            assert "Successfully converted" in captured.out
            assert output_md.exists()

    def test_main_success_with_dash_o_flag(self, capsys, tmp_path):
        # Create a temporary valid JSON file
        input_json = tmp_path / "input.json"
        output_md = tmp_path / "custom_output.md"
        json_data = {
            "trade_plan": {
                "trade": False,
                "no_trade_reason": "Test reason"
            }
        }
        input_json.write_text(json.dumps(json_data))

        with patch.object(sys, 'argv', ['main.py', str(input_json), '-o', str(output_md)]):
            main()
            captured = capsys.readouterr()
            assert "Successfully converted" in captured.out
            assert output_md.exists()

    def test_main_write_error(self, capsys, tmp_path):
        # Create a temporary valid JSON file
        input_json = tmp_path / "input.json"
        json_data = {
            "trade_plan": {
                "trade": False,
                "no_trade_reason": "Test reason"
            }
        }
        input_json.write_text(json.dumps(json_data))

        # Try to write to an invalid path (directory that doesn't exist)
        invalid_output = "/nonexistent_directory/output.md"

        with patch.object(sys, 'argv', ['main.py', str(input_json), invalid_output]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
            captured = capsys.readouterr()
            assert "Could not write" in captured.out
