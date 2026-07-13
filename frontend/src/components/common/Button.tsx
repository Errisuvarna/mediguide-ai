import React, { ButtonHTMLAttributes } from 'react'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger'
  large?: boolean
}

const variants: Record<string, string> = {
  primary: 'bg-primary-600 hover:bg-primary-700 text-white',
  secondary: 'bg-accent-500 hover:bg-accent-600 text-white',
  ghost: 'bg-transparent hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-800 dark:text-gray-100',
  danger: 'bg-red-600 hover:bg-red-700 text-white',
}

export default function Button({ variant = 'primary', large = false, className = '', ...props }: ButtonProps) {
  return (
    <button
      className={`rounded-xl font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed
        ${large ? 'text-lg px-6 py-4' : 'text-sm px-4 py-2'} ${variants[variant]} ${className}`}
      {...props}
    />
  )
}
