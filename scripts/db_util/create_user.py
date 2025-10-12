#!/usr/bin/env python3
"""
Create a new user.

Usage:
  python scripts/create_user.py <username> <email> <full_name> <password>
  python scripts/create_user.py admin admin@example.com "Admin User" secret123 --admin
"""
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlmodel import Session, select
from app.database.connection import engine
from app.services.auth_service import AuthService
from app.models.database import User, SystemRole
from app.models.schemas import UserCreate


def main():
    parser = argparse.ArgumentParser(description="Create a new user")
    parser.add_argument("username")
    parser.add_argument("email")
    parser.add_argument("full_name")
    parser.add_argument("password")
    parser.add_argument("--admin", action="store_true", help="Grant system admin role")
    args = parser.parse_args()

    with Session(engine) as db:
        service = AuthService(db)
        user = service.create_user(UserCreate(
            username=args.username,
            email=args.email,
            full_name=args.full_name,
            password=args.password,
        ))

        if args.admin:
            db_user = db.exec(select(User).where(User.id == user.id)).first()
            db_user.system_role = SystemRole.SYSTEM_ADMIN
            db.add(db_user)
            db.commit()
            print(f"Created user: {user.username} (id={user.id}) [system_admin]")
        else:
            print(f"Created user: {user.username} (id={user.id})")


if __name__ == "__main__":
    main()
