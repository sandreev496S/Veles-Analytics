from sqlalchemy import text
from services.supabase_storage import engine

companies = [
    ("Neuralink", "Neurotechnology", "Implantable BCI", "Invasive", "Series D", "$686M+", "$6.1B valuation", "Regulatory and surgical adoption risk"),
    ("Synchron", "Neurotechnology", "Endovascular BCI", "Minimally invasive", "Clinical-stage", "$145M+", "Private valuation", "Clinical validation and commercialization risk"),
    ("Paradromics", "Neurotechnology", "High-bandwidth implantable BCI", "Invasive", "Clinical-stage", "$100M+", "Private valuation", "Technical execution and trial progression risk"),
    ("Blackrock Neurotech", "Neurotechnology", "Neural interfaces and research systems", "Invasive", "Growth stage", "Private", "Private valuation", "Competitive positioning and scaling risk"),
    ("Precision Neuroscience", "Neurotechnology", "Minimally invasive BCI", "Minimally invasive", "Series B", "$100M+", "Private valuation", "Regulatory pathway and market adoption risk"),
]

with engine.begin() as conn:
    for company in companies:
        conn.execute(
            text("""
                INSERT INTO public.companies (
                    name, sector, focus, modality, stage, funding, valuation, risk
                )
                VALUES (
                    :name, :sector, :focus, :modality, :stage, :funding, :valuation, :risk
                )
                ON CONFLICT (name) DO UPDATE SET
                    sector = EXCLUDED.sector,
                    focus = EXCLUDED.focus,
                    modality = EXCLUDED.modality,
                    stage = EXCLUDED.stage,
                    funding = EXCLUDED.funding,
                    valuation = EXCLUDED.valuation,
                    risk = EXCLUDED.risk,
                    updated_at = now()
            """),
            {
                "name": company[0],
                "sector": company[1],
                "focus": company[2],
                "modality": company[3],
                "stage": company[4],
                "funding": company[5],
                "valuation": company[6],
                "risk": company[7],
            },
        )

print("Seeded companies.")
