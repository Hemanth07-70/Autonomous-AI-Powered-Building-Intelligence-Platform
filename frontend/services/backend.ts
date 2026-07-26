import { api } from "@/lib/api"
import type {
  AgentHealthResponse,
  AgentRunResponse,
  AiChatRequest,
  AiChatResponse,
  AiHealthResponse,
  AiModelsResponse,
  ExecutionPlan,
  SimulationJobCreate,
  SimulationJobRead,
} from "@/types/api"

export const backend = {
  health: async () => (await api.get<{ status: string }>("/health")).data,
  root: async () => (await api.get<{ application: string; status: string; version: string }>("/")).data,
  ai: {
    chat: async (payload: AiChatRequest) => (await api.post<AiChatResponse>("/api/ai/chat", payload)).data,
    plan: async (payload: AiChatRequest) => (await api.post<ExecutionPlan | unknown>("/api/ai/plan", payload)).data,
    models: async () => (await api.get<AiModelsResponse>("/api/ai/models")).data,
    health: async () => (await api.get<AiHealthResponse>("/api/ai/health")).data,
  },
  decision: {
    goals: async () => (await api.get<unknown[]>("/api/decision/goals")).data,
    goal: async (goalId: string) => (await api.get<unknown>(`/api/decision/goals/${goalId}`)).data,
    goalPlan: async (goalId: string) => (await api.post<ExecutionPlan>(`/api/decision/goals/${goalId}/plan`)).data,
    plan: async (planId: string) => (await api.get<ExecutionPlan>(`/api/decision/plans/${planId}`)).data,
  },
  simulations: {
    list: async () => (await api.get<SimulationJobRead[]>("/api/simulations")).data,
    create: async (payload: SimulationJobCreate) => (await api.post<SimulationJobRead>("/api/simulations", payload)).data,
    get: async (jobId: string) => (await api.get<SimulationJobRead>(`/api/simulations/${jobId}`)).data,
    start: async (jobId: string) => (await api.post<SimulationJobRead>(`/api/simulations/${jobId}/start`)).data,
    cancel: async (jobId: string) => (await api.post<SimulationJobRead>(`/api/simulations/${jobId}/cancel`)).data,
  },
  agents: {
    run: async (message: string) => (await api.post<AgentRunResponse>("/api/agents/run", { message })).data,
    health: async () => (await api.get<AgentHealthResponse>("/api/agents/health")).data,
  },
}
