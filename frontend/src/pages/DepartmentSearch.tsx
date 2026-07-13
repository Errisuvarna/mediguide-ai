import React, { useEffect, useState } from 'react'
import api from '../api/client'
import { Department } from '../types'
import { useLanguage } from '../i18n'
import Card from '../components/common/Card'
import LoadingSpinner from '../components/common/LoadingSpinner'

export default function DepartmentSearch() {
  const { t } = useLanguage()
  const [departments, setDepartments] = useState<Department[]>([])
  const [search, setSearch] = useState('')
  const [loading, setLoading] = useState(true)

  const fetchDepartments = (query: string) => {
    setLoading(true)
    api.get<Department[]>('/departments', { params: query ? { search: query } : {} })
      .then((r) => setDepartments(r.data))
      .finally(() => setLoading(false))
  }

  useEffect(() => { fetchDepartments('') }, [])

  useEffect(() => {
    const handle = setTimeout(() => fetchDepartments(search), 300)
    return () => clearTimeout(handle)
  }, [search])

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">{t('departments')}</h1>
      <input
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        placeholder={t('searchDepartments')}
        className="w-full max-w-md rounded-xl px-4 py-3 mb-6 bg-gray-100 dark:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-primary-500"
      />
      {loading ? <LoadingSpinner /> : (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {departments.map((d) => (
            <Card key={d.id}>
              <div className="font-semibold text-lg mb-1">{d.name}</div>
              <div className="text-sm text-gray-500 dark:text-gray-400 mb-3">{d.description}</div>
              <div className="text-sm space-y-1">
                <div>📍 {d.building_name}, {t('floor')} {d.floor_number}</div>
                <div>🕒 {d.office_hours}</div>
                <div>⏱️ ~{d.avg_waiting_time_minutes} min wait</div>
                {d.contact_number && <div>📞 {d.contact_number}</div>}
              </div>
            </Card>
          ))}
          {departments.length === 0 && <p className="text-gray-400">No departments found.</p>}
        </div>
      )}
    </div>
  )
}
