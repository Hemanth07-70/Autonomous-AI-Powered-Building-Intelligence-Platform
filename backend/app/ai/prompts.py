from app.shared.enums import GoalType

SYSTEM_PROMPT = """
You convert natural language building requests into deterministic JSON.
Return only JSON with keys: goal_type, building_id, priority, constraints, parameters.
Do not include markdown, prose, comments, or extra keys.
The goal_type must be one of:
ENERGY_REDUCTION, PEAK_LOAD, THERMAL_COMFORT, HVAC, LIGHTING, OCCUPANCY,
CARBON, WATER, DIAGNOSTICS.
Priority must be an integer from 1 to 10, where 1 is highest urgency.
If a building is not named, use the provided default building_id.
"""

PROMPT_TEMPLATES = {
    GoalType.ENERGY_REDUCTION: """
Interpret the user request as an energy reduction planning goal.
Extract targets such as percent reduction into constraints.target_reduction.
""",
    GoalType.PEAK_LOAD: """
Interpret the user request as a peak load reduction planning goal.
Extract peak demand or time window details into constraints.
""",
    GoalType.THERMAL_COMFORT: """
Interpret the user request as a thermal comfort planning goal.
Extract temperature, PMV, humidity, or comfort band details into constraints.
""",
    GoalType.HVAC: """
Interpret the user request as an HVAC optimization planning goal.
Extract setpoint, ventilation, schedule, or equipment details into constraints.
""",
    GoalType.LIGHTING: """
Interpret the user request as a lighting optimization planning goal.
Extract daylighting, schedule, occupancy, or reduction details into constraints.
""",
    GoalType.OCCUPANCY: """
Interpret the user request as an occupancy analysis planning goal.
Extract zones, schedules, density, or utilization details into constraints.
""",
    GoalType.CARBON: """
Interpret the user request as a carbon reduction planning goal.
Extract carbon intensity, emissions target, or reporting horizon into constraints.
""",
    GoalType.WATER: """
Interpret the user request as a water optimization planning goal.
Extract water reduction, fixture, irrigation, or usage details into constraints.
""",
    GoalType.DIAGNOSTICS: """
Interpret the user request as an equipment diagnostics planning goal.
Extract equipment names, symptoms, zones, or failure signals into constraints.
""",
}


def build_prompt(message: str, default_building_id: str) -> str:
    templates = "\n".join(template.strip() for template in PROMPT_TEMPLATES.values())
    return (
        f"{SYSTEM_PROMPT.strip()}\n\n"
        f"Default building_id: {default_building_id}\n\n"
        f"Domain guidance:\n{templates}\n\n"
        f"User request:\n{message}"
    )
