from __future__ import annotations

import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
import streamlit as st
from supabase import Client, create_client

APP_DIR = Path(__file__).resolve().parent
DB_PATH = APP_DIR / "codeit.db"
OLLAMA_URL = "http://127.0.0.1:11434"
MAX_HISTORY = 24

st.set_page_config(
    page_title="CodeIt — Cinematic AI Workspace",
    page_icon="⌘",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# Cinematic visual system
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
    :root{--bg:#080a11;--panel:#101522;--panel2:#151c2b;--line:rgba(173,185,220,.13);--muted:#8792aa;--text:#eef1fb;--violet:#927dff;--cyan:#60dfd0;}
    html,body,[class*="css"]{font-family:'Manrope',sans-serif}
    .stApp{color:var(--text);background:radial-gradient(ellipse at 75% -10%,rgba(119,91,255,.23),transparent 36%),radial-gradient(ellipse at 5% 45%,rgba(45,190,177,.08),transparent 28%),linear-gradient(135deg,#080a11,#0a0d16 55%,#0b0c17)}
    [data-testid="stHeader"]{background:rgba(8,10,17,.68)}
    [data-testid="stSidebar"]{background:linear-gradient(180deg,#101522,#0b0f18);border-right:1px solid var(--line)}
    [data-testid="stSidebar"]>div:first-child{padding-top:1.15rem}
    .block-container{max-width:1200px;padding-top:1.8rem;padding-bottom:7rem}
    .brand{display:flex;align-items:center;gap:12px;margin:.2rem 0 1.3rem}
    .brand-icon{height:44px;width:44px;display:grid;place-items:center;border-radius:15px;background:linear-gradient(140deg,#a99aff,#6854e8 60%,#3ba9a7);box-shadow:0 9px 34px #7761ff42;color:white;font-size:22px;font-weight:900}
    .brand-name{font-size:1.23rem;font-weight:850;letter-spacing:-.06em;color:#f7f7ff}
    .brand-sub{font: .65rem 'DM Mono',monospace;letter-spacing:.17em;color:#8290a9;margin-top:2px}
    .eyebrow{font:.68rem 'DM Mono',monospace;letter-spacing:.19em;text-transform:uppercase;color:#a697ff}
    .hero{font-size:clamp(2.6rem,6vw,4.5rem);font-weight:850;line-height:1.02;letter-spacing:-.085em;color:#f4f5ff;margin:.7rem 0 1rem}
    .hero span{background:linear-gradient(95deg,#b7aaff,#7fdddc);-webkit-background-clip:text;background-clip:text;color:transparent}
    .subcopy{max-width:680px;color:#929db3;line-height:1.8;font-size:1rem}
    .topbar{display:flex;align-items:center;justify-content:space-between;gap:1rem;margin-bottom:1.8rem}
    .pill{display:inline-flex;align-items:center;gap:8px;border:1px solid #5dd9c533;background:#5dd9c30d;color:#8ce9dc;border-radius:99px;padding:7px 12px;font-size:.73rem;font-weight:750}
    .pill.off{border-color:#ff8d8d33;background:#ff77770c;color:#ffaaaa}
    .dot{width:7px;height:7px;border-radius:50%;background:#61dfce;box-shadow:0 0 13px #61dfce}
    .off .dot{background:#ff8585;box-shadow:0 0 13px #ff8585}
    .section{font:.66rem 'DM Mono',monospace;text-transform:uppercase;letter-spacing:.16em;color:#78849d;margin:1.35rem 0 .65rem}
    .feature{height:100%;min-height:130px;border:1px solid var(--line);border-radius:18px;padding:1.1rem;background:linear-gradient(145deg,#171e2dce,#101521ed);box-shadow:inset 0 1px #ffffff08;transition:transform .2s,border-color .2s}
    .feature:hover{transform:translateY(-3px);border-color:#a394ff66}
    .feature-icon{font-size:1.3rem;margin-bottom:.65rem}.feature-title{font-size:.9rem;font-weight:800;color:#f0f1fb;margin-bottom:.35rem}.feature-desc{font-size:.75rem;line-height:1.6;color:#8d99b0}
    div.stButton>button{border:1px solid var(--line);border-radius:13px;min-height:42px;background:#ffffff06;color:#e6eafa;font-weight:700;transition:all .18s}
    div.stButton>button:hover{border-color:#a18fff99;background:#927dff16;color:white;transform:translateY(-1px)}
    div.stButton>button[kind="primary"]{background:linear-gradient(110deg,#917cff,#6553df);border:0;color:white;box-shadow:0 9px 26px #7058ed3b}
    div.stButton>button[kind="primary"]:hover{background:linear-gradient(110deg,#a493ff,#7564ef)}
    [data-testid="stChatMessage"]{background:#121827bd;border:1px solid var(--line);border-radius:18px;padding:1rem 1.2rem;margin-bottom:.85rem}
    [data-testid="stChatInput"]{border:1px solid #9a88ff55;border-radius:18px;background:#111827}
    [data-testid="stChatInput"]:focus-within{border-color:#9a88ff;box-shadow:0 0 0 1px #9a88ff44}
    [data-testid="stChatInput"] textarea{color:#f5f5ff}
    [data-testid="stExpander"]{border:1px solid var(--line);border-radius:13px;background:#ffffff03}
    input,textarea{color-scheme:dark}
    .tiny{font-size:.72rem;color:#748199;line-height:1.6}
    .model-card{border:1px solid #a18fff33;background:linear-gradient(120deg,#927dff12,#5bd9ce08);border-radius:14px;padding:12px 14px;margin:.5rem 0}
    .auth-wrap{max-width:540px;margin:4vh auto 0;border:1px solid var(--line);border-radius:24px;padding:2rem;background:linear-gradient(145deg,#151b2bdf,#0e1320ed);box-shadow:0 30px 100px #0007,inset 0 1px #ffffff0b}
    .auth-title{font-size:2rem;font-weight:850;letter-spacing:-.07em;color:#f5f5ff;margin:.35rem 0}
    .auth-copy{color:#929db3;line-height:1.7;margin-bottom:1rem}
    hr{border-color:var(--line)}
    code,pre{font-family:'DM Mono',monospace!important}
    @media(max-width:700px){.block-container{padding-top:1rem}.hero{font-size:2.65rem}.topbar{align-items:flex-start;flex-direction:column}.auth-wrap{padding:1.2rem;margin-top:1rem}}
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Configuration and local database (legacy chats are kept intact)
# -----------------------------------------------------------------------------
def get_supabase_config() -> tuple[str | None, str | None]:
    try:
        section = st.secrets.get("supabase", {})
        return section.get("url"), section.get("anon_key")
    except Exception:
        return None, None


def local_connection():
    return sqlite3.connect(DB_PATH)


def initialize_local_database():
    # Keep the original messages table and its contents unchanged.
    with local_connection() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )""")
        con.commit()


def local_chat_ids():
    with local_connection() as con:
        return con.execute(
            "SELECT chat_id, MAX(created_at) FROM messages GROUP BY chat_id ORDER BY MAX(created_at) DESC"
        ).fetchall()


def local_messages(chat_id: str):
    with local_connection() as con:
        rows = con.execute(
            "SELECT role,content,created_at FROM messages WHERE chat_id=? ORDER BY id", (chat_id,)
        ).fetchall()
    return [{"role": r, "content": c, "created_at": d} for r, c, d in rows]


initialize_local_database()

# -----------------------------------------------------------------------------
# Ollama integration
# -----------------------------------------------------------------------------
def ollama_tags() -> tuple[bool, list[dict[str, Any]], str | None]:
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=4)
        response.raise_for_status()
        return True, response.json().get("models", []), None
    except requests.RequestException as exc:
        return False, [], str(exc)


def format_size(size: int | None) -> str:
    if not size:
        return "Unknown size"
    return f"{size / (1024 ** 3):.1f} GB"


def ollama_chat(model: str, messages: list[dict[str, str]]) -> str:
    response = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": 0.35, "num_ctx": 8192},
        },
        timeout=900,
    )
    response.raise_for_status()
    payload = response.json()
    return payload["message"]["content"]


def pull_ollama_model(model_name: str):
    response = requests.post(
        f"{OLLAMA_URL}/api/pull",
        json={"name": model_name, "stream": False},
        timeout=3600,
    )
    response.raise_for_status()
    return response.json()

# -----------------------------------------------------------------------------
# Supabase auth and cloud conversations
# -----------------------------------------------------------------------------
def get_client() -> Client | None:
    existing = st.session_state.get("supabase_client")
    if existing is not None:
        return existing
    url, key = get_supabase_config()
    if not url or not key:
        return None
    try:
        client = create_client(url, key)
        st.session_state.supabase_client = client
        return client
    except Exception:
        return None


def get_user_id() -> str | None:
    return st.session_state.get("user_id")


def cloud_list_chats(client: Client, user_id: str):
    result = (
        client.table("chat_sessions")
        .select("id,title,created_at,updated_at,legacy_chat_id")
        .eq("user_id", user_id)
        .order("updated_at", desc=True)
        .limit(60)
        .execute()
    )
    return result.data or []


def cloud_load_messages(client: Client, chat_id: str):
    result = (
        client.table("chat_messages")
        .select("role,content,created_at")
        .eq("chat_id", chat_id)
        .order("created_at")
        .limit(500)
        .execute()
    )
    return [{"role": row["role"], "content": row["content"]} for row in (result.data or [])]


def cloud_create_chat(client: Client, user_id: str, title: str, legacy_chat_id: str | None = None) -> str:
    row = {"user_id": user_id, "title": title[:120]}
    if legacy_chat_id:
        row["legacy_chat_id"] = legacy_chat_id
    result = client.table("chat_sessions").insert(row).execute()
    return result.data[0]["id"]


def cloud_save_message(client: Client, user_id: str, chat_id: str, role: str, content: str, created_at: str | None = None):
    row = {"user_id": user_id, "chat_id": chat_id, "role": role, "content": content}
    if created_at:
        row["created_at"] = created_at
    client.table("chat_messages").insert(row).execute()
    client.table("chat_sessions").update(
        {"updated_at": datetime.now(timezone.utc).isoformat()}
    ).eq("id", chat_id).eq("user_id", user_id).execute()


def import_local_history(client: Client, user_id: str) -> tuple[int, int]:
    existing = cloud_list_chats(client, user_id)
    imported_ids = {row.get("legacy_chat_id") for row in existing if row.get("legacy_chat_id")}
    added = 0
    skipped = 0
    for old_chat_id, _ in local_chat_ids():
        if old_chat_id in imported_ids:
            skipped += 1
            continue
        old_messages = local_messages(old_chat_id)
        if not old_messages:
            continue
        first_prompt = next((m["content"] for m in old_messages if m["role"] == "user"), "Imported conversation")
        new_chat_id = cloud_create_chat(client, user_id, first_prompt[:120], old_chat_id)
        for message in old_messages:
            cloud_save_message(client, user_id, new_chat_id, message["role"], message["content"], message.get("created_at"))
        added += 1
    return added, skipped


def short_title(value: str | None, limit: int = 29) -> str:
    value = " ".join((value or "New conversation").split())
    return value if len(value) <= limit else value[: limit - 1] + "…"


def sign_out():
    client = get_client()
    try:
        if client:
            client.auth.sign_out()
    except Exception:
        pass
    for key in ("user_id", "user_email", "supabase_client", "chat_id", "messages", "selected_model"):
        st.session_state.pop(key, None)
    st.rerun()

# -----------------------------------------------------------------------------
# Authentication gate
# -----------------------------------------------------------------------------
client = get_client()
if not client:
    st.markdown('<div class="auth-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="brand"><div class="brand-icon">⌘</div><div><div class="brand-name">CodeIt</div><div class="brand-sub">CINEMATIC ONLINE EDITION</div></div></div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-title">Connect your workspace.</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-copy">Online accounts need your Supabase project connection. Your Ollama models and local database are not affected.</div>', unsafe_allow_html=True)
    st.error("Supabase is not configured yet.")
    st.markdown("Create `.streamlit/secrets.toml` using the included `secrets.toml.example`, then add your Supabase Project URL and anon key.")
    st.code('[supabase]\nurl = "https://YOUR_PROJECT.supabase.co"\nanon_key = "YOUR_SUPABASE_ANON_KEY"', language="toml")
    st.markdown("See `README-ONLINE.md` and run `supabase_schema.sql` in your Supabase SQL Editor.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

if not get_user_id():
    st.markdown('<div class="auth-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="brand"><div class="brand-icon">⌘</div><div><div class="brand-name">CodeIt</div><div class="brand-sub">CINEMATIC ONLINE EDITION</div></div></div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-title">Your code. Your workspace.</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-copy">Sign in to sync your conversations across devices. AI generation still runs through Ollama on the computer running CodeIt.</div>', unsafe_allow_html=True)
    tab_login, tab_signup = st.tabs(["Sign in", "Create account"])
    with tab_login:
        with st.form("login_form"):
            email = st.text_input("Email address", placeholder="you@example.com")
            password = st.text_input("Password", type="password", placeholder="Your password")
            submitted = st.form_submit_button("Sign in to CodeIt", type="primary", use_container_width=True)
        if submitted:
            try:
                result = client.auth.sign_in_with_password({"email": email.strip(), "password": password})
                if result.user:
                    st.session_state.user_id = result.user.id
                    st.session_state.user_email = result.user.email or email.strip()
                    st.rerun()
            except Exception as exc:
                st.error(f"Sign-in failed: {exc}")
    with tab_signup:
        with st.form("signup_form"):
            new_email = st.text_input("Email address", key="signup_email", placeholder="you@example.com")
            new_password = st.text_input("Password", type="password", key="signup_password", placeholder="At least 8 characters")
            confirm = st.text_input("Confirm password", type="password", key="signup_confirm")
            submitted_signup = st.form_submit_button("Create my account", type="primary", use_container_width=True)
        if submitted_signup:
            if not new_email.strip() or len(new_password) < 8:
                st.warning("Enter a valid email and a password with at least 8 characters.")
            elif new_password != confirm:
                st.warning("The passwords do not match.")
            else:
                try:
                    result = client.auth.sign_up({"email": new_email.strip(), "password": new_password})
                    if result.session and result.user:
                        st.session_state.user_id = result.user.id
                        st.session_state.user_email = result.user.email or new_email.strip()
                        st.success("Account created. Welcome to CodeIt!")
                        st.rerun()
                    else:
                        st.success("Account created. Check your email to confirm it, then sign in.")
                except Exception as exc:
                    st.error(f"Account creation failed: {exc}")
    st.markdown('<div class="tiny">Your password is handled by Supabase Auth. CodeIt never stores plaintext passwords.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

user_id = get_user_id()
user_email = st.session_state.get("user_email", "CodeIt user")

# Validate the active auth session; if expired, ask the user to sign in again.
try:
    client.auth.get_user()
except Exception:
    st.warning("Your online session expired. Please sign in again.")
    sign_out()

# -----------------------------------------------------------------------------
# Sidebar: model management, account, cloud conversations
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="brand"><div class="brand-icon">⌘</div><div><div class="brand-name">CodeIt</div><div class="brand-sub">ONLINE AI WORKSPACE</div></div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="tiny">Signed in as<br><b style="color:#e9eaff">{user_email}</b></div>', unsafe_allow_html=True)
    if st.button("↪  Sign out", use_container_width=True):
        sign_out()

    st.markdown('<div class="section">AI engine</div>', unsafe_allow_html=True)
    ollama_online, model_data, ollama_error = ollama_tags()
    if ollama_online:
        st.markdown('<div class="pill"><span class="dot"></span> Ollama connected</div>', unsafe_allow_html=True)
        model_names = sorted([m.get("name", "") for m in model_data if m.get("name")])
        if model_names:
            default_model = "codeit:latest" if "codeit:latest" in model_names else model_names[0]
            if st.session_state.get("selected_model") not in model_names:
                st.session_state.selected_model = default_model
            selected_model = st.selectbox("Active model", model_names, key="selected_model")
            selected_info = next((m for m in model_data if m.get("name") == selected_model), {})
            st.markdown(f'<div class="model-card"><div style="font-weight:800;color:#f0efff">{selected_model}</div><div class="tiny">{format_size(selected_info.get("size"))} · Installed locally</div></div>', unsafe_allow_html=True)
        else:
            st.warning("No Ollama models installed yet.")
            selected_model = None
        with st.expander("＋ Get another model"):
            pull_name = st.text_input("Ollama model name", placeholder="qwen2.5-coder:3b", key="pull_model_name")
            st.caption("Use a model name from the Ollama library, for example qwen2.5-coder:3b.")
            if st.button("Download model", use_container_width=True, disabled=not bool(pull_name.strip())):
                try:
                    with st.spinner(f"Downloading {pull_name.strip()}…"):
                        pull_ollama_model(pull_name.strip())
                    st.success("Model downloaded. Refreshing model list…")
                    st.rerun()
                except requests.RequestException as exc:
                    st.error(f"Model download failed: {exc}")
    else:
        selected_model = None
        st.markdown('<div class="pill off"><span class="dot"></span> Ollama offline</div>', unsafe_allow_html=True)
        st.caption("Start the Ollama desktop app. CodeIt checks 127.0.0.1:11434.")
        if ollama_error:
            st.caption(ollama_error[:180])

    st.markdown('<div class="section">Cloud conversations</div>', unsafe_allow_html=True)
    if st.button("＋  New conversation", type="primary", use_container_width=True):
        st.session_state.chat_id = None
        st.session_state.messages = []
        st.rerun()

    try:
        chats = cloud_list_chats(client, user_id)
    except Exception as exc:
        chats = []
        st.error(f"Could not load cloud conversations: {exc}")

    if not chats:
        st.markdown('<div class="tiny">Your synced conversations will appear here.</div>', unsafe_allow_html=True)
    for chat in chats:
        label = short_title(chat.get("title"))
        if chat.get("id") == st.session_state.get("chat_id"):
            label = "●  " + label
        if st.button(label, key=f"cloud-chat-{chat['id']}", use_container_width=True):
            st.session_state.chat_id = chat["id"]
            try:
                st.session_state.messages = cloud_load_messages(client, chat["id"])
            except Exception as exc:
                st.error(f"Could not open conversation: {exc}")
                st.session_state.messages = []
            st.rerun()

    with st.expander("Import previous local conversations"):
        st.caption("Copies your existing codeit.db conversations to your online account. Your local database is not deleted or modified.")
        if st.button("Import local history", use_container_width=True):
            try:
                with st.spinner("Importing local conversations…"):
                    added, skipped = import_local_history(client, user_id)
                st.success(f"Imported {added} conversation(s). Already imported: {skipped}.")
                st.rerun()
            except Exception as exc:
                st.error(f"Import failed: {exc}")

    st.divider()
    st.markdown('<div class="tiny">CLOUD ACCOUNT · LOCAL OLLAMA<br>Conversations sync online. Model inference stays on this PC.</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Main workspace
# -----------------------------------------------------------------------------
left, right = st.columns([4, 1])
with left:
    st.markdown('<div class="eyebrow">YOUR DEVELOPMENT COMMAND CENTER</div>', unsafe_allow_html=True)
with right:
    if ollama_online and selected_model:
        st.markdown('<div style="text-align:right;color:#83e4d5;font-size:.72rem;padding-top:.2rem">● ENGINE READY</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="text-align:right;color:#ffaaaa;font-size:.72rem;padding-top:.2rem">● ENGINE OFFLINE</div>', unsafe_allow_html=True)

if not st.session_state.get("chat_id"):
    st.session_state.chat_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    st.markdown('<div class="hero">Make your next idea<br><span>real with CodeIt.</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="subcopy">A cinematic coding workspace powered by your own Ollama models. Build complete projects, debug code, explore unfamiliar systems, and keep your conversations synced to your account.</div>', unsafe_allow_html=True)
    st.markdown('<div class="section">Choose a launchpad</div>', unsafe_allow_html=True)
    suggestions = [
        ("⌘", "Build a project", "Create a complete app with a clean file structure.", "Help me build a complete software project. Ask only for essential requirements, then provide complete ready-to-use files."),
        ("⌕", "Debug code", "Investigate errors and find reliable fixes.", "Help me debug my project. Ask for the relevant files and complete error output, then diagnose the issue."),
        ("◇", "Design a website", "Create a polished, responsive web experience.", "Help me design and build a cinematic, responsive website with complete files and polished interactions."),
        ("{}", "Understand a codebase", "Explore architecture, files, and dependencies.", "Help me understand my codebase. Explain its file structure, important systems, and how they work together."),
    ]
    cols = st.columns(2, gap="medium")
    for i, (symbol, title, description, prompt_text) in enumerate(suggestions):
        with cols[i % 2]:
            st.markdown(f'<div class="feature"><div class="feature-icon">{symbol}</div><div class="feature-title">{title}</div><div class="feature-desc">{description}</div></div>', unsafe_allow_html=True)
            if st.button("Start building  ↗", key=f"launch-{i}", use_container_width=True):
                st.session_state.pending_prompt = prompt_text
                st.rerun()
else:
    first_user = next((m["content"] for m in st.session_state.messages if m["role"] == "user"), "Conversation")
    st.markdown(f"### {short_title(first_user, 58)}")
    st.caption(f"Synced conversation · {selected_model or 'No model selected'}")
    st.divider()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Tell CodeIt what you want to build…", disabled=not (ollama_online and selected_model))
if "pending_prompt" in st.session_state:
    prompt = st.session_state.pop("pending_prompt")

if prompt:
    if not ollama_online or not selected_model:
        st.error("Start Ollama and select an installed model before sending a message.")
        st.stop()
    if not st.session_state.get("chat_id"):
        try:
            st.session_state.chat_id = cloud_create_chat(client, user_id, short_title(prompt, 100))
        except Exception as exc:
            st.error(f"Could not create cloud conversation: {exc}")
            st.stop()
    chat_id = st.session_state.chat_id
    user_message = {"role": "user", "content": prompt}
    st.session_state.messages.append(user_message)
    try:
        cloud_save_message(client, user_id, chat_id, "user", prompt)
    except Exception as exc:
        st.error(f"Your message could not be synced: {exc}")
        st.stop()
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        try:
            with st.spinner(f"{selected_model} is thinking…"):
                context = [{
                    "role": "system",
                    "content": (
                        "You are CodeIt, a capable programming assistant. Prefer complete, ready-to-use solutions. "
                        "Respect the user's existing project structure, file names, APIs and dependencies. "
                        "State assumptions and never claim you ran code unless you did. Provide exact file paths."
                    ),
                }]
                context.extend(st.session_state.messages[-MAX_HISTORY:])
                answer = ollama_chat(selected_model, context)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            cloud_save_message(client, user_id, chat_id, "assistant", answer)
        except requests.ConnectionError:
            st.error("Cannot connect to Ollama. Make sure the Ollama desktop app is running.")
        except requests.HTTPError as exc:
            st.error(f"Ollama returned an HTTP error: {exc}")
        except requests.Timeout:
            st.error("The model took too long to respond. Try a smaller model or a shorter prompt.")
        except Exception as exc:
            st.error(f"CodeIt encountered an error: {exc}")
