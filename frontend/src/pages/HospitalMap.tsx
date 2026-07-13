import React, { useEffect, useState } from 'react'
import api from '../api/client'
import { MapPoint } from '../types'
import { useLanguage } from '../i18n'
import HospitalMapSvg from '../components/map/HospitalMapSvg'
import LoadingSpinner from '../components/common/LoadingSpinner'

export default function HospitalMap() {
  const { t } = useLanguage()
  const [points, setPoints] = useState<MapPoint[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get<MapPoint[]>('/hospital-map').then((r) => setPoints(r.data)).finally(() => setLoading(false))
  }, [])

  if (loading) return <LoadingSpinner />

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">{t('map')}</h1>
      <HospitalMapSvg points={points} />
    </div>
  )
}
