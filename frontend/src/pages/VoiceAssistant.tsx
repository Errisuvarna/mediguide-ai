import React, { useEffect, useRef, useState } from 'react'
import api from '../api/client'
import { useLanguage } from '../i18n'
import { ChatResponse } from '../types'
import { useSpeechRecognition } from '../hooks/useSpeechRecognition'
import { useSpeechSynthesis } from '../hooks/useSpeechSynthesis'
import Card from '../components/common/Card'

export default function VoiceAssistant() {
  const { t, lang } = useLanguage()
  const { listening, transcript, isSupported, start } = useSpeechRecognition(lang)
  const { speak } = useSpeechSynthesis()
  const [reply, setReply] = useState('')
  const [loading, setLoading] = useState(false)
  const sessionId = useRef(`voice-${Date.now()}`)

  useEffect(() => {
    if (transcript) {
      handleQuery(transcript)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [transcript])

  const handleQuery = async (text: string) => {
    setLoading(true)
    setReply('')
    try {
      const resp = await api.post<ChatResponse>('/chat', {
        session_id: sessionId.current, message: text, language: lang, is_voice: true,
      })
      setReply(resp.data.reply)
      speak(resp.data.reply, lang)
    } catch {
      setReply('Sorry, something went wrong. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-xl mx-auto text-center py-10">
      <h1 className="text-2xl font-bold mb-2">{t('voice')}</h1>
      <p className="text-gray-500 dark:text-gray-400 mb-8">{t('speakNow')}</p>

      {!isSupported && (
        <p className="text-amber-600 mb-6">
          Voice input isn't supported in this browser. Please use Chrome or Edge, or use the text chat instead.
        </p>
      )}

      <button
        onClick={start}
        disabled={!isSupported}
        className={`w-32 h-32 rounded-full text-5xl flex items-center justify-center mx-auto transition-all
          ${listening ? 'bg-red-500 animate-pulse shadow-xl shadow-red-300 dark:shadow-red-900' : 'bg-primary-600 hover:bg-primary-700'}
          text-white disabled:opacity-40`}
      >
        🎤
      </button>
      <p className="mt-4 text-sm text-gray-500">{listening ? t('listening') : t('speakNow')}</p>

      {transcript && (
        <Card className="mt-8 text-left">
          <div className="text-xs uppercase text-gray-400 mb-1">You said</div>
          <div>{transcript}</div>
        </Card>
      )}

      {loading && <p className="mt-6 text-gray-400">…</p>}

      {reply && (
        <Card className="mt-4 text-left">
          <div className="text-xs uppercase text-gray-400 mb-1">MediGuide AI</div>
          <div>{reply}</div>
        </Card>
      )}
    </div>
  )
}
