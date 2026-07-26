"use client"

import React from "react"
import ReactECharts from "echarts-for-react"
import { Filter, LineChart, PieChart } from "lucide-react"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

const option = {
  grid: { left: 35, right: 20, top: 20, bottom: 30 },
  xAxis: { type: "category", data: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"] },
  yAxis: { type: "value" },
  series: [
    { name: "Energy", data: [82, 79, 80, 76, 74, 72, 69], type: "line", smooth: true },
    { name: "Carbon", data: [56, 54, 52, 49, 47, 45, 42], type: "line", smooth: true },
  ],
  tooltip: { trigger: "axis" },
}

export default function AnalyticsPage() {
  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <div className="text-sm uppercase tracking-[0.22em] text-muted-foreground">Analytics</div>
          <h1 className="text-3xl font-semibold tracking-tight">Operational Analytics</h1>
        </div>
        <Button variant="outline" className="rounded-full"><Filter className="mr-2 size-4" /> Filters</Button>
      </div>
      <div className="grid gap-4 xl:grid-cols-2">
        <Card className="border-border/60 bg-background/70 backdrop-blur-xl"><CardHeader><CardTitle>Energy / Carbon</CardTitle><CardDescription>Weekly trend analysis.</CardDescription></CardHeader><CardContent className="h-80"><ReactECharts option={option} style={{ width: "100%", height: "100%" }} /></CardContent></Card>
        <Card className="border-border/60 bg-background/70 backdrop-blur-xl"><CardHeader><CardTitle>Portfolio Mix</CardTitle><CardDescription>Efficiency and consumption segmentation.</CardDescription></CardHeader><CardContent className="grid gap-4 md:grid-cols-2"><div className="rounded-2xl border border-border/60 bg-muted/40 p-4"><LineChart className="size-5" /><div className="mt-3 text-sm text-muted-foreground">Efficiency</div><div className="text-2xl font-semibold">91.4%</div></div><div className="rounded-2xl border border-border/60 bg-muted/40 p-4"><PieChart className="size-5" /><div className="mt-3 text-sm text-muted-foreground">Peak demand</div><div className="text-2xl font-semibold">4.6 MW</div></div></CardContent></Card>
      </div>
      <div className="flex flex-wrap gap-2"><Badge variant="secondary" className="rounded-full">Energy</Badge><Badge variant="secondary" className="rounded-full">Carbon</Badge><Badge variant="secondary" className="rounded-full">Cost</Badge><Badge variant="secondary" className="rounded-full">Comfort</Badge><Badge variant="secondary" className="rounded-full">Occupancy</Badge><Badge variant="secondary" className="rounded-full">HVAC</Badge></div>
    </div>
  )
}
