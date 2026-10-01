import os
import json
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.dialects.postgresql import JSONB

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DEFAULT_USER_EMAIL = os.getenv("DEFAULT_USER_EMAIL", "admin@velesanalytics.com")
DEFAULT_USER_NAME = os.getenv("DEFAULT_USER_NAME", "Admin")

engine = create_engine(DATABASE_URL, pool_pre_ping=True) if DATABASE_URL else None


def _require_engine():
    if engine is None:
        raise RuntimeError(
            "Cloud database is not configured. Set DATABASE_URL or run in demo mode "
            "and use local saved valuations."
        )
    return engine


def get_or_create_default_user():
    with _require_engine().begin() as conn:
        row = conn.execute(
            text("SELECT id FROM users WHERE email = :email"),
            {"email": DEFAULT_USER_EMAIL},
        ).fetchone()

        if row:
            return str(row[0])

        row = conn.execute(
            text("""
                INSERT INTO users (email, name)
                VALUES (:email, :name)
                RETURNING id
            """),
            {"email": DEFAULT_USER_EMAIL, "name": DEFAULT_USER_NAME},
        ).fetchone()

        return str(row[0])


def save_valuation_supabase(valuation_type, name, payload, user_id=None, company_name=None):
    if not user_id:
        raise ValueError("user_id is required to save a valuation")

    with _require_engine().begin() as conn:
        row = conn.execute(
            text("""
                INSERT INTO valuations (
                    user_id,
                    valuation_type,
                    name,
                    company_name,
                    payload
                )
                VALUES (
                    :user_id,
                    :valuation_type,
                    :name,
                    :company_name,
                    CAST(:payload AS jsonb)
                )
                RETURNING id
            """),
            {
                "user_id": user_id,
                "valuation_type": valuation_type,
                "name": name,
                "company_name": company_name or name,
                "payload": json.dumps(payload),
            },
        ).fetchone()

        return str(row[0])


def list_valuations_supabase(user_id=None):
    if not user_id:
        raise ValueError("user_id is required to list valuations")

    with _require_engine().begin() as conn:
        rows = conn.execute(
            text("""
                SELECT id, valuation_type, name, company_name, created_at
                FROM valuations
                WHERE user_id = :user_id
                ORDER BY created_at DESC
            """),
            {"user_id": user_id},
        ).fetchall()

    return [
        {
            "id": str(row[0]),
            "kind": row[1],
            "name": row[2],
            "company_name": row[3],
            "created_at": str(row[4]),
        }
        for row in rows
    ]


def load_valuation_supabase(valuation_id, user_id=None):
    if not user_id:
        raise ValueError("user_id is required to load a valuation")

    with _require_engine().begin() as conn:
        row = conn.execute(
            text("""
                SELECT id, valuation_type, name, payload, created_at
                FROM valuations
                WHERE id = :id
                AND user_id = :user_id
            """),
            {"id": valuation_id, "user_id": user_id},
        ).fetchone()

    if not row:
        return None

    return {
        "id": str(row[0]),
        "kind": row[1],
        "name": row[2],
        "payload": row[3],
        "created_at": str(row[4]),
    }

def delete_valuation_supabase(valuation_id, user_id=None):
    if not user_id:
        raise ValueError("user_id is required to delete a valuation")

    with _require_engine().begin() as conn:
        result = conn.execute(
            text("""
                DELETE FROM valuations
                WHERE id = :id
                AND user_id = :user_id
            """),
            {"id": valuation_id, "user_id": user_id},
        )

    return result.rowcount > 0

