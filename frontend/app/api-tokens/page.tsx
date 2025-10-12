'use client'

import Layout from '@/components/Layout'
import { useState, useEffect } from 'react'
import { authenticationApi } from '@/api'
import { APITokenResponse } from '@/generated'
import Link from 'next/link'
import { PlusIcon, EyeIcon, EyeSlashIcon, TrashIcon } from '@heroicons/react/24/outline'
import { toast } from 'react-hot-toast'

export default function APITokensPage() {
  const [tokens, setTokens] = useState<APITokenResponse[]>([])
  const [loading, setLoading] = useState(true)
  const [expandedId, setExpandedId] = useState<number | null>(null)

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
      toast.success('API token deleted')
      fetchTokens()
    } catch (error) {
      toast.error('Failed to delete API token')
    }
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
          <p className="mt-2 text-sm text-gray-700">Manage your API access tokens</p>
        </div>
        <div className="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
          <Link href="/api-tokens/new" className="btn btn-primary btn-md">
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
                  <div className="flex items-center min-w-0">
                    <div className="flex-shrink-0 h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center">
                      <span className="text-blue-600 font-medium">
                        {token.name.charAt(0).toUpperCase()}
                      </span>
                    </div>
                    <div className="ml-4 min-w-0">
                      <p className="text-sm font-medium text-gray-900">{token.name}</p>
                      <p className="text-sm text-gray-500">
                        Created {new Date(token.createdAt).toLocaleDateString()}
                        {token.lastUsedAt && (
                          <> &middot; Last used {new Date(token.lastUsedAt).toLocaleDateString()}</>
                        )}
                        {!token.isActive && (
                          <span className="ml-2 inline-flex px-2 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-700">Inactive</span>
                        )}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2 ml-4">
                    <button
                      onClick={() => setExpandedId(expandedId === token.id ? null : token.id)}
                      className="text-gray-400 hover:text-gray-600"
                      title={expandedId === token.id ? 'Collapse' : 'View details'}
                    >
                      {expandedId === token.id
                        ? <EyeSlashIcon className="h-4 w-4" />
                        : <EyeIcon className="h-4 w-4" />
                      }
                    </button>
                    <button
                      onClick={() => handleDelete(token.id)}
                      className="text-red-400 hover:text-red-600"
                    >
                      <TrashIcon className="h-4 w-4" />
                    </button>
                  </div>
                </div>

                {expandedId === token.id && (
                  <div className="px-4 pb-4 ml-14 border-t border-gray-100 pt-3">
                    <dl className="grid grid-cols-2 gap-x-8 gap-y-2 text-sm sm:grid-cols-4">
                      <div>
                        <dt className="text-gray-500">Status</dt>
                        <dd className="font-medium text-gray-900">{token.isActive ? 'Active' : 'Inactive'}</dd>
                      </div>
                      <div>
                        <dt className="text-gray-500">Expires</dt>
                        <dd className="font-medium text-gray-900">
                          {token.expiresAt ? new Date(token.expiresAt).toLocaleDateString() : 'Never'}
                        </dd>
                      </div>
                      <div>
                        <dt className="text-gray-500">Created</dt>
                        <dd className="font-medium text-gray-900">{new Date(token.createdAt).toLocaleDateString()}</dd>
                      </div>
                      <div>
                        <dt className="text-gray-500">Last used</dt>
                        <dd className="font-medium text-gray-900">
                          {token.lastUsedAt ? new Date(token.lastUsedAt).toLocaleDateString() : 'Never'}
                        </dd>
                      </div>
                    </dl>
                    <div className="mt-3">
                      <p className="text-xs text-gray-500 mb-1">Scopes</p>
                      <div className="flex flex-wrap gap-1">
                        {token.scopes.map((scope) => (
                          <span
                            key={scope}
                            className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-50 text-blue-700"
                          >
                            {scope}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
              </li>
            ))}
          </ul>
        </div>

        {tokens.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500">No API tokens found</p>
            <Link href="/api-tokens/new" className="btn btn-primary btn-md mt-4">
              Create your first token
            </Link>
          </div>
        )}
      </div>
    </Layout>
  )
}
