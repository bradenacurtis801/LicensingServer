# API Migration to Generated Client

This document outlines the migration from manual axios calls to the generated TypeScript API client.

## What Changed

### Before (Manual Axios)
```typescript
import { api } from '@/lib/api'

// Manual API calls
const response = await api.get('/licenses/')
const data = response.data
```

### After (Generated Client)
```typescript
import { licensesApi } from '@/api'

// Type-safe API calls
const data = await licensesApi.getLicenses()
```

## Benefits

1. **Type Safety**: Full TypeScript support for all API calls
2. **Auto-completion**: IDE support for all available methods
3. **Error Handling**: Consistent error handling across all APIs
4. **Authentication**: Automatic token management
5. **Validation**: Request/response validation

## API Clients Available

- `activationFormsApi` - Activation form management
- `activationsApi` - License activations
- `applicationsApi` - Application management
- `authenticationApi` - User authentication
- `customersApi` - Customer management
- `defaultApi` - General endpoints
- `licensesApi` - License management
- `validationApi` - License validation

## Authentication

The API clients automatically handle authentication:

- Tokens are read from localStorage
- All requests include the Bearer token
- Clients are refreshed when authentication changes
- Invalid tokens are automatically cleared

## Usage Examples

```typescript
// Get all licenses
const licenses = await licensesApi.getLicenses()

// Create a new license
const newLicense = await licensesApi.createLicense({
  customer_id: 1,
  application_id: 1,
  max_activations: 5
})

// Delete a license
await licensesApi.deleteLicense({ id: 123 })

// Get current user
const user = await authenticationApi.getCurrentUser()
```

## Error Handling

All API calls return promises that can be caught:

```typescript
try {
  const result = await licensesApi.getLicenses()
} catch (error) {
  console.error('API Error:', error.message)
}
```

## Configuration

The API base URL is configured via environment variables:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

You can also update the configuration dynamically:

```typescript
import { setCurrentClientConfig } from '@/api'

setCurrentClientConfig('https://api.production.com')
```
