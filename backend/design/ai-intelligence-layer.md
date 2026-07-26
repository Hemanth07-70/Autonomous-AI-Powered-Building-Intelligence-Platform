# AI Intelligence Layer

Milestone 6 introduces a natural-language interface that converts user requests into deterministic `DecisionGoal` objects. The AI layer never executes simulations and never communicates with EnergyPlus.

## Position in the Architecture

```text
User / Dashboard
      ↓
REST API (/api/ai/*)
      ↓
AI Intelligence Layer
  ├── OllamaClient
  ├── AIPlanner
  ├── Parser
  └── Prompts
      ↓
Decision Engine
      ↓
Simulation Orchestrator
      ↓
Simulation Controller
      ↓
SimulationAdapter
      ↓
EnergyPlusAdapter
```

## Module Layout

| File | Responsibility |
|------|----------------|
| `app/ai/client.py` | Ollama HTTP client with health check, model listing, chat completion, timeout, and retry handling |
| `app/ai/planner.py` | Orchestrates prompt construction, inference, parsing, and `DecisionGoal` creation |
| `app/ai/parser.py` | Extracts and validates structured JSON from model output |
| `app/ai/prompts.py` | Reusable system and domain prompts for all supported goal types |
| `app/ai/schemas.py` | FastAPI request and response models |
| `app/ai/exceptions.py` | AI-specific error types |

## Ollama Integration

Configuration is loaded from environment variables:

| Variable | Default | Purpose |
|----------|---------|---------|
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama server base URL |
| `OLLAMA_MODEL` | `qwen3` | Default model name |
| `OLLAMA_TIMEOUT` | `30.0` | Request timeout in seconds |

`OllamaClient` responsibilities:

- Connect to Ollama
- List available models via `GET /api/tags`
- Health check by verifying model listing succeeds
- Chat completion via `POST /api/generate`
- Retry transient failures up to two times
- Raise `ModelUnavailableError` when the configured model is not installed

## Prompt Architecture

Prompts are centralized in `app/ai/prompts.py`. No inline prompts are used elsewhere.

Components:

1. **System prompt** — defines the required JSON schema and supported `goal_type` values
2. **Domain templates** — one reusable template per `GoalType`:
   - Energy optimization
   - HVAC optimization
   - Lighting optimization
   - Occupancy analysis
   - Thermal comfort
   - Diagnostics
   - Water optimization
   - Carbon reduction
   - Peak load reduction
3. **User request** — appended at runtime by `build_prompt()`

Example output shape:

```json
{
  "goal_type": "ENERGY_REDUCTION",
  "building_id": "building-a",
  "priority": 1,
  "constraints": {
    "target_reduction": 15
  },
  "parameters": {}
}
```

## Parser Architecture

`parse_decision_goal()` performs four validation steps:

1. Extract JSON from plain or markdown-wrapped model output
2. Reject malformed JSON with `InvalidAIResponse`
3. Validate `goal_type` against the `GoalType` enum with `UnsupportedGoalError`
4. Validate the full payload against `DecisionGoalCreate` with Pydantic

Validated fields:

- `goal_type`
- `building_id`
- `priority`
- `constraints`
- `parameters`

## Planner Flow

```text
User message
  → build_prompt()
  → ensure_model_available()
  → chat_completion()
  → parse_decision_goal()
  → DecisionEngine.create_goal()
  → DecisionGoal
```

`AIPlanner.chat()` returns both a human-readable summary and the persisted `DecisionGoal`.

## REST Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/ai/chat` | Convert natural language into a response plus `DecisionGoal` |
| POST | `/api/ai/plan` | Convert natural language into a `DecisionGoal` only |
| GET | `/api/ai/models` | List Ollama models and the selected model |
| GET | `/api/ai/health` | Report Ollama availability and configured model |

## Logging

Structured logs are emitted for:

- Incoming prompt metadata
- Selected model
- Inference latency
- Parser success and failure
- DecisionGoal generation
- Connection and retry errors

## Error Handling

| Exception | Meaning |
|-----------|---------|
| `AIConnectionError` | Ollama is unreachable or returned an invalid response |
| `InvalidAIResponse` | Model output was not valid JSON or schema |
| `UnsupportedGoalError` | Model returned an unsupported `goal_type` |
| `ModelUnavailableError` | Configured model is not installed in Ollama |

API endpoints map these exceptions to HTTP 400 responses.

## Testing Strategy

All tests mock Ollama and do not require a running local model server.

Coverage includes:

- Ollama client retries, health check, and model availability
- Parser JSON extraction and validation
- Planner goal generation through the Decision Engine
- REST API success and error paths

## Constraints

This milestone intentionally excludes:

- LangGraph
- Supervisor agents
- MCP servers
- Autonomous execution
- Direct AI access to EnergyPlus or simulation adapters

All execution continues through the existing Decision Engine and Simulation Orchestrator.
