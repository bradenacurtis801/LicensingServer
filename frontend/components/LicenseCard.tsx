'use client'

import Link from 'next/link'
import { EyeIcon, PencilIcon, TrashIcon } from '@heroicons/react/24/outline'

interface LicenseCardProps {
  id: number
  licenseKey: string
  status: string
  maxActivations: number
  currentActivations: number
  expiresAt?: string
  customerName?: string
  customerEmail?: string
  applicationName?: string
  onDelete: (id: number) => void
}

export default function LicenseCard({
  id,
  licenseKey,
  status,
  maxActivations,
  currentActivations,
  expiresAt,
  customerName,
  customerEmail,
  applicationName,
  onDelete
}: LicenseCardProps) {
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

  return (
    <li>
      <div className="px-4 py-4 flex items-center justify-between">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <div className="h-10 w-10 rounded-full bg-primary-100 flex items-center justify-center">
              <span className="text-primary-600 font-medium">
                {id}
              </span>
            </div>
          </div>
          <div className="ml-4">
            <div className="flex items-center">
              <p className="text-sm font-medium text-gray-900">
                {customerName || 'Unknown Customer'}
              </p>
              <span className={`ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(status)}`}>
                {status}
              </span>
            </div>
            <div className="mt-1 flex items-center text-sm text-gray-500">
              <span>{applicationName || 'Unknown Application'}</span>
              <span className="mx-2">•</span>
              <span>{currentActivations}/{maxActivations} activations</span>
              {expiresAt && (
                <>
                  <span className="mx-2">•</span>
                  <span>Expires {new Date(expiresAt).toLocaleDateString()}</span>
                </>
              )}
            </div>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <Link
            href={`/licenses/${id}`}
            className="text-primary-600 hover:text-primary-900"
          >
            <EyeIcon className="h-4 w-4" />
          </Link>
          <Link
            href={`/licenses/${id}/edit`}
            className="text-gray-600 hover:text-gray-900"
          >
            <PencilIcon className="h-4 w-4" />
          </Link>
          <button
            onClick={() => onDelete(id)}
            className="text-red-600 hover:text-red-900"
          >
            <TrashIcon className="h-4 w-4" />
          </button>
        </div>
      </div>
    </li>
  )
}
