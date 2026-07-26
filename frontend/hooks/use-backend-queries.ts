"use client"

import { useMutation, useQuery } from "@tanstack/react-query"
import { backend } from "@/services/backend"
import type { AiChatRequest, SimulationJobCreate } from "@/types/api"

export const backendKeys = {
  health: ["backend", "health"] as const,
  aiHealth: ["backend", "ai", "health"] as const,
  aiModels: ["backend", "ai", "models"] as const,
  aiChat: (payload: AiChatRequest) => ["backend", "ai", "chat", payload] as const,
  simulations: ["backend", "simulations"] as const,
  decisionGoals: ["backend", "decision", "goals"] as const,
  agentsHealth: ["backend", "agents", "health"] as const,
} 

export function useHealthQuery() {
  return useQuery({ queryKey: backendKeys.health, queryFn: backend.health, retry: 1 })
}

export function useAiHealthQuery() {
  return useQuery({ queryKey: backendKeys.aiHealth, queryFn: backend.ai.health, retry: 1 })
}

export function useAiModelsQuery() {
  return useQuery({ queryKey: backendKeys.aiModels, queryFn: backend.ai.models, retry: 1 })
}

export function useSimulationsQuery() {
  return useQuery({ queryKey: backendKeys.simulations, queryFn: backend.simulations.list, retry: 1 })
}

export function useDecisionGoalsQuery() {
  return useQuery({ queryKey: backendKeys.decisionGoals, queryFn: backend.decision.goals, retry: 1 })
}

export function useAgentHealthQuery() {
  return useQuery({ queryKey: backendKeys.agentsHealth, queryFn: backend.agents.health, retry: 1 })
}

export function useAiChatMutation() {
  return useMutation({
    mutationFn: (payload: AiChatRequest) => backend.ai.chat(payload),
  })
}

export function useCreateSimulationMutation() {
  return useMutation({
    mutationFn: (payload: SimulationJobCreate) => backend.simulations.create(payload),
  })
}
