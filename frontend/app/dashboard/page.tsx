'use client'

import Layout from '@/components/Layout'
import { useAuth } from '@/contexts/AuthContext'
import { useEffect, useState } from 'react'
import { licensesApi, customersApi, applicationsApi } from '@/api'
import {
  KeyIcon,
  UsersIcon,
  CogIcon,
  ClipboardDocumentListIcon,
} from '@heroicons/react/24/outline'

interface DashboardStats {
  total_licenses: number
  active_licenses: number
  total_customers: number
  total_applications: number
  pending_activation_forms: number
}

export default function DashboardPage() {
  const { user } = useAuth()
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      // Fetch real data from APIs
      const [licensesResponse, customersResponse, applicationsResponse] = await Promise.all([
        licensesApi.listLicensesApiV1LicensesGet(),
        customersApi.listCustomersApiV1CustomersGet(),
        applicationsApi.listApplicationsApiV1ApplicationsGet()
      ])

      // Count active licenses
      const activeLicenses = licensesResponse.filter(license => license.status === 'active').length

      setStats({
        total_licenses: licensesResponse.length,
        active_licenses: activeLicenses,
        total_customers: customersResponse.length,
        total_applications: applicationsResponse.length,
        pending_activation_forms: 0, // This would need a separate endpoint
      })
    } catch (error) {
      console.error('Failed to fetch dashboard stats:', error)
      // Set zeros on error
      setStats({
        total_licenses: 0,
        active_licenses: 0,
        total_customers: 0,
        total_applications: 0,
        pending_activation_forms: 0,
      })
    } finally {
      setLoading(false)
    }
  }

  const statCards = [
    {
      name: 'Total Licenses',
      value: stats?.total_licenses || 0,
      icon: KeyIcon,
      color: 'bg-blue-500',
    },
    {
      name: 'Active Licenses',
      value: stats?.active_licenses || 0,
      icon: KeyIcon,
      color: 'bg-green-500',
    },
    {
      name: 'Customers',
      value: stats?.total_customers || 0,
      icon: UsersIcon,
      color: 'bg-purple-500',
    },
    {
      name: 'Applications',
      value: stats?.total_applications || 0,
      icon: CogIcon,
      color: 'bg-orange-500',
    },
    {
      name: 'Pending Activations',
      value: stats?.pending_activation_forms || 0,
      icon: ClipboardDocumentListIcon,
      color: 'bg-yellow-500',
    },
  ]

  if (loading) {
    return (
      <Layout>
        <div className="animate-pulse">
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="bg-white overflow-hidden shadow rounded-lg">
                <div className="p-5">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <div className="w-8 h-8 bg-gray-200 rounded"></div>
                    </div>
                    <div className="ml-5 w-0 flex-1">
                      <dl>
                        <dt className="text-sm font-medium text-gray-500 truncate">
                          <div className="h-4 bg-gray-200 rounded w-24"></div>
                        </dt>
                        <dd className="text-lg font-medium text-gray-900">
                          <div className="h-6 bg-gray-200 rounded w-16 mt-1"></div>
                        </dd>
                      </dl>
                    </div>
                  </div>
                </div>
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
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-1 text-sm text-gray-500">
          Welcome to your license management system
        </p>
      </div>

      <div className="mt-8">
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {statCards.map((card) => (
            <div key={card.name} className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className={`w-8 h-8 ${card.color} rounded-md flex items-center justify-center`}>
                      <card.icon className="w-5 h-5 text-white" />
                    </div>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">
                        {card.name}
                      </dt>
                      <dd className="text-lg font-medium text-gray-900">
                        {card.value.toLocaleString()}
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="mt-8">
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900">
              Quick Actions
            </h3>
            <div className="mt-5">
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
                <a
                  href="/licenses/new"
                  className="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-primary-500 rounded-lg border border-gray-200 hover:border-gray-300"
                >
                  <div>
                    <span className="rounded-lg inline-flex p-3 bg-primary-50 text-primary-600">
                      <KeyIcon className="h-6 w-6" />
                    </span>
                  </div>
                  <div className="mt-4">
                    <h3 className="text-lg font-medium">
                      <span className="absolute inset-0" aria-hidden="true" />
                      Create License
                    </h3>
                    <p className="mt-2 text-sm text-gray-500">
                      Generate a new license key for a customer
                    </p>
                  </div>
                </a>

                <a
                  href="/customers/new"
                  className="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-primary-500 rounded-lg border border-gray-200 hover:border-gray-300"
                >
                  <div>
                    <span className="rounded-lg inline-flex p-3 bg-purple-50 text-purple-600">
                      <UsersIcon className="h-6 w-6" />
                    </span>
                  </div>
                  <div className="mt-4">
                    <h3 className="text-lg font-medium">
                      <span className="absolute inset-0" aria-hidden="true" />
                      Add Customer
                    </h3>
                    <p className="mt-2 text-sm text-gray-500">
                      Register a new customer in the system
                    </p>
                  </div>
                </a>

                <a
                  href="/applications/new"
                  className="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-primary-500 rounded-lg border border-gray-200 hover:border-gray-300"
                >
                  <div>
                    <span className="rounded-lg inline-flex p-3 bg-orange-50 text-orange-600">
                      <CogIcon className="h-6 w-6" />
                    </span>
                  </div>
                  <div className="mt-4">
                    <h3 className="text-lg font-medium">
                      <span className="absolute inset-0" aria-hidden="true" />
                      Register App
                    </h3>
                    <p className="mt-2 text-sm text-gray-500">
                      Register a new application for licensing
                    </p>
                  </div>
                </a>

                <a
                  href="/activation-forms"
                  className="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-primary-500 rounded-lg border border-gray-200 hover:border-gray-300"
                >
                  <div>
                    <span className="rounded-lg inline-flex p-3 bg-yellow-50 text-yellow-600">
                      <ClipboardDocumentListIcon className="h-6 w-6" />
                    </span>
                  </div>
                  <div className="mt-4">
                    <h3 className="text-lg font-medium">
                      <span className="absolute inset-0" aria-hidden="true" />
                      View Activations
                    </h3>
                    <p className="mt-2 text-sm text-gray-500">
                      Review pending activation requests
                    </p>
                  </div>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  )
}
