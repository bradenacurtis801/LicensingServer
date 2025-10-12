# LicensingServer

A self-hosted license management system. Issue and validate license keys, track activations per machine, and manage customers and applications through a REST API and web dashboard.

## Stack

- **Backend**: FastAPI, SQLModel, PostgreSQL
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS
- **Auth**: Session tokens and scoped API tokens

## Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 13+

## Getting Started

### 1. Clone and configure

```bash
git clone https://github.com/bradenacurtis801/LicensingServer.git
cd LicensingServer
cp .env.example .env
```

Edit `.env` with your database credentials.

### 2. Backend

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8999
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

The dashboard is available at `http://localhost:3000` and the API at `http://localhost:8999`.

### 4. Database (development)

Start a local PostgreSQL container:

```bash
python scripts/db_util/run_dev_db.py
```

Seed sample data:

```bash
python scripts/db_util/seed_data.py
```

## API Documentation

With the server running:

- Swagger UI: `http://localhost:8999/docs`
- ReDoc: `http://localhost:8999/redoc`

## Environment Variables

```env
# PostgreSQL
POSTGRES_DB_NAME=license_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USERNAME=postgres
POSTGRES_PASSWORD=your_password

# RSA signing — generate with: openssl genrsa -out private.pem 2048
RSA_PRIVATE_KEY_PATH=/path/to/private.pem

# Server
BACKEND_PORT=8999
DEBUG=false
```

## Project Structure

```
LicensingServer/
├── app/
│   ├── api/v1/endpoints/   # Route handlers
│   ├── services/           # Business logic
│   ├── models/             # Database models and schemas
│   ├── database/           # Connection and migrations
│   └── core/               # Auth, exceptions, constants
├── frontend/               # Next.js dashboard
├── client_sdk/             # Python SDK for license validation
├── scripts/
│   └── db_util/            # Database management utilities
├── tests/                  # Integration and unit tests
└── migrations/             # Alembic migrations
```

## Client SDK

```python
from client_sdk.methods import LicenseKey, Helpers

result, message = LicenseKey.activate(
    server_url="http://localhost:8999",
    license_key="YOUR-LICENSE-KEY",
    machine_code=Helpers.GetMachineCode()
)
```

## Utility Scripts

```bash
python scripts/db_util/create_user.py <username> <email> <full_name> <password> [--admin]
python scripts/db_util/create_token.py <username> <token_name> --scopes license:read license:write
python scripts/db_util/list_users.py
python scripts/db_util/list_user.py <username> [--licenses] [--customers] [--applications]
```

## License

MIT
