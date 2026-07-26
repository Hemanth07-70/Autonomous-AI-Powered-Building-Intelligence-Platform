import pytest

from app.ai.exceptions import InvalidAIResponse, UnsupportedGoalError
from app.ai.parser import parse_decision_goal
from app.shared.enums import GoalType


def test_parse_valid_decision_goal_json():
    goal = parse_decision_goal(
        """
        {
            "goal_type": "ENERGY_REDUCTION",
            "building_id": "building-a",
            "priority": 1,
            "constraints": {"target_reduction": 15},
            "parameters": {}
        }
        """
    )

    assert goal.goal_type == GoalType.ENERGY_REDUCTION
    assert goal.building_id == "building-a"
    assert goal.priority == 1
    assert goal.constraints["target_reduction"] == 15


def test_parse_extracts_json_from_wrapped_response():
    goal = parse_decision_goal(
        'Here is the JSON: {"goal_type":"HVAC","building_id":"b1","priority":3,'
        '"constraints":{},"parameters":{}}'
    )

    assert goal.goal_type == GoalType.HVAC


def test_parse_rejects_malformed_json():
    with pytest.raises(InvalidAIResponse):
        parse_decision_goal("not-json")


def test_parse_rejects_unsupported_goal():
    with pytest.raises(UnsupportedGoalError):
        parse_decision_goal(
            '{"goal_type":"UNSUPPORTED","building_id":"b1","priority":3,'
            '"constraints":{},"parameters":{}}'
        )


def test_parse_rejects_invalid_schema():
    with pytest.raises(InvalidAIResponse):
        parse_decision_goal(
            '{"goal_type":"HVAC","building_id":"","priority":99,'
            '"constraints":{},"parameters":{}}'
        )
