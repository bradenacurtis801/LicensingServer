'use client'

import Layout from '@/components/Layout'
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { applicationsApi } from '@/api'
import { toast } from 'react-hot-toast'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const createApplicationSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  description: z.string().min(1, 'Description is required'),
  version: z.string().min(1, 'Version is required'),
})

type CreateApplicationForm = z.infer<typeof createApplicationSchema>

export default function NewApplicationPage() {
  const router = useRouter()
  const [submitting, setSubmitting] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<CreateApplicationForm>({
    resolver: zodResolver(createApplicationSchema),
  })

  const onSubmit = async (data: CreateApplicationForm) => {
    setSubmitting(true)
    try {
      const response = await applicationsApi.createApplicationApiV1ApplicationsPost({
        applicationCreate: data
      })
      toast.success('Application registered successfully')
      router.push(`/applications/${response.id}`)
    } catch (error: any) {
      toast.error(error.message || 'Failed to register application')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <Layout>
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">Register New Application</h1>
        <p className="mt-2 text-sm text-gray-700">
          Register a new application for license management
        </p>
      </div>

      <div className="mt-8">
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div className="bg-white shadow px-4 py-5 sm:rounded-lg sm:p-6">
            <div className="grid grid-cols-1 gap-6">
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                  Application Name *
                </label>
                <input
                  type="text"
                  {...register('name')}
                  className="mt-1 input"
                  placeholder="Enter application name"
                />
                {errors.name && (
                  <p className="mt-1 text-sm text-red-600">{errors.name.message}</p>
                )}
              </div>

              <div>
                <label htmlFor="version" className="block text-sm font-medium text-gray-700">
                  Version *
                </label>
                <input
                  type="text"
                  {...register('version')}
                  className="mt-1 input"
                  placeholder="e.g., 1.0.0"
                />
                {errors.version && (
                  <p className="mt-1 text-sm text-red-600">{errors.version.message}</p>
                )}
              </div>

              <div>
                <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                  Description *
                </label>
                <textarea
                  {...register('description')}
                  rows={4}
                  className="mt-1 input"
                  placeholder="Enter application description"
                />
                {errors.description && (
                  <p className="mt-1 text-sm text-red-600">{errors.description.message}</p>
                )}
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
              {submitting ? 'Registering...' : 'Register Application'}
            </button>
          </div>
        </form>
      </div>
    </Layout>
  )
}
