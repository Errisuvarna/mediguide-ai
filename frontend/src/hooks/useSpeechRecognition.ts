import { useCallback, useEffect, useRef, useState } from 'react'
import { LangCode, voiceLocales } from '../i18n/translations'

/**
 * Wraps the browser's Web Speech API (SpeechRecognition) for speech-to-text.
 * Falls back gracefully (isSupported=false) on browsers without support,
 * e.g. Firefox/Safari — callers should hide the mic button in that case.
 */
export function useSpeechRecognition(lang: LangCode) {
  const [listening, setListening] = useState(false)
  const [transcript, setTranscript] = useState('')
  const [isSupported, setIsSupported] = useState(false)
  const recognitionRef = useRef<any>(null)

  useEffect(() => {
    const SpeechRecognition =
      (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
    setIsSupported(Boolean(SpeechRecognition))
  }, [])

  const start = useCallback(() => {
    const SpeechRecognition =
      (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
    if (!SpeechRecognition) return

    const recognition = new SpeechRecognition()
    recognition.lang = voiceLocales[lang]
    recognition.interimResults = false
    recognition.maxAlternatives = 1

    recognition.onstart = () => setListening(true)
    recognition.onend = () => setListening(false)
    recognition.onerror = () => setListening(false)
    recognition.onresult = (event: any) => {
      const text = event.results[0][0].transcript
      setTranscript(text)
    }

    recognitionRef.current = recognition
    recognition.start()
  }, [lang])

  const stop = useCallback(() => {
    recognitionRef.current?.stop()
  }, [])

  return { listening, transcript, isSupported, start, stop, setTranscript }
}
