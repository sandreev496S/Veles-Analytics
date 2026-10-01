# Launching Veles Analytics

## macOS or Linux

From the extracted project directory:

```bash
chmod +x setup.sh
./setup.sh
```

The script creates `.venv`, installs every pinned dependency, creates `.env`
in demo mode when needed, runs the environment check, and starts Streamlit at
`http://localhost:8501`.

## Windows PowerShell

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\setup.ps1
```

## Verify without starting Streamlit

```bash
source .venv/bin/activate
python scripts/check_environment.py
```

## Production mode

Change `APP_MODE=demo` to `APP_MODE=production` in `.env` and configure:

- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`
- `DATABASE_URL`
- `OPENAI_API_KEY` (optional if AI commentary is disabled)

Never commit `.env` or production credentials to source control.
