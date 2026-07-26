from typing import Any, Callable

import structlog

from app.energyplus.errors import CallbackError

logger = structlog.get_logger("energyplus.callbacks")


class CallbackManager:
    """
    Manages the registration and execution of EnergyPlus runtime callbacks.
    """

    def __init__(self, api: Any, state_ref: Any, on_zone_timestep: Callable[[], None]):
        """
        Args:
            api: The pyenergyplus API instance.
            state_ref: The pointer to the EnergyPlus runtime state.
            on_zone_timestep: A callable to trigger when a zone timestep completes.
        """
        self.api = api
        self.state_ref = state_ref
        self.on_zone_timestep = on_zone_timestep
        self._is_registered = False

    def register_all(self):
        """Registers all necessary callbacks with the EnergyPlus runtime."""
        if self._is_registered:
            return

        try:
            self.api.runtime.callback_end_zone_timestep_after_zone_reporting(
                self.state_ref, self._handle_end_zone_timestep
            )
            self._is_registered = True
            logger.debug("EnergyPlus callbacks successfully registered")
        except Exception as e:
            logger.error("Failed to register callbacks", error=str(e))
            raise CallbackError(f"Failed to register callbacks: {e}") from e

    def _handle_end_zone_timestep(self, state: Any) -> None:
        """
        Triggered natively by EnergyPlus at the end of each zone timestep.
        """
        try:
            if self.on_zone_timestep:
                self.on_zone_timestep()
        except Exception as e:
            logger.error(
                "Error during zone timestep callback execution",
                error=str(e),
                exc_info=True,
            )
            # Cannot raise exceptions back into C-engine safely,
            # must swallow or signal thread
