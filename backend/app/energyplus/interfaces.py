from abc import ABC, abstractmethod
from typing import List

from app.energyplus.simulation_state import BuildingState, ControlAction, SensorData


class SimulationAdapter(ABC):
    """
    Abstract Base Class defining the contract for any simulation engine
    (e.g., EnergyPlus).
    The AI and Digital Twin must only depend on this interface, never concrete
    implementations.
    """

    @abstractmethod
    def connect(self) -> None:
        """Establishes a connection to the simulation engine."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Closes the connection to the simulation engine."""
        pass

    @abstractmethod
    def initialize(self) -> None:
        """Initializes the simulation with necessary configurations."""
        pass

    @abstractmethod
    def start(self) -> None:
        """Starts the simulation loop."""
        pass

    @abstractmethod
    def stop(self) -> None:
        """Stops the active simulation gracefully."""
        pass

    @abstractmethod
    def pause(self) -> None:
        """Pauses the active simulation."""
        pass

    @abstractmethod
    def resume(self) -> None:
        """Resumes a paused simulation."""
        pass

    @abstractmethod
    def step(self) -> None:
        """Advances the simulation by one configured time step."""
        pass

    @abstractmethod
    def restart(self) -> None:
        """Restarts the simulation from the beginning."""
        pass

    @abstractmethod
    def get_state(self) -> BuildingState:
        """Retrieves the current macro state of the building and environment."""
        pass

    @abstractmethod
    def get_sensor_data(self) -> List[SensorData]:
        """Retrieves all current sensor readings from the building zones."""
        pass

    @abstractmethod
    def apply_control(self, action: ControlAction) -> None:
        """Applies a specific control action (setpoints/overrides) to the simulator."""
        pass

    @abstractmethod
    def shutdown(self) -> None:
        """Performs full teardown and cleanup of the simulation resources."""
        pass
