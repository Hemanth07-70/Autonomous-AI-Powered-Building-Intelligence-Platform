"use client"

import { create } from "zustand"
import type { DecisionGoal } from "@/types/api"

export type ThemeMode = "light" | "dark" | "system"

export type CopilotMessage = {
  role: "user" | "assistant"
  content: string
  goal?: DecisionGoal
}

interface AppState {
  theme: ThemeMode
  selectedBuildingId: string | null
  selectedSimulationId: string | null
  commandPaletteOpen: boolean
  notificationsOpen: boolean
  filters: Record<string, string[]>
  copilotMessages: CopilotMessage[]
  setTheme: (theme: ThemeMode) => void
  setSelectedBuildingId: (buildingId: string | null) => void
  setSelectedSimulationId: (simulationId: string | null) => void
  setCommandPaletteOpen: (open: boolean) => void
  setNotificationsOpen: (open: boolean) => void
  setFilter: (key: string, values: string[]) => void
  addCopilotMessage: (message: CopilotMessage) => void
  clearCopilotMessages: () => void
}

const initialCopilotMessage: CopilotMessage = {
  role: "assistant",
  content:
    "I can synthesize decisions, build execution plans, and return a structured operating goal for the selected building.",
}

export const useAppStore = create<AppState>((set) => ({
  theme: "system",
  selectedBuildingId: null,
  selectedSimulationId: null,
  commandPaletteOpen: false,
  notificationsOpen: false,
  filters: {},
  copilotMessages: [initialCopilotMessage],
  setTheme: (theme) => set({ theme }),
  setSelectedBuildingId: (selectedBuildingId) => set({ selectedBuildingId }),
  setSelectedSimulationId: (selectedSimulationId) => set({ selectedSimulationId }),
  setCommandPaletteOpen: (commandPaletteOpen) => set({ commandPaletteOpen }),
  setNotificationsOpen: (notificationsOpen) => set({ notificationsOpen }),
  setFilter: (key, values) =>
    set((state) => ({ filters: { ...state.filters, [key]: values } })),
  addCopilotMessage: (message) =>
    set((state) => ({ copilotMessages: [...state.copilotMessages, message] })),
  clearCopilotMessages: () => set({ copilotMessages: [initialCopilotMessage] }),
}))

