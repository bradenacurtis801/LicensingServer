# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of LicensingServer
- FastAPI-based license management API
- PostgreSQL database support with Alembic migrations
- JWT-based authentication with role-based access control
- Python client SDK with license activation and validation
- Docker support for development and production
- User management with multi-tenant support
- License key generation with SHA-256 hashing
- Machine fingerprinting for device identification
- Activation tracking and limits
- Feature management with JSON-based feature flags
- Activation forms for offline activation workflows
- Comprehensive API documentation with Swagger/ReDoc
- Database seeding scripts for development
- Clean, optimized client SDK (60% smaller than original)

### Security
- Secure license key generation using cryptographic randomness
- SHA-256 hashed license key storage
- JWT token-based authentication
- SQL injection protection via SQLModel ORM
- Rate limiting on validation endpoints
- Machine fingerprinting for device identification

### Performance
- Optimized database queries with proper indexing
- Connection pooling for database connections
- Efficient license validation with caching
- Clean client SDK with minimal dependencies

## [1.0.0] - 2025-01-27

### Added
- Initial public release
- Complete license management system
- Production-ready Docker configuration
- MIT License for open source distribution
- Comprehensive documentation and examples

---

For more details, see the [GitHub Releases](https://github.com/bradenacurtis801/LicensingServer/releases).
