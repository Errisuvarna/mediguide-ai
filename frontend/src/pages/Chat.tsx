import React, { useEffect, useRef, useState } from 'react'
import api from '../api/client'
import { useLanguage } from '../i18n'
import { ChatMessage, ChatResponse } from '../types'
import ChatBubble from '../components/chat/ChatBubble'
import VoiceButton from '../components/chat/VoiceButton'
import Button from '../components/common/Button'
import { useSpeechRecognition } from '../hooks/useSpeechRecognition'
import { useSpeechSynthesis } from '../hooks/useSpeechSynthesis'

function getSessionId(): string {
  let id = sessionStorage.getItem('mediguide_session')
  if (!id) {
    id = `sess-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`
    sessionStorage.setItem('mediguide_session', id)
  }
  return id
}

export default function Chat() {
  const { t, lang } = useLanguage()
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef<HTMLDivElement>(null)
  const sessionId = useRef(getSessionId())

  const { listening, transcript, isSupported, start } = useSpeechRecognition(lang)
  const { speak } = useSpeechSynthesis()

  useEffect(() => {
    if (transcript) {
      setInput(transcript)
    }
  }, [transcript])

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = async (text: string) => {
    if (!text.trim()) return
    const userMsg: ChatMessage = { role: 'user', message: text, language: lang }
    setMessages((prev) => [...prev, userMsg])
    setInput('')
    setLoading(true)
    try {
      const resp = await api.post<ChatResponse>('/chat', {
        session_id: sessionId.current, message: text, language: lang, is_voice: false,
      })
      const assistantMsg: ChatMessage = { role: 'assistant', message: resp.data.reply, language: lang }
      setMessages((prev) => [...prev, assistantMsg])
      speak(resp.data.reply, lang)
    } catch (err) {
      setMessages((prev) => [...prev, {
        role: 'assistant',
        message: 'Sorry, something went wrong reaching the assistant. Please try again.',
        language: lang,
      }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto flex flex-col h-[70vh]">
      <div className="flex-1 overflow-y-auto space-y-3 pr-1">
        {messages.length === 0 && (
          <div className="text-center text-gray-400 mt-16">
            👋 {t('speakNow')} — {t('typeMessage')}
          </div>
        )}
        {messages.map((m, i) => <ChatBubble key={i} msg={m} />)}
        {loading && <ChatBubble msg={{ role: 'assistant', message: '…', language: lang }} />}
        <div ref={bottomRef} />
      </div>

      <form
        className="mt-4 flex items-center gap-2"
        onSubmit={(e) => { e.preventDefault(); sendMessage(input) }}
      >
        <VoiceButton listening={listening} isSupported={isSupported} onClick={start} />
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={t('typeMessage')}
          className="flex-1 rounded-xl px-4 py-3 bg-gray-100 dark:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-primary-500"
        />
        <Button type="submit" disabled={loading}>{t('send')}</Button>
      </form>
    </div>
  )
}
