import React, { useEffect, useState } from 'react'
import api from '../api/client'
import { Doctor, Department } from '../types'
import { useLanguage } from '../i18n'
import Card from '../components/common/Card'
import LoadingSpinner from '../components/common/LoadingSpinner'

export default function DoctorSearch() {
  const { t } = useLanguage()
  const [doctors, setDoctors] = useState<Doctor[]>([])
  const [departments, setDepartments] = useState<Department[]>([])
  const [search, setSearch] = useState('')
  const [deptId, setDeptId] = useState<string>('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get<Department[]>('/departments').then((r) => setDepartments(r.data))
  }, [])

  useEffect(() => {
    setLoading(true)
    const params: Record<string, string> = {}
    if (search) params.search = search
    if (deptId) params.department_id = deptId
    api.get<Doctor[]>('/doctors', { params }).then((r) => setDoctors(r.data)).finally(() => setLoading(false))
  }, [search, deptId])

  const deptName = (id: number) => departments.find((d) => d.id === id)?.name ?? ''

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">{t('doctors')}</h1>
      <div className="flex flex-wrap gap-3 mb-6">
        <input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder={t('searchDoctors')}
          className="flex-1 min-w-[220px] rounded-xl px-4 py-3 bg-gray-100 dark:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-primary-500"
        />
        <select
          value={deptId}
          onChange={(e) => setDeptId(e.target.value)}
          className="rounded-xl px-4 py-3 bg-gray-100 dark:bg-gray-800"
        >
          <option value="">All departments</option>
          {departments.map((d) => <option key={d.id} value={d.id}>{d.name}</option>)}
        </select>
      </div>

      {loading ? <LoadingSpinner /> : (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {doctors.map((doc) => (
            <Card key={doc.id}>
              <div className="font-semibold text-lg">{doc.full_name}</div>
              <div className="text-sm text-primary-600 dark:text-primary-400 mb-2">{deptName(doc.department_id)}</div>
              <div className="text-sm space-y-1 text-gray-600 dark:text-gray-300">
                <div>{doc.designation} · {doc.qualification}</div>
                <div>🏢 Room {doc.room_number}</div>
                <div>📅 {doc.available_days} · {doc.available_time}</div>
                <div>💰 {t('fee')}: ₹{doc.consultation_fee}</div>
                <div>⭐ {doc.experience_years} {t('experience')}</div>
              </div>
            </Card>
          ))}
          {doctors.length === 0 && <p className="text-gray-400">No doctors found.</p>}
        </div>
      )}
    </div>
  )
}
