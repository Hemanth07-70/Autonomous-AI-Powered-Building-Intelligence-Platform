export type GoalType =
  | "energy_optimization"
  | "comfort_optimization"
  | "carbon_reduction"
  | "fault_detection"
  | string

export type PlanStatus = "CREATED" | "READY" | "RUNNING" | "COMPLETED" | string

export type SimulationStatus =
  | "PENDING"
  | "QUEUED"
  | "RUNNING"
  | "COMPLETED"
  | "FAILED"
  | "CANCELLED"
  | string

export interface AiChatRequest {
  message: string
  building_id?: string | null
}

export interface DecisionGoal {
  id: string
  goal_type: GoalType
  priority: number
  building_id: string
  constraints: Record<string, unknown>
  parameters: Record<string, unknown>
  created_at: string
}

export interface AiChatResponse {
  response: string
  decision_goal: DecisionGoal
}

export interface AiHealthResponse {
  available: boolean
  provider: string
  model: string
}

export interface AiModelsResponse {
  models: string[]
  selected_model: string
}

export interface ExecutionPlan {
  id: string
  goal_id: string
  simulation_jobs: string[]
  execution_order: string[]
  status: PlanStatus
  estimated_runtime: number
  created_at: string
}

export interface SimulationJobRead {
  id: string
  twin_id: string
  scenario_name: string
  status: SimulationStatus
  created_at: string
  started_at: string | null
  completed_at: string | null
  progress: number
  simulation_state: unknown | null
  error_message: string | null
  output_directory: string
  duration_seconds: number | null
}

export interface SimulationJobCreate {
  twin_id: string
  scenario_name: string
  output_directory?: string | null
}

export interface AgentRunResponse {
  decision_goal: DecisionGoal | null
  execution_plan: ExecutionPlan | null
  analytics: unknown | null
  diagnostics: unknown | null
  recommendations: unknown[]
}

export interface AgentHealthResponse {
  langgraph: boolean
  agents: string[]
  version: string
}
