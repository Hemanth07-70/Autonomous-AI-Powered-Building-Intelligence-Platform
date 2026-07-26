"use client"

import * as React from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import {
  Bell,
  Bot,
  Building2,
  Command,
  LayoutDashboard,
  Menu,
  MoonStar,
  Search,
  Settings,
  SunMedium,
  Zap,
} from "lucide-react"

import { AppSidebar } from "@/components/layout/app-sidebar"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Separator } from "@/components/ui/separator"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { cn } from "@/lib/utils"
import { useAppStore } from "@/store/app-store"

const navigationItems = [
  { href: "/", label: "Dashboard", icon: LayoutDashboard },
  { href: "/copilot", label: "AI Copilot", icon: Bot },
  { href: "/buildings", label: "Buildings", icon: Building2 },
  { href: "/digital-twin", label: "Digital Twin", icon: Zap },
  { href: "/simulations", label: "Simulation Center", icon: Command },
  { href: "/decisions", label: "Decision Center", icon: Search },
  { href: "/analytics", label: "Analytics", icon: LayoutDashboard },
  { href: "/diagnostics", label: "Diagnostics", icon: Settings },
  { href: "/recommendations", label: "Recommendations", icon: SunMedium },
  { href: "/alerts", label: "Alerts", icon: Bell },
  { href: "/reports", label: "Reports", icon: Menu },
  { href: "/settings", label: "Settings", icon: Settings },
]

function Breadcrumbs() {
  const pathname = usePathname()
  const segments = pathname.split("/").filter(Boolean)
  const items = segments.length ? ["Home", ...segments.map((segment) => segment.replace(/-/g, " "))] : ["Home", "Executive Dashboard"]

  return (
    <div className="flex flex-wrap items-center gap-2 text-sm text-muted-foreground">
      {items.map((item, index) => (
        <React.Fragment key={`${item}-${index}`}>
          {index > 0 ? <span>/</span> : null}
          <span className={cn(index === items.length - 1 && "text-foreground font-medium")}>{item}</span>
        </React.Fragment>
      ))}
    </div>
  )
}

function TopBar() {
  const { setCommandPaletteOpen, notificationsOpen, setNotificationsOpen, theme, setTheme } = useAppStore()
  return (
    <div className="sticky top-0 z-30 border-b border-border/60 bg-background/75 backdrop-blur-xl">
      <div className="flex items-center justify-between gap-4 px-4 py-3 lg:px-6">
        <div className="flex items-center gap-3">
          <SidebarTrigger className="lg:hidden" />
          <div className="hidden md:block">
            <Breadcrumbs />
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" className="hidden h-9 rounded-full px-3 md:inline-flex" onClick={() => setCommandPaletteOpen(true)}>
            <Command className="mr-2 size-4" />
            Search
            <Badge className="ml-3 rounded-md bg-muted px-1.5 py-0.5 text-[10px] font-medium text-muted-foreground">Ctrl K</Badge>
          </Button>
          <Button variant="ghost" size="icon-sm" onClick={() => setCommandPaletteOpen(true)} className="md:hidden">
            <Search className="size-4" />
          </Button>
          <Button variant="ghost" size="icon-sm" onClick={() => setTheme(theme === "dark" ? "light" : "dark")}>
            <MoonStar className="size-4 dark:hidden" />
            <SunMedium className="hidden size-4 dark:block" />
          </Button>
          <Button variant="ghost" size="icon-sm" onClick={() => setNotificationsOpen(!notificationsOpen)}>
            <Bell className="size-4" />
          </Button>
          <DropdownMenu>
            <DropdownMenuTrigger
              render={
                <Button variant="ghost" className="h-9 rounded-full px-2">
                  <Avatar className="size-7">
                    <AvatarFallback>IB</AvatarFallback>
                  </Avatar>
                  <span className="hidden px-2 text-sm font-medium md:inline-flex">Enterprise Ops</span>
                </Button>
              }
            />
            <DropdownMenuContent>
              <DropdownMenuLabel>IntelliBuild AI</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem render={<Link href="/settings">Profile</Link>} />
              <DropdownMenuItem render={<Link href="/settings">Theme</Link>} />
              <DropdownMenuItem render={<Link href="/settings">AI Provider</Link>} />
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </div>
  )
}

function CommandPalette() {
  const open = useAppStore((state) => state.commandPaletteOpen)
  const setOpen = useAppStore((state) => state.setCommandPaletteOpen)
  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogContent className="max-w-2xl border-border/60 bg-popover/95 backdrop-blur-xl">
        <DialogHeader>
          <DialogTitle>Command Palette</DialogTitle>
          <DialogDescription>Navigate the enterprise control center quickly.</DialogDescription>
        </DialogHeader>
        <div className="space-y-3">
          <Input placeholder="Search pages, buildings, simulations, decisions..." className="h-11 rounded-xl" />
          <div className="grid gap-2 md:grid-cols-2">
            {navigationItems.slice(0, 6).map((item) => (
              <Button
                key={item.href}
                variant="outline"
                className="justify-start rounded-xl px-3 py-6"
                render={
                  <Link href={item.href} onClick={() => setOpen(false)}>
                    <item.icon className="mr-3 size-4" />
                    {item.label}
                  </Link>
                }
              />
            ))}
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}

function NotificationDrawer() {
  const open = useAppStore((state) => state.notificationsOpen)
  const setOpen = useAppStore((state) => state.setNotificationsOpen)
  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogContent className="max-w-md border-border/60 bg-popover/95 backdrop-blur-xl">
        <DialogHeader>
          <DialogTitle>Notifications</DialogTitle>
          <DialogDescription>Operational events and AI execution updates.</DialogDescription>
        </DialogHeader>
        <ScrollArea className="h-[28rem] pr-4">
          <div className="space-y-3">
            {[
              { title: "Simulation queued", body: "Energy model for Tower A queued for execution." },
              { title: "AI goal created", body: "Comfort optimization goal generated with 92% confidence." },
              { title: "Alert escalation", body: "AHU-2 vibration anomaly moved to high severity." },
            ].map((item) => (
              <div key={item.title} className="rounded-xl border border-border/60 bg-background/60 p-3">
                <div className="font-medium">{item.title}</div>
                <div className="text-sm text-muted-foreground">{item.body}</div>
              </div>
            ))}
          </div>
        </ScrollArea>
      </DialogContent>
    </Dialog>
  )
}

export function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <TooltipProvider>
      <SidebarProvider>
        <AppSidebar />
        <SidebarInset>
          <TopBar />
          <main className="relative flex-1">
            <div className="absolute inset-0 -z-10 bg-[radial-gradient(circle_at_top_left,rgba(255,255,255,0.08),transparent_30%),radial-gradient(circle_at_top_right,rgba(255,255,255,0.05),transparent_28%)] dark:bg-[radial-gradient(circle_at_top_left,rgba(255,255,255,0.04),transparent_26%),radial-gradient(circle_at_top_right,rgba(255,255,255,0.03),transparent_24%)]" />
            <div className="mx-auto max-w-[1600px] px-4 py-6 lg:px-6">{children}</div>
          </main>
        </SidebarInset>
        <CommandPalette />
        <NotificationDrawer />
      </SidebarProvider>
    </TooltipProvider>
  )
}
