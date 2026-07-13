import React, { useEffect, useState } from 'react'
import api from '../api/client'
import { RequiredDocument } from '../types'
import { useLanguage } from '../i18n'
import Card from '../components/common/Card'
import LoadingSpinner from '../components/common/LoadingSpinner'

export default function DocumentChecklist() {
  const { t } = useLanguage()
  const [docs, setDocs] = useState<RequiredDocument[]>([])
  const [process, setProcess] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    api.get<RequiredDocument[]>('/documents', { params: process ? { process_name: process } : {} })
      .then((r) => setDocs(r.data))
      .finally(() => setLoading(false))
  }, [process])

  const processes = ['', 'Registration', 'Admission', 'Billing', 'Insurance', 'Discharge', 'Laboratory', 'Pharmacy']
  const grouped = docs.reduce<Record<string, RequiredDocument[]>>((acc, d) => {
    acc[d.process_name] = acc[d.process_name] || []
    acc[d.process_name].push(d)
    return acc
  }, {})

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">{t('documents')}</h1>
      <div className="flex flex-wrap gap-2 mb-6">
        {processes.map((p) => (
          <button
            key={p || 'all'}
            onClick={() => setProcess(p)}
            className={`px-4 py-2 rounded-full text-sm font-medium
              ${process === p ? 'bg-primary-600 text-white' : 'bg-gray-100 dark:bg-gray-800'}`}
          >
            {p || 'All'}
          </button>
        ))}
      </div>

      {loading ? <LoadingSpinner /> : (
        <div className="space-y-6">
          {Object.entries(grouped).map(([proc, items]) => (
            <Card key={proc}>
              <div className="font-semibold text-lg mb-3">{proc}</div>
              <ul className="space-y-2">
                {items.map((doc) => (
                  <li key={doc.id} className="flex items-start justify-between gap-3 border-b border-gray-100 dark:border-gray-800 pb-2 last:border-0">
                    <span>{doc.document_name}</span>
                    <span className={`text-xs px-2 py-1 rounded-full whitespace-nowrap
                      ${doc.is_mandatory === 'yes'
                        ? 'bg-red-50 text-red-600 dark:bg-red-950 dark:text-red-400'
                        : 'bg-gray-100 text-gray-500 dark:bg-gray-800'}`}>
                      {doc.is_mandatory === 'yes' ? t('mandatory') : t('optional')}
                    </span>
                  </li>
                ))}
              </ul>
            </Card>
          ))}
          {docs.length === 0 && <p className="text-gray-400">No documents found.</p>}
        </div>
      )}
    </div>
  )
}
