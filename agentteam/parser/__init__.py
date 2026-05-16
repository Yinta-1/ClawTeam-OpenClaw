"""Output parsing engine for ClawTeam multi-agent teams.

Parses AI provider outputs, detects activity events, estimates token usage,
and supports multiple provider formats (Claude Code, Codex, Gemini, etc.).

Inspired by SpectrAI's OutputParser.ts.
"""

from agentteam.parser.confirmation_detector import (
    ConfirmationDetector,
    ProviderConfirmationConfig,
    detect_confirmation,
    get_default_detector,
)
from agentteam.parser.integration import (
    ClawTeamIntegration,
    get_integration,
    parse_and_notify,
    remove_integration,
)
from agentteam.parser.output_parser import OutputParser, get_parser, parse_output
from agentteam.parser.rules import PARSER_RULES
from agentteam.parser.types import (
    ActivityEvent,
    ActivityEventType,
    ConfirmationDetection,
    ParserRule,
    ParserState,
    UsageSummary,
)
from agentteam.parser.usage_estimator import UsageEstimator

__all__ = [
    # Core parser
    "OutputParser",
    "get_parser",
    "parse_output",
    # Types
    "ActivityEvent",
    "ActivityEventType",
    "ParserState",
    "ParserRule",
    "ConfirmationDetection",
    "UsageSummary",
    # Rules
    "PARSER_RULES",
    # Confirmation detector
    "ConfirmationDetector",
    "ProviderConfirmationConfig",
    "detect_confirmation",
    "get_default_detector",
    # Usage estimator
    "UsageEstimator",
    # Integration
    "ClawTeamIntegration",
    "get_integration",
    "parse_and_notify",
    "remove_integration",
]
