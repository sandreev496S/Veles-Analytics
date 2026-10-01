from datetime import datetime, timezone

from sqlalchemy import text

from services.supabase_storage import engine


def list_research_notes(user_id, company_name):
    with engine.begin() as conn:
        rows = conn.execute(
            text("""
                SELECT id, user_id, company_name, note_type, content, created_at, updated_at
                FROM research_notes
                WHERE user_id = :user_id
                AND company_name = :company_name
                ORDER BY updated_at DESC
            """),
            {
                "user_id": user_id,
                "company_name": company_name,
            },
        ).fetchall()

    return [
        {
            "id": str(row[0]),
            "user_id": str(row[1]),
            "company_name": row[2],
            "note_type": row[3],
            "content": row[4],
            "created_at": str(row[5]),
            "updated_at": str(row[6]),
        }
        for row in rows
    ]


def load_research_note(user_id, company_name, note_type="general"):
    with engine.begin() as conn:
        row = conn.execute(
            text("""
                SELECT id, user_id, company_name, note_type, content, created_at, updated_at
                FROM research_notes
                WHERE user_id = :user_id
                AND company_name = :company_name
                AND note_type = :note_type
                LIMIT 1
            """),
            {
                "user_id": user_id,
                "company_name": company_name,
                "note_type": note_type,
            },
        ).fetchone()

    if not row:
        return None

    return {
        "id": str(row[0]),
        "user_id": str(row[1]),
        "company_name": row[2],
        "note_type": row[3],
        "content": row[4],
        "created_at": str(row[5]),
        "updated_at": str(row[6]),
    }


def save_research_note(user_id, company_name, note_type, content):
    existing = load_research_note(
        user_id=user_id,
        company_name=company_name,
        note_type=note_type,
    )

    now = datetime.now(timezone.utc)

    with engine.begin() as conn:
        if existing:
            row = conn.execute(
                text("""
                    UPDATE research_notes
                    SET content = :content,
                        updated_at = :updated_at
                    WHERE id = :id
                    AND user_id = :user_id
                    RETURNING id, user_id, company_name, note_type, content, created_at, updated_at
                """),
                {
                    "id": existing["id"],
                    "user_id": user_id,
                    "content": content,
                    "updated_at": now,
                },
            ).fetchone()
        else:
            row = conn.execute(
                text("""
                    INSERT INTO research_notes (
                        user_id,
                        company_name,
                        note_type,
                        content,
                        created_at,
                        updated_at
                    )
                    VALUES (
                        :user_id,
                        :company_name,
                        :note_type,
                        :content,
                        :created_at,
                        :updated_at
                    )
                    RETURNING id, user_id, company_name, note_type, content, created_at, updated_at
                """),
                {
                    "user_id": user_id,
                    "company_name": company_name,
                    "note_type": note_type,
                    "content": content,
                    "created_at": now,
                    "updated_at": now,
                },
            ).fetchone()

    return {
        "id": str(row[0]),
        "user_id": str(row[1]),
        "company_name": row[2],
        "note_type": row[3],
        "content": row[4],
        "created_at": str(row[5]),
        "updated_at": str(row[6]),
    }


def delete_research_note(user_id, note_id):
    with engine.begin() as conn:
        row = conn.execute(
            text("""
                DELETE FROM research_notes
                WHERE id = :id
                AND user_id = :user_id
                RETURNING id
            """),
            {
                "id": note_id,
                "user_id": user_id,
            },
        ).fetchone()

    return row is not None
