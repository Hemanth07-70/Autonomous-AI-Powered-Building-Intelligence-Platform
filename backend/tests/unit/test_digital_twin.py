from datetime import datetime

import pytest

from app.energyplus.digital_twin import DigitalTwinManager
from app.energyplus.repository import SimulationRepository
from app.energyplus.simulation_state import (
    BuildingState,
    WeatherState,
)
from app.shared.enums import SimulationStatus


@pytest.fixture
def twin_manager():
    repo = SimulationRepository()
    return DigitalTwinManager(repo)


def test_twin_manager_update_state(twin_manager):
    state = BuildingState(
        simulation_time=datetime.now(),
        weather=WeatherState(
            outside_temperature=20.0,
            humidity=50.0,
            wind_speed=2.0,
            solar_radiation=400.0,
        ),
        occupancy=50,
        hvac_status=False,
        simulation_status=SimulationStatus.INITIALIZED,
    )
    twin_manager.update_state(state)
    latest = twin_manager.get_latest_state()
    assert latest is not None
    assert latest.occupancy == 50


def test_twin_manager_snapshot_and_reset(twin_manager):
    state = BuildingState(
        simulation_time=datetime.now(),
        weather=WeatherState(
            outside_temperature=20.0,
            humidity=50.0,
            wind_speed=2.0,
            solar_radiation=400.0,
        ),
        occupancy=50,
        hvac_status=False,
        simulation_status=SimulationStatus.INITIALIZED,
    )
    twin_manager.update_state(state)
    snapshot = twin_manager.snapshot()
    assert snapshot is not None
    assert snapshot.building_state.occupancy == 50

    twin_manager.reset()
    assert twin_manager.get_latest_state() is None
