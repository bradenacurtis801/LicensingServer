'use client'

import Layout from '@/components/Layout'
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { customersApi } from '@/api'
import { toast } from 'react-hot-toast'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const createCustomerSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  email: z.string().email('Invalid email address'),
})

type CreateCustomerForm = z.infer<typeof createCustomerSchema>

export default function NewCustomerPage() {
  const router = useRouter()
  const [submitting, setSubmitting] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<CreateCustomerForm>({
    resolver: zodResolver(createCustomerSchema),
  })

  const onSubmit = async (data: CreateCustomerForm) => {
    setSubmitting(true)
    try {
      const response = await customersApi.createCustomerApiV1CustomersPost({
        customerCreate: data
      })
      toast.success('Customer created successfully')
      router.push(`/customers/${response.id}`)
    } catch (error: any) {
      toast.error(error.message || 'Failed to create customer')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <Layout>
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">Add New Customer</h1>
        <p className="mt-2 text-sm text-gray-700">
          Register a new customer in the system
        </p>
      </div>

      <div className="mt-8">
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div className="bg-white shadow px-4 py-5 sm:rounded-lg sm:p-6">
            <div className="grid grid-cols-1 gap-6">
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                  Customer Name *
                </label>
                <input
                  type="text"
                  {...register('name')}
                  className="mt-1 input"
                  placeholder="Enter customer name"
                />
                {errors.name && (
                  <p className="mt-1 text-sm text-red-600">{errors.name.message}</p>
                )}
              </div>

              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                  Email Address *
                </label>
                <input
                  type="email"
                  {...register('email')}
                  className="mt-1 input"
                  placeholder="Enter email address"
                />
                {errors.email && (
                  <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
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
              {submitting ? 'Creating...' : 'Create Customer'}
            </button>
          </div>
        </form>
      </div>
    </Layout>
  )
}
