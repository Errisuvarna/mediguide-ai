import React from 'react'
import { useLanguage } from '../i18n'
import { useTheme } from '../context/ThemeContext'
import { useAuth } from '../context/AuthContext'
import Card from '../components/common/Card'
import Button from '../components/common/Button'
import { LangCode } from '../i18n/translations'

export default function Settings() {
  const { t, lang, setLang } = useLanguage()
  const { dark, toggleDark } = useTheme()
  const { user, logout } = useAuth()

  return (
    <Card className="max-w-md mx-auto space-y-6">
      <h1 className="text-xl font-bold">{t('settings')}</h1>

      <div className="flex items-center justify-between">
        <span>{t('language')}</span>
        <select
          value={lang} onChange={(e) => setLang(e.target.value as LangCode)}
          className="rounded-lg px-3 py-2 bg-gray-100 dark:bg-gray-800"
        >
          <option value="en">English</option>
          <option value="hi">हिन्दी</option>
          <option value="te">తెలుగు</option>
        </select>
      </div>

      <div className="flex items-center justify-between">
        <span>{t('darkMode')}</span>
        <button
          onClick={toggleDark}
          className={`w-14 h-8 rounded-full flex items-center px-1 transition-colors ${dark ? 'bg-primary-600 justify-end' : 'bg-gray-300 justify-start'}`}
        >
          <span className="w-6 h-6 rounded-full bg-white block" />
        </button>
      </div>

      {user && (
        <div className="border-t border-gray-100 dark:border-gray-800 pt-4">
          <p className="text-sm text-gray-500 mb-2">Logged in as {user.full_name} ({user.role})</p>
          <Button variant="danger" onClick={logout}>Logout</Button>
        </div>
      )}
    </Card>
  )
}
