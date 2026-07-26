from typing import List, Optional

import structlog

from app.energyplus.repository import SimulationRepository
from app.energyplus.simulation_state import (
    BuildingState,
    ControlAction,
    SensorData,
    SimulationSnapshot,
)

logger = structlog.get_logger("digital_twin")


class DigitalTwinManager:
    """
    Manager orchestrating the state of the Digital Twin.
    Provides dependency-injected thread-safe state mutations.
    """

    def __init__(self, repository: SimulationRepository):
        self._repository = repository
        logger.info("DigitalTwinManager initialized")

    def update_state(self, state: BuildingState) -> None:
        """Updates the macro building state."""
        logger.debug(
            "Updating building state", simulation_time=str(state.simulation_time)
        )
        self._repository.save_building_state(state)

    def update_sensor_data(self, data: List[SensorData]) -> None:
        """Updates sensor readings for all zones."""
        logger.debug("Updating sensor data", sensor_count=len(data))
        self._repository.save_sensor_data(data)

    def update_control(self, action: ControlAction) -> None:
        """Records a new control action applied to the building."""
        logger.info(
            "Updating control action", zone_id=action.zone_id, reason=action.reason
        )
        self._repository.save_control_action(action)

    def snapshot(self) -> Optional[SimulationSnapshot]:
        """Triggers a state snapshot in the repository."""
        logger.debug("Taking simulation snapshot")
        return self._repository.take_snapshot()

    def reset(self) -> None:
        """Resets the Digital Twin to a clean state."""
        logger.info("Resetting digital twin state")
        self._repository.clear_history()

    def get_latest_state(self) -> Optional[BuildingState]:
        """Returns the most recent macro building state."""
        return self._repository.get_building_state()

    def get_latest_sensor_data(self) -> List[SensorData]:
        """Returns all current sensor readings."""
        return self._repository.get_sensor_data()

    def get_latest_control(self) -> Optional[ControlAction]:
        """Returns the most recently recorded control action."""
        return self._repository.get_control_action()
