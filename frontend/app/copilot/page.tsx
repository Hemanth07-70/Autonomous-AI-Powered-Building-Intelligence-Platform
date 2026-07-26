"use client"

import * as React from "react"
import { z } from "zod"
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { Bot, Code2, Copy, Loader2, SendHorizonal, Sparkles } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Textarea } from "@/components/ui/textarea"
import { useAiChatMutation } from "@/hooks/use-backend-queries"
import { useAppStore } from "@/store/app-store"
import type { CopilotMessage } from "@/store/app-store"

const promptSchema = z.object({
  message: z.string().min(2, "Enter a prompt for the copilot"),
  buildingId: z.string().optional(),
})

type PromptForm = z.infer<typeof promptSchema>

function MarkdownBlock({ text }: { text: string }) {
  const blocks = React.useMemo(() => text.split(/```/g), [text])
  return (
    <div className="space-y-4 text-sm leading-6 text-foreground">
      {blocks.map((block, index) =>
        index % 2 === 1 ? (
          <pre key={index} className="overflow-x-auto rounded-xl border border-border/60 bg-muted/70 p-4 text-xs"><code>{block}</code></pre>
        ) : (
          <p key={index} className="whitespace-pre-wrap">{block.trim()}</p>
        )
      )}
    </div>
  )
}

export default function CopilotPage() {
  const messages = useAppStore((state) => state.copilotMessages)
  const addMessage = useAppStore((state) => state.addCopilotMessage)
  const [streamedText, setStreamedText] = React.useState<string>("")
  const [streaming, setStreaming] = React.useState(false)
  const selectedBuildingId = useAppStore((state) => state.selectedBuildingId)
  const chat = useAiChatMutation()

  const form = useForm<PromptForm>({
    resolver: zodResolver(promptSchema),
    defaultValues: {
      message: "Optimize HVAC scheduling for Tower A to reduce energy while preserving comfort.",
      buildingId: selectedBuildingId ?? "tower-a",
    },
  })

  React.useEffect(() => {
    form.setValue("buildingId", selectedBuildingId ?? "")
  }, [form, selectedBuildingId])

  async function onSubmit(values: PromptForm) {
    addMessage({ role: "user", content: values.message })
    const response = await chat.mutateAsync({
      message: values.message,
      building_id: values.buildingId || selectedBuildingId || undefined,
    })
    const nextMessage: CopilotMessage = {
      role: "assistant",
      content: response.response,
      goal: response.decision_goal,
    }
    addMessage(nextMessage)
    setStreamedText("")
    setStreaming(true)
    const chunks = response.response.split(/\s+/)
    let index = 0
    const timer = window.setInterval(() => {
      index += 1
      setStreamedText(chunks.slice(0, index).join(" "))
      if (index >= chunks.length) {
        window.clearInterval(timer)
        setStreaming(false)
      }
    }, 18)
  }

  const latestAssistant = [...messages].reverse().find((message) => message.role === "assistant")

  return (
    <div className="grid gap-4 lg:grid-cols-[1.1fr_0.9fr]">
      <Card className="border-border/60 bg-background/70 backdrop-blur-xl">
        <CardHeader>
          <div className="flex items-center gap-3">
            <div className="flex size-10 items-center justify-center rounded-2xl bg-foreground text-background"><Bot className="size-5" /></div>
            <div>
              <CardTitle>AI Copilot</CardTitle>
              <CardDescription>Decision-making assistant with structured outputs from the backend AI planner.</CardDescription>
            </div>
          </div>
          <div className="pt-2">
            <Badge variant="secondary" className="rounded-full px-3 py-1">
              {selectedBuildingId ? `Connected to twin building: ${selectedBuildingId}` : "No twin building selected"}
            </Badge>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-3 rounded-2xl border border-border/60 bg-muted/30 p-4">
            {messages.map((message, index) => (
              <div key={`${message.role}-${index}`} className={`rounded-2xl p-4 ${message.role === "user" ? "ml-auto max-w-[80%] bg-foreground text-background" : "bg-background/70"}`}>
                {message.role === "assistant" ? <MarkdownBlock text={index === messages.length - 1 && streaming ? streamedText || message.content : message.content} /> : <div className="whitespace-pre-wrap text-sm leading-6">{message.content}</div>}
              </div>
            ))}
          </div>

          <form
            className="space-y-3 rounded-2xl border border-border/60 bg-background/80 p-4"
            onSubmit={form.handleSubmit(onSubmit)}
          >
            <div className="grid gap-3 md:grid-cols-[1fr_220px]">
              <Textarea
                rows={4}
                className="min-h-28 rounded-2xl"
                placeholder="Ask the copilot to optimize energy, generate a decision goal, or build a simulation plan..."
                {...form.register("message")}
              />
              <Input
                placeholder="Building ID"
                className="h-12 rounded-2xl"
                {...form.register("buildingId")}
              />
            </div>
            <div className="flex items-center justify-between gap-3">
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <Sparkles className="size-4" />
                {chat.isPending || streaming ? "Streaming response from AI backend" : "Ready for a new operating request"}
              </div>
              <Button type="submit" className="rounded-full px-5" disabled={chat.isPending}>
                {chat.isPending ? <Loader2 className="mr-2 size-4 animate-spin" /> : <SendHorizonal className="mr-2 size-4" />}
                Submit
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>

      <div className="space-y-4">
        <Card className="border-border/60 bg-background/70 backdrop-blur-xl">
          <CardHeader>
            <CardTitle>Decision Goal</CardTitle>
            <CardDescription>The structured objective returned by the backend after each prompt.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <Badge variant="secondary" className="rounded-full px-3 py-1">{latestAssistant?.goal?.goal_type ?? "Awaiting prompt"}</Badge>
            <div className="grid grid-cols-2 gap-3 text-sm">
              <div className="rounded-xl border border-border/60 bg-muted/40 p-3"><div className="text-muted-foreground">Priority</div><div className="font-medium">{latestAssistant?.goal?.priority ?? "-"}</div></div>
              <div className="rounded-xl border border-border/60 bg-muted/40 p-3"><div className="text-muted-foreground">Building</div><div className="font-medium">{latestAssistant?.goal?.building_id ?? "-"}</div></div>
              <div className="rounded-xl border border-border/60 bg-muted/40 p-3"><div className="text-muted-foreground">Created</div><div className="font-medium">{latestAssistant?.goal?.created_at ? new Date(latestAssistant.goal.created_at).toLocaleString() : "-"}</div></div>
              <div className="rounded-xl border border-border/60 bg-muted/40 p-3"><div className="text-muted-foreground">Status</div><div className="font-medium">Structured</div></div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-border/60 bg-background/70 backdrop-blur-xl">
          <CardHeader>
            <CardTitle>Execution Plan</CardTitle>
            <CardDescription>Backend response used to orchestrate downstream simulation jobs.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3 text-sm">
            <div className="rounded-xl border border-border/60 bg-muted/40 p-3"><div className="text-muted-foreground">Decision Goal</div><div className="font-medium">Generate AI optimization goal</div></div>
            <div className="rounded-xl border border-border/60 bg-muted/40 p-3"><div className="text-muted-foreground">Expected Savings</div><div className="font-medium">Projected 7-12% energy reduction</div></div>
            <div className="rounded-xl border border-border/60 bg-muted/40 p-3"><div className="text-muted-foreground">Estimated Runtime</div><div className="font-medium">18-24 minutes</div></div>
            <div className="rounded-xl border border-border/60 bg-muted/40 p-3"><div className="text-muted-foreground">Recommendations</div><div className="font-medium">Pre-cool early, shift setpoints, run validation simulation</div></div>
          </CardContent>
        </Card>

        <Card className="border-border/60 bg-background/70 backdrop-blur-xl">
          <CardHeader>
            <CardTitle>Conversation Utilities</CardTitle>
            <CardDescription>Enterprise features designed for operators and engineers.</CardDescription>
          </CardHeader>
          <CardContent className="grid grid-cols-2 gap-3">
            <Button variant="outline" className="justify-start rounded-2xl"><Code2 className="mr-2 size-4" /> Code snippets</Button>
            <Button variant="outline" className="justify-start rounded-2xl"><Copy className="mr-2 size-4" /> Copy output</Button>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
