"use client"

import { FileDown, FileText } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export default function ReportsPage() {
  return (
    <div className="space-y-6">
      <div>
        <div className="text-sm uppercase tracking-[0.22em] text-muted-foreground">Reports</div>
        <h1 className="text-3xl font-semibold tracking-tight">Reporting and Export</h1>
      </div>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {[
          "Daily",
          "Weekly",
          "Monthly",
          "Energy Audit",
          "Sustainability",
        ].map((report) => (
          <Card key={report} className="border-border/60 bg-background/70 backdrop-blur-xl">
            <CardHeader><CardTitle className="flex items-center gap-2"><FileText className="size-5" />{report}</CardTitle><CardDescription>Prepared report template for enterprise export.</CardDescription></CardHeader>
            <CardContent className="flex gap-2"><Button className="rounded-full"><FileDown className="mr-2 size-4" /> PDF</Button><Button variant="outline" className="rounded-full">CSV</Button></CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
