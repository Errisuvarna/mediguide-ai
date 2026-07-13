import React, { useEffect, useState } from 'react'
import api from '../api/client'
import { DashboardData } from '../types'
import { useLanguage } from '../i18n'
import StatCard from '../components/common/StatCard'
import BarChartCard from '../components/dashboard/BarChartCard'
import LineChartCard from '../components/dashboard/LineChartCard'
import PieChartCard from '../components/dashboard/PieChartCard'
import RecentQueriesTable from '../components/dashboard/RecentQueriesTable'
import LoadingSpinner from '../components/common/LoadingSpinner'

export default function Dashboard() {
  const { t } = useLanguage()
  const [data, setData] = useState<DashboardData | null>(null)

  useEffect(() => {
    const load = () => api.get<DashboardData>('/analytics').then((r) => setData(r.data))
    load()
    const interval = setInterval(load, 15000) // live refresh every 15s
    return () => clearInterval(interval)
  }, [])

  if (!data) return <LoadingSpinner label="Loading dashboard..." />

  const s = data.summary
  const c = data.charts

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">{t('dashboard')}</h1>

      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard label="Total Queries" value={s.total_queries} icon="💬" />
        <StatCard label="Today's Queries" value={s.today_queries} icon="📅" />
        <StatCard label="Weekly Queries" value={s.weekly_queries} icon="📈" />
        <StatCard label="Monthly Queries" value={s.monthly_queries} icon="🗓️" />
        <StatCard label="Emergency Queries" value={s.emergency_queries} icon="🚨" accent="text-red-500" />
        <StatCard label="Avg Response Time" value={`${s.avg_response_time_ms} ms`} icon="⚡" />
        <StatCard label="Feedback Score" value={`${s.feedback_score} / 5`} icon="⭐" />
        <StatCard label="Patient Satisfaction" value={`${s.patient_satisfaction_pct}%`} icon="😊" />
      </div>

      <div className="grid lg:grid-cols-2 gap-5 mb-5">
        <BarChartCard title="Department-wise Queries" data={c.department_wise_queries} />
        <PieChartCard title="Popular Services" data={c.popular_services} />
      </div>

      <div className="grid lg:grid-cols-3 gap-5 mb-5">
        <LineChartCard title="Daily Trend (7d)" data={c.daily_trend} />
        <LineChartCard title="Weekly Trend (4w)" data={c.weekly_trend} color="#1487f0" />
        <LineChartCard title="Monthly Trend (6mo)" data={c.monthly_trend} color="#f59e0b" />
      </div>

      <div className="grid lg:grid-cols-3 gap-5 mb-5">
        <BarChartCard title="Most Asked Questions" data={c.most_asked_questions} color="#8b5cf6" />
        <PieChartCard title="Voice vs Text Usage" data={c.voice_usage} />
        <PieChartCard title="Language Usage" data={c.language_usage} />
      </div>

      <div className="grid lg:grid-cols-1 gap-5 mb-5">
        <BarChartCard title="Unanswered Questions" data={c.unanswered_questions} color="#ef4444" />
      </div>

      <RecentQueriesTable rows={data.recent_queries} />
    </div>
  )
}
