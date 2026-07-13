import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import Landing from '../src/pages/Landing'
import { LanguageProvider } from '../src/i18n'

function renderWithProviders(ui: React.ReactElement) {
  return render(
    <BrowserRouter>
      <LanguageProvider>{ui}</LanguageProvider>
    </BrowserRouter>
  )
}

describe('Landing page', () => {
  it('renders the hero heading', () => {
    renderWithProviders(<Landing />)
    expect(screen.getByText(/Find your way around the hospital/i)).toBeInTheDocument()
  })

  it('renders start chat and voice buttons', () => {
    renderWithProviders(<Landing />)
    expect(screen.getByText(/Start Chatting/i)).toBeInTheDocument()
    expect(screen.getByText(/Use Voice/i)).toBeInTheDocument()
  })
})
