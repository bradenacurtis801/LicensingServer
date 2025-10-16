'use client'

import Layout from '@/components/Layout'
import { useState, useEffect } from 'react'
import { customersApi } from '@/api'
import { CustomerResponse } from '@/generated'
import Link from 'next/link'
import { PlusIcon, EyeIcon, PencilIcon, TrashIcon } from '@heroicons/react/24/outline'
import { toast } from 'react-hot-toast'

export default function CustomersPage() {
  const [customers, setCustomers] = useState<CustomerResponse[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    fetchCustomers()
  }, [])

  const fetchCustomers = async () => {
    try {
      const response = await customersApi.listCustomersApiV1CustomersGet()
      // Map CustomerResponse to Customer interface
      setCustomers(response)
    } catch (error) {
      toast.error('Failed to fetch customers')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this customer?')) return

    try {
      await customersApi.deleteCustomerApiV1CustomersCustomerIdDelete({ customerId: id })
      toast.success('Customer deleted successfully')
      fetchCustomers()
    } catch (error) {
      toast.error('Failed to delete customer')
    }
  }

  const filteredCustomers = customers.filter(customer =>
    customer.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    customer.email.toLowerCase().includes(searchTerm.toLowerCase())
  )

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
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-2xl font-semibold text-gray-900">Customers</h1>
          <p className="mt-2 text-sm text-gray-700">
            Manage your customer accounts
          </p>
        </div>
        <div className="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
          <Link
            href="/customers/new"
            className="btn btn-primary btn-md"
          >
            <PlusIcon className="h-4 w-4 mr-2" />
            New Customer
          </Link>
        </div>
      </div>

      <div className="mt-8">
        <div className="mb-4">
          <input
            type="text"
            placeholder="Search customers..."
            className="input max-w-md"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        <div className="bg-white shadow overflow-hidden sm:rounded-md">
          <ul className="divide-y divide-gray-200">
            {filteredCustomers.map((customer) => (
              <li key={customer.id}>
                <div className="px-4 py-4 flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <div className="h-10 w-10 rounded-full bg-purple-100 flex items-center justify-center">
                        <span className="text-purple-600 font-medium">
                          {customer.name.charAt(0).toUpperCase()}
                        </span>
                      </div>
                    </div>
                    <div className="ml-4">
                      <div className="flex items-center">
                        <p className="text-sm font-medium text-gray-900">
                          {customer.name}
                        </p>
                      </div>
                      <div className="mt-1 flex items-center text-sm text-gray-500">
                        <span>{customer.email}</span>
                        <span className="mx-2">•</span>
                        <span>Joined {new Date(customer.createdAt).toLocaleDateString()}</span>
                        {customer.company && (
                          <>
                            <span className="mx-2">•</span>
                            <span>{customer.company}</span>
                          </>
                        )}
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Link
                      href={`/customers/${customer.id}`}
                      className="text-primary-600 hover:text-primary-900"
                    >
                      <EyeIcon className="h-4 w-4" />
                    </Link>
                    <Link
                      href={`/customers/${customer.id}/edit`}
                      className="text-gray-600 hover:text-gray-900"
                    >
                      <PencilIcon className="h-4 w-4" />
                    </Link>
                    <button
                      onClick={() => handleDelete(customer.id)}
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

        {filteredCustomers.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500">No customers found</p>
            <Link href="/customers/new" className="btn btn-primary btn-md mt-4">
              Add your first customer
            </Link>
          </div>
        )}
      </div>
    </Layout>
  )
}
