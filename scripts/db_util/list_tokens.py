#!/usr/bin/env python3
"""
List API tokens for a user.

Usage:
  python scripts/list_tokens.py <username>
"""
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlmodel import Session
from app.database.connection import engine
from app.services.auth_service import AuthService


def main():
    parser = argparse.ArgumentParser(description="List API tokens for a user")
    parser.add_argument("username")
    args = parser.parse_args()

    with Session(engine) as db:
        service = AuthService(db)
        user = service.get_user_by_username(args.username)
        if not user:
            print(f"User '{args.username}' not found.")
            sys.exit(1)

        tokens = service.list_api_tokens(user.id)

    if not tokens:
        print(f"No tokens for '{args.username}'.")
        return

    print(f"{'ID':<5} {'Name':<25} {'Active':<8} {'Expires':<22} {'Last Used':<22} Scopes")
    print("-" * 110)
    for t in tokens:
        scopes = ", ".join(s.value for s in t.scopes)
        last_used = str(t.last_used_at)[:19] if t.last_used_at else "never"
        expires = str(t.expires_at)[:19] if t.expires_at else "never"
        print(f"{t.id:<5} {t.name:<25} {str(t.is_active):<8} {expires:<22} {last_used:<22} {scopes}")


if __name__ == "__main__":
    main()
