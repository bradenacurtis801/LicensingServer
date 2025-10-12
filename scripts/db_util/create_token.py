#!/usr/bin/env python3
"""
Create an API token for a user.

Available scopes:
  license:read  license:write  license:delete
  customer:read  customer:write  customer:delete
  application:read  application:write  application:delete
  activation:read  activation:write  activation:delete
  validation  user:management  token:management

Usage:
  python scripts/create_token.py <username> <token_name> --scopes license:read license:write
  python scripts/create_token.py alice my-sdk-token --scopes validation license:read
"""
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlmodel import Session
from app.database.connection import engine
from app.services.auth_service import AuthService
from app.models.database import TokenScope
from app.models.schemas import APITokenCreate


def main():
    parser = argparse.ArgumentParser(description="Create an API token for a user")
    parser.add_argument("username")
    parser.add_argument("token_name")
    parser.add_argument("--scopes", nargs="+", required=True, metavar="SCOPE",
                        help="One or more token scopes")
    args = parser.parse_args()

    try:
        scopes = [TokenScope(s) for s in args.scopes]
    except ValueError as e:
        print(f"Invalid scope: {e}")
        sys.exit(1)

    with Session(engine) as db:
        service = AuthService(db)
        user = service.get_user_by_username(args.username)
        if not user:
            print(f"User '{args.username}' not found.")
            sys.exit(1)

        result = service.create_api_token(user, APITokenCreate(
            name=args.token_name,
            scopes=scopes,
        ))

    print(f"Token created: {result.name} (id={result.id})")
    print(f"Scopes: {', '.join(s.value for s in result.scopes)}")
    print(f"Expires: {result.expires_at}")
    print()
    print(f"Token: {result.token}")
    print()
    print("Save this token — it will not be shown again.")


if __name__ == "__main__":
    main()
