export interface Department {
  id: number
  name: string
  description?: string
  floor_number?: number
  building_name?: string
  contact_number?: string
  office_hours?: string
  avg_waiting_time_minutes: number
  keywords?: string
}

export interface Doctor {
  id: number
  full_name: string
  department_id: number
  designation?: string
  qualification?: string
  consultation_fee: number
  room_number?: string
  available_days?: string
  available_time?: string
  experience_years: number
}

export interface ServiceItem {
  id: number
  name: string
  department_id?: number
  description?: string
  fee: number
  location?: string
}

export interface RequiredDocument {
  id: number
  process_name: string
  document_name: string
  is_mandatory: string
  notes?: string
}

export interface MapPoint {
  id: number
  name: string
  category?: string
  building_name?: string
  floor_number?: number
  x_coordinate: number
  y_coordinate: number
  description?: string
}

export interface ChatMessage {
  role: 'user' | 'assistant'
  message: string
  language: string
  created_at?: string
}

export interface ChatResponse {
  session_id: string
  reply: string
  department_matched?: string | null
  is_emergency: boolean
  sources: { source_file: string; snippet: string }[]
  response_time_ms: number
}

export interface DashboardData {
  summary: {
    total_queries: number
    today_queries: number
    weekly_queries: number
    monthly_queries: number
    emergency_queries: number
    avg_response_time_ms: number
    feedback_score: number
    patient_satisfaction_pct: number
  }
  charts: {
    department_wise_queries: { label: string; value: number }[]
    daily_trend: { label: string; value: number }[]
    weekly_trend: { label: string; value: number }[]
    monthly_trend: { label: string; value: number }[]
    most_asked_questions: { label: string; value: number }[]
    popular_services: { label: string; value: number }[]
    voice_usage: { label: string; value: number }[]
    language_usage: { label: string; value: number }[]
    unanswered_questions: { label: string; value: number }[]
  }
  recent_queries: { message: string; department: string | null; language: string; created_at: string }[]
}

export interface AuthUser {
  id: number
  full_name: string
  email: string
  role: string
  is_active: boolean
}
