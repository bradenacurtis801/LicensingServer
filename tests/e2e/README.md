# E2E Tests

These tests require a running server and a seeded database.

## Setup

1. Start the server:
   ```bash
   uvicorn app.main:app --reload --port 8999
   ```

2. Seed sample data:
   ```bash
   python scripts/db_util/seed_data.py
   ```

3. Run:
   ```bash
   pytest tests/e2e/ -v
   ```

These are not run as part of the standard `pytest` suite — run them manually before deploying.
