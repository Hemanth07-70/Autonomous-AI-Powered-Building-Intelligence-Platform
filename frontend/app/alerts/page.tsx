"use client"

import { BellRing } from "lucide-react"

import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

const alerts = [
  { severity: "Critical", title: "AHU-2 vibration anomaly", time: "2m ago" },
  { severity: "High", title: "Cooling loop pressure rise", time: "18m ago" },
  { severity: "Medium", title: "Zone 5 occupancy spike", time: "42m ago" },
  { severity: "Low", title: "Daily summary queued", time: "1h ago" },
]

export default function AlertsPage() {
  return (
    <div className="space-y-6">
      <div>
        <div className="text-sm uppercase tracking-[0.22em] text-muted-foreground">Alerts</div>
        <h1 className="text-3xl font-semibold tracking-tight">Real-time Alert Center</h1>
      </div>
      <Card className="border-border/60 bg-background/70 backdrop-blur-xl">
        <CardHeader><CardTitle><BellRing className="mr-2 inline-block size-5" />Timeline</CardTitle><CardDescription>Operational incident stream with severity prioritization.</CardDescription></CardHeader>
        <CardContent className="space-y-4">
          {alerts.map((item) => (
            <div key={item.title} className="flex items-center justify-between rounded-2xl border border-border/60 bg-muted/40 px-4 py-3">
              <div>
                <div className="font-medium">{item.title}</div>
                <div className="text-sm text-muted-foreground">{item.time}</div>
              </div>
              <Badge variant={item.severity === "Critical" ? "destructive" : "secondary"} className="rounded-full">{item.severity}</Badge>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  )
}
