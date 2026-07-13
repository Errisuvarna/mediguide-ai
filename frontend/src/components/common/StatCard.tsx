import React from 'react'
import Card from './Card'

interface StatCardProps {
  label: string
  value: string | number
  icon?: string
  accent?: string
}

export default function StatCard({ label, value, icon, accent = 'text-primary-600' }: StatCardProps) {
  return (
    <Card className="flex items-center gap-4">
      {icon && <div className={`text-3xl ${accent}`}>{icon}</div>}
      <div>
        <div className="text-2xl font-bold">{value}</div>
        <div className="text-sm text-gray-500 dark:text-gray-400">{label}</div>
      </div>
    </Card>
  )
}
