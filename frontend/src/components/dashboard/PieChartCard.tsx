import React from 'react'
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from 'recharts'
import Card from '../common/Card'

const COLORS = ['#1487f0', '#0d9488', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899']

export default function PieChartCard({
  title, data,
}: { title: string; data: { label: string; value: number }[] }) {
  return (
    <Card>
      <h3 className="font-semibold mb-4">{title}</h3>
      <ResponsiveContainer width="100%" height={240}>
        <PieChart>
          <Pie data={data} dataKey="value" nameKey="label" outerRadius={80} label>
            {data.map((_, i) => (
              <Cell key={i} fill={COLORS[i % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </Card>
  )
}
