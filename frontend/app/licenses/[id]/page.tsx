'use client'

import Layout from '@/components/Layout'
import { useState, useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { licensesApi } from '@/api'
import { LicenseKeyWithRelationsResponse } from '@/generated'
import { toast } from 'react-hot-toast'
import { 
  EyeIcon, 
  PencilIcon, 
  TrashIcon, 
  ArrowLeftIcon,
  CalendarIcon,
  UserIcon,
  CogIcon,
  KeyIcon
} from '@heroicons/react/24/outline'
import Link from 'next/link'

export default function LicenseDetailPage() {
  const params = useParams()
  const router = useRouter()
  const [license, setLicense] = useState<LicenseKeyWithRelationsResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const licenseId = parseInt(params.id as string)

  const fetchLicense = async () => {
    try {
      setLoading(true)
      setError(null)
      
      const response = await licensesApi.getLicenseApiV1LicensesLicenseIdGet({ licenseId: licenseId })
      setLicense(response)
    } catch (err: any) {
      console.error('Error fetching license:', err)
      setError('Failed to fetch license details')
      toast.error('Failed to fetch license details')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (licenseId) {
      fetchLicense()
    }
  }, [licenseId])

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this license? This action cannot be undone.')) return

    try {
      await licensesApi.deleteLicenseApiV1LicensesLicenseIdDelete({ licenseId: licenseId })
      toast.success('License deleted successfully')
      router.push('/licenses')
    } catch (error: any) {
      toast.error('Failed to delete license')
    }
  }

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'active':
        return 'bg-green-100 text-green-800'
      case 'expired':
        return 'bg-red-100 text-red-800'
      case 'blocked':
        return 'bg-yellow-100 text-yellow-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  if (loading) {
    return (
      <Layout>
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-48 mb-4"></div>
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="h-4 bg-gray-200 rounded w-3/4 mb-4"></div>
            <div className="h-4 bg-gray-200 rounded w-1/2 mb-4"></div>
            <div className="h-4 bg-gray-200 rounded w-2/3"></div>
          </div>
        </div>
      </Layout>
    )
  }

  if (error || !license) {
    return (
      <Layout>
        <div className="text-center py-12">
          <h2 className="text-xl font-semibold text-red-600 mb-4">Error Loading License</h2>
          <p className="text-gray-600 mb-4">{error || 'License not found'}</p>
          <div className="space-x-3">
            <button 
              onClick={() => fetchLicense()}
              className="btn btn-primary"
            >
              Try Again
            </button>
            <Link href="/licenses" className="btn btn-secondary">
              Back to Licenses
            </Link>
          </div>
        </div>
      </Layout>
    )
  }

  return (
    <Layout>
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Link
              href="/licenses"
              className="text-gray-400 hover:text-gray-600"
            >
              <ArrowLeftIcon className="h-5 w-5" />
            </Link>
            <div>
              <h1 className="text-2xl font-semibold text-gray-900">License Details</h1>
              <p className="text-sm text-gray-500">License ID: {license.id}</p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <Link
              href={`/licenses/${license.id}/edit`}
              className="btn btn-secondary btn-sm"
            >
              <PencilIcon className="h-4 w-4 mr-1" />
              Edit
            </Link>
            <button
              onClick={handleDelete}
              className="btn btn-danger btn-sm"
            >
              <TrashIcon className="h-4 w-4 mr-1" />
              Delete
            </button>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main License Information */}
        <div className="lg:col-span-2 space-y-6">
          {/* License Key */}
          <div className="bg-white shadow rounded-lg p-6">
            <div className="flex items-center mb-4">
              <KeyIcon className="h-5 w-5 text-gray-400 mr-2" />
              <h3 className="text-lg font-medium text-gray-900">License Key</h3>
            </div>
            <div className="bg-gray-50 p-4 rounded-md">
              <code className="text-sm font-mono break-all">{license.licenseKey}</code>
            </div>
          </div>

          {/* Status and Activation Info */}
          <div className="bg-white shadow rounded-lg p-6">
            <div className="flex items-center mb-4">
              <CogIcon className="h-5 w-5 text-gray-400 mr-2" />
              <h3 className="text-lg font-medium text-gray-900">Status & Activations</h3>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium text-gray-500">Status</label>
                <div className="mt-1">
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(license.status)}`}>
                    {license.status}
                  </span>
                </div>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Activations</label>
                <p className="mt-1 text-sm text-gray-900">
                  {license.currentActivations} / {license.maxActivations}
                </p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Expiration</label>
                <p className="mt-1 text-sm text-gray-900">
                  {license.expiresAt ? new Date(license.expiresAt).toLocaleDateString() : 'Never'}
                </p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Created</label>
                <p className="mt-1 text-sm text-gray-900">
                  {new Date(license.createdAt).toLocaleDateString()}
                </p>
              </div>
            </div>
          </div>

          {/* Features */}
          {license.features && Object.keys(license.features).length > 0 && (
            <div className="bg-white shadow rounded-lg p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Features</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {Object.entries(license.features).map(([feature, enabled]) => (
                  <div key={feature} className="flex items-center justify-between p-3 bg-gray-50 rounded-md">
                    <span className="text-sm font-medium text-gray-900">{feature}</span>
                    <span className={`px-2 py-1 text-xs rounded-full ${
                      enabled ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                    }`}>
                      {enabled ? 'Enabled' : 'Disabled'}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Notes */}
          {license.notes && (
            <div className="bg-white shadow rounded-lg p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Notes</h3>
              <p className="text-sm text-gray-700 whitespace-pre-wrap">{license.notes}</p>
            </div>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Customer Information */}
          <div className="bg-white shadow rounded-lg p-6">
            <div className="flex items-center mb-4">
              <UserIcon className="h-5 w-5 text-gray-400 mr-2" />
              <h3 className="text-lg font-medium text-gray-900">Customer</h3>
            </div>
            {license.customer ? (
              <div className="space-y-3">
                <div>
                  <label className="text-sm font-medium text-gray-500">Name</label>
                  <p className="text-sm text-gray-900">{license.customer.name}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Email</label>
                  <p className="text-sm text-gray-900">{license.customer.email}</p>
                </div>
                {license.customer.company && (
                  <div>
                    <label className="text-sm font-medium text-gray-500">Company</label>
                    <p className="text-sm text-gray-900">{license.customer.company}</p>
                  </div>
                )}
                <div>
                  <label className="text-sm font-medium text-gray-500">Customer Since</label>
                  <p className="text-sm text-gray-900">
                    {new Date(license.customer.createdAt).toLocaleDateString()}
                  </p>
                </div>
              </div>
            ) : (
              <p className="text-sm text-gray-500">No customer information available</p>
            )}
          </div>

          {/* Application Information */}
          <div className="bg-white shadow rounded-lg p-6">
            <div className="flex items-center mb-4">
              <CogIcon className="h-5 w-5 text-gray-400 mr-2" />
              <h3 className="text-lg font-medium text-gray-900">Application</h3>
            </div>
            {license.application ? (
              <div className="space-y-3">
                <div>
                  <label className="text-sm font-medium text-gray-500">Name</label>
                  <p className="text-sm text-gray-900">{license.application.name}</p>
                </div>
                {license.application.version && (
                  <div>
                    <label className="text-sm font-medium text-gray-500">Version</label>
                    <p className="text-sm text-gray-900">{license.application.version}</p>
                  </div>
                )}
                {license.application.description && (
                  <div>
                    <label className="text-sm font-medium text-gray-500">Description</label>
                    <p className="text-sm text-gray-900">{license.application.description}</p>
                  </div>
                )}
                <div>
                  <label className="text-sm font-medium text-gray-500">Created</label>
                  <p className="text-sm text-gray-900">
                    {new Date(license.application.createdAt).toLocaleDateString()}
                  </p>
                </div>
              </div>
            ) : (
              <p className="text-sm text-gray-500">No application information available</p>
            )}
          </div>
        </div>
      </div>
    </Layout>
  )
}
