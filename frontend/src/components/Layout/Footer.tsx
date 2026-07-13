import React from 'react'
import { Link } from 'react-router-dom'
import { useLanguage } from '../../i18n'

export default function Footer() {
  const { t } = useLanguage()
  return (
    <footer className="mt-16 border-t border-gray-100 dark:border-gray-800 py-8 text-center text-sm text-gray-500 dark:text-gray-400">
      <p>🏥 {t('appName')} — {t('tagline')}</p>
      <p className="mt-1">This assistant provides hospital navigation only. It does not diagnose or prescribe.</p>
      <div className="mt-2 flex justify-center gap-4">
        <Link to="/dashboard" className="hover:underline">{t('dashboard')}</Link>
        <Link to="/admin-login" className="hover:underline">{t('adminLogin')}</Link>
        <Link to="/settings" className="hover:underline">{t('settings')}</Link>
      </div>
    </footer>
  )
}
