# Running Veles as a Streamlit web app

## Local demo mode

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\\Scripts\\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

Open the local URL printed by Streamlit, normally `http://localhost:8501`.
Demo mode bypasses Supabase authentication and lets the interface load without cloud credentials.

## Production mode

Set `APP_MODE=production` and configure:

- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`
- `DATABASE_URL`
- `OPENAI_API_KEY` when AI memo generation is enabled

Never commit production secrets to Git. Add them in Streamlit Community Cloud or Render's environment-variable settings.

## Streamlit Community Cloud

1. Push this folder to a GitHub repository.
2. In Streamlit Community Cloud, create an app from the repository.
3. Set the entry point to `app.py`.
4. For a public demo, add this secret:

```toml
APP_MODE = "demo"
```

5. For production, add all variables listed above and use `APP_MODE = "production"`.

## Render

The included `render.yaml` uses:

```text
streamlit run app.py --server.address 0.0.0.0 --server.port $PORT --server.headless true
```

For an initial demo deployment, add `APP_MODE=demo` in Render. For production, add the Supabase/Postgres secrets.

## Health checks

Before deployment:

```bash
python -m compileall app.py services components ui
pytest -q
streamlit run app.py --server.headless true
```
