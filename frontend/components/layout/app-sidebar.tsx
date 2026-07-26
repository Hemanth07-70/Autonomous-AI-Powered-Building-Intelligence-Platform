"use client"

import * as React from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import {
  Activity,
  AlertTriangle,
  BarChart3,
  Bot,
  Building2,
  FileText,
  Home,
  LayoutDashboard,
  Settings,
  Target,
  Zap
} from "lucide-react"

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
} from "@/components/ui/sidebar"

const navigation = [
  { name: "Dashboard", href: "/", icon: LayoutDashboard },
  { name: "AI Copilot", href: "/copilot", icon: Bot },
  { name: "Buildings", href: "/buildings", icon: Building2 },
  { name: "Digital Twin", href: "/digital-twin", icon: Activity },
  { name: "Simulation Center", href: "/simulations", icon: Zap },
  { name: "Decision Center", href: "/decisions", icon: Target },
  { name: "Analytics", href: "/analytics", icon: BarChart3 },
  { name: "Diagnostics", href: "/diagnostics", icon: AlertTriangle },
  { name: "Recommendations", href: "/recommendations", icon: Home },
  { name: "Alerts", href: "/alerts", icon: AlertTriangle },
  { name: "Reports", href: "/reports", icon: FileText },
  { name: "Settings", href: "/settings", icon: Settings },
]

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  const pathname = usePathname()

  return (
    <Sidebar collapsible="icon" {...props} className="border-r border-border/50 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <SidebarHeader className="h-16 flex items-center justify-center border-b border-border/50">
        <div className="flex items-center gap-2 px-2 font-semibold text-lg tracking-tight">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
            <Building2 className="h-5 w-5" />
          </div>
          <span className="group-data-[collapsible=icon]:hidden">IntelliBuild OS</span>
        </div>
      </SidebarHeader>
      <SidebarContent className="px-2 py-4">
        <SidebarMenu>
          {navigation.map((item) => {
            const isActive = pathname === item.href || (pathname.startsWith(item.href + "/") && item.href !== "/")
            return (
              <SidebarMenuItem key={item.name}>
                <SidebarMenuButton
                  isActive={isActive}
                  tooltip={item.name}
                  render={
                    <Link href={item.href} className="flex items-center gap-3 transition-colors">
                      <item.icon className="h-4 w-4" />
                      <span>{item.name}</span>
                    </Link>
                  }
                />
              </SidebarMenuItem>
            )
          })}
        </SidebarMenu>
      </SidebarContent>
      <SidebarFooter className="border-t border-border/50 p-4">
        <div className="group-data-[collapsible=icon]:hidden text-xs text-muted-foreground text-center">
          IntelliBuild AI v1.0
        </div>
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  )
}
