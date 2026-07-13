import { useCallback } from 'react'
import { LangCode, voiceLocales } from '../i18n/translations'

/**
 * Wraps the browser's SpeechSynthesis API for text-to-speech.
 */
export function useSpeechSynthesis() {
  const speak = useCallback((text: string, lang: LangCode) => {
    if (!('speechSynthesis' in window)) return
    window.speechSynthesis.cancel()
    const utterance = new SpeechSynthesisUtterance(text)
    utterance.lang = voiceLocales[lang]
    utterance.rate = 0.95
    window.speechSynthesis.speak(utterance)
  }, [])

  const stop = useCallback(() => {
    if ('speechSynthesis' in window) window.speechSynthesis.cancel()
  }, [])

  return { speak, stop, isSupported: 'speechSynthesis' in window }
}
