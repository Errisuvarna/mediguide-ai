import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout/Layout'
import { useAuth } from './context/AuthContext'

import Landing from './pages/Landing'
import Chat from './pages/Chat'
import VoiceAssistant from './pages/VoiceAssistant'
import HospitalMap from './pages/HospitalMap'
import DepartmentSearch from './pages/DepartmentSearch'
import DoctorSearch from './pages/DoctorSearch'
import DocumentChecklist from './pages/DocumentChecklist'
import Feedback from './pages/Feedback'
import Dashboard from './pages/Dashboard'
import AdminLogin from './pages/AdminLogin'
import Settings from './pages/Settings'
import NotFound from './pages/NotFound'

function ProtectedRoute({ children }: { children: React.ReactElement }) {
  const { user } = useAuth()
  if (!user || user.role !== 'admin') {
    return <Navigate to="/admin-login" replace />
  }
  return children
}

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="/voice" element={<VoiceAssistant />} />
        <Route path="/map" element={<HospitalMap />} />
        <Route path="/departments" element={<DepartmentSearch />} />
        <Route path="/doctors" element={<DoctorSearch />} />
        <Route path="/documents" element={<DocumentChecklist />} />
        <Route path="/feedback" element={<Feedback />} />
        <Route path="/admin-login" element={<AdminLogin />} />
        <Route path="/settings" element={<Settings />} />
        <Route
          path="/dashboard"
          element={<ProtectedRoute><Dashboard /></ProtectedRoute>}
        />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Layout>
  )
}
