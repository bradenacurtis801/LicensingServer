'use client'

import Layout from '@/components/Layout'
import { useState, useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { customersApi } from '@/api'
import { toast } from 'react-hot-toast'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const editCustomerSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  email: z.string().email('Invalid email address'),
  company: z.string().optional(),
})

type EditCustomerForm = z.infer<typeof editCustomerSchema>

export default function EditCustomerPage() {
  const { id } = useParams()
  const router = useRouter()
  const customerId = Number(id)
  const [loading, setLoading] = useState(true)

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<EditCustomerForm>({
    resolver: zodResolver(editCustomerSchema),
  })

  useEffect(() => {
    customersApi.getCustomerApiV1CustomersCustomerIdGet({ customerId })
      .then(customer => reset({ name: customer.name, email: customer.email, company: customer.company ?? '' }))
      .catch(() => { toast.error('Failed to load customer'); router.push('/customers') })
      .finally(() => setLoading(false))
  }, [customerId])

  const onSubmit = async (data: EditCustomerForm) => {
    try {
      await customersApi.updateCustomerApiV1CustomersCustomerIdPut({
        customerId,
        customerUpdate: data,
      })
      toast.success('Customer updated')
      router.push(`/customers/${customerId}`)
    } catch {
      toast.error('Failed to update customer')
    }
  }

  if (loading) {
    return (
      <Layout>
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-200 rounded w-48" />
          <div className="h-32 bg-gray-200 rounded" />
        </div>
      </Layout>
    )
  }

  return (
    <Layout>
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">Edit Customer</h1>
        <p className="mt-2 text-sm text-gray-700">Update customer information</p>
      </div>

      <div className="mt-8">
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div className="bg-white shadow px-4 py-5 sm:rounded-lg sm:p-6">
            <div className="grid grid-cols-1 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700">Name *</label>
                <input type="text" {...register('name')} className="mt-1 input" />
                {errors.name && <p className="mt-1 text-sm text-red-600">{errors.name.message}</p>}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">Email *</label>
                <input type="email" {...register('email')} className="mt-1 input" />
                {errors.email && <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">Company</label>
                <input type="text" {...register('company')} className="mt-1 input" placeholder="Optional" />
              </div>
            </div>
          </div>

          <div className="flex justify-end space-x-3">
            <button type="button" onClick={() => router.push(`/customers/${customerId}`)} className="btn btn-secondary btn-md">
              Cancel
            </button>
            <button type="submit" disabled={isSubmitting} className="btn btn-primary btn-md">
              {isSubmitting ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </form>
      </div>
    </Layout>
  )
}
