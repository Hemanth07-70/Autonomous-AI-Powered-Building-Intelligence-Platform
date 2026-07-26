import "./globals.css"
import type { Metadata } from "next"
import { Inter, IBM_Plex_Mono } from "next/font/google"
import { AppShell } from "@/components/layout/app-shell"
import { Providers } from "@/components/providers"

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-sans",
})

const ibmPlexMono = IBM_Plex_Mono({
  subsets: ["latin"],
  variable: "--font-geist-mono",
  weight: ["400", "500", "600"],
})

export const metadata: Metadata = {
  title: "IntelliBuild AI",
  description: "Enterprise AI-powered Building Management Platform",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head />
      <body className={`${inter.variable} ${ibmPlexMono.variable} bg-background text-foreground min-h-screen antialiased`}>
        <Providers>
            <AppShell>{children}</AppShell>
        </Providers>
      </body>
    </html>
  );
}
