import { createContext, useState, useContext, ReactNode } from 'react'

interface AuthContextProps {
  token: string | null
  setToken: (token: string | null) => void
}

const AuthContext = createContext<AuthContextProps | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('token'))

  const handleSetToken = (t: string | null) => {
    setToken(t)
    if (t) localStorage.setItem('token', t)
    else localStorage.removeItem('token')
  }

  return <AuthContext.Provider value={{ token, setToken: handleSetToken }}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('AuthContext not found')
  return ctx
}
