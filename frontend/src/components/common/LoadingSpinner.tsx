import React from 'react'

export default function LoadingSpinner({ label }: { label?: string }) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 py-10 text-gray-500 dark:text-gray-400">
      <div className="w-8 h-8 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin" />
      {label && <span>{label}</span>}
    </div>
  )
}
