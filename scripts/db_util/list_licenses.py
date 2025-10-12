#!/usr/bin/env python3
"""
List licenses for a user.

Usage:
  python scripts/list_licenses.py <username>
"""
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlmodel import Session
from app.database.connection import engine
from app.services.auth_service import AuthService
from app.services.license_service import LicenseService


def main():
    parser = argparse.ArgumentParser(description="List licenses for a user")
    parser.add_argument("username")
    args = parser.parse_args()

    with Session(engine) as db:
        auth_service = AuthService(db)
        user = auth_service.get_user_by_username(args.username)
        if not user:
            print(f"User '{args.username}' not found.")
            sys.exit(1)

        license_service = LicenseService(db)
        licenses = license_service.list_licenses(user, include_relations=True)

    if not licenses:
        print(f"No licenses for '{args.username}'.")
        return

    print(f"{'ID':<5} {'Key':<30} {'Status':<12} {'Customer':<20} {'Application':<20} {'Activations':<12} Expires")
    print("-" * 120)
    for lic in licenses:
        customer = lic.customer.name if lic.customer else str(lic.customer_id)
        app = lic.application.name if lic.application else str(lic.application_id)
        expires = str(lic.expires_at)[:19] if lic.expires_at else "never"
        activations = f"{lic.current_activations}/{lic.max_activations}"
        print(f"{lic.id:<5} {lic.license_key:<30} {lic.status.value:<12} {customer:<20} {app:<20} {activations:<12} {expires}")


if __name__ == "__main__":
    main()
