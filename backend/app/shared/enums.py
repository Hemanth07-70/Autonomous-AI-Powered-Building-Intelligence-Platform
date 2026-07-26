from enum import Enum


class SimulationStatus(str, Enum):
    """
    Status of the simulation engine.
    """

    INITIALIZED = "INITIALIZED"
    READY = "READY"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    STOPPED = "STOPPED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    PENDING = "PENDING"
    QUEUED = "QUEUED"
    STARTING = "STARTING"
    CANCELLED = "CANCELLED"


class GoalType(str, Enum):
    """
    Deterministic decision goal categories supported by the Decision Engine.
    """

    ENERGY_REDUCTION = "ENERGY_REDUCTION"
    PEAK_LOAD = "PEAK_LOAD"
    THERMAL_COMFORT = "THERMAL_COMFORT"
    HVAC = "HVAC"
    LIGHTING = "LIGHTING"
    OCCUPANCY = "OCCUPANCY"
    CARBON = "CARBON"
    WATER = "WATER"
    DIAGNOSTICS = "DIAGNOSTICS"


class PlanStatus(str, Enum):
    """
    Lifecycle status for deterministic execution plans.
    """

    CREATED = "CREATED"
    VALIDATED = "VALIDATED"
    READY = "READY"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
