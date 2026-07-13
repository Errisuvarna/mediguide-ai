import { describe, it, expect } from 'vitest'
import { translations } from '../src/i18n/translations'

describe('translations', () => {
  it('has matching keys across all languages', () => {
    const enKeys = Object.keys(translations.en).sort()
    const hiKeys = Object.keys(translations.hi).sort()
    const teKeys = Object.keys(translations.te).sort()
    expect(hiKeys).toEqual(enKeys)
    expect(teKeys).toEqual(enKeys)
  })
})
