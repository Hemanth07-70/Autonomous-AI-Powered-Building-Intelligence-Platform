from datetime import datetime

import pytest

from app.energyplus.repository import SimulationRepository
from app.energyplus.simulation_state import (
    BuildingState,
    ControlAction,
    SensorData,
    WeatherState,
)
from app.shared.enums import SimulationStatus


@pytest.fixture
def mock_building_state():
    return BuildingState(
        simulation_time=datetime.now(),
        weather=WeatherState(
            outside_temperature=25.0,
            humidity=50.0,
            wind_speed=2.5,
            solar_radiation=800.0,
        ),
        occupancy=100,
        hvac_status=True,
        simulation_status=SimulationStatus.RUNNING,
    )


@pytest.fixture
def mock_sensor_data():
    return [
        SensorData(
            zone_id="zone_1",
            zone_name="Office 1",
            temperature=23.5,
            humidity=45.0,
            energy_consumption=1200.0,
            timestamp=datetime.now(),
        )
    ]


@pytest.fixture
def mock_control_action():
    return ControlAction(
        zone_id="zone_1",
        cooling_setpoint=24.0,
        reason="Test action",
        issued_at=datetime.now(),
    )


def test_repository_save_and_get_state(mock_building_state):
    repo = SimulationRepository()
    repo.save_building_state(mock_building_state)
    state = repo.get_building_state()
    assert state is not None
    assert state.occupancy == 100


def test_repository_save_and_get_sensor_data(mock_sensor_data):
    repo = SimulationRepository()
    repo.save_sensor_data(mock_sensor_data)
    data = repo.get_sensor_data()
    assert len(data) == 1
    assert data[0].zone_id == "zone_1"


def test_repository_snapshot_and_history(
    mock_building_state, mock_sensor_data, mock_control_action
):
    repo = SimulationRepository()
    repo.save_building_state(mock_building_state)
    repo.save_sensor_data(mock_sensor_data)
    repo.save_control_action(mock_control_action)

    snapshot = repo.take_snapshot()
    assert snapshot is not None
    assert snapshot.building_state.occupancy == 100
    assert len(snapshot.sensor_data) == 1
    assert snapshot.last_control.zone_id == "zone_1"

    history = repo.get_history()
    assert len(history) == 1

    repo.clear_history()
    assert len(repo.get_history()) == 0
