"use client"

import { create } from "zustand"

export type ThemeMode = "light" | "dark" | "system"

interface AppState {
  theme: ThemeMode
  selectedBuildingId: string | null
  selectedSimulationId: string | null
  commandPaletteOpen: boolean
  notificationsOpen: boolean
  filters: Record<string, string[]>
  setTheme: (theme: ThemeMode) => void
  setSelectedBuildingId: (buildingId: string | null) => void
  setSelectedSimulationId: (simulationId: string | null) => void
  setCommandPaletteOpen: (open: boolean) => void
  setNotificationsOpen: (open: boolean) => void
  setFilter: (key: string, values: string[]) => void
}

export const useAppStore = create<AppState>((set) => ({
  theme: "system",
  selectedBuildingId: null,
  selectedSimulationId: null,
  commandPaletteOpen: false,
  notificationsOpen: false,
  filters: {},
  setTheme: (theme) => set({ theme }),
  setSelectedBuildingId: (selectedBuildingId) => set({ selectedBuildingId }),
  setSelectedSimulationId: (selectedSimulationId) => set({ selectedSimulationId }),
  setCommandPaletteOpen: (commandPaletteOpen) => set({ commandPaletteOpen }),
  setNotificationsOpen: (notificationsOpen) => set({ notificationsOpen }),
  setFilter: (key, values) =>
    set((state) => ({ filters: { ...state.filters, [key]: values } })),
}))
