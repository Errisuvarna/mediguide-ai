import React, { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useLanguage } from '../../i18n'
import { useTheme } from '../../context/ThemeContext'
import { LangCode } from '../../i18n/translations'

const NAV_ITEMS = [
  { to: '/', key: 'home' },
  { to: '/chat', key: 'chat' },
  { to: '/voice', key: 'voice' },
  { to: '/map', key: 'map' },
  { to: '/departments', key: 'departments' },
  { to: '/doctors', key: 'doctors' },
  { to: '/documents', key: 'documents' },
  { to: '/feedback', key: 'feedback' },
]

export default function Navbar() {
  const { t, lang, setLang } = useLanguage()
  const { dark, toggleDark } = useTheme()
  const location = useLocation()
  const [open, setOpen] = useState(false)

  return (
    <header className="sticky top-0 z-40 bg-white/90 dark:bg-gray-950/90 backdrop-blur border-b border-gray-100 dark:border-gray-800">
      <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 font-bold text-xl text-primary-700 dark:text-primary-400">
          <span>🏥</span> {t('appName')}
        </Link>

        <nav className="hidden lg:flex items-center gap-1">
          {NAV_ITEMS.map((item) => (
            <Link
              key={item.to}
              to={item.to}
              className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors
                ${location.pathname === item.to
                  ? 'bg-primary-100 text-primary-700 dark:bg-primary-900 dark:text-primary-300'
                  : 'hover:bg-gray-100 dark:hover:bg-gray-800'}`}
            >
              {t(item.key)}
            </Link>
          ))}
        </nav>

        <div className="flex items-center gap-2">
          <select
            aria-label={t('language')}
            value={lang}
            onChange={(e) => setLang(e.target.value as LangCode)}
            className="text-sm bg-gray-100 dark:bg-gray-800 rounded-lg px-2 py-1.5"
          >
            <option value="en">English</option>
            <option value="hi">हिन्दी</option>
            <option value="te">తెలుగు</option>
          </select>
          <button
            onClick={toggleDark}
            aria-label={t('darkMode')}
            className="w-9 h-9 rounded-lg bg-gray-100 dark:bg-gray-800 flex items-center justify-center"
          >
            {dark ? '☀️' : '🌙'}
          </button>
          <button
            className="lg:hidden w-9 h-9 rounded-lg bg-gray-100 dark:bg-gray-800 flex items-center justify-center"
            onClick={() => setOpen((o) => !o)}
            aria-label="Menu"
          >
            ☰
          </button>
        </div>
      </div>

      {open && (
        <nav className="lg:hidden px-4 pb-3 flex flex-col gap-1">
          {NAV_ITEMS.map((item) => (
            <Link
              key={item.to}
              to={item.to}
              onClick={() => setOpen(false)}
              className="px-3 py-2 rounded-lg text-sm font-medium hover:bg-gray-100 dark:hover:bg-gray-800"
            >
              {t(item.key)}
            </Link>
          ))}
        </nav>
      )}
    </header>
  )
}
