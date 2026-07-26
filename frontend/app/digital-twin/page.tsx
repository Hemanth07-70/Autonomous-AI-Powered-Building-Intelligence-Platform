"use client"

import { Cpu, Layers3, Radar, ThermometerSun, Wind } from "lucide-react"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

const zones = ["Building", "Floors", "Zones", "Sensors", "HVAC", "Occupancy", "Temperature"]

export default function DigitalTwinPage() {
  return (
    <div className="space-y-6">
      <div>
        <div className="text-sm uppercase tracking-[0.22em] text-muted-foreground">Digital twin</div>
        <h1 className="text-3xl font-semibold tracking-tight">Spatial Operations View</h1>
      </div>
      <Card className="border-border/60 bg-background/70 backdrop-blur-xl">
        <CardHeader>
          <CardTitle>Future 3D-ready architecture</CardTitle>
          <CardDescription>Prepared for immersive building visualization and sensor overlays.</CardDescription>
        </CardHeader>
        <CardContent className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {zones.map((zone) => (
            <div key={zone} className="rounded-2xl border border-border/60 bg-muted/40 p-4">
              <div className="flex items-center gap-2 text-sm text-muted-foreground"><Radar className="size-4" /> {zone}</div>
              <div className="mt-3 font-medium">Live synchronization enabled</div>
            </div>
          ))}
        </CardContent>
      </Card>
      <div className="grid gap-4 md:grid-cols-3">
        <Card className="border-border/60 bg-background/70 backdrop-blur-xl"><CardHeader><CardTitle><Cpu className="size-5 inline-block mr-2" />Building</CardTitle></CardHeader><CardContent>Hierarchy and site context.</CardContent></Card>
        <Card className="border-border/60 bg-background/70 backdrop-blur-xl"><CardHeader><CardTitle><Layers3 className="size-5 inline-block mr-2" />Floors</CardTitle></CardHeader><CardContent>Floor-level zoning and telemetry.</CardContent></Card>
        <Card className="border-border/60 bg-background/70 backdrop-blur-xl"><CardHeader><CardTitle><ThermometerSun className="size-5 inline-block mr-2" />Sensors</CardTitle></CardHeader><CardContent><div className="flex items-center gap-2"><Wind className="size-4" /> Occupancy and airflow probes.</div></CardContent></Card>
      </div>
    </div>
  )
}
