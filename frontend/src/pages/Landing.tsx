import React from 'react'
import { Link } from 'react-router-dom'
import { useLanguage } from '../i18n'
import Button from '../components/common/Button'
import Card from '../components/common/Card'

const FEATURE_CARDS = [
  { icon: '💬', titleKey: 'chat', descKey: 'Ask anything about the hospital, get instant answers.' },
  { icon: '🎤', titleKey: 'voice', descKey: 'Speak your question and hear the answer aloud.' },
  { icon: '🗺️', titleKey: 'map', descKey: 'Find departments, labs, and counters visually.' },
  { icon: '🩺', titleKey: 'doctors', descKey: 'Search doctors by department, fee, or availability.' },
]

export default function Landing() {
  const { t } = useLanguage()
  return (
    <div>
      <section className="text-center py-12">
        <div className="text-6xl mb-4">🏥</div>
        <h1 className="text-4xl md:text-5xl font-bold tracking-tight mb-4">{t('heroTitle')}</h1>
        <p className="text-lg text-gray-500 dark:text-gray-400 mb-8 max-w-xl mx-auto">{t('heroSubtitle')}</p>
        <div className="flex flex-wrap justify-center gap-4">
          <Link to="/chat"><Button large>{t('startChat')}</Button></Link>
          <Link to="/voice"><Button large variant="secondary">{t('useVoice')}</Button></Link>
        </div>
      </section>

      <section className="bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-900 rounded-2xl p-4 text-amber-800 dark:text-amber-300 text-center mb-12">
        ⚠️ {t('emergencyBanner')}
      </section>

      <section className="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
        {FEATURE_CARDS.map((f) => (
          <Card key={f.titleKey} className="text-center">
            <div className="text-4xl mb-3">{f.icon}</div>
            <div className="font-semibold mb-1">{t(f.titleKey)}</div>
            <div className="text-sm text-gray-500 dark:text-gray-400">{f.descKey}</div>
          </Card>
        ))}
      </section>
    </div>
  )
}
