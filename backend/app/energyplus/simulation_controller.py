from typing import Optional

import structlog

from app.energyplus.digital_twin import DigitalTwinManager
from app.energyplus.interfaces import SimulationAdapter
from app.energyplus.simulation_state import ControlAction, SimulationSnapshot
from app.shared.exceptions import SimulationException

logger = structlog.get_logger("simulation_controller")


class SimulationController:
    """
    High-level orchestrator for the simulation engine.
    Bridges the gap between the concrete simulator adapter and the digital twin state.
    """

    def __init__(self, adapter: SimulationAdapter, twin_manager: DigitalTwinManager):
        self._adapter = adapter
        self._twin = twin_manager
        logger.info("SimulationController initialized")

    def start_simulation(self) -> None:
        """Connects, initializes, and starts the simulation engine."""
        logger.info("Starting simulation sequence")
        try:
            self._adapter.connect()
            self._adapter.initialize()
            self._adapter.start()

            # Initial state pull
            self.process_sensor_update()

            logger.info("Simulation started successfully")
        except Exception as e:
            logger.error("Failed to start simulation", error=str(e), exc_info=True)
            raise SimulationException(f"Could not start simulation: {e}") from e

    def stop_simulation(self) -> None:
        """Stops the engine and cleanly shuts down the connection."""
        logger.info("Stopping simulation")
        try:
            self._adapter.stop()
            self._adapter.disconnect()
            logger.info("Simulation stopped successfully")
        except Exception as e:
            logger.error(
                "Failed to stop simulation cleanly", error=str(e), exc_info=True
            )
            raise SimulationException(f"Could not stop simulation cleanly: {e}") from e

    def pause_simulation(self) -> None:
        """Pauses the active simulation."""
        logger.info("Pausing simulation")
        try:
            self._adapter.pause()
            logger.info("Simulation paused successfully")
        except Exception as e:
            logger.error("Failed to pause simulation", error=str(e), exc_info=True)
            raise SimulationException(f"Could not pause simulation: {e}") from e

    def resume_simulation(self) -> None:
        """Resumes a paused simulation."""
        logger.info("Resuming simulation")
        try:
            self._adapter.resume()
            logger.info("Simulation resumed successfully")
        except Exception as e:
            logger.error("Failed to resume simulation", error=str(e), exc_info=True)
            raise SimulationException(f"Could not resume simulation: {e}") from e

    def restart_simulation(self) -> None:
        """Restarts the simulation and resets the digital twin."""
        logger.info("Restarting simulation")
        try:
            self._adapter.restart()
            self._twin.reset()

            # Initial state pull post-restart
            self.process_sensor_update()

            logger.info("Simulation restarted successfully")
        except Exception as e:
            logger.error("Failed to restart simulation", error=str(e), exc_info=True)
            raise SimulationException(f"Could not restart simulation: {e}") from e

    def process_sensor_update(self) -> None:
        """Pulls the latest state from the engine and updates the Digital Twin."""
        logger.debug("Processing simulation sensor update")
        try:
            state = self._adapter.get_state()
            sensors = self._adapter.get_sensor_data()

            self._twin.update_state(state)
            self._twin.update_sensor_data(sensors)

            # Record a snapshot of this time step
            self._twin.snapshot()

            logger.debug("Sensor update processed successfully")
        except Exception as e:
            logger.error("Failed to process sensor update", error=str(e), exc_info=True)
            raise SimulationException(f"Error during sensor update: {e}") from e

    def apply_control_action(self, action: ControlAction) -> None:
        """Forwards a control action to the simulator and logs it in the twin."""
        logger.info(
            "Applying control action", zone_id=action.zone_id, reason=action.reason
        )
        try:
            self._adapter.apply_control(action)
            self._twin.update_control(action)
            logger.info("Control action applied successfully")
        except Exception as e:
            logger.error("Failed to apply control action", error=str(e), exc_info=True)
            raise SimulationException(f"Failed to apply control action: {e}") from e

    def get_snapshot(self) -> Optional[SimulationSnapshot]:
        """Retrieves a point-in-time snapshot directly from the Twin manager."""
        return self._twin.snapshot()
