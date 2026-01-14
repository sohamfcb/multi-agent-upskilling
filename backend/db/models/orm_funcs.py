import sqlalchemy as db
import uuid
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import (
    sessionmaker, 
    Session, 
    declarative_base, 
    Mapped, 
    mapped_column,
    relationship
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql import func

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URI=os.getenv("DATABASE_URI")

engine=create_engine(url=DATABASE_URI, echo=True, future=True)
SessionLocal=sessionmaker(bind=engine, autoflush=True, autocommit=False)
Base=declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Users(Base):
    __tablename__="users"

    id: Mapped[uuid.UUID]=mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid()
    )
    first_name: Mapped[str]=mapped_column(db.String(20), nullable=False)
    last_name: Mapped[str]=mapped_column(db.String(30), nullable=False)
    email: Mapped[str] = mapped_column(db.String(50), nullable=False, unique=True)
    username: Mapped[str] = mapped_column(db.String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    last_login: Mapped[datetime | None]
    token_version: Mapped[int] = mapped_column(db.Integer, nullable=False, default=0)
    is_verified: Mapped[bool] = mapped_column(db.Boolean, default=False)
    phone: Mapped[str | None] = mapped_column(db.String(12), nullable=True)

    __table_args__ = (
        db.UniqueConstraint("email", name="uq_users_email"),
        db.UniqueConstraint("username", name="uq_users_username"),
        db.Index("ix_users_email", "email"),
        db.Index("ix_users_username", "username"),
    )


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid()   # requires: CREATE EXTENSION IF NOT EXISTS "pgcrypto";
    )
    user_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    highest_qualification = db.Column(db.String(120))
    degree = db.Column(db.String(120))
    institution = db.Column(db.String(120))
    graduation_year = db.Column(db.Integer)
    years_experience = db.Column(db.Integer)
    current_job_title = db.Column(db.String(120))
    current_company = db.Column(db.String(120))

    # TEXT[] in Postgres
    skills = db.Column(ARRAY(db.Text))

    career_goal_short = db.Column(db.Text)
    career_goal_long  = db.Column(db.Text)
    resume_url        = db.Column(db.Text)

    # relationship to User (assumes a User model with __tablename__ = "users")
    user = relationship("Users", backref="profiles", lazy="selectin")


