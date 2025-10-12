'use client'

import Layout from '@/components/Layout'
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { authenticationApi } from '@/api'
import { TokenScope } from '@/generated'
import { toast } from 'react-hot-toast'
import { ClipboardDocumentIcon, CheckIcon } from '@heroicons/react/24/outline'

const SCOPE_GROUPS = [
  {
    label: 'Licenses',
    scopes: [TokenScope.LicenseRead, TokenScope.LicenseWrite, TokenScope.LicenseDelete],
  },
  {
    label: 'Customers',
    scopes: [TokenScope.CustomerRead, TokenScope.CustomerWrite, TokenScope.CustomerDelete],
  },
  {
    label: 'Applications',
    scopes: [TokenScope.ApplicationRead, TokenScope.ApplicationWrite, TokenScope.ApplicationDelete],
  },
  {
    label: 'Activations',
    scopes: [TokenScope.ActivationRead, TokenScope.ActivationWrite, TokenScope.ActivationDelete],
  },
  {
    label: 'Other',
    scopes: [TokenScope.Validation, TokenScope.UserManagement, TokenScope.TokenManagement],
  },
]

export default function NewAPITokenPage() {
  const router = useRouter()
  const [name, setName] = useState('')
  const [nameError, setNameError] = useState('')
  const [selectedScopes, setSelectedScopes] = useState<Set<TokenScope>>(new Set())
  const [scopeError, setScopeError] = useState('')
  const [expiresAt, setExpiresAt] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [createdToken, setCreatedToken] = useState<string | null>(null)
  const [copied, setCopied] = useState(false)

  const toggleScope = (scope: TokenScope) => {
    setSelectedScopes(prev => {
      const next = new Set(prev)
      next.has(scope) ? next.delete(scope) : next.add(scope)
      return next
    })
    setScopeError('')
  }

  const toggleGroup = (scopes: TokenScope[]) => {
    const allSelected = scopes.every(s => selectedScopes.has(s))
    setSelectedScopes(prev => {
      const next = new Set(prev)
      scopes.forEach(s => allSelected ? next.delete(s) : next.add(s))
      return next
    })
    setScopeError('')
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    let valid = true
    if (!name.trim()) {
      setNameError('Token name is required')
      valid = false
    }
    if (selectedScopes.size === 0) {
      setScopeError('Select at least one scope')
      valid = false
    }
    if (!valid) return

    setSubmitting(true)
    try {
      const result = await authenticationApi.createApiTokenApiV1AuthTokensPost({
        aPITokenCreate: {
          name: name.trim(),
          scopes: Array.from(selectedScopes),
          expiresAt: expiresAt ? new Date(expiresAt) : undefined,
        },
      })
      setCreatedToken(result.token)
    } catch (error: any) {
      toast.error(error.message || 'Failed to create token')
    } finally {
      setSubmitting(false)
    }
  }

  const copyToken = async () => {
    if (!createdToken) return
    await navigator.clipboard.writeText(createdToken)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  // One-time token display shown after creation
  if (createdToken) {
    return (
      <Layout>
        <div className="max-w-2xl">
          <h1 className="text-2xl font-semibold text-gray-900">Token Created</h1>
          <p className="mt-2 text-sm text-gray-600">
            Copy your token now. It will not be shown again.
          </p>

          <div className="mt-6 bg-white shadow sm:rounded-lg p-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">Your API Token</label>
            <div className="flex items-center gap-2">
              <code className="flex-1 block bg-gray-50 border border-gray-200 rounded px-3 py-2 text-sm font-mono break-all">
                {createdToken}
              </code>
              <button
                onClick={copyToken}
                className="flex-shrink-0 btn btn-secondary btn-md"
              >
                {copied
                  ? <CheckIcon className="h-4 w-4 text-green-600" />
                  : <ClipboardDocumentIcon className="h-4 w-4" />
                }
              </button>
            </div>
          </div>

          <div className="mt-6 flex gap-3">
            <button onClick={() => router.push('/api-tokens')} className="btn btn-primary btn-md">
              Done
            </button>
          </div>
        </div>
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="max-w-2xl">
        <h1 className="text-2xl font-semibold text-gray-900">New API Token</h1>
        <p className="mt-2 text-sm text-gray-700">
          Give your token a descriptive name so you can identify it later.
        </p>

        <form onSubmit={handleSubmit} className="mt-8 space-y-6">
          {/* Name */}
          <div className="bg-white shadow px-4 py-5 sm:rounded-lg sm:p-6">
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Token Name <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  className="mt-1 input"
                  placeholder="e.g. Production SDK, CI Pipeline"
                  value={name}
                  onChange={e => { setName(e.target.value); setNameError('') }}
                />
                {nameError && <p className="mt-1 text-sm text-red-600">{nameError}</p>}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">Expiry Date</label>
                <input
                  type="date"
                  className="mt-1 input"
                  value={expiresAt}
                  onChange={e => setExpiresAt(e.target.value)}
                />
                <p className="mt-1 text-xs text-gray-500">Leave blank for no expiry.</p>
              </div>
            </div>
          </div>

          {/* Scopes */}
          <div className="bg-white shadow px-4 py-5 sm:rounded-lg sm:p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-sm font-medium text-gray-900">
                Scopes <span className="text-red-500">*</span>
              </h2>
              {scopeError && <p className="text-sm text-red-600">{scopeError}</p>}
            </div>

            <div className="space-y-4">
              {SCOPE_GROUPS.map(group => {
                const allSelected = group.scopes.every(s => selectedScopes.has(s))
                return (
                  <div key={group.label}>
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs font-semibold text-gray-500 uppercase tracking-wide">
                        {group.label}
                      </span>
                      <button
                        type="button"
                        onClick={() => toggleGroup(group.scopes)}
                        className="text-xs text-primary-600 hover:underline"
                      >
                        {allSelected ? 'Deselect all' : 'Select all'}
                      </button>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {group.scopes.map(scope => (
                        <label
                          key={scope}
                          className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium cursor-pointer border transition-colors ${
                            selectedScopes.has(scope)
                              ? 'bg-blue-50 border-blue-300 text-blue-700'
                              : 'bg-gray-50 border-gray-200 text-gray-600 hover:border-gray-300'
                          }`}
                        >
                          <input
                            type="checkbox"
                            className="sr-only"
                            checked={selectedScopes.has(scope)}
                            onChange={() => toggleScope(scope)}
                          />
                          {scope}
                        </label>
                      ))}
                    </div>
                  </div>
                )
              })}
            </div>
          </div>

          <div className="flex justify-end gap-3">
            <button type="button" onClick={() => router.push('/api-tokens')} className="btn btn-secondary btn-md">
              Cancel
            </button>
            <button type="submit" disabled={submitting} className="btn btn-primary btn-md">
              {submitting ? 'Creating...' : 'Create Token'}
            </button>
          </div>
        </form>
      </div>
    </Layout>
  )
}
