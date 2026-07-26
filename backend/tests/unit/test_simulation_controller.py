from datetime import datetime
from typing import List

import pytest

from app.energyplus.digital_twin import DigitalTwinManager
from app.energyplus.interfaces import SimulationAdapter
from app.energyplus.repository import SimulationRepository
from app.energyplus.simulation_controller import SimulationController
from app.energyplus.simulation_state import (
    BuildingState,
    ControlAction,
    SensorData,
    WeatherState,
)
from app.shared.enums import SimulationStatus


class MockAdapter(SimulationAdapter):
    def connect(self) -> None:
        pass

    def disconnect(self) -> None:
        pass

    def initialize(self) -> None:
        pass

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def pause(self) -> None:
        pass

    def resume(self) -> None:
        pass

    def step(self) -> None:
        pass

    def restart(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def get_state(self) -> BuildingState:
        return BuildingState(
            simulation_time=datetime.now(),
            weather=WeatherState(
                outside_temperature=22.0,
                humidity=40.0,
                wind_speed=1.0,
                solar_radiation=100.0,
            ),
            occupancy=0,
            hvac_status=False,
            simulation_status=SimulationStatus.RUNNING,
        )

    def get_sensor_data(self) -> List[SensorData]:
        return []

    def apply_control(self, action: ControlAction) -> None:
        pass


@pytest.fixture
def controller():
    adapter = MockAdapter()
    repo = SimulationRepository()
    twin = DigitalTwinManager(repo)
    return SimulationController(adapter, twin)


def test_start_simulation(controller):
    # This should call connect, initialize, start, and pull initial state
    controller.start_simulation()
    snapshot = controller.get_snapshot()
    assert snapshot is not None
    assert snapshot.building_state.simulation_status == SimulationStatus.RUNNING


def test_apply_control_action(controller):
    action = ControlAction(
        zone_id="zone_test",
        cooling_setpoint=25.0,
        reason="Testing",
        issued_at=datetime.now(),
    )
    controller.apply_control_action(action)

    controller.get_snapshot()
    # It might be None if process_sensor_update hasn't run to pull a state,
    # but the control action should be registered in the twin
    assert controller._twin.get_latest_control() is not None
    assert controller._twin.get_latest_control().zone_id == "zone_test"
