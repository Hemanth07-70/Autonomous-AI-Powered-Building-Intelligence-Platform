import os
import re

def fix_file(filepath, replacements):
    with open(filepath, 'r') as f:
        content = f.read()
    for old, new in replacements:
        content = content.replace(old, new)
    with open(filepath, 'w') as f:
        f.write(content)

fix_file('backend/app/main.py', [
    (
        '"description": "Endpoints related to AI inference, agents, and LLM integrations.",',
        '"description": (\n            "Endpoints related to AI inference, agents, "\n            "and LLM integrations."\n        ),'
    ),
    (
        '"description": "Endpoints managing the EnergyPlus Digital Twin and simulations.",',
        '"description": (\n            "Endpoints managing the EnergyPlus Digital Twin "\n            "and simulations."\n        ),'
    ),
    (
        'description="An autonomous AI platform that continuously monitors, reasons, and optimizes smart building energy consumption using EnergyPlus as a Digital Twin.",',
        'description=(\n        "An autonomous AI platform that continuously monitors, reasons, "\n        "and optimizes smart building energy consumption "\n        "using EnergyPlus as a Digital Twin."\n    ),'
    ),
    (
        '# Register Middlewares (Note: Last added runs first for response, but first added runs first for request)',
        '# Register Middlewares (Note: Last added runs first for response,\n    # but first added runs first for request)'
    )
])

fix_file('backend/app/monitoring/alerts.py', [
    (
        'logger.error("Failed to execute alert handler", error=str(e), exc_info=True)',
        'logger.error(\n                    "Failed to execute alert handler",\n                    error=str(e),\n                    exc_info=True\n                )'
    )
])

fix_file('backend/app/orchestrator/decision_engine.py', [
    (
        '    Core engine responsible for evaluating states and determining optimal control actions.',
        '    Core engine responsible for evaluating states and determining optimal\n    control actions.'
    )
])

fix_file('backend/app/orchestrator/planner.py', [
    (
        '    Module responsible for long-term strategic planning and goal-setting for the building\'s energy usage.',
        '    Module responsible for long-term strategic planning and goal-setting\n    for the building\'s energy usage.'
    )
])

fix_file('backend/app/scheduler/polling.py', [
    (
        'def __init__(self, callback: Callable[[], Awaitable[None]], interval_seconds: float):',
        'def __init__(\n        self, callback: Callable[[], Awaitable[None]], interval_seconds: float\n    ):'
    )
])

fix_file('backend/app/scheduler/simulation_loop.py', [
    (
        'def __init__(self, step_function: Callable[[], Awaitable[None]], interval_seconds: float):',
        'def __init__(\n        self, step_function: Callable[[], Awaitable[None]], interval_seconds: float\n    ):'
    ),
    (
        'logger.error("Error during simulation tick", error=str(e), exc_info=True)',
        'logger.error(\n                    "Error during simulation tick", error=str(e), exc_info=True\n                )'
    )
])

fix_file('backend/app/scheduler/task_scheduler.py', [
    (
        'logger.info("TaskScheduler shutting down", pending_tasks=len(self._background_tasks))',
        'logger.info(\n            "TaskScheduler shutting down", pending_tasks=len(self._background_tasks)\n        )'
    )
])

fix_file('backend/app/telemetry/collector.py', [
    (
        '    Central hub for aggregating telemetry data before dispatching it to external systems.',
        '    Central hub for aggregating telemetry data before dispatching it to\n    external systems.'
    )
])

fix_file('backend/app/telemetry/metrics.py', [
    (
        'def increment_counter(self, name: str, tags: Optional[Dict[str, str]] = None) -> None:',
        'def increment_counter(\n        self, name: str, tags: Optional[Dict[str, str]] = None\n    ) -> None:'
    ),
    (
        'def record_gauge(self, name: str, value: float, tags: Optional[Dict[str, str]] = None) -> None:',
        'def record_gauge(\n        self, name: str, value: float, tags: Optional[Dict[str, str]] = None\n    ) -> None:'
    )
])

fix_file('backend/app/telemetry/performance.py', [
    (
        'logger.debug("Operation completed", operation=operation_name, duration_s=duration)',
        'logger.debug(\n                "Operation completed",\n                operation=operation_name,\n                duration_s=duration\n            )'
    )
])

fix_file('backend/tests/unit/test_repository.py', [
    (
        'def test_repository_snapshot_and_history(mock_building_state, mock_sensor_data, mock_control_action):',
        'def test_repository_snapshot_and_history(\n    mock_building_state, mock_sensor_data, mock_control_action\n):'
    )
])

fix_file('backend/tests/unit/test_simulation_controller.py', [
    (
        'weather=WeatherState(outside_temperature=22.0, humidity=40.0, wind_speed=1.0, solar_radiation=100.0),',
        'weather=WeatherState(\n                outside_temperature=22.0,\n                humidity=40.0,\n                wind_speed=1.0,\n                solar_radiation=100.0\n            ),'
    ),
    (
        'snapshot = controller.get_snapshot()',
        'controller.get_snapshot()'
    )
])
