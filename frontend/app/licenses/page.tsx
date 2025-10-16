'use client'

import Layout from '@/components/Layout'
import { useState, useEffect } from 'react'
import { LicenseKeyWithRelationsResponse } from '@/generated'
import { licensesApi } from '@/api'
import Link from 'next/link'
import { PlusIcon } from '@heroicons/react/24/outline'
import { toast } from 'react-hot-toast'
import LicenseList from '@/components/LicenseList'

export default function LicensesPage() {
  const [licenses, setLicenses] = useState<LicenseKeyWithRelationsResponse[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Fetch licenses using REST API
  const fetchLicenses = async () => {
    try {
      setLoading(true)
      setError(null)
      
      const response = await licensesApi.listLicensesApiV1LicensesGet({ includeRelations: true })
      setLicenses(response)
    } catch (err) {
      console.error('Error fetching licenses:', err)
      setError('Failed to fetch licenses')
      toast.error('Failed to fetch licenses')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchLicenses()
  }, [])

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this license?')) return

    try {
      const response = await fetch(`http://localhost:8999/api/v1/licenses/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
          'Content-Type': 'application/json',
        },
      });
      
      if (response.ok) {
        toast.success('License deleted successfully')
        fetchLicenses() // Refetch using REST API
      } else {
        throw new Error('Delete failed');
      }
    } catch (error) {
      toast.error('Failed to delete license')
    }
  }

  if (error) {
    return (
      <Layout>
        <div className="text-center py-12">
          <h2 className="text-xl font-semibold text-red-600 mb-4">Error Loading Licenses</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button 
            onClick={() => fetchLicenses()}
            className="btn btn-primary"
          >
            Try Again
          </button>
        </div>
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-2xl font-semibold text-gray-900">Licenses</h1>
          <p className="mt-2 text-sm text-gray-700">
            Manage your license keys and track activations
          </p>
        </div>
        <div className="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
          <Link
            href="/licenses/new"
            className="btn btn-primary"
          >
            <PlusIcon className="h-4 w-4 mr-2" />
            New License
          </Link>
        </div>
      </div>

      <div className="mt-8">
        <LicenseList
          licenses={licenses}
          onDelete={handleDelete}
          loading={loading}
        />
      </div>
    </Layout>
  )
}