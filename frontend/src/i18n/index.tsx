import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react'
import { translations, LangCode } from './translations'

interface LanguageContextValue {
  lang: LangCode
  setLang: (l: LangCode) => void
  t: (key: string) => string
}

const LanguageContext = createContext<LanguageContextValue | undefined>(undefined)

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [lang, setLangState] = useState<LangCode>(
    (localStorage.getItem('mediguide_lang') as LangCode) || 'en'
  )

  const setLang = useCallback((l: LangCode) => {
    setLangState(l)
    localStorage.setItem('mediguide_lang', l)
  }, [])

  const t = useCallback((key: string) => translations[lang][key] ?? translations.en[key] ?? key, [lang])

  return (
    <LanguageContext.Provider value={{ lang, setLang, t }}>
      {children}
    </LanguageContext.Provider>
  )
}

export function useLanguage() {
  const ctx = useContext(LanguageContext)
  if (!ctx) throw new Error('useLanguage must be used within LanguageProvider')
  return ctx
}

export * from './translations'
