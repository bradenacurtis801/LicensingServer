#!/usr/bin/env python3
"""
Clear data from the database.

Usage:
  python scripts/db_util/clear_data.py --all           # clear all app data (keeps users)
  python scripts/db_util/clear_data.py --licenses       # licenses + activations only
  python scripts/db_util/clear_data.py --customers      # customers + their licenses
  python scripts/db_util/clear_data.py --applications   # applications + their licenses
  python scripts/db_util/clear_data.py --users          # everything including users
  python scripts/db_util/clear_data.py --all --yes      # skip confirmation
"""
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlalchemy import text
from sqlmodel import Session
from app.database.connection import engine


TABLES_ALL = [
    "offlineactivationcode",
    "activationform",
    "activation",
    "licensekey",
    "application",
    "customer",
]

TABLES_LICENSES = [
    "offlineactivationcode",
    "activationform",
    "activation",
    "licensekey",
]

TABLES_CUSTOMERS = [
    "offlineactivationcode",
    "activationform",
    "activation",
    "licensekey",
    "customer",
]

TABLES_APPLICATIONS = [
    "offlineactivationcode",
    "activationform",
    "activation",
    "licensekey",
    "application",
]

TABLES_USERS = [
    "offlineactivationcode",
    "activationform",
    "activation",
    "licensekey",
    "application",
    "customer",
    "apitoken",
    "session",
    "user",
]


def confirm(prompt: str) -> bool:
    answer = input(f"{prompt} [y/N] ").strip().lower()
    return answer == "y"


def clear_tables(tables: list[str]):
    with Session(engine) as db:
        for table in tables:
            db.exec(text(f"DELETE FROM {table}"))
            print(f"  Cleared: {table}")
        db.commit()
    print("Done.")


def main():
    parser = argparse.ArgumentParser(description="Clear database data")
    parser.add_argument("--all", action="store_true", help="Clear all app data (keeps users)")
    parser.add_argument("--licenses", action="store_true", help="Clear licenses and activations")
    parser.add_argument("--customers", action="store_true", help="Clear customers and their licenses")
    parser.add_argument("--applications", action="store_true", help="Clear applications and their licenses")
    parser.add_argument("--users", action="store_true", help="Clear everything including users")
    parser.add_argument("--yes", action="store_true", help="Skip confirmation prompt")
    args = parser.parse_args()

    if not any([args.all, args.licenses, args.customers, args.applications, args.users]):
        parser.print_help()
        sys.exit(1)

    if args.users:
        tables = TABLES_USERS
        description = "ALL data including users"
    elif args.all:
        tables = TABLES_ALL
        description = "all app data (customers, applications, licenses)"
    elif args.customers and args.applications:
        tables = TABLES_ALL
        description = "customers, applications, and licenses"
    elif args.customers:
        tables = TABLES_CUSTOMERS
        description = "customers and their licenses"
    elif args.applications:
        tables = TABLES_APPLICATIONS
        description = "applications and their licenses"
    else:
        tables = TABLES_LICENSES
        description = "licenses and activations"

    if not args.yes and not confirm(f"This will delete {description}. Continue?"):
        print("Aborted.")
        sys.exit(0)

    clear_tables(tables)


if __name__ == "__main__":
    main()
