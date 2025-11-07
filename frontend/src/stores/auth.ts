import { computed, reactive, ref } from 'vue'
import { defineStore } from 'pinia'

import api from '@/api/http'
import { getTokens, setTokens, subscribe } from '@/api/token-storage'

type User = {
  id: string
  email: string
  full_name?: string | null
  is_active: boolean
  is_superuser: boolean
}

type LoginPayload = {
  email: string
  password: string
}

type RegisterPayload = {
  email: string
  password: string
  full_name?: string | null
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const status = ref<'idle' | 'loading' | 'error'>('idle')
  const tokens = ref(getTokens())

  const errors = reactive<{ message: string | null }>({ message: null })

  const isAuthenticated = computed(() => Boolean(tokens.value?.accessToken))

  subscribe((nextTokens) => {
    tokens.value = nextTokens
    if (!nextTokens) {
      user.value = null
    }
  })

  async function loadUserProfile() {
    if (!tokens.value?.accessToken) {
      user.value = null
      return
    }
    try {
      const { data } = await api.get<User>('/users/me')
      user.value = data
    } catch (error) {
      console.error('Failed to load user profile', error)
      setTokens(null)
      user.value = null
    }
  }

  async function login(payload: LoginPayload) {
    status.value = 'loading'
    errors.message = null
    try {
      const { data } = await api.post('/auth/login', payload)
      setTokens({
        accessToken: data.access_token,
        refreshToken: data.refresh_token,
        expiresAt: data.expires_at,
        refreshExpiresAt: data.refresh_expires_at,
      })
      await loadUserProfile()
    } catch (error) {
      errors.message = 'Invalid credentials'
      setTokens(null)
      throw error
    } finally {
      status.value = 'idle'
    }
  }

  async function register(payload: RegisterPayload) {
    status.value = 'loading'
    errors.message = null
    try {
      await api.post('/auth/register', payload)
      await login({ email: payload.email, password: payload.password })
    } finally {
      status.value = 'idle'
    }
  }

  async function logout() {
    const refreshToken = tokens.value?.refreshToken
    try {
      if (refreshToken) {
        await api.post('/auth/logout', { refresh_token: refreshToken })
      }
    } catch (error) {
      console.warn('Error during logout', error)
    } finally {
      setTokens(null)
      user.value = null
    }
  }

  async function initialize() {
    if (tokens.value) {
      await loadUserProfile()
    }
  }

  initialize()

  return {
    user,
    status,
    errors,
    tokens,
    isAuthenticated,
    login,
    register,
    logout,
    loadUserProfile,
  }
})


