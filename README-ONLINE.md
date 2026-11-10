# CodeIt 2.0 — Cinematic Online Edition

CodeIt keeps Ollama as its local inference engine and uses Supabase for online accounts and synchronized chat history.

## What is online and what stays local?

- Accounts and authentication: Supabase Auth.
- Conversation history: Supabase Postgres, protected by Row Level Security (RLS).
- Model inference: Ollama on the computer currently running CodeIt.
- Installed models: local to each computer. Model selection shows models installed in that computer's Ollama instance.
- Existing `codeit.db`: preserved. The app includes an import action that copies its old conversations to the signed-in account without deleting or changing the local database.

To use CodeIt from another computer, install Ollama and the required model on that computer, configure the same Supabase project, and run CodeIt there. Your account and cloud conversations will sync; the AI model itself is not hosted in the cloud.

## 1. Create the Supabase project

1. Open https://supabase.com/ and create a free project.
2. In the project dashboard, open **SQL Editor** and create a new query.
3. Paste all contents of `supabase_schema.sql` and run it.
4. Open **Project Settings → API** (or **Data API / API Keys**, depending on dashboard layout).
5. Copy the Project URL and the **anon / publishable** key. Never use or share the `service_role` / secret key in this app.

## 2. Configure CodeIt

1. In the CodeIt folder, create a folder named `.streamlit` if it does not exist.
2. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`.
3. Replace the placeholder values with your Supabase Project URL and anon/publishable key:

```toml
[supabase]
url = "https://YOUR_PROJECT_ID.supabase.co"
anon_key = "YOUR_SUPABASE_ANON_KEY"
```

Keep `secrets.toml` private. Do not upload it to GitHub or send it to anyone.

## 3. Configure email confirmation

In Supabase Dashboard → Authentication → Providers → Email, choose whether to require email confirmation. If confirmation is enabled, users must confirm their email before signing in. For reliable email delivery beyond testing, configure SMTP in Supabase Authentication settings.

For a private personal project, you can disable email confirmation while testing. Do not disable security protections for a public production service without understanding the trade-offs.

## 4. Install and run

Open PowerShell in the CodeIt folder:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\setup_codeit.ps1
.\start_codeit.ps1
```

Open http://localhost:8501.

## 5. First login and old history

- Create an account in the **Create account** tab.
- Sign in.
- Open **Import previous local conversations** in the sidebar and select **Import local history**.
- This copies old conversations to your account. It does not delete `codeit.db` or alter its rows. Re-running the import skips conversations already imported for that account.

## 6. Model selection

The sidebar reads the installed model list from `http://127.0.0.1:11434/api/tags`. Select any installed model from **Active model**. Use **Get another model** to pull a model by its Ollama library name. The downloaded model becomes available in the selector after refresh.

Examples:

- `codeit:latest`
- `qwen2.5-coder:7b`
- `qwen2.5-coder:3b`

A model must be installed on each computer where you want to use it.

## Security notes

- Passwords are managed by Supabase Auth; CodeIt does not store plaintext passwords.
- The app uses only the Supabase anon/publishable key. Never put a service-role key in `secrets.toml`.
- The SQL schema enables RLS and scopes each chat and message to its authenticated owner.
- Use a strong unique password and enable email confirmation for accounts exposed beyond a private test.
- This is a starter deployment. For a public multi-user hosted service, use a properly deployed HTTPS app, configure Supabase redirect/email settings, and review rate limits and backups.

## Troubleshooting

- **Supabase is not configured:** create `.streamlit/secrets.toml` and verify the URL/key.
- **Invalid API key:** use the anon/publishable key, not the service-role secret.
- **Table not found:** run `supabase_schema.sql` in the correct Supabase project.
- **Email not confirmed:** check the account email and Supabase Auth email settings.
- **Ollama offline:** start the Ollama desktop app. CodeIt checks `127.0.0.1:11434`.
- **No models appear:** run `ollama list` in PowerShell or use **Get another model**.
- **Slow response:** try a smaller model such as `qwen2.5-coder:3b`.
