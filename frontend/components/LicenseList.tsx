'use client'

import { useState } from 'react'
import { LicenseKeyWithRelationsResponse } from '@/generated'
import LicenseCard from './LicenseCard'

interface LicenseListProps {
  licenses: LicenseKeyWithRelationsResponse[]
  onDelete: (id: number) => void
  loading?: boolean
}

export default function LicenseList({ licenses, onDelete, loading = false }: LicenseListProps) {
  const [searchTerm, setSearchTerm] = useState('')

  const filteredLicenses = licenses.filter(license =>
    license.customer?.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    license.application?.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    license.status.toLowerCase().includes(searchTerm.toLowerCase())
  )

  if (loading) {
    return (
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
    )
  }

  if (licenses.length === 0) {
    return (
      <div className="text-center py-12">
        <h3 className="text-lg font-medium text-gray-900 mb-2">No licenses found</h3>
        <p className="text-gray-500 mb-4">Get started by creating your first license.</p>
      </div>
    )
  }

  return (
    <div>
      <div className="mb-4">
        <input
          type="text"
          placeholder="Search licenses..."
          className="input max-w-md"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        <ul className="divide-y divide-gray-200">
          {filteredLicenses.map((license) => (
            <LicenseCard
              key={license.id}
              id={license.id}
              licenseKey={license.licenseKey}
              status={license.status}
              maxActivations={license.maxActivations}
              currentActivations={license.currentActivations}
              expiresAt={license.expiresAt}
              customerName={license.customer?.name}
              customerEmail={license.customer?.email}
              applicationName={license.application?.name}
              onDelete={onDelete}
            />
          ))}
        </ul>
      </div>
    </div>
  )
}
