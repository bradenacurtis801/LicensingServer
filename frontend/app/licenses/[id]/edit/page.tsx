'use client'

import Layout from '@/components/Layout'
import { useState, useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { licensesApi, customersApi, applicationsApi } from '@/api'
import { LicenseKeyWithRelationsResponse, CustomerResponse, ApplicationResponse, LicenseKeyUpdate } from '@/generated'
import { toast } from 'react-hot-toast'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { ArrowLeftIcon } from '@heroicons/react/24/outline'
import Link from 'next/link'

const updateLicenseSchema = z.object({
  maxActivations: z.number().min(1, 'Max activations must be at least 1'),
  expiresAt: z.string().optional(),
  features: z.record(z.boolean()).optional(),
  notes: z.string().optional(),
})

type UpdateLicenseForm = z.infer<typeof updateLicenseSchema>

export default function EditLicensePage() {
  const params = useParams()
  const router = useRouter()
  const [license, setLicense] = useState<LicenseKeyWithRelationsResponse | null>(null)
  const [customers, setCustomers] = useState<CustomerResponse[]>([])
  const [applications, setApplications] = useState<ApplicationResponse[]>([])
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const licenseId = parseInt(params.id as string)

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    watch,
  } = useForm<UpdateLicenseForm>({
    resolver: zodResolver(updateLicenseSchema),
  })

  const fetchData = async () => {
    try {
      setLoading(true)
      setError(null)

      // Fetch license details
      const licenseResponse = await licensesApi.getLicenseApiV1LicensesLicenseIdGet({ licenseId: licenseId })
      setLicense(licenseResponse)

      // Fetch customers and applications for reference
      const [customersResponse, applicationsResponse] = await Promise.all([
        customersApi.listCustomersApiV1CustomersGet(),
        applicationsApi.listApplicationsApiV1ApplicationsGet()
      ])
      
      setCustomers(customersResponse)
      setApplications(applicationsResponse)

      // Reset form with current license data
      reset({
        maxActivations: licenseResponse.maxActivations,
        expiresAt: licenseResponse.expiresAt ? new Date(licenseResponse.expiresAt).toISOString().slice(0, 16) : '',
        features: licenseResponse.features || {},
        notes: licenseResponse.notes || '',
      })
    } catch (err: any) {
      console.error('Error fetching data:', err)
      setError('Failed to fetch license details')
      toast.error('Failed to fetch license details')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (licenseId) {
      fetchData()
    }
  }, [licenseId])

  const onSubmit = async (data: UpdateLicenseForm) => {
    setSubmitting(true)
    try {
      const updateData: LicenseKeyUpdate = {
        maxActivations: data.maxActivations,
        expiresAt: data.expiresAt ? new Date(data.expiresAt) : null,
        features: data.features,
        notes: data.notes,
      }

      await licensesApi.updateLicenseApiV1LicensesLicenseIdPut({
        licenseId: licenseId,
        licenseKeyUpdate: updateData
      })
      
      toast.success('License updated successfully')
      router.push(`/licenses/${licenseId}`)
    } catch (error: any) {
      toast.error(error.message || 'Failed to update license')
    } finally {
      setSubmitting(false)
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
              onClick={() => fetchData()}
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
        <div className="flex items-center space-x-3">
          <Link
            href={`/licenses/${licenseId}`}
            className="text-gray-400 hover:text-gray-600"
          >
            <ArrowLeftIcon className="h-5 w-5" />
          </Link>
          <div>
            <h1 className="text-2xl font-semibold text-gray-900">Edit License</h1>
            <p className="text-sm text-gray-500">License ID: {license.id}</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Edit Form */}
        <div className="lg:col-span-2">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <div className="bg-white shadow px-4 py-5 sm:rounded-lg sm:p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-6">License Settings</h3>
              
              <div className="grid grid-cols-1 gap-6">
                {/* Max Activations */}
                <div>
                  <label htmlFor="maxActivations" className="block text-sm font-medium text-gray-700">
                    Max Activations *
                  </label>
                  <input
                    type="number"
                    {...register('maxActivations', { valueAsNumber: true })}
                    className="mt-1 input"
                    min="1"
                  />
                  {errors.maxActivations && (
                    <p className="mt-1 text-sm text-red-600">{errors.maxActivations.message}</p>
                  )}
                </div>

                {/* Expiration Date */}
                <div>
                  <label htmlFor="expiresAt" className="block text-sm font-medium text-gray-700">
                    Expiration Date
                  </label>
                  <input
                    type="datetime-local"
                    {...register('expiresAt')}
                    className="mt-1 input"
                  />
                  <p className="mt-1 text-sm text-gray-500">
                    Leave empty for no expiration
                  </p>
                </div>

                {/* Features */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-3">
                    Features
                  </label>
                  <div className="space-y-2">
                    {license.application?.features && typeof license.application.features === 'object' ? (
                      Object.entries(license.application.features).map(([feature, _]) => (
                        <div key={feature} className="flex items-center justify-between p-3 bg-gray-50 rounded-md">
                          <span className="text-sm font-medium text-gray-900">{feature}</span>
                          <input
                            type="checkbox"
                            {...register(`features.${feature}`)}
                            className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                          />
                        </div>
                      ))
                    ) : (
                      <p className="text-sm text-gray-500">No features available for this application</p>
                    )}
                  </div>
                </div>

                {/* Notes */}
                <div>
                  <label htmlFor="notes" className="block text-sm font-medium text-gray-700">
                    Notes
                  </label>
                  <textarea
                    {...register('notes')}
                    rows={4}
                    className="mt-1 input"
                    placeholder="Add any additional notes about this license..."
                  />
                </div>
              </div>
            </div>

            <div className="flex justify-end space-x-3">
              <Link
                href={`/licenses/${licenseId}`}
                className="btn btn-secondary btn-md"
              >
                Cancel
              </Link>
              <button
                type="submit"
                disabled={submitting}
                className="btn btn-primary btn-md"
              >
                {submitting ? 'Updating...' : 'Update License'}
              </button>
            </div>
          </form>
        </div>

        {/* Sidebar - Read-only Info */}
        <div className="space-y-6">
          {/* License Key (Read-only) */}
          <div className="bg-white shadow rounded-lg p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">License Key</h3>
            <div className="bg-gray-50 p-3 rounded-md">
              <code className="text-xs font-mono break-all">{license.licenseKey}</code>
            </div>
            <p className="mt-2 text-xs text-gray-500">License key cannot be changed</p>
          </div>

          {/* Customer (Read-only) */}
          <div className="bg-white shadow rounded-lg p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Customer</h3>
            {license.customer ? (
              <div className="space-y-2">
                <p className="text-sm font-medium text-gray-900">{license.customer.name}</p>
                <p className="text-sm text-gray-500">{license.customer.email}</p>
                {license.customer.company && (
                  <p className="text-sm text-gray-500">{license.customer.company}</p>
                )}
              </div>
            ) : (
              <p className="text-sm text-gray-500">No customer information</p>
            )}
            <p className="mt-2 text-xs text-gray-500">Customer cannot be changed</p>
          </div>

          {/* Application (Read-only) */}
          <div className="bg-white shadow rounded-lg p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Application</h3>
            {license.application ? (
              <div className="space-y-2">
                <p className="text-sm font-medium text-gray-900">{license.application.name}</p>
                {license.application.version && (
                  <p className="text-sm text-gray-500">v{license.application.version}</p>
                )}
                {license.application.description && (
                  <p className="text-sm text-gray-500">{license.application.description}</p>
                )}
              </div>
            ) : (
              <p className="text-sm text-gray-500">No application information</p>
            )}
            <p className="mt-2 text-xs text-gray-500">Application cannot be changed</p>
          </div>

          {/* Current Status */}
          <div className="bg-white shadow rounded-lg p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Current Status</h3>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm text-gray-500">Status:</span>
                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                  license.status === 'active' 
                    ? 'bg-green-100 text-green-800'
                    : license.status === 'expired'
                    ? 'bg-red-100 text-red-800'
                    : 'bg-gray-100 text-gray-800'
                }`}>
                  {license.status}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-500">Activations:</span>
                <span className="text-sm text-gray-900">
                  {license.currentActivations} / {license.maxActivations}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-500">Created:</span>
                <span className="text-sm text-gray-900">
                  {new Date(license.createdAt).toLocaleDateString()}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  )
}
