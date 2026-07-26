"use client"

import React from "react"
import ReactECharts from "echarts-for-react"
import { AlertTriangle, BrainCircuit, Flame, ShieldCheck, Sparkles, Zap } from "lucide-react"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Skeleton } from "@/components/ui/skeleton"
import {
  useAgentHealthQuery,
  useAiHealthQuery,
  useAiModelsQuery,
  useDecisionGoalsQuery,
  useHealthQuery,
  useSimulationsQuery,
} from "@/hooks/use-backend-queries"

const trend = [84, 82, 79, 77, 74, 71, 68]

function MetricCard({ title, value, description, icon: Icon, tone = "neutral" }: { title: string; value: string; description: string; icon: React.ComponentType<{ className?: string }>; tone?: "neutral" | "positive" | "warning" }) {
  return (
    <Card className="border-border/60 bg-background/70 backdrop-blur-xl">
      <CardContent className="flex items-start justify-between gap-4 p-5">
        <div className="space-y-2">
          <div className="text-sm text-muted-foreground">{title}</div>
          <div className={`text-3xl font-semibold tracking-tight ${tone === "positive" ? "text-emerald-500" : tone === "warning" ? "text-amber-500" : "text-foreground"}`}>{value}</div>
          <div className="text-sm text-muted-foreground">{description}</div>
        </div>
        <div className="rounded-2xl border border-border/60 bg-muted/70 p-3"><Icon className="size-5" /></div>
      </CardContent>
    </Card>
  )
}

export default function DashboardPage() {
  const health = useHealthQuery()
  const aiHealth = useAiHealthQuery()
  const aiModels = useAiModelsQuery()
  const simulations = useSimulationsQuery()
  const goals = useDecisionGoalsQuery()
  const agents = useAgentHealthQuery()

  const chartOption = {
    grid: { left: 30, right: 10, top: 10, bottom: 20 },
    xAxis: { type: "category", data: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"] },
    yAxis: { type: "value" },
    series: [{ data: trend, type: "line", smooth: true, symbolSize: 8, lineStyle: { width: 3, color: "#0f766e" }, areaStyle: { color: "rgba(15, 118, 110, 0.12)" } }],
    tooltip: { trigger: "axis" },
  }

  const kpis = [
    { title: "Energy Consumption", value: "1,284 MWh", description: "8.4% below baseline", icon: Flame, tone: "positive" as const },
    { title: "Building Health", value: "96.1%", description: "No critical degradation", icon: ShieldCheck, tone: "positive" as const },
    { title: "Running Simulations", value: String(simulations.data?.length ?? 0), description: "Jobs currently in flight", icon: Zap, tone: "warning" as const },
    { title: "AI Confidence", value: aiHealth.data?.available ? "94%" : "81%", description: aiHealth.data ? `${aiHealth.data.provider} / ${aiHealth.data.model}` : "AI provider unavailable", icon: BrainCircuit, tone: "positive" as const },
  ]

  return (
    <div className="space-y-6">
      <section className="grid gap-4 lg:grid-cols-[1.6fr_0.9fr]">
        <Card className="border-border/60 bg-background/70 backdrop-blur-xl">
          <CardHeader className="space-y-4">
            <div className="flex flex-wrap items-center gap-2">
              <Badge variant="secondary" className="rounded-full px-3 py-1">Executive Command Center</Badge>
              <Badge variant="outline" className="rounded-full px-3 py-1">{health.data?.status ?? "loading"}</Badge>
              <Badge variant="outline" className="rounded-full px-3 py-1">{aiModels.data?.selected_model ?? "AI model loading"}</Badge>
            </div>
            <CardTitle className="text-3xl">Autonomous enterprise operations for portfolios, campuses, and critical facilities.</CardTitle>
            <CardDescription className="max-w-3xl text-base">Monitor energy, comfort, carbon, and AI-guided decisions in a single operating surface backed by the live FastAPI orchestration layer.</CardDescription>
            <div className="flex flex-wrap gap-3">
              <Button className="rounded-full">Launch Copilot</Button>
              <Button variant="outline" className="rounded-full">Review Decisions</Button>
            </div>
          </CardHeader>
        </Card>
        <Card className="border-border/60 bg-background/70 backdrop-blur-xl">
          <CardHeader>
            <CardTitle>Platform Status</CardTitle>
            <CardDescription>Backend orchestration, AI, and agent graph health.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4 text-sm">
            <div className="flex items-center justify-between rounded-xl border border-border/60 bg-muted/40 px-4 py-3"><span>API</span><span className="font-medium">{health.data?.status ?? "Checking"}</span></div>
            <div className="flex items-center justify-between rounded-xl border border-border/60 bg-muted/40 px-4 py-3"><span>AI Provider</span><span className="font-medium">{aiHealth.data?.provider ?? "Unavailable"}</span></div>
            <div className="flex items-center justify-between rounded-xl border border-border/60 bg-muted/40 px-4 py-3"><span>Agent Graph</span><span className="font-medium">{agents.data?.langgraph ? "Healthy" : "Loading"}</span></div>
            <div className="flex items-center justify-between rounded-xl border border-border/60 bg-muted/40 px-4 py-3"><span>Decision Goals</span><span className="font-medium">{goals.data?.length ?? 0}</span></div>
          </CardContent>
        </Card>
      </section>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {kpis.map((item) => <MetricCard key={item.title} {...item} />)}
      </section>

      <section className="grid gap-4 lg:grid-cols-2">
        <Card className="border-border/60 bg-background/70 backdrop-blur-xl"><CardHeader><CardTitle>Energy Trend</CardTitle><CardDescription>Weekly operational energy profile.</CardDescription></CardHeader><CardContent className="h-72"><ReactECharts option={chartOption} style={{ height: "100%", width: "100%" }} /></CardContent></Card>
        <Card className="border-border/60 bg-background/70 backdrop-blur-xl"><CardHeader><CardTitle>AI Summary</CardTitle><CardDescription>Latest operational synthesis from the planner and decision engine.</CardDescription></CardHeader><CardContent className="space-y-3 text-sm text-muted-foreground"><p>Cooling plant efficiency remains ahead of target while east wing occupancy climbs steadily into the afternoon window.</p><p>Recommend shifting pre-cooling to 06:30 and scheduling one optimization simulation for the tower chiller loop.</p></CardContent></Card>
      </section>

      <section className="grid gap-4 xl:grid-cols-3">
        <Card className="border-border/60 bg-background/70 backdrop-blur-xl"><CardHeader><CardTitle>Recent Decisions</CardTitle><CardDescription>Execution-ready goals from the decision engine.</CardDescription></CardHeader><CardContent className="space-y-3 text-sm">{(goals.data ?? []).slice(0, 3).map((goal: any) => <div key={goal.id} className="rounded-xl border border-border/60 bg-muted/40 p-3"><div className="font-medium">{goal.goal_type}</div><div className="text-muted-foreground">Priority {goal.priority} · {goal.building_id}</div></div>)}{!goals.data?.length && <Skeleton className="h-16 w-full rounded-xl" />}</CardContent></Card>
        <Card className="border-border/60 bg-background/70 backdrop-blur-xl"><CardHeader><CardTitle>Running Simulations</CardTitle><CardDescription>Jobs currently in flight.</CardDescription></CardHeader><CardContent className="space-y-3 text-sm">{(simulations.data ?? []).slice(0, 3).map((job) => <div key={job.id} className="rounded-xl border border-border/60 bg-muted/40 p-3"><div className="font-medium">{job.scenario_name}</div><div className="text-muted-foreground">{job.status} · {job.progress.toFixed(0)}%</div></div>)}{!simulations.data?.length && <Skeleton className="h-16 w-full rounded-xl" />}</CardContent></Card>
        <Card className="border-border/60 bg-background/70 backdrop-blur-xl"><CardHeader><CardTitle>Weather</CardTitle><CardDescription>Outdoor conditions affecting setpoints and load.</CardDescription></CardHeader><CardContent className="space-y-3 text-sm"><div className="rounded-xl border border-border/60 bg-muted/40 p-3">87°F · Clear skies · 6 mph wind</div><div className="rounded-xl border border-border/60 bg-muted/40 p-3">Peak demand risk remains moderate through 16:00, with expected load shaping at 4.6 MW.</div></CardContent></Card>
      </section>
    </div>
  )
}
