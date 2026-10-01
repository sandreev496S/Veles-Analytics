import os
import uuid
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client
from services.supabase_storage import engine
from sqlalchemy import text

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
REPORTS_BUCKET = os.getenv("SUPABASE_REPORTS_BUCKET", "reports")

storage_client = (
    create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    if SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY
    else None
)


def _require_report_storage():
    if storage_client is None or engine is None:
        raise RuntimeError(
            "Cloud report storage is not configured. Set SUPABASE_URL, "
            "SUPABASE_SERVICE_ROLE_KEY, and DATABASE_URL."
        )


def upload_report_bytes(
    user_id,
    report_type,
    file_name,
    file_bytes,
    mime_type,
    valuation_id=None,
    company_name=None,
):
    _require_report_storage()

    if not user_id:
        raise ValueError("user_id is required")

    if not file_bytes:
        raise ValueError("file_bytes is required")

    safe_file_name = file_name.replace("/", "_").replace("\\", "_")
    storage_path = f"{user_id}/{datetime.utcnow().strftime('%Y/%m/%d')}/{uuid.uuid4()}_{safe_file_name}"

    storage_client.storage.from_(REPORTS_BUCKET).upload(
        path=storage_path,
        file=file_bytes,
        file_options={
            "content-type": mime_type,
            "upsert": "false",
        },
    )

    with engine.begin() as conn:
        row = conn.execute(
            text("""
                INSERT INTO public.reports (
                    user_id,
                    report_type,
                    name,
                    company_name,
                    storage_path,
                    file_name,
                    mime_type,
                    file_size_bytes,
                    payload
                )
                VALUES (
                    :user_id,
                    :report_type,
                    :name,
                    :company_name,
                    :storage_path,
                    :file_name,
                    :mime_type,
                    :file_size_bytes,
                    CAST(:payload AS jsonb)
                )
                RETURNING id
            """),
            {
                "user_id": user_id,
                "report_type": report_type,
                "name": file_name,
                "company_name": company_name,
                "storage_path": storage_path,
                "file_name": file_name,
                "mime_type": mime_type,
                "file_size_bytes": len(file_bytes),
                "payload": "{}",
            },
        ).fetchone()

    return str(row[0]), storage_path


def create_signed_report_url(storage_path, expires_in=3600):
    _require_report_storage()
    response = storage_client.storage.from_(REPORTS_BUCKET).create_signed_url(
        storage_path,
        expires_in,
    )

    if isinstance(response, dict):
        if "signedURL" in response:
            return response["signedURL"]
        if "signedUrl" in response:
            return response["signedUrl"]
        if "signed_url" in response:
            return response["signed_url"]

        data = response.get("data")
        if isinstance(data, dict):
            return (
                data.get("signedURL")
                or data.get("signedUrl")
                or data.get("signed_url")
            )

    if hasattr(response, "signed_url"):
        return response.signed_url

    if hasattr(response, "signedURL"):
        return response.signedURL

    if hasattr(response, "dict"):
        data = response.dict()
        return (
            data.get("signedURL")
            or data.get("signedUrl")
            or data.get("signed_url")
        )

    raise RuntimeError(f"Could not create signed URL from response: {response}")


def list_user_reports(user_id):
    if engine is None:
        return []
    with engine.begin() as conn:
        rows = conn.execute(
            text("""
                SELECT id, report_type, name, company_name, storage_path, file_name, mime_type, file_size_bytes, created_at
                FROM public.reports
                WHERE user_id = :user_id
                ORDER BY created_at DESC
            """),
            {"user_id": user_id},
        ).fetchall()

    return [
        {
            "id": str(row[0]),
            "report_type": row[1],
            "name": row[2],
            "company_name": row[3],
            "storage_path": row[4],
            "file_name": row[5],
            "mime_type": row[6],
            "file_size_bytes": row[7],
            "created_at": str(row[8]),
        }
        for row in rows
    ]
