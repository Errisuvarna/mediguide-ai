import React, { useState } from 'react'
import api from '../api/client'
import { useLanguage } from '../i18n'
import Card from '../components/common/Card'
import Button from '../components/common/Button'

export default function Feedback() {
  const { t } = useLanguage()
  const [name, setName] = useState('')
  const [rating, setRating] = useState(5)
  const [comments, setComments] = useState('')
  const [submitted, setSubmitted] = useState(false)
  const [loading, setLoading] = useState(false)

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    try {
      await api.post('/feedback', { name: name || undefined, rating, comments: comments || undefined })
      setSubmitted(true)
    } finally {
      setLoading(false)
    }
  }

  if (submitted) {
    return (
      <Card className="max-w-md mx-auto text-center py-10">
        <div className="text-5xl mb-4">🙏</div>
        <p className="text-lg font-semibold">{t('thankYou')}</p>
      </Card>
    )
  }

  return (
    <Card className="max-w-md mx-auto">
      <h1 className="text-xl font-bold mb-6">{t('feedback')}</h1>
      <form onSubmit={submit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">Name (optional)</label>
          <input
            value={name} onChange={(e) => setName(e.target.value)}
            className="w-full rounded-xl px-4 py-3 bg-gray-100 dark:bg-gray-800"
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">{t('yourRating')}</label>
          <div className="flex gap-2">
            {[1, 2, 3, 4, 5].map((n) => (
              <button
                type="button" key={n} onClick={() => setRating(n)}
                className={`text-2xl ${n <= rating ? 'opacity-100' : 'opacity-30'}`}
              >⭐</button>
            ))}
          </div>
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">{t('comments')}</label>
          <textarea
            value={comments} onChange={(e) => setComments(e.target.value)} rows={4}
            className="w-full rounded-xl px-4 py-3 bg-gray-100 dark:bg-gray-800"
          />
        </div>
        <Button type="submit" disabled={loading} className="w-full">{t('submitFeedback')}</Button>
      </form>
    </Card>
  )
}
