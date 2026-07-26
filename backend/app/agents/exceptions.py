class AgentException(Exception):
    """Base exception for the LangGraph agent module."""

    pass


class GraphExecutionError(AgentException):
    """Raised when the LangGraph workflow encounters a fatal error."""

    pass


class AgentToolError(AgentException):
    """Raised when an agent tool fails."""

    pass


class AgentStateError(AgentException):
    """Raised when the graph state is invalid or missing required data."""

    pass
