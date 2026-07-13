import React from 'react'

interface VoiceButtonProps {
  listening: boolean
  isSupported: boolean
  onClick: () => void
  size?: 'sm' | 'lg'
}

export default function VoiceButton({ listening, isSupported, onClick, size = 'sm' }: VoiceButtonProps) {
  if (!isSupported) return null
  const dims = size === 'lg' ? 'w-20 h-20 text-4xl' : 'w-11 h-11 text-xl'
  return (
    <button
      onClick={onClick}
      aria-label="Voice input"
      className={`${dims} rounded-full flex items-center justify-center transition-all shrink-0
        ${listening
          ? 'bg-red-500 text-white animate-pulse shadow-lg shadow-red-300 dark:shadow-red-900'
          : 'bg-primary-600 hover:bg-primary-700 text-white'}`}
    >
      🎤
    </button>
  )
}
