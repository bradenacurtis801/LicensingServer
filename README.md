# 🚀 LicensingServer

A modern, FastAPI-based license management system with a clean Python client SDK. Built for developers who need robust license key generation, validation, and management capabilities.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)](https://www.postgresql.org/)

## ✨ Features

- **🔐 Secure License Management** - SHA-256 hashed license keys with secure generation
- **👥 User Authentication** - Role-based access control with JWT tokens
- **🏢 Multi-tenant Support** - Users can manage their own customers and applications
- **📱 Client SDK** - Clean Python SDK for easy integration
- **🐳 Docker Ready** - Complete containerization with Docker Compose
- **📊 Activation Tracking** - Monitor license usage and machine activations
- **🔧 Feature Management** - JSON-based feature flags for flexible licensing
- **📋 Activation Forms** - Support for offline activation workflows
- **🔄 Database Migrations** - Alembic-powered schema management

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│           API Layer                 │ ← FastAPI Endpoints
├─────────────────────────────────────┤
│         Service Layer               │ ← Business Logic
├─────────────────────────────────────┤
│          Model Layer                │ ← SQLModel + Pydantic
├─────────────────────────────────────┤
│        Database Layer               │ ← PostgreSQL
└─────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL 13+
- Docker & Docker Compose (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/bradenacurtis801/LicensingServer.git
   cd LicensingServer
   ```

2. **Set up environment**
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit .env with your database settings
   nano .env
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up database**
   ```bash
   # Run migrations
   python -m alembic upgrade head
   
   # Create sample data (optional)
   python scripts/create_sample_data.py
   ```

5. **Start the server**
   ```bash
   python run_server.py
   ```

The API will be available at `http://localhost:8999`

### Docker Setup

```bash
# Start PostgreSQL
docker-compose -f docker/docker-compose.postgres.yml up -d

# Start the application
docker-compose -f docker/docker-compose.app.yml up -d
```

## 📖 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8999/docs
- **ReDoc**: http://localhost:8999/redoc

## 🔧 Client SDK Usage

```python
from client_sdk.methods import LicenseKey, Helpers

# Activate a license
result, message = LicenseKey.activate(
    server_url="http://localhost:8999",
    license_key="YOUR-LICENSE-KEY",
    machine_code=Helpers.GetMachineCode()
)

if result:
    print("License activated successfully!")
    print(f"Expires: {result['expires_at']}")
else:
    print(f"Activation failed: {message}")

# Validate a license
result, message = LicenseKey.validate(
    server_url="http://localhost:8999",
    license_key="YOUR-LICENSE-KEY"
)

if result:
    print("License is valid!")
else:
    print(f"Validation failed: {message}")
```

## 🗂️ Project Structure

```
LicensingServer/
├── 📁 app/                    # FastAPI application
│   ├── api/                   # API endpoints
│   ├── core/                  # Core utilities
│   ├── models/                # Database models
│   ├── services/              # Business logic
│   └── utils/                 # Helper utilities
├── 📁 client_sdk/             # Python client SDK
├── 📁 docker/                 # Docker configurations
├── 📁 migrations/             # Database migrations
├── 📁 scripts/                # Utility scripts
└── 📁 docs/                   # Documentation
```

## 🔐 Security Features

- **License Key Security**: SHA-256 hashed storage, secure random generation
- **Authentication**: JWT-based with role-based access control
- **Machine Fingerprinting**: Hardware-based device identification
- **Rate Limiting**: Built-in protection against abuse
- **SQL Injection Protection**: SQLModel ORM prevents injection attacks

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_licenses.py
```

## 📊 Database Schema

The system uses PostgreSQL with the following main entities:

- **Users** - System users with role-based permissions
- **Applications** - Software products that need licensing
- **Customers** - End users who purchase licenses
- **LicenseKeys** - Generated license keys with features and limits
- **Activations** - Machine activations for license tracking

## 🚀 Deployment

### Production Deployment

1. **Set up PostgreSQL database**
2. **Configure environment variables**
3. **Run database migrations**
4. **Deploy with Docker or directly**

```bash
# Production Docker deployment
docker-compose -f docker/docker-compose.app.yml up -d
```

### Environment Variables

Key environment variables to configure:

```env
# Database
POSTGRES_DB_NAME=licensing_server
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Security
SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server
HOST=0.0.0.0
PORT=8999
DEBUG=False
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework
- [SQLModel](https://sqlmodel.tiangolo.com/) - SQL databases in Python
- [PostgreSQL](https://www.postgresql.org/) - Powerful open source database
- [Alembic](https://alembic.sqlalchemy.org/) - Database migration tool
- [Cryptolens Python SDK](https://github.com/Cryptolens/cryptolens-python) - Client SDK foundation (adapted and cleaned)

### Client SDK Attribution

The client SDK in this project is based on the [Cryptolens Python SDK](https://github.com/Cryptolens/cryptolens-python) by Cryptolens AB, but has been significantly adapted and cleaned for this specific license server implementation:

- **Removed unused classes** (AI, Message, Product, Customer, Data, PaymentForm, Subscription, User)
- **Adapted to our API** endpoints and data structures
- **Removed f1-f8 fields** in favor of JSON-based features
- **Renamed classes** to use our own naming conventions
- **Optimized for our use case** (60% smaller codebase)
- **Added our own helpers** and utilities

The original Cryptolens SDK is licensed under the MIT License, and we maintain proper attribution as required.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/bradenacurtis801/LicensingServer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/bradenacurtis801/LicensingServer/discussions)

## 🗺️ Roadmap

- [ ] REST API client SDKs for other languages
- [ ] Web-based admin dashboard
- [ ] Advanced analytics and reporting
- [ ] Multi-currency support
- [ ] Webhook support for real-time notifications
- [ ] GraphQL API support

---

**Made with ❤️ by [Braden Curtis](https://github.com/bradenacurtis801)**