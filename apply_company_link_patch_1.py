from pathlib import Path

path = Path("services/supabase_storage.py")
text = path.read_text()

text = text.replace(
    'def save_valuation_supabase(valuation_type, name, payload, user_id=None):',
    'def save_valuation_supabase(valuation_type, name, payload, user_id=None, company_name=None):',
    1,
)

text = text.replace(
    '''                INSERT INTO valuations (
                    user_id,
                    valuation_type,
                    name,
                    payload
                )''',
    '''                INSERT INTO valuations (
                    user_id,
                    valuation_type,
                    name,
                    company_name,
                    payload
                )''',
    1,
)

text = text.replace(
    '''                VALUES (
                    :user_id,
                    :valuation_type,
                    :name,
                    CAST(:payload AS jsonb)
                )''',
    '''                VALUES (
                    :user_id,
                    :valuation_type,
                    :name,
                    :company_name,
                    CAST(:payload AS jsonb)
                )''',
    1,
)

text = text.replace(
    '''                "name": name,
                "payload": json.dumps(payload),''',
    '''                "name": name,
                "company_name": company_name or name,
                "payload": json.dumps(payload),''',
    1,
)

text = text.replace(
    '''                SELECT id, valuation_type, name, created_at
                FROM valuations''',
    '''                SELECT id, valuation_type, name, company_name, created_at
                FROM valuations''',
    1,
)

text = text.replace(
    '''            "created_at": str(row[3]),''',
    '''            "company_name": row[3],
            "created_at": str(row[4]),''',
    1,
)

path.write_text(text)
print("Valuation service now supports company_name.")
