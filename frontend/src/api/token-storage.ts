type Tokens = {
  accessToken: string
  refreshToken: string
  expiresAt?: string
  refreshExpiresAt?: string
}

type Listener = (tokens: Tokens | null) => void

const ACCESS_TOKEN_KEY = 'fv_access_token'
const REFRESH_TOKEN_KEY = 'fv_refresh_token'
const ACCESS_TOKEN_EXP_KEY = 'fv_access_expires_at'
const REFRESH_TOKEN_EXP_KEY = 'fv_refresh_expires_at'

const listeners = new Set<Listener>()

export function getTokens(): Tokens | null {
  const accessToken = localStorage.getItem(ACCESS_TOKEN_KEY)
  const refreshToken = localStorage.getItem(REFRESH_TOKEN_KEY)
  if (!accessToken || !refreshToken) {
    return null
  }
  return {
    accessToken,
    refreshToken,
    expiresAt: localStorage.getItem(ACCESS_TOKEN_EXP_KEY) ?? undefined,
    refreshExpiresAt: localStorage.getItem(REFRESH_TOKEN_EXP_KEY) ?? undefined,
  }
}

export function setTokens(tokens: Tokens | null): void {
  if (!tokens) {
    localStorage.removeItem(ACCESS_TOKEN_KEY)
    localStorage.removeItem(REFRESH_TOKEN_KEY)
    localStorage.removeItem(ACCESS_TOKEN_EXP_KEY)
    localStorage.removeItem(REFRESH_TOKEN_EXP_KEY)
  } else {
    localStorage.setItem(ACCESS_TOKEN_KEY, tokens.accessToken)
    localStorage.setItem(REFRESH_TOKEN_KEY, tokens.refreshToken)
    if (tokens.expiresAt) {
      localStorage.setItem(ACCESS_TOKEN_EXP_KEY, tokens.expiresAt)
    }
    if (tokens.refreshExpiresAt) {
      localStorage.setItem(REFRESH_TOKEN_EXP_KEY, tokens.refreshExpiresAt)
    }
  }
  notify(tokens)
}

export function subscribe(listener: Listener): () => void {
  listeners.add(listener)
  return () => listeners.delete(listener)
}

function notify(tokens: Tokens | null): void {
  for (const listener of listeners) {
    listener(tokens)
  }
}


