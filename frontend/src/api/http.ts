import axios, { AxiosError, type AxiosResponse, type InternalAxiosRequestConfig } from 'axios'

import { getTokens, setTokens } from './token-storage'

declare module 'axios' {
  interface InternalAxiosRequestConfig {
    _retry?: boolean
  }
}

const DEFAULT_API_BASE_URL = 'http://localhost:8000/api/v1'
const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? DEFAULT_API_BASE_URL).replace(/\/$/, '')

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: false,
})

let isRefreshing = false
let subscribers: Array<(token: string | null) => void> = []

function subscribeTokenRefresh(callback: (token: string | null) => void) {
  subscribers.push(callback)
}

function onTokenRefreshed(token: string | null) {
  subscribers.forEach((callback) => callback(token))
  subscribers = []
}

api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const tokens = getTokens()
  if (tokens?.accessToken) {
    config.headers.Authorization = `Bearer ${tokens.accessToken}`
  }
  return config
})

api.interceptors.response.use(
  (response: AxiosResponse) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig | undefined
    if (!originalRequest || !error.response) {
      throw error
    }

    if (error.response.status !== 401 || originalRequest._retry) {
      throw error
    }

    const tokens = getTokens()
    if (!tokens?.refreshToken) {
      setTokens(null)
      throw error
    }

    if (isRefreshing) {
      return new Promise((resolve, reject) => {
        subscribeTokenRefresh((token) => {
          if (!token) {
            reject(error)
            return
          }
          originalRequest.headers.Authorization = `Bearer ${token}`
          resolve(api(originalRequest))
        })
      })
    }

    originalRequest._retry = true
    isRefreshing = true

    try {
      const { data } = await axios.post(`${API_BASE_URL}/auth/refresh`, {
        refresh_token: tokens.refreshToken,
      })

      setTokens({
        accessToken: data.access_token,
        refreshToken: data.refresh_token,
        expiresAt: data.expires_at,
        refreshExpiresAt: data.refresh_expires_at,
      })

      onTokenRefreshed(data.access_token)
      originalRequest.headers.Authorization = `Bearer ${data.access_token}`
      return api(originalRequest)
    } catch (refreshError) {
      setTokens(null)
      onTokenRefreshed(null)
      throw refreshError
    } finally {
      isRefreshing = false
    }
  }
)

export default api


