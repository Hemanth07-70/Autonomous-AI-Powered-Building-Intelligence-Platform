"use client"

import { Check, CircleSlash2, Play, Sparkles } from "lucide-react"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

const recommendations = [
  { title: "Pre-cool Tower A", priority: "High", confidence: 94, impact: "-6.2% energy" },
  { title: "Reset AHU schedule", priority: "Medium", confidence: 88, impact: "-3.1% carbon" },
  { title: "Shift occupancy band", priority: "Low", confidence: 81, impact: "+2.4% comfort" },
]

export default function RecommendationsPage() {
  return (
    <div className="space-y-6">
      <div>
        <div className="text-sm uppercase tracking-[0.22em] text-muted-foreground">Recommendations</div>
        <h1 className="text-3xl font-semibold tracking-tight">Recommendation Center</h1>
      </div>
      <div className="grid gap-4 md:grid-cols-3">
        {recommendations.map((item) => (
          <Card key={item.title} className="border-border/60 bg-background/70 backdrop-blur-xl">
            <CardHeader>
              <div className="flex items-start justify-between gap-3">
                <div>
                  <CardTitle>{item.title}</CardTitle>
                  <CardDescription>{item.impact}</CardDescription>
                </div>
                <Badge variant="secondary" className="rounded-full">{item.priority}</Badge>
              </div>
            </CardHeader>
            <CardContent className="space-y-4 text-sm">
              <div className="rounded-2xl border border-border/60 bg-muted/40 p-4">Confidence {item.confidence}%</div>
              <div className="flex gap-2">
                <Button className="rounded-full"><Check className="mr-2 size-4" /> Accept</Button>
                <Button variant="outline" className="rounded-full"><CircleSlash2 className="mr-2 size-4" /> Reject</Button>
                <Button variant="ghost" className="rounded-full"><Play className="mr-2 size-4" /> Execute</Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
      <Card className="border-border/60 bg-background/70 backdrop-blur-xl">
        <CardHeader><CardTitle><Sparkles className="mr-2 inline-block size-5" />Impact forecast</CardTitle><CardDescription>Portfolio-wide outcome projection.</CardDescription></CardHeader>
        <CardContent className="grid gap-4 md:grid-cols-3"><div className="rounded-2xl border border-border/60 bg-muted/40 p-4">Energy savings<br /><span className="text-2xl font-semibold">-8.4%</span></div><div className="rounded-2xl border border-border/60 bg-muted/40 p-4">Carbon reduction<br /><span className="text-2xl font-semibold">-6.9%</span></div><div className="rounded-2xl border border-border/60 bg-muted/40 p-4">Comfort gain<br /><span className="text-2xl font-semibold">+4.2%</span></div></CardContent>
      </Card>
    </div>
  )
}
