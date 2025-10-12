#!/usr/bin/env python3
"""
List users.

Usage:
  python scripts/db_util/list_users.py
  python scripts/db_util/list_users.py --limit 50
"""
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlmodel import Session, func, select
from app.database.connection import engine
from app.models.database import User
from app.services.auth_service import AuthService

DISPLAY_LIMIT = 20


def main():
    parser = argparse.ArgumentParser(description="List users")
    parser.add_argument("--limit", type=int, default=DISPLAY_LIMIT, help=f"Max rows to display (default {DISPLAY_LIMIT})")
    args = parser.parse_args()

    with Session(engine) as db:
        total = db.exec(select(func.count()).select_from(User)).one()
        service = AuthService(db)
        users = service.get_all_users(limit=args.limit)

    if not users:
        print("No users found.")
        return

    print(f"{'ID':<5} {'Username':<20} {'Email':<30} {'Full Name':<25} {'System Role':<15} {'Active'}")
    print("-" * 100)
    for u in users:
        print(f"{u.id:<5} {u.username:<20} {u.email:<30} {u.full_name:<25} {u.system_role:<15} {u.is_active}")

    if total > args.limit:
        print(f"... {total - args.limit} more users (use --limit to show more)")


if __name__ == "__main__":
    main()
