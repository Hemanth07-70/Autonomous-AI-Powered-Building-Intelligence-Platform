"use client"

import Link from "next/link"
import { useAppStore } from "@/store/app-store"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Building2, ChevronRight, Database, Leaf, ShieldCheck, ThermometerSnowflake } from "lucide-react"

const buildings = [
  { id: "tower-a", name: "Tower A", status: "Optimal", energy: 91, comfort: 94, carbon: 88, occupancy: "76%", twin: "Synced" },
  { id: "campus-west", name: "Campus West", status: "Attention", energy: 83, comfort: 89, carbon: 86, occupancy: "61%", twin: "Synced" },
  { id: "hq-east", name: "HQ East", status: "Healthy", energy: 96, comfort: 92, carbon: 95, occupancy: "84%", twin: "Calibrating" },
  { id: "lab-north", name: "Lab North", status: "Stable", energy: 90, comfort: 97, carbon: 82, occupancy: "44%", twin: "Synced" },
]

export default function BuildingsPage() {
  const setSelectedBuildingId = useAppStore((state) => state.setSelectedBuildingId)

  return (
    <div className="space-y-6">
      <div className="flex items-end justify-between gap-4">
        <div>
          <div className="text-sm uppercase tracking-[0.22em] text-muted-foreground">Portfolio</div>
          <h1 className="text-3xl font-semibold tracking-tight">Buildings</h1>
          <p className="mt-2 max-w-2xl text-muted-foreground">Portfolio command view for enterprise buildings with operational scores and digital twin synchronization.</p>
        </div>
        <Badge variant="secondary" className="rounded-full px-3 py-1">4 buildings online</Badge>
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {buildings.map((building) => (
          <Card key={building.id} className="border-border/60 bg-background/70 backdrop-blur-xl">
            <CardHeader>
              <div className="flex items-start justify-between gap-4">
                <div>
                  <CardTitle className="flex items-center gap-2"><Building2 className="size-5" />{building.name}</CardTitle>
                  <CardDescription>{building.id}</CardDescription>
                </div>
                <Badge variant={building.status === "Attention" ? "destructive" : "secondary"} className="rounded-full">{building.status}</Badge>
              </div>
            </CardHeader>
            <CardContent className="space-y-4 text-sm">
              <div className="grid grid-cols-2 gap-3">
                <div className="rounded-xl border border-border/60 bg-muted/40 p-3"><div className="text-muted-foreground">Energy</div><div className="text-lg font-semibold">{building.energy}</div></div>
                <div className="rounded-xl border border-border/60 bg-muted/40 p-3"><div className="text-muted-foreground">Comfort</div><div className="text-lg font-semibold">{building.comfort}</div></div>
                <div className="rounded-xl border border-border/60 bg-muted/40 p-3"><div className="text-muted-foreground">Carbon</div><div className="text-lg font-semibold">{building.carbon}</div></div>
                <div className="rounded-xl border border-border/60 bg-muted/40 p-3"><div className="text-muted-foreground">Occupancy</div><div className="text-lg font-semibold">{building.occupancy}</div></div>
              </div>
              <div className="flex items-center justify-between rounded-xl border border-border/60 bg-muted/40 px-3 py-2">
                <span>Digital twin</span><span className="font-medium">{building.twin}</span>
              </div>
              <Button variant="outline" className="w-full justify-between rounded-xl" onClick={() => setSelectedBuildingId(building.id)} render={
                <Link href={`/buildings/${building.id}`}>
                  Open details
                  <ChevronRight className="size-4" />
                </Link>
              } />
            </CardContent>
          </Card>
        ))}
      </div>

      <Card className="border-border/60 bg-background/70 backdrop-blur-xl">
        <CardHeader>
          <CardTitle>Portfolio Snapshot</CardTitle>
          <CardDescription>Enterprise KPIs at a glance across all connected buildings.</CardDescription>
        </CardHeader>
        <CardContent className="grid gap-4 md:grid-cols-4">
          <div className="rounded-2xl border border-border/60 bg-muted/40 p-4"><ThermometerSnowflake className="size-5" /><div className="mt-3 text-sm text-muted-foreground">Cooling load</div><div className="text-2xl font-semibold">31.4 MW</div></div>
          <div className="rounded-2xl border border-border/60 bg-muted/40 p-4"><Leaf className="size-5" /><div className="mt-3 text-sm text-muted-foreground">Carbon delta</div><div className="text-2xl font-semibold">-8.2%</div></div>
          <div className="rounded-2xl border border-border/60 bg-muted/40 p-4"><ShieldCheck className="size-5" /><div className="mt-3 text-sm text-muted-foreground">Health index</div><div className="text-2xl font-semibold">96.0</div></div>
          <div className="rounded-2xl border border-border/60 bg-muted/40 p-4"><Database className="size-5" /><div className="mt-3 text-sm text-muted-foreground">Twin sync</div><div className="text-2xl font-semibold">100%</div></div>
        </CardContent>
      </Card>
    </div>
  )
}
