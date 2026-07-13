import React from 'react'
import Card from '../common/Card'

interface RecentQuery {
  message: string
  department: string | null
  language: string
  created_at: string
}

export default function RecentQueriesTable({ rows }: { rows: RecentQuery[] }) {
  return (
    <Card>
      <h3 className="font-semibold mb-4">Recent Queries</h3>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="text-left text-gray-500 dark:text-gray-400">
            <tr>
              <th className="py-2 pr-4">Type</th>
              <th className="py-2 pr-4">Department</th>
              <th className="py-2 pr-4">Language</th>
              <th className="py-2 pr-4">Time</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r, i) => (
              <tr key={i} className="border-t border-gray-100 dark:border-gray-800">
                <td className="py-2 pr-4">{r.message}</td>
                <td className="py-2 pr-4">{r.department ?? '—'}</td>
                <td className="py-2 pr-4 uppercase">{r.language}</td>
                <td className="py-2 pr-4">{new Date(r.created_at).toLocaleString()}</td>
              </tr>
            ))}
            {rows.length === 0 && (
              <tr><td colSpan={4} className="py-4 text-center text-gray-400">No queries yet</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </Card>
  )
}
