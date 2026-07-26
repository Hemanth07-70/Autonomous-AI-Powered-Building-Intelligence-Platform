"use client"

import { Search, ShieldAlert } from "lucide-react"

import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"

const diagnostics = [
  { severity: "Critical", label: "AHU-2 vibration anomaly", detail: "Escalated to engineering review" },
  { severity: "High", label: "Chiller setpoint drift", detail: "Operating above target band" },
  { severity: "Medium", label: "Zone sensor latency", detail: "Pending recalibration" },
  { severity: "Low", label: "Trend cache refresh", detail: "No operator action required" },
]

export default function DiagnosticsPage() {
  return (
    <div className="space-y-6">
      <div>
        <div className="text-sm uppercase tracking-[0.22em] text-muted-foreground">Diagnostics</div>
        <h1 className="text-3xl font-semibold tracking-tight">Diagnostics Center</h1>
      </div>
      <Card className="border-border/60 bg-background/70 backdrop-blur-xl">
        <CardContent className="pt-6">
          <div className="relative max-w-lg">
            <Search className="pointer-events-none absolute top-3 left-3 size-4 text-muted-foreground" />
            <Input className="h-12 rounded-2xl pl-9" placeholder="Search diagnostics, sensors, or anomalies" />
          </div>
        </CardContent>
      </Card>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {diagnostics.map((item) => (
          <Card key={item.label} className="border-border/60 bg-background/70 backdrop-blur-xl">
            <CardHeader>
              <div className="flex items-center justify-between gap-3">
                <CardTitle>{item.label}</CardTitle>
                <Badge variant={item.severity === "Critical" ? "destructive" : "secondary"} className="rounded-full">{item.severity}</Badge>
              </div>
              <CardDescription>{item.detail}</CardDescription>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground"><ShieldAlert className="size-4 inline-block mr-2" /> Severity trace is available for audit logging.</CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
