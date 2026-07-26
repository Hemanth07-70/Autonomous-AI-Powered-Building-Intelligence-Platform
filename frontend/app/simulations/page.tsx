"use client"

import * as React from "react"
import { z } from "zod"
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { CheckCircle2, CircleSlash, Play, Plus, RefreshCw, Square, Timer } from "lucide-react"
import { useQueryClient } from "@tanstack/react-query"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { useCreateSimulationMutation, useSimulationsQuery } from "@/hooks/use-backend-queries"
import type { SimulationJobCreate } from "@/types/api"

const schema = z.object({
  twinId: z.string().min(1),
  scenarioName: z.string().min(3),
  outputDirectory: z.string().optional(),
})

type FormValues = z.infer<typeof schema>

export default function SimulationsPage() {
  const simulations = useSimulationsQuery()
  const createSimulation = useCreateSimulationMutation()
  const queryClient = useQueryClient()

  const form = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: {
      twinId: "tower-a",
      scenarioName: "Peak demand reduction scenario",
      outputDirectory: "/simulations/tower-a",
    },
  })

  const onSubmit = async (values: FormValues) => {
    const payload: SimulationJobCreate = {
      twin_id: values.twinId,
      scenario_name: values.scenarioName,
      output_directory: values.outputDirectory || undefined,
    }
    await createSimulation.mutateAsync(payload)
    await queryClient.invalidateQueries({ queryKey: ["backend", "simulations"] })
  }

  const performAction = async (jobId: string, action: "start" | "cancel") => {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"}/api/simulations/${jobId}/${action}`, { method: "POST" })
    if (response.ok) {
      await queryClient.invalidateQueries({ queryKey: ["backend", "simulations"] })
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <div className="text-sm uppercase tracking-[0.22em] text-muted-foreground">Simulation center</div>
          <h1 className="text-3xl font-semibold tracking-tight">Simulation Center</h1>
          <p className="mt-2 max-w-3xl text-muted-foreground">Create, queue, start, cancel, and inspect EnergyPlus simulation jobs from a single operational surface.</p>
        </div>
        <Badge variant="secondary" className="rounded-full px-3 py-1">{simulations.data?.length ?? 0} jobs tracked</Badge>
      </div>

      <Card className="border-border/60 bg-background/70 backdrop-blur-xl">
        <CardHeader>
          <CardTitle>Create Simulation Job</CardTitle>
          <CardDescription>Submit a new execution request to the backend orchestrator.</CardDescription>
        </CardHeader>
        <CardContent>
          <form className="grid gap-4 md:grid-cols-4" onSubmit={form.handleSubmit(onSubmit)}>
            <Input className="h-12 rounded-xl" placeholder="Twin ID" {...form.register("twinId")} />
            <Input className="h-12 rounded-xl md:col-span-2" placeholder="Scenario name" {...form.register("scenarioName")} />
            <Input className="h-12 rounded-xl" placeholder="Output directory" {...form.register("outputDirectory")} />
            <div className="md:col-span-4 flex justify-end">
              <Button type="submit" className="rounded-full px-5"><Plus className="mr-2 size-4" /> Create job</Button>
            </div>
          </form>
        </CardContent>
      </Card>

      <Card className="border-border/60 bg-background/70 backdrop-blur-xl">
        <CardHeader>
          <div className="flex items-center justify-between gap-3">
            <div>
              <CardTitle>Execution Queue</CardTitle>
              <CardDescription>Simulation IDs, progress, runtime, and orchestration actions.</CardDescription>
            </div>
            <Button variant="outline" className="rounded-full" onClick={() => simulations.refetch()}><RefreshCw className="mr-2 size-4" /> Refresh</Button>
          </div>
        </CardHeader>
        <CardContent className="overflow-hidden rounded-2xl border border-border/60">
          <table className="w-full text-sm">
            <thead className="bg-muted/60 text-left text-muted-foreground">
              <tr>
                <th className="px-4 py-3">Simulation ID</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">Runtime</th>
                <th className="px-4 py-3">Progress</th>
                <th className="px-4 py-3">Execution Order</th>
                <th className="px-4 py-3"></th>
              </tr>
            </thead>
            <tbody>
              {(simulations.data ?? []).map((job) => (
                <tr key={job.id} className="border-t border-border/60">
                  <td className="px-4 py-4 font-medium">{job.id}</td>
                  <td className="px-4 py-4"><Badge variant={job.status === "FAILED" ? "destructive" : "secondary"} className="rounded-full">{job.status}</Badge></td>
                  <td className="px-4 py-4">{job.duration_seconds ? `${Math.round(job.duration_seconds)} sec` : "Running"}</td>
                  <td className="px-4 py-4"><div className="h-2 rounded-full bg-muted"><div className="h-2 rounded-full bg-foreground" style={{ width: `${job.progress}%` }} /></div><div className="mt-1 text-xs text-muted-foreground">{job.progress.toFixed(0)}%</div></td>
                  <td className="px-4 py-4">{job.scenario_name}</td>
                  <td className="px-4 py-4">
                    <div className="flex flex-wrap justify-end gap-2">
                      <Button variant="outline" size="sm" className="rounded-full" onClick={() => performAction(job.id, "start")}><Play className="mr-1 size-4" /> Run</Button>
                      <Button variant="ghost" size="sm" className="rounded-full" onClick={() => performAction(job.id, "cancel")}><Square className="mr-1 size-4" /> Cancel</Button>
                    </div>
                  </td>
                </tr>
              ))}
              {!simulations.data?.length && (
                <tr><td className="px-4 py-10 text-center text-muted-foreground" colSpan={6}>No simulation jobs yet. Create one above.</td></tr>
              )}
            </tbody>
          </table>
        </CardContent>
      </Card>

      <div className="grid gap-4 md:grid-cols-3">
        <Card className="border-border/60 bg-background/70 backdrop-blur-xl"><CardHeader><CardTitle>Running</CardTitle><CardDescription>Active and queued simulations.</CardDescription></CardHeader><CardContent className="flex items-center gap-3 text-sm"><Timer className="size-5 text-muted-foreground" /> Orchestration is ready to scale.</CardContent></Card>
        <Card className="border-border/60 bg-background/70 backdrop-blur-xl"><CardHeader><CardTitle>Validation</CardTitle><CardDescription>Execution safeguards.</CardDescription></CardHeader><CardContent className="flex items-center gap-3 text-sm"><CheckCircle2 className="size-5 text-emerald-500" /> Lifecycle events are tracked end to end.</CardContent></Card>
        <Card className="border-border/60 bg-background/70 backdrop-blur-xl"><CardHeader><CardTitle>Failures</CardTitle><CardDescription>Failure detection and retry posture.</CardDescription></CardHeader><CardContent className="flex items-center gap-3 text-sm"><CircleSlash className="size-5 text-red-500" /> Failed jobs stay visible for operator review.</CardContent></Card>
      </div>
    </div>
  )
}
