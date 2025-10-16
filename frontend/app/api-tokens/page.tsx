'use client'

import Layout from '@/components/Layout'
import { useState, useEffect } from 'react'
import { authenticationApi } from '@/api'
import Link from 'next/link'
import { PlusIcon, EyeIcon, TrashIcon } from '@heroicons/react/24/outline'
import { toast } from 'react-hot-toast'

interface APIToken {
  id: number
  name: string
  token_hash: string
  scopes: string[]
  created_at: string
  last_used_at: string | null
}

export default function APITokensPage() {
  const [tokens, setTokens] = useState<APIToken[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchTokens()
  }, [])

  const fetchTokens = async () => {
    try {
      const response = await authenticationApi.listApiTokensApiV1AuthTokensGet()
      setTokens(response)
    } catch (error) {
      toast.error('Failed to fetch API tokens')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this API token?')) return

    try {
      await authenticationApi.deleteApiTokenApiV1AuthTokensTokenIdDelete({ tokenId: id })
      toast.success('API token deleted successfully')
      fetchTokens()
    } catch (error) {
      toast.error('Failed to delete API token')
    }
  }

  const maskToken = (tokenHash: string) => {
    return `lt_${'*'.repeat(28)}`
  }

  if (loading) {
    return (
      <Layout>
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-48 mb-4"></div>
          <div className="space-y-4">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="bg-white p-6 rounded-lg shadow">
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                <div className="h-4 bg-gray-200 rounded w-1/2"></div>
              </div>
            ))}
          </div>
        </div>
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-2xl font-semibold text-gray-900">API Tokens</h1>
          <p className="mt-2 text-sm text-gray-700">
            Manage your API access tokens
          </p>
        </div>
        <div className="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
          <Link
            href="/api-tokens/new"
            className="btn btn-primary btn-md"
          >
            <PlusIcon className="h-4 w-4 mr-2" />
            New Token
          </Link>
        </div>
      </div>

      <div className="mt-8">
        <div className="bg-white shadow overflow-hidden sm:rounded-md">
          <ul className="divide-y divide-gray-200">
            {tokens.map((token) => (
              <li key={token.id}>
                <div className="px-4 py-4 flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <div className="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center">
                        <span className="text-blue-600 font-medium">
                          {token.name.charAt(0).toUpperCase()}
                        </span>
                      </div>
                    </div>
                    <div className="ml-4">
                      <div className="flex items-center">
                        <p className="text-sm font-medium text-gray-900">
                          {token.name}
                        </p>
                      </div>
                      <div className="mt-1 flex items-center text-sm text-gray-500">
                        <span className="font-mono text-xs bg-gray-100 px-2 py-1 rounded">
                          {maskToken(token.token_hash)}
                        </span>
                        <span className="mx-2">•</span>
                        <span>Created {new Date(token.created_at).toLocaleDateString()}</span>
                        {token.last_used_at && (
                          <>
                            <span className="mx-2">•</span>
                            <span>Last used {new Date(token.last_used_at).toLocaleDateString()}</span>
                          </>
                        )}
                      </div>
                      <div className="mt-1">
                        <div className="flex flex-wrap gap-1">
                          {token.scopes.map((scope) => (
                            <span
                              key={scope}
                              className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800"
                            >
                              {scope}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => {/* View details */}}
                      className="text-primary-600 hover:text-primary-900"
                    >
                      <EyeIcon className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => handleDelete(token.id)}
                      className="text-red-600 hover:text-red-900"
                    >
                      <TrashIcon className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>

        {tokens.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500">No API tokens found</p>
            <Link href="/api-tokens/new" className="btn btn-primary btn-md mt-4">
              Create your first API token
            </Link>
          </div>
        )}
      </div>
    </Layout>
  )
}
