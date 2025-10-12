"""data handeling and mathcin gunctions"""

from functools import lru_cache
from typing import List, Dict, Any


@lru_cache(maxsize=1)
def _get_supabase():
    """Create a Supabase client from st.secrets or environment variables."""
    import os
    try:
        import streamlit as st  # optional; available at runtime
        s = getattr(st, "secrets", {})
        url = (s.get("supabase", {}) or {}).get("url") or os.environ.get("SUPABASE_URL")
        key = (s.get("supabase", {}) or {}).get("key") or os.environ.get("SUPABASE_KEY")
    except Exception:
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")

    if not url or not key:
        raise RuntimeError("Supabase credentials missing. Set SUPABASE_URL and SUPABASE_KEY or st.secrets['supabase'].")

    from supabase import create_client
    return create_client(url, key)


def save_user(data: Dict[str, Any], filename: str = "users.csv") -> bool:
    """Insert a user row into Supabase (ignores filename)."""
    sb = _get_supabase()
    payload = {k: str(data.get(k, "")).strip() for k in ["name", "subject", "mode", "time", "contact"]}
    resp = sb.table("users").insert(payload).execute()
    return bool(getattr(resp, "data", None))


def load_users(filename: str = "users.csv") -> List[Dict[str, Any]]:
    """Load all users from Supabase (ignores filename)."""
    sb = _get_supabase()
    resp = sb.table("users").select("*").order("created_at", desc=True).execute()
    return resp.data or []


def find_match(subject: str, mode: str, time: str, name: str, contact: str, filename: str = "users.csv") -> List[Dict[str, Any]]:
    """Find matching users from Supabase (same subject/mode/time, exclude self)."""
    sb = _get_supabase()
    q = (
        sb.table("users")
        .select("*")
        .eq("subject", subject)
        .eq("mode", mode)
        .eq("time", time)
        .neq("name", name)
    )
    if contact:
        q = q.neq("contact", contact)
    resp = q.execute()
    return resp.data or []


def get_user_info(name: str, filename: str = "users.csv") -> List[Dict[str, Any]]:
    """Get user rows by name."""
    sb = _get_supabase()
    resp = sb.table("users").select("*").eq("name", name).execute()
    return resp.data or []


def delete_info_by_index(index: int, filename: str = "users.csv") -> bool:
    """Delete a row by Supabase id (index acts as id)."""
    sb = _get_supabase()
    resp = sb.table("users").delete().eq("id", index).execute()
    return bool(resp.data)


def get_user_info_with_index(name: str, filename: str = "users.csv") -> List[Dict[str, Any]]:
    """Get rows with id for later deletion."""
    sb = _get_supabase()
    resp = sb.table("users").select("id,name,subject,mode,time,contact,created_at").eq("name", name).order("created_at", desc=True).execute()
    return resp.data or []