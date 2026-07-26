import threading
from typing import Dict, List, Optional

from app.energyplus.simulation_state import (
    BuildingState,
    ControlAction,
    SensorData,
    SimulationSnapshot,
)


class SimulationRepository:
    """
    In-memory, thread-safe repository storing the immediate state of the Digital Twin.
    Allows ultra-fast lookup and snapshot retrieval without database latency.
    """

    def __init__(self):
        self._lock = threading.RLock()

        self._latest_building_state: Optional[BuildingState] = None
        # Zone ID -> latest SensorData mapping
        self._latest_sensor_data: Dict[str, SensorData] = {}
        self._latest_control_action: Optional[ControlAction] = None

        self._history: List[SimulationSnapshot] = []

    def save_building_state(self, state: BuildingState) -> None:
        """Stores the latest macro building state."""
        with self._lock:
            self._latest_building_state = state

    def get_building_state(self) -> Optional[BuildingState]:
        """Retrieves the latest building state."""
        with self._lock:
            return self._latest_building_state

    def save_sensor_data(self, data: List[SensorData]) -> None:
        """Stores or updates the latest sensor data per zone."""
        with self._lock:
            for reading in data:
                self._latest_sensor_data[reading.zone_id] = reading

    def get_sensor_data(self) -> List[SensorData]:
        """Retrieves all latest sensor readings across zones."""
        with self._lock:
            return list(self._latest_sensor_data.values())

    def save_control_action(self, action: ControlAction) -> None:
        """Stores the most recently issued control action."""
        with self._lock:
            self._latest_control_action = action

    def get_control_action(self) -> Optional[ControlAction]:
        """Retrieves the most recent control action."""
        with self._lock:
            return self._latest_control_action

    def take_snapshot(self) -> Optional[SimulationSnapshot]:
        """Creates a point-in-time snapshot of the current state and appends
        to history."""
        with self._lock:
            if not self._latest_building_state:
                return None

            snapshot = SimulationSnapshot(
                building_state=self._latest_building_state,
                sensor_data=list(self._latest_sensor_data.values()),
                last_control=self._latest_control_action,
            )
            self._history.append(snapshot)
            return snapshot

    def get_history(self) -> List[SimulationSnapshot]:
        """Returns the full historical snapshots recorded."""
        with self._lock:
            return list(self._history)

    def clear_history(self) -> None:
        """Clears all historical snapshots and memory."""
        with self._lock:
            self._history.clear()
            self._latest_building_state = None
            self._latest_sensor_data.clear()
            self._latest_control_action = None
