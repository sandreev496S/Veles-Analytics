from sqlalchemy import text

from services.supabase_storage import engine


def list_companies():
    if engine is None:
        return []
    with engine.begin() as conn:
        rows = conn.execute(
            text("""
                SELECT
                    id,
                    name,
                    sector,
                    focus,
                    modality,
                    stage,
                    funding,
                    valuation,
                    risk,
                    website,
                    created_at,
                    updated_at
                FROM public.companies
                ORDER BY name ASC
            """)
        ).fetchall()

    return [
        {
            "id": str(row[0]),
            "name": row[1],
            "sector": row[2],
            "focus": row[3],
            "modality": row[4],
            "stage": row[5],
            "funding": row[6],
            "valuation": row[7],
            "risk": row[8],
            "website": row[9],
            "created_at": str(row[10]),
            "updated_at": str(row[11]),
        }
        for row in rows
    ]


def get_company(company_name):
    if engine is None:
        return None
    with engine.begin() as conn:
        row = conn.execute(
            text("""
                SELECT
                    id,
                    name,
                    sector,
                    focus,
                    modality,
                    stage,
                    funding,
                    valuation,
                    risk,
                    website,
                    created_at,
                    updated_at
                FROM public.companies
                WHERE name = :name
                LIMIT 1
            """),
            {"name": company_name},
        ).fetchone()

    if not row:
        return None

    return {
        "id": str(row[0]),
        "name": row[1],
        "sector": row[2],
        "focus": row[3],
        "modality": row[4],
        "stage": row[5],
        "funding": row[6],
        "valuation": row[7],
        "risk": row[8],
        "website": row[9],
        "created_at": str(row[10]),
        "updated_at": str(row[11]),
    }


def get_company_profiles():
    companies = list_companies()

    return {
        company["name"]: {
            "stage": company["stage"],
            "focus": company["focus"],
            "modality": company["modality"],
            "funding": company["funding"],
            "valuation": company["valuation"],
            "risk": company["risk"],
            "sector": company["sector"],
            "website": company["website"],
        }
        for company in companies
    }


def get_company_names():
    return [company["name"] for company in list_companies()]


def create_company(
    name,
    sector=None,
    focus=None,
    modality=None,
    stage=None,
    funding=None,
    valuation=None,
    risk=None,
    website=None,
):
    if engine is None:
        raise RuntimeError("Company database is unavailable because DATABASE_URL is not configured.")
    with engine.begin() as conn:
        row = conn.execute(
            text("""
                INSERT INTO public.companies (
                    name,
                    sector,
                    focus,
                    modality,
                    stage,
                    funding,
                    valuation,
                    risk,
                    website
                )
                VALUES (
                    :name,
                    :sector,
                    :focus,
                    :modality,
                    :stage,
                    :funding,
                    :valuation,
                    :risk,
                    :website
                )
                RETURNING id
            """),
            {
                "name": name,
                "sector": sector,
                "focus": focus,
                "modality": modality,
                "stage": stage,
                "funding": funding,
                "valuation": valuation,
                "risk": risk,
                "website": website,
            },
        ).fetchone()

    return str(row[0])


def update_company(company_id, **fields):
    if engine is None:
        raise RuntimeError("Company database is unavailable because DATABASE_URL is not configured.")
    allowed_fields = {
        "name",
        "sector",
        "focus",
        "modality",
        "stage",
        "funding",
        "valuation",
        "risk",
        "website",
    }

    updates = {
        key: value
        for key, value in fields.items()
        if key in allowed_fields
    }

    if not updates:
        return None

    set_clause = ", ".join(
        [f"{key} = :{key}" for key in updates.keys()]
    )

    query = text(f"""
        UPDATE public.companies
        SET {set_clause},
            updated_at = now()
        WHERE id = :company_id
        RETURNING id
    """)

    updates["company_id"] = company_id

    with engine.begin() as conn:
        row = conn.execute(query, updates).fetchone()

    return str(row[0]) if row else None


def delete_company(company_id):
    if engine is None:
        raise RuntimeError("Company database is unavailable because DATABASE_URL is not configured.")
    with engine.begin() as conn:
        row = conn.execute(
            text("""
                DELETE FROM public.companies
                WHERE id = :company_id
                RETURNING id
            """),
            {"company_id": company_id},
        ).fetchone()

    return row is not None
