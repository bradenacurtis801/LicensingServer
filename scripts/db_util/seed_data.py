#!/usr/bin/env python3
"""
Seed the database with sample data for development.

Creates a user with sample customers, applications, and licenses.

Usage:
  python scripts/db_util/seed_data.py
  python scripts/db_util/seed_data.py --username alice --password secret123
"""
import sys
import argparse
from pathlib import Path
from datetime import datetime, timedelta, timezone

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlmodel import Session, select
from app.database.connection import engine
from app.models.database import User, Application, Customer, LicenseKey, SystemRole
from app.models.schemas import UserCreate, CustomerCreate, ApplicationCreate, LicenseKeyCreate
from app.services.auth_service import AuthService
from app.services.customer_service import CustomerService
from app.services.application_service import ApplicationService
from app.services.license_service import LicenseService


SAMPLE_APPLICATIONS = [
    {"name": "MyApp Pro", "version": "1.0.0", "description": "Professional edition"},
    {"name": "MyApp Pro", "version": "2.0.0", "description": "Professional edition v2"},
    {"name": "DataTool", "version": "1.0.0", "description": "Data processing tool"},
]

SAMPLE_CUSTOMERS = [
    {"name": "Acme Corp", "email": "billing@acme.com", "company": "Acme Corporation"},
    {"name": "Jane Smith", "email": "jane@example.com", "company": "Smith Consulting"},
    {"name": "Bob Dev", "email": "bob@devshop.io", "company": "Dev Shop"},
]


def get_or_create_user(db: Session, username: str, password: str) -> User:
    auth = AuthService(db)
    user = auth.get_user_by_username(username)
    if user:
        print(f"Using existing user: {username} (id={user.id})")
        return user

    auth.create_user(UserCreate(
        username=username,
        email=f"{username}@example.com",
        full_name=username.capitalize(),
        password=password,
    ))
    user = auth.get_user_by_username(username)
    user.system_role = SystemRole.SYSTEM_ADMIN
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"Created user: {username} (id={user.id})")
    return user


def seed(username: str, password: str):
    with Session(engine) as db:
        user = get_or_create_user(db, username, password)

        # Applications
        app_svc = ApplicationService(db)
        apps = []
        for data in SAMPLE_APPLICATIONS:
            existing = db.exec(
                select(Application).where(
                    Application.name == data["name"],
                    Application.version == data["version"],
                    Application.user_id == user.id,
                )
            ).first()
            if existing:
                print(f"  App exists: {data['name']} v{data['version']}")
                apps.append(existing)
            else:
                app_resp = app_svc.create_application(ApplicationCreate(**data), user)
                app = db.exec(select(Application).where(Application.id == app_resp.id)).first()
                print(f"  Created app: {app.name} v{app.version} (id={app.id})")
                apps.append(app)

        # Customers + one license each
        cust_svc = CustomerService(db)
        lic_svc = LicenseService(db)

        for i, data in enumerate(SAMPLE_CUSTOMERS):
            existing = db.exec(
                select(Customer).where(Customer.email == data["email"], Customer.user_id == user.id)
            ).first()
            if existing:
                print(f"  Customer exists: {data['name']}")
                customer_id = existing.id
            else:
                cust = cust_svc.create_customer(CustomerCreate(**data), user)
                print(f"  Created customer: {cust.name} (id={cust.id})")
                customer_id = cust.id

            app = apps[i % len(apps)]
            existing_lic = db.exec(
                select(LicenseKey).where(
                    LicenseKey.customer_id == customer_id,
                    LicenseKey.application_id == app.id,
                )
            ).first()
            if existing_lic:
                print(f"    License exists for {data['name']} / {app.name}")
            else:
                lic = lic_svc.create_license(LicenseKeyCreate(
                    customer_id=customer_id,
                    application_id=app.id,
                    max_activations=3,
                    expires_at=datetime.now(timezone.utc) + timedelta(days=365),
                ), user)
                print(f"    Created license: {lic.license_key[:20]}... (id={lic.id})")

    print("\nSeed complete.")


def main():
    parser = argparse.ArgumentParser(description="Seed database with sample data")
    parser.add_argument("--username", default="dev", help="Seed user username (default: dev)")
    parser.add_argument("--password", default="password123", help="Seed user password (default: password123)")
    args = parser.parse_args()

    seed(args.username, args.password)


if __name__ == "__main__":
    main()
