from __future__ import annotations

import json
import os
from datetime import datetime, timezone

STATE = {
    "rag_slow": False,
    "tool_fail": False,
    "cost_spike": False,
}


def enable(name: str) -> None:
    if name not in STATE:
        raise KeyError(f"Unknown incident: {name}")
    STATE[name] = True
    _log_audit("enable", name)



def disable(name: str) -> None:
    if name not in STATE:
        raise KeyError(f"Unknown incident: {name}")
    STATE[name] = False
    _log_audit("disable", name)
    
def _log_audit(action: str, name: str) -> None:
    audit_path = os.getenv("AUDIT_LOG_PATH", "data/audit.jsonl")
    try:
        with open(audit_path, "a", encoding="utf-8") as f:
            log_entry = {
                "ts": datetime.now(timezone.utc).isoformat(),
                "action": action,
                "incident": name
            }
            f.write(json.dumps(log_entry) + "\n")
    except Exception:
        pass



def status() -> dict[str, bool]:
    return dict(STATE)
