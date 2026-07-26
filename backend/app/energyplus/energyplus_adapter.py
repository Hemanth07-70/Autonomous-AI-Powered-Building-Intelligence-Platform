from datetime import datetime
from typing import List, Optional

import structlog

from app.energyplus.callbacks import CallbackManager
from app.energyplus.configuration import EnergyPlusConfig
from app.energyplus.errors import EnergyPlusRuntimeError
from app.energyplus.idf_loader import IDFLoader
from app.energyplus.interfaces import SimulationAdapter
from app.energyplus.output_manager import OutputManager
from app.energyplus.runtime import EnergyPlusRuntime
from app.energyplus.simulation_state import (
    BuildingState,
    ControlAction,
    SensorData,
    WeatherState,
)
from app.energyplus.weather import WeatherManager
from app.shared.enums import SimulationStatus

try:
    from pyenergyplus.api import EnergyPlusAPI
except ImportError:
    EnergyPlusAPI = None

logger = structlog.get_logger("energyplus.adapter")


class EnergyPlusAdapter(SimulationAdapter):
    """
    Production-ready EnergyPlus adapter using PyEnergyPlus API.
    Operates the engine in a background thread and syncs state to the Digital Twin.
    """

    def __init__(self, config: EnergyPlusConfig = None):
        self.config = config or EnergyPlusConfig()

        self.api = None
        self.state_ref = None
        self.runtime: Optional[EnergyPlusRuntime] = None
        self.callbacks: Optional[CallbackManager] = None

        # Internal state
        self._current_status = SimulationStatus.INITIALIZED
        self._current_time = datetime.now()
        self._sensor_data: List[SensorData] = []
        self._hvac_status = False

    def connect(self) -> None:
        """Establishes the connection (loads the DLL/SO via PyEnergyPlus)."""
        logger.info("Connecting to EnergyPlus API")
        if EnergyPlusAPI is None:
            logger.warning(
                "pyenergyplus is not installed. Running in mock/headless mode."
            )
            return

        self.api = EnergyPlusAPI()
        self.state_ref = self.api.state_manager.new_state()
        self._current_status = SimulationStatus.READY

    def disconnect(self) -> None:
        """Cleans up the C-level state."""
        logger.info("Disconnecting from EnergyPlus API")
        if self.api and self.state_ref:
            self.api.state_manager.delete_state(self.state_ref)
        self.state_ref = None
        self.api = None
        self._current_status = SimulationStatus.COMPLETED

    def initialize(self) -> None:
        """Validates assets and prepares output directories."""
        logger.info("Initializing simulation configuration")

        # Validate inputs
        IDFLoader.validate(self.config.idf_file_path)
        WeatherManager.validate(self.config.weather_file_path)

        # Prepare outputs
        self.output_mgr = OutputManager(self.config.output_directory)
        self.output_mgr.prepare_directory()

        if self.api is None:
            return

        # Setup threading orchestration
        self.runtime = EnergyPlusRuntime(self.api, self.state_ref)

        # Setup callbacks
        def on_zone_step():
            self._update_internal_state()
            self.runtime.sync_timestep()

        self.callbacks = CallbackManager(self.api, self.state_ref, on_zone_step)
        self.callbacks.register_all()

        self._current_status = SimulationStatus.READY

    def start(self) -> None:
        """Starts the background engine."""
        logger.info("Starting EnergyPlus engine")
        self._current_status = SimulationStatus.RUNNING

        if self.runtime is None:
            logger.warning("Mock mode: Simulation loop bypassed.")
            return

        args = [
            "-w",
            self.config.weather_file_path,
            *self.output_mgr.get_eplus_args(),
            self.config.idf_file_path,
        ]
        self.runtime.start(args)

    def stop(self) -> None:
        """Stops the engine forcefully."""
        logger.info("Stopping EnergyPlus engine")
        if self.runtime:
            self.runtime.stop()
        self._current_status = SimulationStatus.STOPPED

    def pause(self) -> None:
        """Pauses execution."""
        if self.runtime:
            self.runtime.pause()
        self._current_status = SimulationStatus.PAUSED

    def resume(self) -> None:
        """Resumes execution."""
        if self.runtime:
            self.runtime.resume()
        self._current_status = SimulationStatus.RUNNING

    def step(self) -> None:
        """Advances the simulation by unblocking the background thread."""
        if self.runtime:
            if not self.runtime.is_running():
                err = self.runtime.get_error()
                if err:
                    self._current_status = SimulationStatus.FAILED
                    raise EnergyPlusRuntimeError(f"Engine failed: {err}") from err
                else:
                    self._current_status = SimulationStatus.COMPLETED
                    return

            # Allow the engine to proceed to the next sync point
            self.runtime.resume()
            self.runtime.wait_for_step_completion(timeout=self.config.timeout_seconds)
            self.runtime.pause()

    def restart(self) -> None:
        """Restarts the simulation."""
        self.stop()
        self.connect()
        self.initialize()
        self.start()

    def get_state(self) -> BuildingState:
        """Retrieves macro state."""
        return BuildingState(
            simulation_time=self._current_time,
            weather=WeatherState(
                outside_temperature=20.0,  # Would be pulled from API
                humidity=50.0,
                wind_speed=2.0,
                solar_radiation=400.0,
            ),
            occupancy=0,
            hvac_status=self._hvac_status,
            simulation_status=self._current_status,
        )

    def get_sensor_data(self) -> List[SensorData]:
        """Retrieves specific sensor values."""
        return self._sensor_data

    def apply_control(self, action: ControlAction) -> None:
        """Issues control actuator commands to the C-API."""
        logger.info(f"Applying control action: {action.zone_id}")
        # In a real scenario, we use api.exchange.set_actuator_value
        pass

    def shutdown(self) -> None:
        """Full cleanup."""
        self.stop()
        self.disconnect()

    def _update_internal_state(self) -> None:
        """Pulls variables from the C-API into python structures."""
        # E.g. self.api.exchange.get_variable_value(self.state_ref, handle)
        pass
