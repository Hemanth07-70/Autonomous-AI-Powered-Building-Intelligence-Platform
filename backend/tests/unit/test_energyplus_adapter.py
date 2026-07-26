"""
Unit tests for the EnergyPlus Adapter, Runtime, Callbacks, and supporting modules.
All tests mock the PyEnergyPlus API — no EnergyPlus installation required.
"""
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from app.energyplus.callbacks import CallbackManager
from app.energyplus.configuration import EnergyPlusConfig
from app.energyplus.energyplus_adapter import EnergyPlusAdapter
from app.energyplus.errors import (
    CallbackError,
    EnergyPlusRuntimeError,
    MissingIDFError,
    MissingWeatherError,
)
from app.energyplus.idf_loader import IDFLoader
from app.energyplus.output_manager import OutputManager
from app.energyplus.runtime import EnergyPlusRuntime
from app.energyplus.simulation_state import (
    BuildingState,
    ControlAction,
)
from app.energyplus.weather import WeatherManager
from app.shared.enums import SimulationStatus

# ──────────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────────


@pytest.fixture
def tmp_idf(tmp_path: Path) -> Path:
    """Creates a temporary IDF file."""
    idf = tmp_path / "test_building.idf"
    idf.write_text("!- Minimal IDF\nVersion,23.2;\n")
    return idf


@pytest.fixture
def tmp_epw(tmp_path: Path) -> Path:
    """Creates a temporary EPW file."""
    epw = tmp_path / "test_weather.epw"
    epw.write_text("LOCATION,Test City\n")
    return epw


@pytest.fixture
def tmp_output(tmp_path: Path) -> Path:
    """Creates a temporary output directory path."""
    out = tmp_path / "eplus_output"
    return out


@pytest.fixture
def config(tmp_idf: Path, tmp_epw: Path, tmp_output: Path):
    """Creates an EnergyPlusConfig pointing to temp files."""
    return EnergyPlusConfig(
        energyplus_path="/usr/local/EnergyPlus-23-2-0",
        idf_file_path=str(tmp_idf),
        weather_file_path=str(tmp_epw),
        output_directory=str(tmp_output),
        timeout_seconds=10,
    )


@pytest.fixture
def mock_api():
    """Creates a fully mocked PyEnergyPlus API."""
    api = MagicMock()
    api.state_manager.new_state.return_value = MagicMock()
    api.runtime.run_energyplus.return_value = 0
    api.runtime.callback_end_zone_timestep_after_zone_reporting = MagicMock()
    return api


# ──────────────────────────────────────────────
# IDFLoader Tests
# ──────────────────────────────────────────────


class TestIDFLoader:
    def test_validate_existing_file(self, tmp_idf: Path):
        result = IDFLoader.validate(str(tmp_idf))
        assert result == tmp_idf

    def test_validate_missing_file_raises(self):
        with pytest.raises(MissingIDFError):
            IDFLoader.validate("/nonexistent/path/building.idf")

    def test_validate_directory_raises(self, tmp_path: Path):
        with pytest.raises(MissingIDFError):
            IDFLoader.validate(str(tmp_path))


# ──────────────────────────────────────────────
# WeatherManager Tests
# ──────────────────────────────────────────────


class TestWeatherManager:
    def test_validate_existing_file(self, tmp_epw: Path):
        result = WeatherManager.validate(str(tmp_epw))
        assert result == tmp_epw

    def test_validate_missing_file_raises(self):
        with pytest.raises(MissingWeatherError):
            WeatherManager.validate("/nonexistent/path/weather.epw")

    def test_validate_directory_raises(self, tmp_path: Path):
        with pytest.raises(MissingWeatherError):
            WeatherManager.validate(str(tmp_path))


# ──────────────────────────────────────────────
# OutputManager Tests
# ──────────────────────────────────────────────


class TestOutputManager:
    def test_prepare_directory_creates_dir(self, tmp_output: Path):
        mgr = OutputManager(str(tmp_output))
        mgr.prepare_directory()
        assert tmp_output.exists()
        assert tmp_output.is_dir()

    def test_get_eplus_args(self, tmp_output: Path):
        mgr = OutputManager(str(tmp_output))
        args = mgr.get_eplus_args()
        assert args[0] == "-d"
        assert str(tmp_output.absolute()) in args[1]


# ──────────────────────────────────────────────
# EnergyPlusConfig Tests
# ──────────────────────────────────────────────


class TestEnergyPlusConfig:
    def test_defaults(self):
        cfg = EnergyPlusConfig()
        assert cfg.timeout_seconds == 3600
        assert cfg.log_level == "INFO"

    def test_custom_values(self, tmp_idf, tmp_epw, tmp_output):
        cfg = EnergyPlusConfig(
            idf_file_path=str(tmp_idf),
            weather_file_path=str(tmp_epw),
            output_directory=str(tmp_output),
            timeout_seconds=120,
        )
        assert cfg.timeout_seconds == 120
        assert cfg.idf_file_path == str(tmp_idf)

    def test_validate_paths_creates_output_dir(self, tmp_idf, tmp_epw, tmp_output):
        cfg = EnergyPlusConfig(
            idf_file_path=str(tmp_idf),
            weather_file_path=str(tmp_epw),
            output_directory=str(tmp_output),
        )
        cfg.validate_paths()
        assert tmp_output.exists()


# ──────────────────────────────────────────────
# CallbackManager Tests
# ──────────────────────────────────────────────


class TestCallbackManager:
    def test_register_all_calls_api(self, mock_api):
        state_ref = mock_api.state_manager.new_state()
        handler = MagicMock()
        mgr = CallbackManager(mock_api, state_ref, handler)
        mgr.register_all()

        mock_api.runtime.callback_end_zone_timestep_after_zone_reporting.assert_called_once()
        assert mgr._is_registered is True

    def test_register_all_idempotent(self, mock_api):
        state_ref = mock_api.state_manager.new_state()
        mgr = CallbackManager(mock_api, state_ref, MagicMock())
        mgr.register_all()
        mgr.register_all()

        assert (
            mock_api.runtime.callback_end_zone_timestep_after_zone_reporting.call_count
            == 1
        )

    def test_register_all_raises_callback_error(self, mock_api):
        mock_api.runtime.callback_end_zone_timestep_after_zone_reporting.side_effect = (
            RuntimeError("C-API failure")
        )
        state_ref = mock_api.state_manager.new_state()
        mgr = CallbackManager(mock_api, state_ref, MagicMock())

        with pytest.raises(CallbackError):
            mgr.register_all()

    def test_handle_end_zone_timestep_calls_handler(self, mock_api):
        state_ref = mock_api.state_manager.new_state()
        handler = MagicMock()
        mgr = CallbackManager(mock_api, state_ref, handler)

        mgr._handle_end_zone_timestep(state_ref)
        handler.assert_called_once()

    def test_handle_end_zone_timestep_swallows_error(self, mock_api):
        state_ref = mock_api.state_manager.new_state()
        handler = MagicMock(side_effect=ValueError("boom"))
        mgr = CallbackManager(mock_api, state_ref, handler)

        # Should not raise
        mgr._handle_end_zone_timestep(state_ref)


# ──────────────────────────────────────────────
# EnergyPlusRuntime Tests
# ──────────────────────────────────────────────


class TestEnergyPlusRuntime:
    def test_start_launches_thread(self, mock_api):
        state_ref = mock_api.state_manager.new_state()
        rt = EnergyPlusRuntime(mock_api, state_ref)

        # The engine exits immediately with 0
        rt.start(["-w", "test.epw", "test.idf"])

        # Wait for the thread to finish
        rt._thread.join(timeout=2)

        assert rt.is_running() is False
        assert rt.get_error() is None

    def test_start_captures_nonzero_exit(self, mock_api):
        mock_api.runtime.run_energyplus.return_value = 1
        state_ref = mock_api.state_manager.new_state()
        rt = EnergyPlusRuntime(mock_api, state_ref)

        rt.start(["-w", "test.epw", "test.idf"])
        rt._thread.join(timeout=2)

        assert rt.is_running() is False
        assert rt.get_error() is not None
        assert isinstance(rt.get_error(), EnergyPlusRuntimeError)

    def test_pause_and_resume(self, mock_api):
        state_ref = mock_api.state_manager.new_state()
        rt = EnergyPlusRuntime(mock_api, state_ref)

        rt._is_running = True
        rt.pause()
        assert rt._is_paused is True

        rt.resume()
        assert rt._is_paused is False

    def test_stop_sets_flags(self, mock_api):
        state_ref = mock_api.state_manager.new_state()
        rt = EnergyPlusRuntime(mock_api, state_ref)

        rt._is_running = True
        rt.stop()
        assert rt._is_running is False
        assert rt._is_paused is False

    def test_sync_timestep_signals_event(self, mock_api):
        state_ref = mock_api.state_manager.new_state()
        rt = EnergyPlusRuntime(mock_api, state_ref)
        rt._is_running = True

        rt.sync_timestep()
        assert rt._step_completed_event.is_set()

    def test_wait_for_step_completion(self, mock_api):
        state_ref = mock_api.state_manager.new_state()
        rt = EnergyPlusRuntime(mock_api, state_ref)

        rt._step_completed_event.set()
        result = rt.wait_for_step_completion(timeout=1.0)
        assert result is True
        assert not rt._step_completed_event.is_set()


# ──────────────────────────────────────────────
# EnergyPlusAdapter Tests
# ──────────────────────────────────────────────


class TestEnergyPlusAdapter:
    def test_initial_status(self, config):
        adapter = EnergyPlusAdapter(config)
        assert adapter._current_status == SimulationStatus.INITIALIZED

    def test_connect_without_pyenergyplus(self, config):
        adapter = EnergyPlusAdapter(config)
        adapter.connect()
        # Without pyenergyplus installed, stays INITIALIZED
        assert adapter.api is None

    @patch(
        "app.energyplus.energyplus_adapter.EnergyPlusAPI",
        new_callable=lambda: MagicMock,
    )
    def test_connect_with_mock_api(self, mock_cls, config):
        mock_instance = MagicMock()
        mock_cls.return_value = mock_instance
        mock_instance.state_manager.new_state.return_value = MagicMock()

        adapter = EnergyPlusAdapter(config)
        adapter.connect()

        assert adapter.api is not None
        assert adapter._current_status == SimulationStatus.READY

    def test_initialize_validates_files(self, config):
        adapter = EnergyPlusAdapter(config)
        adapter.initialize()
        assert adapter.output_mgr is not None

    def test_initialize_missing_idf_raises(self, tmp_epw, tmp_output):
        cfg = EnergyPlusConfig(
            idf_file_path="/nonexistent/building.idf",
            weather_file_path=str(tmp_epw),
            output_directory=str(tmp_output),
        )
        adapter = EnergyPlusAdapter(cfg)
        with pytest.raises(MissingIDFError):
            adapter.initialize()

    def test_initialize_missing_epw_raises(self, tmp_idf, tmp_output):
        cfg = EnergyPlusConfig(
            idf_file_path=str(tmp_idf),
            weather_file_path="/nonexistent/weather.epw",
            output_directory=str(tmp_output),
        )
        adapter = EnergyPlusAdapter(cfg)
        with pytest.raises(MissingWeatherError):
            adapter.initialize()

    def test_start_mock_mode(self, config):
        adapter = EnergyPlusAdapter(config)
        adapter.connect()
        adapter.initialize()
        adapter.start()
        assert adapter._current_status == SimulationStatus.RUNNING

    def test_stop(self, config):
        adapter = EnergyPlusAdapter(config)
        adapter.stop()
        assert adapter._current_status == SimulationStatus.STOPPED

    def test_pause(self, config):
        adapter = EnergyPlusAdapter(config)
        adapter.pause()
        assert adapter._current_status == SimulationStatus.PAUSED

    def test_resume(self, config):
        adapter = EnergyPlusAdapter(config)
        adapter.resume()
        assert adapter._current_status == SimulationStatus.RUNNING

    def test_get_state_returns_building_state(self, config):
        adapter = EnergyPlusAdapter(config)
        state = adapter.get_state()
        assert isinstance(state, BuildingState)
        assert state.simulation_status == SimulationStatus.INITIALIZED

    def test_get_sensor_data_returns_list(self, config):
        adapter = EnergyPlusAdapter(config)
        data = adapter.get_sensor_data()
        assert isinstance(data, list)

    def test_apply_control(self, config):
        adapter = EnergyPlusAdapter(config)
        action = ControlAction(
            zone_id="zone_1",
            cooling_setpoint=24.0,
            reason="Test action",
            issued_at=datetime.now(),
        )
        adapter.apply_control(action)

    def test_shutdown(self, config):
        adapter = EnergyPlusAdapter(config)
        adapter.shutdown()
        assert adapter._current_status == SimulationStatus.COMPLETED

    def test_implements_simulation_adapter(self, config):
        """Verify that EnergyPlusAdapter is a valid SimulationAdapter."""
        from app.energyplus.interfaces import SimulationAdapter

        adapter = EnergyPlusAdapter(config)
        assert isinstance(adapter, SimulationAdapter)

    def test_full_lifecycle_mock_mode(self, config):
        """End-to-end lifecycle in headless/mock mode."""
        adapter = EnergyPlusAdapter(config)

        adapter.connect()
        adapter.initialize()
        adapter.start()
        assert adapter._current_status == SimulationStatus.RUNNING

        state = adapter.get_state()
        assert isinstance(state, BuildingState)

        adapter.pause()
        assert adapter._current_status == SimulationStatus.PAUSED

        adapter.resume()
        assert adapter._current_status == SimulationStatus.RUNNING

        adapter.stop()
        assert adapter._current_status == SimulationStatus.STOPPED

        adapter.shutdown()
        assert adapter._current_status == SimulationStatus.COMPLETED
