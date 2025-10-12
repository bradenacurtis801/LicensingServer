'use client'

import Layout from '@/components/Layout'
import { useState, useEffect } from 'react'
import { activationFormsApi } from '@/api'
import { toast } from 'react-hot-toast'
import { EyeIcon, CheckIcon, XMarkIcon } from '@heroicons/react/24/outline'
import { format } from 'date-fns'

interface ActivationForm {
  id: number
  request_code: string
  machine_id: string
  machine_name: string
  status: string
  created_at: string
  expires_at: string
  license_key?: {
    id: number
    key_hash: string
    customer?: {
      name: string
    }
    application?: {
      name: string
    }
  }
}

export default function ActivationFormsPage() {
  const [forms, setForms] = useState<ActivationForm[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<'all' | 'pending' | 'approved' | 'rejected'>('all')

  useEffect(() => {
    fetchActivationForms()
  }, [])

  const fetchActivationForms = async () => {
    try {
      const response = await activationFormsApi.listActivationFormsApiV1ActivationFormsGet()
      setForms(response)
    } catch (error) {
      toast.error('Failed to fetch activation forms')
    } finally {
      setLoading(false)
    }
  }

  const handleApprove = async (id: number) => {
    try {
      // Note: Approve/reject functionality may need to be implemented in the backend
      await activationFormsApi.completeActivationFormApiV1ActivationFormsCompletePost({ 
        formId: id,
        activationFormComplete: { status: 'approved' }
      })
      toast.success('Activation form approved')
      fetchActivationForms()
    } catch (error) {
      toast.error('Failed to approve activation form')
    }
  }

  const handleReject = async (id: number) => {
    try {
      // Note: Approve/reject functionality may need to be implemented in the backend
      await activationFormsApi.completeActivationFormApiV1ActivationFormsCompletePost({ 
        formId: id,
        activationFormComplete: { status: 'rejected' }
      })
      toast.success('Activation form rejected')
      fetchActivationForms()
    } catch (error) {
      toast.error('Failed to reject activation form')
    }
  }

  const filteredForms = forms.filter(form => {
    if (filter === 'all') return true
    return form.status === filter
  })

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending':
        return 'bg-yellow-100 text-yellow-800'
      case 'approved':
        return 'bg-green-100 text-green-800'
      case 'rejected':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  if (loading) {
    return (
      <Layout>
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-48 mb-4"></div>
          <div className="space-y-4">
            {[...Array(5)].map((_, i) => (
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
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">Activation Forms</h1>
        <p className="mt-2 text-sm text-gray-700">
          Manage license activation requests
        </p>
      </div>

      <div className="mt-8">
        <div className="mb-6">
          <div className="flex space-x-4">
            {[
              { key: 'all', label: 'All' },
              { key: 'pending', label: 'Pending' },
              { key: 'approved', label: 'Approved' },
              { key: 'rejected', label: 'Rejected' },
            ].map(({ key, label }) => (
              <button
                key={key}
                onClick={() => setFilter(key as any)}
                className={`px-3 py-2 text-sm font-medium rounded-md ${
                  filter === key
                    ? 'bg-primary-100 text-primary-700'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                {label}
              </button>
            ))}
          </div>
        </div>

        <div className="bg-white shadow overflow-hidden sm:rounded-md">
          <ul className="divide-y divide-gray-200">
            {filteredForms.map((form) => (
              <li key={form.id}>
                <div className="px-4 py-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <div className="flex-shrink-0">
                        <div className="h-10 w-10 rounded-full bg-yellow-100 flex items-center justify-center">
                          <span className="text-yellow-600 font-medium">
                            {form.id}
                          </span>
                        </div>
                      </div>
                      <div className="ml-4">
                        <div className="flex items-center">
                          <p className="text-sm font-medium text-gray-900">
                            {form.license_key?.customer?.name || 'Unknown Customer'}
                          </p>
                          <span className={`ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(form.status)}`}>
                            {form.status}
                          </span>
                        </div>
                        <div className="mt-1 flex items-center text-sm text-gray-500">
                          <span>{form.license_key?.application?.name}</span>
                          <span className="mx-2">•</span>
                          <span>Machine: {form.machine_name}</span>
                          <span className="mx-2">•</span>
                          <span>Requested {format(new Date(form.created_at), 'MMM d, yyyy')}</span>
                        </div>
                        <div className="mt-1 text-xs text-gray-400">
                          Request Code: {form.request_code}
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
                      {form.status === 'pending' && (
                        <>
                          <button
                            onClick={() => handleApprove(form.id)}
                            className="text-green-600 hover:text-green-900"
                          >
                            <CheckIcon className="h-4 w-4" />
                          </button>
                          <button
                            onClick={() => handleReject(form.id)}
                            className="text-red-600 hover:text-red-900"
                          >
                            <XMarkIcon className="h-4 w-4" />
                          </button>
                        </>
                      )}
                    </div>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>

        {filteredForms.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500">No activation forms found</p>
          </div>
        )}
      </div>
    </Layout>
  )
}
