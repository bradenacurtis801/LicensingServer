# License Management Frontend

A modern Next.js frontend for the License Management System, built with React, TypeScript, and Tailwind CSS.

## Features

- 🔐 **Authentication** - Secure login with JWT tokens
- 📊 **Dashboard** - Overview of licenses, customers, and applications
- 🔑 **License Management** - Create, view, edit, and delete license keys
- 👥 **Customer Management** - Manage customer accounts
- 🚀 **Application Management** - Register and manage applications
- 📋 **Activation Forms** - Review and approve activation requests
- 🔧 **API Tokens** - Manage API access tokens
- 📱 **Responsive Design** - Works on desktop and mobile devices

## Tech Stack

- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first CSS framework
- **React Hook Form** - Form handling with validation
- **Zod** - Schema validation
- **Axios** - HTTP client
- **React Hot Toast** - Toast notifications
- **Heroicons** - Beautiful SVG icons

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Running License Management Backend

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create environment file:
```bash
cp .env.example .env.local
```

3. Configure environment variables:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

4. Start the development server:
```bash
npm run dev
```

5. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── dashboard/         # Dashboard page
│   ├── licenses/          # License management pages
│   ├── customers/         # Customer management pages
│   ├── applications/      # Application management pages
│   ├── activation-forms/  # Activation form management
│   ├── api-tokens/        # API token management
│   └── login/             # Login page
├── components/            # Reusable React components
│   ├── Layout.tsx         # Main layout wrapper
│   ├── Sidebar.tsx        # Navigation sidebar
│   └── Header.tsx         # Top header bar
├── contexts/              # React contexts
│   └── AuthContext.tsx    # Authentication context
├── lib/                   # Utility libraries
│   └── api.ts            # API client configuration
└── public/               # Static assets
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## API Integration

The frontend communicates with the backend through a configured Axios instance:

- **Base URL**: Configurable via `NEXT_PUBLIC_API_URL`
- **Authentication**: JWT tokens stored in localStorage
- **Error Handling**: Automatic token refresh and logout on 401 errors
- **Request/Response Interceptors**: Automatic token injection and error handling

## Authentication Flow

1. User enters credentials on login page
2. Backend validates credentials and returns JWT token
3. Token is stored in localStorage
4. All API requests include the token in Authorization header
5. Token is automatically refreshed or user is logged out on expiration

## Component Architecture

### Layout Components
- **Layout**: Main wrapper with authentication checks
- **Sidebar**: Navigation menu with active state
- **Header**: User profile and logout functionality

### Page Components
- **Dashboard**: Overview with statistics and quick actions
- **Licenses**: List, create, and manage license keys
- **Customers**: Customer management interface
- **Applications**: Application registration and management
- **Activation Forms**: Review and approve activation requests
- **API Tokens**: Manage API access tokens

## Styling

The project uses Tailwind CSS with custom component classes:

- **Buttons**: `.btn`, `.btn-primary`, `.btn-secondary`, `.btn-danger`
- **Forms**: `.input` for form inputs
- **Cards**: `.card`, `.card-header`, `.card-content`, `.card-footer`
- **Colors**: Custom primary color palette

## Development

### Adding New Pages

1. Create page component in `app/[route]/page.tsx`
2. Add route to sidebar navigation in `components/Sidebar.tsx`
3. Implement API calls in the page component
4. Add form validation using React Hook Form + Zod

### Adding New API Endpoints

1. Add endpoint methods to `lib/api.ts`
2. Create TypeScript interfaces for request/response types
3. Implement error handling and loading states
4. Add toast notifications for user feedback

## Deployment

### Build for Production

```bash
npm run build
```

### Environment Variables

Set the following environment variables in production:

- `NEXT_PUBLIC_API_URL` - Backend API URL
- `NODE_ENV=production`

### Static Export (Optional)

For static hosting, add to `next.config.js`:

```javascript
module.exports = {
  output: 'export',
  trailingSlash: true,
}
```

## Contributing

1. Follow the existing code style and patterns
2. Use TypeScript for all new code
3. Add proper error handling and loading states
4. Include toast notifications for user actions
5. Test on both desktop and mobile devices

## License

This project is part of the License Management System and follows the same MIT license.
