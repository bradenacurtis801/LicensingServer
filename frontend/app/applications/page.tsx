'use client'

import Layout from '@/components/Layout'
import { useState, useEffect } from 'react'
import { applicationsApi } from '@/api'
import { ApplicationResponse } from '@/generated'
import Link from 'next/link'
import { PlusIcon, EyeIcon, PencilIcon, TrashIcon } from '@heroicons/react/24/outline'
import { toast } from 'react-hot-toast'

export default function ApplicationsPage() {
  const [applications, setApplications] = useState<ApplicationResponse[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    fetchApplications()
  }, [])

  const fetchApplications = async () => {
    try {
      const response = await applicationsApi.listApplicationsApiV1ApplicationsGet()
      setApplications(response)
    } catch (error) {
      toast.error('Failed to fetch applications')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this application?')) return

    try {
      await applicationsApi.deleteApplicationApiV1ApplicationsApplicationIdDelete({ applicationId: id })
      toast.success('Application deleted successfully')
      fetchApplications()
    } catch (error) {
      toast.error('Failed to delete application')
    }
  }

  const filteredApplications = applications.filter(app =>
    app.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    app.description.toLowerCase().includes(searchTerm.toLowerCase())
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
          <h1 className="text-2xl font-semibold text-gray-900">Applications</h1>
          <p className="mt-2 text-sm text-gray-700">
            Manage your registered applications
          </p>
        </div>
        <div className="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
          <Link
            href="/applications/new"
            className="btn btn-primary btn-md"
          >
            <PlusIcon className="h-4 w-4 mr-2" />
            New Application
          </Link>
        </div>
      </div>

      <div className="mt-8">
        <div className="mb-4">
          <input
            type="text"
            placeholder="Search applications..."
            className="input max-w-md"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        <div className="bg-white shadow overflow-hidden sm:rounded-md">
          <ul className="divide-y divide-gray-200">
            {filteredApplications.map((app) => (
              <li key={app.id}>
                <div className="px-4 py-4 flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <div className="h-10 w-10 rounded-full bg-orange-100 flex items-center justify-center">
                        <span className="text-orange-600 font-medium">
                          {app.name.charAt(0).toUpperCase()}
                        </span>
                      </div>
                    </div>
                    <div className="ml-4">
                      <div className="flex items-center">
                        <p className="text-sm font-medium text-gray-900">
                          {app.name}
                        </p>
                      </div>
                      <div className="mt-1 flex items-center text-sm text-gray-500">
                        <span>{app.description || 'No description'}</span>
                        <span className="mx-2">•</span>
                        <span>Created {new Date(app.createdAt).toLocaleDateString()}</span>
                        {app.version && (
                          <>
                            <span className="mx-2">•</span>
                            <span>v{app.version}</span>
                          </>
                        )}
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Link
                      href={`/applications/${app.id}`}
                      className="text-primary-600 hover:text-primary-900"
                    >
                      <EyeIcon className="h-4 w-4" />
                    </Link>
                    <Link
                      href={`/applications/${app.id}/edit`}
                      className="text-gray-600 hover:text-gray-900"
                    >
                      <PencilIcon className="h-4 w-4" />
                    </Link>
                    <button
                      onClick={() => handleDelete(app.id)}
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

        {filteredApplications.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500">No applications found</p>
            <Link href="/applications/new" className="btn btn-primary btn-md mt-4">
              Register your first application
            </Link>
          </div>
        )}
      </div>
    </Layout>
  )
}
