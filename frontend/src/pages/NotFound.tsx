import React from 'react'
import { Link } from 'react-router-dom'
import { useLanguage } from '../i18n'
import Button from '../components/common/Button'

export default function NotFound() {
  const { t } = useLanguage()
  return (
    <div className="text-center py-24">
      <div className="text-7xl mb-4">🧭</div>
      <h1 className="text-2xl font-bold mb-2">{t('notFoundTitle')}</h1>
      <p className="text-gray-500 mb-8">404 — the page you're looking for doesn't exist.</p>
      <Link to="/"><Button>{t('backHome')}</Button></Link>
    </div>
  )
}
