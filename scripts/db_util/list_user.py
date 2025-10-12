#!/usr/bin/env python3
"""
Show info for a specific user. By default prints a summary of their data.

Usage:
  python scripts/db_util/list_user.py <username>
  python scripts/db_util/list_user.py <username> --licenses
  python scripts/db_util/list_user.py <username> --customers
  python scripts/db_util/list_user.py <username> --applications
  python scripts/db_util/list_user.py <username> --tokens
  python scripts/db_util/list_user.py <username> --activations
"""
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlmodel import Session
from app.database.connection import engine
from app.services.auth_service import AuthService
from app.services.license_service import LicenseService
from app.services.customer_service import CustomerService
from app.services.application_service import ApplicationService
from app.services.activation_service import ActivationService


def print_summary(user, db):
    auth = AuthService(db)
    tokens = auth.list_api_tokens(user.id)

    license_svc = LicenseService(db)
    licenses = license_svc.list_licenses(user, limit=10000)

    customer_svc = CustomerService(db)
    customers = customer_svc.list_customers(user, limit=10000)

    app_svc = ApplicationService(db)
    applications = app_svc.list_applications(user, limit=10000)

    activation_svc = ActivationService(db)
    activations = activation_svc.list_activations_for_user(user, limit=10000)

    print(f"User:         {user.username} (id={user.id})")
    print(f"Email:        {user.email}")
    print(f"Full name:    {user.full_name}")
    print(f"System role:  {user.system_role}")
    print(f"Active:       {user.is_active}")
    print(f"Created:      {str(user.created_at)[:19]}")
    print()
    print(f"  Customers:    {len(customers)}")
    print(f"  Applications: {len(applications)}")
    print(f"  Licenses:     {len(licenses)}")
    print(f"  Activations:  {len(activations)}")
    print(f"  API Tokens:   {len(tokens)}")


def print_licenses(user, db):
    svc = LicenseService(db)
    licenses = svc.list_licenses(user, limit=10000, include_relations=True)
    if not licenses:
        print("No licenses.")
        return
    print(f"{'ID':<5} {'Key':<30} {'Status':<12} {'Customer':<20} {'Application':<20} {'Act.':<8} Expires")
    print("-" * 110)
    for lic in licenses:
        customer = lic.customer.name if lic.customer else str(lic.customer_id)
        app = lic.application.name if lic.application else str(lic.application_id)
        expires = str(lic.expires_at)[:19] if lic.expires_at else "never"
        acts = f"{lic.current_activations}/{lic.max_activations}"
        print(f"{lic.id:<5} {lic.license_key:<30} {lic.status.value:<12} {customer:<20} {app:<20} {acts:<8} {expires}")


def print_customers(user, db):
    svc = CustomerService(db)
    customers = svc.list_customers(user, limit=10000)
    if not customers:
        print("No customers.")
        return
    print(f"{'ID':<5} {'Name':<25} {'Email':<30} Company")
    print("-" * 80)
    for c in customers:
        print(f"{c.id:<5} {c.name:<25} {c.email:<30} {c.company or ''}")


def print_applications(user, db):
    svc = ApplicationService(db)
    applications = svc.list_applications(user, limit=10000)
    if not applications:
        print("No applications.")
        return
    print(f"{'ID':<5} {'Name':<25} {'Version':<12} Description")
    print("-" * 80)
    for a in applications:
        print(f"{a.id:<5} {a.name:<25} {a.version:<12} {a.description or ''}")


def print_tokens(user, db):
    svc = AuthService(db)
    tokens = svc.list_api_tokens(user.id)
    if not tokens:
        print("No API tokens.")
        return
    print(f"{'ID':<5} {'Name':<25} {'Active':<8} {'Expires':<22} {'Last Used':<22} Scopes")
    print("-" * 110)
    for t in tokens:
        scopes = ", ".join(s.value for s in t.scopes)
        last_used = str(t.last_used_at)[:19] if t.last_used_at else "never"
        expires = str(t.expires_at)[:19] if t.expires_at else "never"
        print(f"{t.id:<5} {t.name:<25} {str(t.is_active):<8} {expires:<22} {last_used:<22} {scopes}")


def print_activations(user, db):
    svc = ActivationService(db)
    activations = svc.list_activations_for_user(user, limit=10000)
    if not activations:
        print("No activations.")
        return
    print(f"{'ID':<5} {'License ID':<12} {'Machine ID':<36} {'Machine Name':<20} {'Status':<10} Activated")
    print("-" * 100)
    for a in activations:
        print(f"{a.id:<5} {a.license_key_id:<12} {a.machine_id:<36} {(a.machine_name or ''):<20} {a.status.value:<10} {str(a.activated_at)[:19]}")


def main():
    parser = argparse.ArgumentParser(description="Show info for a user")
    parser.add_argument("username")
    parser.add_argument("--licenses", action="store_true")
    parser.add_argument("--customers", action="store_true")
    parser.add_argument("--applications", action="store_true")
    parser.add_argument("--tokens", action="store_true")
    parser.add_argument("--activations", action="store_true")
    args = parser.parse_args()

    with Session(engine) as db:
        auth = AuthService(db)
        user = auth.get_user_by_username(args.username)
        if not user:
            print(f"User '{args.username}' not found.")
            sys.exit(1)

        any_flag = args.licenses or args.customers or args.applications or args.tokens or args.activations

        if not any_flag:
            print_summary(user, db)
        else:
            if args.licenses:
                print_licenses(user, db)
            if args.customers:
                print_customers(user, db)
            if args.applications:
                print_applications(user, db)
            if args.tokens:
                print_tokens(user, db)
            if args.activations:
                print_activations(user, db)


if __name__ == "__main__":
    main()
