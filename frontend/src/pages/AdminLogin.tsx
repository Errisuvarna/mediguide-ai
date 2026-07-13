import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useLanguage } from '../i18n'
import Card from '../components/common/Card'
import Button from '../components/common/Button'

export default function AdminLogin() {
  const { login } = useAuth()
  const { t } = useLanguage()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await login(email, password)
      navigate('/dashboard')
    } catch {
      setError('Invalid email or password.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card className="max-w-sm mx-auto">
      <h1 className="text-xl font-bold mb-6">{t('adminLogin')}</h1>
      <form onSubmit={submit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">Email</label>
          <input
            type="email" required value={email} onChange={(e) => setEmail(e.target.value)}
            className="w-full rounded-xl px-4 py-3 bg-gray-100 dark:bg-gray-800"
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Password</label>
          <input
            type="password" required value={password} onChange={(e) => setPassword(e.target.value)}
            className="w-full rounded-xl px-4 py-3 bg-gray-100 dark:bg-gray-800"
          />
        </div>
        {error && <p className="text-red-500 text-sm">{error}</p>}
        <Button type="submit" disabled={loading} className="w-full">Login</Button>
      </form>
      <p className="text-xs text-gray-400 mt-4">
        First time? Register an admin via POST /api/auth/register with role=admin.
      </p>
    </Card>
  )
}
