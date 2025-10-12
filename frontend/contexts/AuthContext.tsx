'use client'

import React, { createContext, useContext, useEffect, useState } from 'react'
import { authenticationApi, updateApiClients, setAuthToken } from '@/api'

interface User {
  id: number
  username: string
  email: string
  full_name: string
  business_role: string
  system_role: string
}

interface AuthContextType {
  user: User | null
  login: (username: string, password: string) => Promise<void>
  logout: () => void
  loading: boolean
  isAuthenticated: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('auth_token')
    if (token) {
      // Verify token and get user info
      verifyToken()
    } else {
      setLoading(false)
    }
  }, [])

  const verifyToken = async () => {
    try {
      // Update API clients with current token
      updateApiClients()
      
      const response = await authenticationApi.getCurrentUserInfoApiV1AuthMeGet()
      // Map UserResponse to User interface
      setUser({
        id: response.id,
        username: response.username,
        email: response.email,
        full_name: response.fullName,
        business_role: response.businessRole,
        system_role: response.systemRole,
      })
    } catch (error) {
      localStorage.removeItem('auth_token')
      updateApiClients() // Update API clients to remove invalid token
    } finally {
      setLoading(false)
    }
  }

  const login = async (username: string, password: string) => {
    try {
      console.log('🔐 Attempting login for:', username)
      
      const response = await authenticationApi.loginApiV1AuthLoginPost({
        userLogin: {
          username,
          password,
        }
      })
      
      console.log('🔐 Login response:', response)
      
      if (!response || !response.sessionToken) {
        throw new Error('Invalid login response - no session token received')
      }
      
      const { sessionToken } = response
      // Set token into API layer and localStorage atomically
      setAuthToken(sessionToken)
      console.log('🔐 Token applied to API clients and saved')
      console.log('🔐 API clients updated with new token')
      
      // Get user info using the updated API client
      const userResponse = await authenticationApi.getCurrentUserInfoApiV1AuthMeGet()
      console.log('👤 User info response:', userResponse)
      
      if (!userResponse) {
        throw new Error('Failed to get user information')
      }
      
      // Map UserResponse to User interface
      setUser({
        id: userResponse.id,
        username: userResponse.username,
        email: userResponse.email,
        full_name: userResponse.fullName,
        business_role: userResponse.businessRole,
        system_role: userResponse.systemRole,
      })
      
      console.log('✅ Login successful for:', username)
    } catch (error: any) {
      console.error('❌ Login error:', error)
      throw new Error(error.message || 'Login failed')
    }
  }

  const logout = () => {
    setAuthToken(null) // clears localStorage and updates clients
    setUser(null)
  }

  const value = {
    user,
    login,
    logout,
    loading,
    isAuthenticated: !!user,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
