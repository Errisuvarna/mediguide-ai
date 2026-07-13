import React, { createContext, useContext, useState, ReactNode } from 'react'
import api from '../api/client'
import { AuthUser } from '../types'

interface AuthContextValue {
  user: AuthUser | null
  login: (email: string, password: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(() => {
    const stored = localStorage.getItem('mediguide_user')
    return stored ? JSON.parse(stored) : null
  })

  const login = async (email: string, password: string) => {
    const resp = await api.post('/auth/login', { email, password })
    localStorage.setItem('mediguide_token', resp.data.access_token)
    localStorage.setItem('mediguide_user', JSON.stringify(resp.data.user))
    setUser(resp.data.user)
  }

  const logout = () => {
    localStorage.removeItem('mediguide_token')
    localStorage.removeItem('mediguide_user')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
