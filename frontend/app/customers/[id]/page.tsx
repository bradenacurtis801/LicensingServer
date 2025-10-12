'use client'

import Layout from '@/components/Layout'
import { useState, useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { customersApi, licensesApi } from '@/api'
import { CustomerResponse, LicenseKeyWithRelationsResponse } from '@/generated'
import Link from 'next/link'
import { PencilIcon, TrashIcon, PlusIcon } from '@heroicons/react/24/outline'
import { toast } from 'react-hot-toast'

export default function CustomerDetailPage() {
  const { id } = useParams()
  const router = useRouter()
  const customerId = Number(id)

  const [customer, setCustomer] = useState<CustomerResponse | null>(null)
  const [licenses, setLicenses] = useState<LicenseKeyWithRelationsResponse[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchData()
  }, [customerId])

  const fetchData = async () => {
    try {
      const [customerData, allLicenses] = await Promise.all([
        customersApi.getCustomerApiV1CustomersCustomerIdGet({ customerId }),
        licensesApi.listLicensesApiV1LicensesGet({ includeRelations: true }),
      ])
      setCustomer(customerData)
      setLicenses(allLicenses.filter(l => l.customerId === customerId))
    } catch (error) {
      toast.error('Failed to load customer')
      router.push('/customers')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async () => {
    if (!confirm(`Delete customer "${customer?.name}"? This cannot be undone.`)) return
    try {
      await customersApi.deleteCustomerApiV1CustomersCustomerIdDelete({ customerId })
      toast.success('Customer deleted')
      router.push('/customers')
    } catch {
      toast.error('Failed to delete customer')
    }
  }

  if (loading) {
    return (
      <Layout>
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-200 rounded w-64" />
          <div className="h-4 bg-gray-200 rounded w-48" />
          <div className="h-32 bg-gray-200 rounded" />
        </div>
      </Layout>
    )
  }

  if (!customer) return null

  return (
    <Layout>
      {/* Header */}
      <div className="sm:flex sm:items-center sm:justify-between">
        <div>
          <div className="flex items-center space-x-3">
            <div className="h-12 w-12 rounded-full bg-purple-100 flex items-center justify-center">
              <span className="text-purple-600 text-lg font-semibold">
                {customer.name.charAt(0).toUpperCase()}
              </span>
            </div>
            <div>
              <h1 className="text-2xl font-semibold text-gray-900">{customer.name}</h1>
              <p className="text-sm text-gray-500">{customer.email}</p>
            </div>
          </div>
        </div>
        <div className="mt-4 sm:mt-0 flex space-x-3">
          <Link href={`/customers/${customerId}/edit`} className="btn btn-secondary btn-md">
            <PencilIcon className="h-4 w-4 mr-2" />
            Edit
          </Link>
          <button onClick={handleDelete} className="btn btn-danger btn-md">
            <TrashIcon className="h-4 w-4 mr-2" />
            Delete
          </button>
        </div>
      </div>

      {/* Details */}
      <div className="mt-8 bg-white shadow sm:rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Details</h2>
          <dl className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <dt className="text-sm font-medium text-gray-500">Company</dt>
              <dd className="mt-1 text-sm text-gray-900">{customer.company || '—'}</dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-gray-500">Customer since</dt>
              <dd className="mt-1 text-sm text-gray-900">
                {new Date(customer.createdAt).toLocaleDateString()}
              </dd>
            </div>
          </dl>
        </div>
      </div>

      {/* Licenses */}
      <div className="mt-8">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-medium text-gray-900">
            Licenses <span className="text-gray-400 font-normal">({licenses.length})</span>
          </h2>
          <Link href={`/licenses/new?customerId=${customerId}`} className="btn btn-primary btn-sm">
            <PlusIcon className="h-4 w-4 mr-1" />
            New License
          </Link>
        </div>

        {licenses.length === 0 ? (
          <div className="text-center py-10 bg-white shadow sm:rounded-lg">
            <p className="text-gray-500 text-sm">No licenses for this customer.</p>
          </div>
        ) : (
          <div className="bg-white shadow overflow-hidden sm:rounded-lg">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">License Key</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Application</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Activations</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Expires</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {licenses.map(lic => (
                  <tr key={lic.id}>
                    <td className="px-6 py-4 text-sm font-mono text-gray-900">
                      <Link href={`/licenses/${lic.id}`} className="text-primary-600 hover:underline">
                        {lic.licenseKey.slice(0, 20)}…
                      </Link>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-700">
                      {lic.application?.name ?? lic.applicationId}
                    </td>
                    <td className="px-6 py-4 text-sm">
                      <span className={`inline-flex px-2 py-0.5 rounded-full text-xs font-medium ${
                        lic.status === 'active' ? 'bg-green-100 text-green-800' :
                        lic.status === 'expired' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {lic.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-700">
                      {lic.currentActivations} / {lic.maxActivations}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-700">
                      {lic.expiresAt ? new Date(lic.expiresAt).toLocaleDateString() : 'Never'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <div className="mt-6">
        <Link href="/customers" className="text-sm text-gray-500 hover:text-gray-700">
          ← Back to Customers
        </Link>
      </div>
    </Layout>
  )
}
