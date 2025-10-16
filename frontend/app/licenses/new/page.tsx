'use client'

import Layout from '@/components/Layout'
import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { licensesApi, customersApi, applicationsApi } from '@/api'
import { CustomerResponse, ApplicationResponse } from '@/generated'
import { toast } from 'react-hot-toast'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const createLicenseSchema = z.object({
  customerId: z.number().min(1, 'Customer is required'),
  applicationId: z.number().min(1, 'Application is required'),
  maxActivations: z.number().min(1, 'Max activations must be at least 1'),
  expiresAt: z.string().optional(),
  features: z.record(z.boolean()).optional(),
  notes: z.string().optional(),
})

type CreateLicenseForm = z.infer<typeof createLicenseSchema>


export default function NewLicensePage() {
  const router = useRouter()
  const [customers, setCustomers] = useState<CustomerResponse[]>([])
  const [applications, setApplications] = useState<ApplicationResponse[]>([])
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
  } = useForm<CreateLicenseForm>({
    resolver: zodResolver(createLicenseSchema),
  })

  const selectedApplicationId = watch('applicationId')

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [customersRes, applicationsRes] = await Promise.all([
        customersApi.listCustomersApiV1CustomersGet(),
        applicationsApi.listApplicationsApiV1ApplicationsGet(),
      ])
      setCustomers(customersRes)
      setApplications(applicationsRes)
    } catch (error) {
      toast.error('Failed to fetch data')
    } finally {
      setLoading(false)
    }
  }

  const onSubmit = async (data: CreateLicenseForm) => {
    setSubmitting(true)
    try {
      const licenseData = {
        ...data,
        expiresAt: data.expiresAt ? new Date(data.expiresAt) : null
      }
      const response = await licensesApi.createLicenseApiV1LicensesPost({
        licenseKeyCreate: licenseData
      })
      toast.success('License created successfully')
      router.push(`/licenses/${response.id}`)
    } catch (error: any) {
      toast.error(error.message || 'Failed to create license')
    } finally {
      setSubmitting(false)
    }
  }

  const selectedApplication = applications.find(app => app.id === selectedApplicationId)

  if (loading) {
    return (
      <Layout>
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-48 mb-6"></div>
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="space-y-4">
              <div className="h-4 bg-gray-200 rounded w-1/4"></div>
              <div className="h-10 bg-gray-200 rounded"></div>
              <div className="h-4 bg-gray-200 rounded w-1/4"></div>
              <div className="h-10 bg-gray-200 rounded"></div>
            </div>
          </div>
        </div>
      </Layout>
    )
  }

  return (
    <Layout>
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">Create New License</h1>
        <p className="mt-2 text-sm text-gray-700">
          Generate a new license key for a customer
        </p>
      </div>

      <div className="mt-8">
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div className="bg-white shadow px-4 py-5 sm:rounded-lg sm:p-6">
            <div className="grid grid-cols-1 gap-6">
              <div>
                <label htmlFor="customer_id" className="block text-sm font-medium text-gray-700">
                  Customer *
                </label>
                <select
                  {...register('customerId', { valueAsNumber: true })}
                  className="mt-1 input"
                >
                  <option value="">Select a customer</option>
                  {customers.map((customer) => (
                    <option key={customer.id} value={customer.id}>
                      {customer.name} ({customer.email})
                    </option>
                  ))}
                </select>
                {errors.customerId && (
                  <p className="mt-1 text-sm text-red-600">{errors.customerId.message}</p>
                )}
              </div>

              <div>
                <label htmlFor="application_id" className="block text-sm font-medium text-gray-700">
                  Application *
                </label>
                <select
                  {...register('applicationId', { valueAsNumber: true })}
                  className="mt-1 input"
                >
                  <option value="">Select an application</option>
                  {applications.map((app) => (
                    <option key={app.id} value={app.id}>
                      {app.name}
                    </option>
                  ))}
                </select>
                {errors.applicationId && (
                  <p className="mt-1 text-sm text-red-600">{errors.applicationId.message}</p>
                )}
              </div>

              <div>
                <label htmlFor="max_activations" className="block text-sm font-medium text-gray-700">
                  Max Activations *
                </label>
                <input
                  type="number"
                  {...register('maxActivations', { valueAsNumber: true })}
                  className="mt-1 input"
                  min="1"
                  defaultValue="1"
                />
                {errors.maxActivations && (
                  <p className="mt-1 text-sm text-red-600">{errors.maxActivations.message}</p>
                )}
              </div>

              <div>
                <label htmlFor="expires_at" className="block text-sm font-medium text-gray-700">
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

              <div>
                <label htmlFor="notes" className="block text-sm font-medium text-gray-700">
                  Notes
                </label>
                <textarea
                  {...register('notes')}
                  rows={3}
                  className="mt-1 input"
                  placeholder="Optional notes about this license"
                />
              </div>
            </div>
          </div>

          <div className="flex justify-end space-x-3">
            <button
              type="button"
              onClick={() => router.back()}
              className="btn btn-secondary btn-md"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={submitting}
              className="btn btn-primary btn-md"
            >
              {submitting ? 'Creating...' : 'Create License'}
            </button>
          </div>
        </form>
      </div>
    </Layout>
  )
}
