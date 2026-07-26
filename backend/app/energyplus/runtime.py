import threading
from typing import Any

import structlog

from app.energyplus.errors import EnergyPlusRuntimeError

logger = structlog.get_logger("energyplus.runtime")


class EnergyPlusRuntime:
    """
    Manages the synchronous PyEnergyPlus C-engine inside a dedicated background thread.
    Exposes threading primitives to allow step-by-step synchronization.
    """

    def __init__(self, api: Any, state_ref: Any):
        self.api = api
        self.state_ref = state_ref

        self._thread: threading.Thread | None = None
        self._run_condition = threading.Condition()
        self._step_completed_event = threading.Event()

        self._is_running = False
        self._is_paused = False
        self._fatal_error: Exception | None = None

    def start(self, args: list[str]) -> None:
        """Starts the EnergyPlus engine in a background thread."""
        if self._is_running:
            return

        self._is_running = True
        self._is_paused = False
        self._fatal_error = None
        self._step_completed_event.clear()

        self._thread = threading.Thread(
            target=self._run_engine, args=(args,), daemon=True
        )
        self._thread.start()
        logger.info("EnergyPlus runtime thread started")

    def _run_engine(self, args: list[str]) -> None:
        """The blocking call to the native C-engine."""
        try:
            exit_code = self.api.runtime.run_energyplus(self.state_ref, args)
            if exit_code != 0:
                raise EnergyPlusRuntimeError(
                    f"EnergyPlus engine exited with non-zero code: {exit_code}"
                )
        except Exception as e:
            self._fatal_error = e
            logger.error(
                "Fatal error inside EnergyPlus runtime", error=str(e), exc_info=True
            )
        finally:
            self._is_running = False
            # Unblock any waiting threads on exit
            self._step_completed_event.set()
            with self._run_condition:
                self._run_condition.notify_all()

    def sync_timestep(self) -> None:
        """
        Called by the callback inside the C-engine thread.
        Signals the main thread that a step completed, then blocks if paused.
        """
        # Signal that the step is done
        self._step_completed_event.set()

        # Block if the engine is paused
        with self._run_condition:
            while self._is_paused and self._is_running:
                self._run_condition.wait()

    def wait_for_step_completion(self, timeout: float = 5.0) -> bool:
        """
        Called by the main thread.
        Waits for the C-engine to complete a timestep.
        """
        success = self._step_completed_event.wait(timeout=timeout)
        if success:
            self._step_completed_event.clear()
        return success

    def pause(self) -> None:
        """Pauses the engine at the next timestep."""
        with self._run_condition:
            self._is_paused = True

    def resume(self) -> None:
        """Resumes the engine if paused."""
        with self._run_condition:
            self._is_paused = False
            self._run_condition.notify_all()

    def stop(self) -> None:
        """Stops the engine forcefully by signaling the C-API."""
        self._is_running = False
        with self._run_condition:
            self._is_paused = False
            self._run_condition.notify_all()
        # Instruct the API to stop if possible
        if hasattr(self.api.runtime, "stop_simulation"):
            self.api.runtime.stop_simulation(self.state_ref)

    def is_running(self) -> bool:
        return self._is_running

    def get_error(self) -> Exception | None:
        return self._fatal_error
