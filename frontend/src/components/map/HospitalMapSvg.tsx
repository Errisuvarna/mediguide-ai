import React, { useState } from 'react'
import { MapPoint } from '../../types'

const CATEGORY_COLORS: Record<string, string> = {
  Entrance: '#1487f0', Reception: '#0d9488', Department: '#8b5cf6',
  Lab: '#f59e0b', Pharmacy: '#ec4899', Emergency: '#ef4444',
  Parking: '#64748b', Cafeteria: '#22c55e', ATM: '#eab308', 'Billing Counter': '#06b6d4',
}

export default function HospitalMapSvg({ points }: { points: MapPoint[] }) {
  const [active, setActive] = useState<MapPoint | null>(null)

  return (
    <div className="relative">
      <svg viewBox="0 0 100 100" className="w-full h-[420px] bg-gray-50 dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-800">
        <rect x="2" y="2" width="96" height="96" fill="none" stroke="currentColor" strokeOpacity="0.15" strokeWidth="0.5" rx="2" />
        {points.map((p) => (
          <g key={p.id} onClick={() => setActive(p)} className="cursor-pointer">
            <circle
              cx={p.x_coordinate} cy={p.y_coordinate} r={active?.id === p.id ? 2.4 : 1.6}
              fill={CATEGORY_COLORS[p.category ?? ''] ?? '#1487f0'}
              stroke="white" strokeWidth="0.3"
            />
          </g>
        ))}
      </svg>

      {active && (
        <div className="absolute bottom-3 left-3 right-3 bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 border border-gray-100 dark:border-gray-700">
          <div className="flex justify-between items-start">
            <div>
              <div className="font-semibold">{active.name}</div>
              <div className="text-sm text-gray-500 dark:text-gray-400">
                {active.building_name} · Floor {active.floor_number} · {active.category}
              </div>
              {active.description && <div className="text-sm mt-1">{active.description}</div>}
            </div>
            <button onClick={() => setActive(null)} className="text-gray-400 hover:text-gray-700">✕</button>
          </div>
        </div>
      )}

      <div className="flex flex-wrap gap-3 mt-4 text-xs">
        {Object.entries(CATEGORY_COLORS).map(([label, color]) => (
          <span key={label} className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full inline-block" style={{ background: color }} />
            {label}
          </span>
        ))}
      </div>
    </div>
  )
}
