import { describe, it, expect } from 'vitest'

import { mount } from '@vue/test-utils'
import Welcome from '../TheWelcome.vue'

describe('TheWelcome', () => {
  it('should render', () => {
    const wrapper = mount(Welcome)
    expect(wrapper.html()).toContain('Welcome to Your Vue.js + TypeScript App')
  })
})
