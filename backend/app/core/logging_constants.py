"""
Centralized constants for structured logging.
Ensures uniform log keys across all microservices and layers.
"""

# Context Keys
LOG_KEY_REQUEST_ID = "request_id"
LOG_KEY_SIMULATION_TICK = "simulation_tick"
LOG_KEY_AGENT_ID = "agent_id"

# Event Types
EVENT_HTTP_REQUEST = "http.request"
EVENT_SIMULATION_START = "simulation.start"
EVENT_SIMULATION_STEP = "simulation.step"
EVENT_AI_REASONING = "ai.reasoning"

# Standard Metadata
META_DURATION_MS = "duration_ms"
META_STATUS_CODE = "status_code"
