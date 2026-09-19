import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import Link from 'next/link'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Synapse AI ERP',
  description: 'Next-Gen AI Supply Chain & Demand Forecasting Studio',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-gray-50 dark:bg-zinc-950 text-gray-900 dark:text-zinc-50 antialiased`}>
        <div className="max-w-7xl mx-auto min-h-screen flex flex-col p-8">
          
          <header className="flex justify-between items-end border-b border-gray-200 dark:border-zinc-800 pb-4 mb-8">
            <div>
              <h1 className="text-3xl font-bold tracking-tight">SYNAPSE AI ERP</h1>
              <p className="text-gray-500 dark:text-zinc-400 mt-1">Intelligence Control Center</p>
            </div>
            <nav className="flex gap-4">
              <Link href="/" className="px-4 py-2 bg-white dark:bg-zinc-900 border border-gray-200 dark:border-zinc-800 rounded text-sm hover:bg-gray-100 dark:hover:bg-zinc-800 transition-colors font-medium">Dashboard</Link>
              <Link href="/inventory" className="px-4 py-2 text-gray-500 dark:text-zinc-400 hover:text-gray-900 dark:hover:text-zinc-50 text-sm font-medium transition-colors">Inventory</Link>
              <Link href="/forecast" className="px-4 py-2 text-gray-500 dark:text-zinc-400 hover:text-gray-900 dark:hover:text-zinc-50 text-sm font-medium transition-colors">Forecast</Link>
              <Link href="/suppliers" className="px-4 py-2 text-gray-500 dark:text-zinc-400 hover:text-gray-900 dark:hover:text-zinc-50 text-sm font-medium transition-colors">Suppliers</Link>
              <Link href="/simulation" className="px-4 py-2 text-gray-500 dark:text-zinc-400 hover:text-gray-900 dark:hover:text-zinc-50 text-sm font-medium transition-colors">Simulation</Link>
            </nav>
          </header>

          <main className="flex-1">
            {children}
          </main>
          
        </div>
      </body>
    </html>
  )
}
