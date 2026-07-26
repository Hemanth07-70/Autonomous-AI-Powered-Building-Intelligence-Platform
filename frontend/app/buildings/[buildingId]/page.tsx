"use client"

import { useParams } from "next/navigation"
import { Activity, Database, Droplets, Flame, ThermometerSun, Wind } from "lucide-react"

import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

const sections = ["Overview", "Sensors", "Energy", "Comfort", "Occupancy", "HVAC", "History", "Information"]

const metrics = [
  { label: "Floor Area", value: "1.2M sq ft", icon: Database },
  { label: "Energy Score", value: "91", icon: Flame },
  { label: "Comfort Score", value: "94", icon: ThermometerSun },
  { label: "Occupancy", value: "76%", icon: Activity },
  { label: "Humidity", value: "48%", icon: Droplets },
  { label: "Airflow", value: "2.6 m/s", icon: Wind },
]

export default function BuildingDetailsPage() {
  const params = useParams<{ buildingId: string }>()
  const buildingId = params.buildingId

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <div className="text-sm uppercase tracking-[0.22em] text-muted-foreground">Building details</div>
          <h1 className="text-3xl font-semibold tracking-tight">{buildingId.replace(/-/g, " ").toUpperCase()}</h1>
          <p className="mt-2 max-w-3xl text-muted-foreground">Operational record for the selected building with data grouped by enterprise control domains.</p>
        </div>
        <Badge variant="secondary" className="rounded-full px-3 py-1">Digital twin synced</Badge>
      </div>

      <Card className="border-border/60 bg-background/70 backdrop-blur-xl">
        <CardHeader>
          <CardTitle>Building Overview</CardTitle>
          <CardDescription>Backend information and operational state for the active site.</CardDescription>
        </CardHeader>
        <CardContent className="grid gap-3 md:grid-cols-3 xl:grid-cols-6">
          {metrics.map((metric) => (
            <div key={metric.label} className="rounded-2xl border border-border/60 bg-muted/40 p-4">
              <metric.icon className="size-4 text-muted-foreground" />
              <div className="mt-3 text-sm text-muted-foreground">{metric.label}</div>
              <div className="text-lg font-semibold">{metric.value}</div>
            </div>
          ))}
        </CardContent>
      </Card>

      <Tabs defaultValue="Overview" className="space-y-4">
        <TabsList className="flex w-full flex-wrap gap-2 rounded-2xl bg-background/70 p-2">
          {sections.map((section) => <TabsTrigger key={section} value={section} className="rounded-xl px-4 py-2">{section}</TabsTrigger>)}
        </TabsList>
        {sections.map((section) => (
          <TabsContent key={section} value={section}>
            <Card className="border-border/60 bg-background/70 backdrop-blur-xl">
              <CardHeader>
                <CardTitle>{section}</CardTitle>
                <CardDescription>Operational detail for {buildingId}.</CardDescription>
              </CardHeader>
              <CardContent className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
                {Array.from({ length: 4 }).map((_, index) => (
                  <div key={index} className="rounded-2xl border border-border/60 bg-muted/40 p-4">
                    <div className="text-sm text-muted-foreground">{section} signal {index + 1}</div>
                    <div className="mt-2 font-medium">Stable and within operating band</div>
                  </div>
                ))}
              </CardContent>
            </Card>
          </TabsContent>
        ))}
      </Tabs>
    </div>
  )
}
