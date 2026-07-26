"use client"

import { SlidersHorizontal, Users } from "lucide-react"

import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

const sections = ["Profile", "Buildings", "Users", "Notifications", "Theme", "AI Provider", "Simulation Settings"]

export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <div>
        <div className="text-sm uppercase tracking-[0.22em] text-muted-foreground">Settings</div>
        <h1 className="text-3xl font-semibold tracking-tight">System Settings</h1>
      </div>
      <Card className="border-border/60 bg-background/70 backdrop-blur-xl">
        <CardHeader><CardTitle><SlidersHorizontal className="mr-2 inline-block size-5" />Configuration</CardTitle><CardDescription>Enterprise control surface for platform preferences and operational policies.</CardDescription></CardHeader>
        <CardContent className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
          {sections.map((section) => <div key={section} className="rounded-2xl border border-border/60 bg-muted/40 p-4"><div className="font-medium">{section}</div><div className="text-sm text-muted-foreground">Managed through the application shell and backend APIs.</div></div>)}
        </CardContent>
      </Card>
      <Badge variant="secondary" className="rounded-full px-3 py-1"><Users className="mr-2 size-4" /> Role-aware access and profile management ready</Badge>
    </div>
  )
}
