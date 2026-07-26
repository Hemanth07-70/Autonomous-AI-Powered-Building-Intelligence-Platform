from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.shared.enums import SimulationStatus


class WeatherState(BaseModel):
    """
    Represents the current weather conditions in the simulation.
    """

    outside_temperature: float = Field(
        ..., description="Outside air temperature in Celsius"
    )
    humidity: float = Field(..., description="Outside relative humidity percentage")
    wind_speed: float = Field(..., description="Wind speed in m/s")
    solar_radiation: float = Field(..., description="Solar radiation in W/m^2")


class BuildingState(BaseModel):
    """
    Represents the macro state of the building and simulation engine.
    """

    simulation_time: datetime = Field(
        ..., description="Current virtual time in the simulation"
    )
    weather: WeatherState = Field(..., description="Current weather conditions")
    occupancy: int = Field(..., description="Total building occupancy count")
    hvac_status: bool = Field(..., description="True if central HVAC system is active")
    simulation_status: SimulationStatus = Field(
        ..., description="Current status of the engine"
    )


class SensorData(BaseModel):
    """
    Represents readings from a specific zone/sensor in the building.
    """

    zone_id: str = Field(..., description="Unique identifier for the zone")
    zone_name: str = Field(..., description="Human-readable name of the zone")
    temperature: float = Field(..., description="Current zone temperature in Celsius")
    humidity: float = Field(
        ..., description="Current zone relative humidity percentage"
    )
    energy_consumption: float = Field(
        ..., description="Current power consumption in Watts"
    )
    pmv: Optional[float] = Field(
        None, description="Predicted Mean Vote (thermal comfort index)"
    )
    air_quality: Optional[float] = Field(None, description="General air quality index")
    co2: Optional[float] = Field(None, description="CO2 concentration in ppm")
    timestamp: datetime = Field(
        ..., description="Simulation time when reading was taken"
    )


class ControlAction(BaseModel):
    """
    Represents a command sent to modify building setpoints.
    """

    zone_id: str = Field(..., description="Target zone identifier")
    cooling_setpoint: Optional[float] = Field(
        None, description="New cooling setpoint in Celsius"
    )
    heating_setpoint: Optional[float] = Field(
        None, description="New heating setpoint in Celsius"
    )
    fan_speed: Optional[float] = Field(None, description="Fan speed percentage (0-100)")
    ventilation_rate: Optional[float] = Field(
        None, description="Ventilation rate in m^3/s"
    )
    reason: str = Field(
        ..., description="Explanation of why this action was taken (for AI tracking)"
    )
    issued_at: datetime = Field(
        ..., description="Simulation time when action was issued"
    )


class SimulationSnapshot(BaseModel):
    """
    Represents an aggregated, point-in-time state of the entire digital twin.
    """

    building_state: BuildingState
    sensor_data: List[SensorData] = Field(default_factory=list)
    last_control: Optional[ControlAction] = Field(
        None, description="The most recent control action applied"
    )
