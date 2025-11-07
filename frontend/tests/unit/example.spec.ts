import { describe, expect, it } from 'vitest'

import { mount } from '@vue/test-utils'

import App from '@/App.vue'

describe('App', () => {
  it('renders navigation', () => {
    const wrapper = mount(App)
    expect(wrapper.text()).toContain('FastAPI + Vue Template')
  })
})
