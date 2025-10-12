/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    // Use environment variable for backend URL, fallback to 127.0.0.1
    const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8999'
    
    return [
      {
        source: '/api/:path*',
        destination: `${backendUrl}/api/:path*`,
      },
    ]
  },
}

module.exports = nextConfig
