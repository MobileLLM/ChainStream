"""
Per-user JSONL logs for the web Generator chat (debug / analytics).

Log files live under backend/generator_logs/<YYYY-MM-DD>/<session_id>.jsonl
"""
import json
import os
import uuid
from datetime import datetime, timezone
from threading import Lock
from typing import Optional

_lock = Lock()
# user_uuid (str) -> {"session_id": str, "path": str, "turn": int}
_sessions: dict[str, dict] = {}


def _backend_dir() -> str:
    return os.path.abspath(os.path.dirname(__file__))


def _touch_file(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8"):
        pass


def generator_new_session(user_uuid: str) -> dict:
    """
    Start a new logging session for this user. Creates a new empty .jsonl file.
    """
    uid = str(user_uuid or "anonymous")
    with _lock:
        now = datetime.now(timezone.utc)
        date_str = now.strftime("%Y-%m-%d")
        session_id = f"session_{now.strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:10]}"
        log_dir = os.path.join(_backend_dir(), "generator_logs", date_str)
        os.makedirs(log_dir, exist_ok=True)
        path = os.path.join(log_dir, f"{session_id}.jsonl")
        _touch_file(path)
        _sessions[uid] = {"session_id": session_id, "path": path, "turn": 0}
        return {"session_id": session_id, "log_path": path}


def _ensure_session_locked(user_uuid: str) -> dict:
    uid = str(user_uuid or "anonymous")
    if uid not in _sessions:
        now = datetime.now(timezone.utc)
        date_str = now.strftime("%Y-%m-%d")
        session_id = f"session_{now.strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:10]}"
        log_dir = os.path.join(_backend_dir(), "generator_logs", date_str)
        os.makedirs(log_dir, exist_ok=True)
        path = os.path.join(log_dir, f"{session_id}.jsonl")
        _touch_file(path)
        _sessions[uid] = {"session_id": session_id, "path": path, "turn": 0}
    return _sessions[uid]


def generator_log_turn(user_uuid: str, record: dict) -> None:
    """
    Append one JSON line for a completed generator chat turn.
    """
    uid = str(user_uuid or "anonymous")
    with _lock:
        sess = _ensure_session_locked(uid)
        sess["turn"] += 1
        turn = sess["turn"]
        path = sess["path"]
        session_id = sess["session_id"]

        line = {
            "session_id": session_id,
            "turn": turn,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **record,
        }
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(line, ensure_ascii=False) + "\n")


def generator_current_session_info(user_uuid: str) -> Optional[dict]:
    uid = str(user_uuid or "anonymous")
    with _lock:
        s = _sessions.get(uid)
        if not s:
            return None
        return {"session_id": s["session_id"], "log_path": s["path"], "turn": s["turn"]}
