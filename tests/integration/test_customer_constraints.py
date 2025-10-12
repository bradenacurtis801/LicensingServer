"""
Integration tests for customer email uniqueness constraints.

Verifies:
- Two different users can share the same customer email
- A single user cannot have two customers with the same email
"""
import pytest
from sqlalchemy.exc import IntegrityError
from app.models.database import Customer, User, SystemRole
from app.models.schemas import UserRole


def _make_user(db, username: str) -> User:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    user = User(
        username=username,
        email=f"{username}@example.com",
        full_name=username.title(),
        password_hash=pwd_context.hash("password"),
        business_role=UserRole.USER,
        system_role=SystemRole.USER,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.mark.integration
class TestCustomerEmailConstraints:

    def test_different_users_can_share_customer_email(self, db_session):
        user1 = _make_user(db_session, "alice")
        user2 = _make_user(db_session, "bob")
        shared_email = "shared@example.com"

        db_session.add(Customer(name="Alice's Customer", email=shared_email, user_id=user1.id))
        db_session.commit()

        db_session.add(Customer(name="Bob's Customer", email=shared_email, user_id=user2.id))
        db_session.commit()  # Should not raise

        customers = [c for c in db_session.exec(
            __import__("sqlmodel").select(Customer).where(Customer.email == shared_email)
        ).all()]
        assert len(customers) == 2

    def test_same_user_cannot_have_duplicate_customer_email(self, db_session):
        user = _make_user(db_session, "charlie")
        email = "unique@example.com"

        db_session.add(Customer(name="First Customer", email=email, user_id=user.id))
        db_session.commit()

        db_session.add(Customer(name="Duplicate Customer", email=email, user_id=user.id))
        with pytest.raises(IntegrityError, match="uq_user_email"):
            db_session.commit()
