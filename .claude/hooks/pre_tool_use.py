#!/usr/bin/env python3
"""PreToolUse guard (RULES R3, R4, R10-R13, R15-R17).

Blocks: forbidden shell commands, direct writes to protected learning stores, cross-role data
access, secrets, customer PII outside private folders, and copying company data out of the repo.
Asks a human for: edits to RULES.md / settings / hooks (R14).
Output format per doc:cc-hooks: hookSpecificOutput.permissionDecision = deny | ask, exit 0.
"""
from __future__ import annotations

import fnmatch
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as c  # noqa: E402

# --- R13 / never-events: destructive or outward-facing shell commands ---
FORBIDDEN_CMDS = [
    (r"\brm\s+-[a-zA-Z]*r[a-zA-Z]*f?\s+(/|~|\$HOME|\.|\*)(\s|$)", "recursive delete of root/home/repo"),
    (r"\brm\s+-[a-zA-Z]*r[a-zA-Z]*\s+.*\b(memory|library|tasks|evals|metrics|incidents|\.git)\b", "recursive delete of a learning store"),
    (r"\bgit\s+push\b.*(--force|-f\b|--mirror|--delete)", "force/destructive git push"),
    (r"\bgit\s+reset\s+--hard\b", "git reset --hard discards work"),
    (r"\bgit\s+clean\s+-[a-z]*f", "git clean deletes untracked work"),
    (r"\bgit\s+filter-(branch|repo)\b", "history rewrite"),
    (r"\b(mkfs|dd\s+if=|shutdown|reboot)\b", "system-destructive command"),
    (r":\(\)\s*\{\s*:\|:&\s*\};:", "fork bomb"),
    (r"\bchmod\s+-R\s+777\b", "world-writable permissions"),
]
# --- R16: company data leaving the repo / personal copies ---
EXFIL_CMDS = [
    (r"\b(scp|sftp|ftp|rsync)\b[^|;]*\S+@?\S+:", "copy to a remote host"),
    (r"\bcurl\b[^|;]*(\s-T\s|--upload-file|\s-F\s|--form|--data(-binary|-raw)?\s+@|\s-d\s+@)", "upload with curl"),
    (r"\bwget\b[^|;]*--post-file", "upload with wget"),
    (r"\b(nc|ncat|netcat)\b\s+\S+\s+\d+", "raw network send"),
    (r"\b(gh\s+gist\s+create|transfer\.sh|file\.io|pastebin)", "public paste/share service"),
]
COPY_TOOLS = re.compile(r"\b(cp|mv|tar|zip|7z|rsync|install|ditto)\b")
COMPANY_STORE = re.compile(r"(?:^|[\s'\"=./])(data|memory|tasks|canon|incidents|metrics)(/|\s|$)")
OUTSIDE = re.compile(r"(?:^|\s|=)(/tmp|/mnt|/media|/home|/root|/Users|~|\$HOME)(/|\s|$)")


def copies_out(cmd: str) -> bool:
    """R16: a copy/archive command that touches a company store and an outside destination, in any order."""
    for part in re.split(r"&&|\|\||;|\|", cmd):
        if COPY_TOOLS.search(part) and COMPANY_STORE.search(part) and OUTSIDE.search(part):
            return True
    return False
PROTECTED_WRITE = [  # R3: only scripts (promote/skill_stats/ledger/hooks) write these
    "memory/semantic/**", "memory/INDEX.md", "memory/archive/**", "metrics/ledger.jsonl", "metrics/sessions.jsonl",
    ".claude/skills/*/SKILL.md", ".claude/skills/*/stats.json", ".claude/skills/*/scripts/**",
    "library/MANIFEST.csv", "incidents/INCIDENTS.md", "evals/runs/**", ".claude/state/**",
]
ASK_WRITE = ["RULES.md", ".claude/settings.json", ".claude/hooks/**", "canon/roles/ROLES.json", ".githooks/**"]
PRIVATE_OK = ["data/*/private/**"]

SECRETS = [
    (r"AKIA[0-9A-Z]{16}", "AWS key"), (r"sk-ant-[A-Za-z0-9_-]{20,}", "Anthropic key"),
    (r"sk-[A-Za-z0-9]{32,}", "API secret key"), (r"gh[pousr]_[A-Za-z0-9]{30,}", "GitHub token"),
    (r"xox[abpr]-[A-Za-z0-9-]{10,}", "Slack token"), (r"AIza[0-9A-Za-z_-]{35}", "Google API key"),
    (r"EAA[A-Za-z0-9]{40,}", "Facebook access token"), (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "private key"),
    (r"(?i)\b(password|passwd|secret|api[_-]?key|access[_-]?token)\b\s*[:=]\s*['\"][^'\"\s]{8,}['\"]", "credential assignment"),
]
PII = [
    (r"(?<![\d.])(?:\+?84|0)(?:3|5|7|8|9)\d{8}(?!\d)", "VN phone number"),
    (r"(?<!\d)0\d{11}(?!\d)", "VN citizen ID (CCCD)"),
    (r"\b[A-Za-z0-9._%+-]+@(?!(?:example\.(?:com|vn)|lunobeau\.vn|anthropic\.com|users\.noreply\.github\.com)\b)"
     r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", "personal email address"),
]


def match_any(rel: str, globs: list[str]) -> bool:
    return any(fnmatch.fnmatch(rel, g) for g in globs)


def scan(text: str, patterns) -> str | None:
    for pat, label in patterns:
        if re.search(pat, text or ""):
            return label
    return None


def role_violation(rel: str, role: str | None, write: bool) -> str | None:
    """R17: data/<area>/ is visible only to roles that own it. tasks of another role are off-limits."""
    if not rel:
        return None
    m = re.match(r"data/([^/]+)(?:/|$)", rel)
    cfg = c.roles_config().get("roles", {})
    if m:
        if not role:
            return "session role is not set; data/ is closed until the role is confirmed (tools/set_role.py)"
        areas = cfg.get(role, {}).get("data_areas", [])
        if "*" not in areas and m.group(1) not in areas:
            return f"role '{role}' may not access data/{m.group(1)}/"
        if "/private/" in rel + "/" and not cfg.get(role, {}).get("private", False):
            return f"role '{role}' may not access private customer data"
    t = c.task_of_path(rel)
    if t and (t / "TASK.md").exists() and role and role != "founder":
        owner = c.frontmatter(t / "TASK.md").get("role")
        if owner and owner != role:
            return f"task belongs to role '{owner}'"
    return None


def paths_in_command(cmd: str) -> list[str]:
    return re.findall(r"(?:\./)?((?:data|tasks)/[^\s'\"|;&>)]+)", cmd)


def decide(data: dict) -> tuple[str, str, str | None] | None:
    """Return (decision, reason, incident_kind) or None to stay silent."""
    tool = data.get("tool_name", "")
    ti = data.get("tool_input") or {}
    sid = data.get("session_id")
    cwd = data.get("cwd")
    role = c.session_role(sid)

    if tool == "Bash":
        cmd = ti.get("command", "")
        for pat, why in FORBIDDEN_CMDS:
            if re.search(pat, cmd):
                return "deny", f"Blocked (R13): {why}. Ask the human to run it if it is really needed.", None
        for pat, why in EXFIL_CMDS:
            if re.search(pat, cmd):
                return "deny", f"Blocked (R16): {why}. Company data stays in the repo; the admin has been notified.", "exfiltration"
        if copies_out(cmd):
            return "deny", "Blocked (R16): copying company data outside the repo. The admin has been notified.", "exfiltration"
        s = scan(cmd, SECRETS)
        if s:
            return "deny", f"Blocked (R12): command contains a {s}. Use an environment secret instead.", "secret"
        # Redirections/in-place edits into protected stores bypass Write/Edit; block them too.
        for tgt in re.findall(r"(?:>>?|\btee\s+(?:-a\s+)?|\bsed\s+-i\S*\s+(?:'[^']*'|\"[^\"]*\"|\S+)\s+)\s*([^\s|;&]+)", cmd):
            rel = c.rel_path(tgt, cwd)
            if rel and match_any(rel, PROTECTED_WRITE):
                return "deny", f"Blocked (R3): '{rel}' is written only by repo scripts (tools/promote.py, skill_stats.py, task scripts).", None
            if rel and match_any(rel, ASK_WRITE):
                return "ask", f"Shell edit of '{rel}' changes rules/permissions (R14). Approve only with evidence logged in metrics/IMPROVEMENTS.md.", None
        for p in paths_in_command(cmd):
            v = role_violation(c.rel_path(p, cwd) or p, role, write=False)
            if v:
                return "deny", f"Blocked (R17): {v}.", "role-boundary" if role else None
        return None

    path = ti.get("file_path") or ti.get("notebook_path") or ti.get("path") or ""
    rel = c.rel_path(path, cwd) if path else None
    if tool in ("Grep", "Glob"):
        scope = c.rel_path(path or ".", cwd)
        if scope in (".", "data") and role != "founder":
            return "deny", ("Blocked (R17): a search over the whole repo would read other roles' data/. "
                            "Scope it to a folder, e.g. memory/, canon/, or data/<your-role>/."), None
    if tool in ("Read", "Write", "Edit", "MultiEdit", "NotebookEdit", "Glob", "Grep") and rel:
        v = role_violation(rel, role, write=tool in ("Write", "Edit", "MultiEdit", "NotebookEdit"))
        if v:
            return "deny", f"Blocked (R17): {v}.", "role-boundary" if role else None

    if tool in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
        if path and rel is None and not str(path).startswith(("/tmp/", str(c.ROOT))):
            content = json.dumps(ti)
            if re.search(r"data/|memory/|canon/", content) or scan(content, PII):
                return "deny", "Blocked (R16): writing company data outside the repo.", "exfiltration"
        if rel and match_any(rel, PROTECTED_WRITE):
            return "deny", (f"Blocked (R3): '{rel}' is a protected store. Write a candidate to memory/inbox/ "
                            "or a skill draft to .claude/skill-drafts/, then run the promote script after verification."), None
        content = "\n".join(str(ti.get(k, "")) for k in ("content", "new_string", "new_source"))
        content += "\n".join(str(e.get("new_string", "")) for e in ti.get("edits", []) if isinstance(e, dict))
        s = scan(content, SECRETS)
        if s:
            return "deny", f"Blocked (R12): content contains a {s}. Never store secrets in the repo, logs or memory.", "secret"
        if not (rel and match_any(rel, PRIVATE_OK)):
            p = scan(content, PII)
            if p:
                return "deny", (f"Blocked (R15): content contains a {p}. Customer personal data may live only in "
                                "data/<role>/private/ (gitignored). Use aggregates or a pseudonym like KH-0012."), "pii"
        if rel and match_any(rel, ASK_WRITE):
            return "ask", f"'{rel}' changes rules/permissions (R14). Approve only with an incident or eval result logged in metrics/IMPROVEMENTS.md.", None
    return None


def main() -> int:
    data = c.read_input()
    try:
        res = decide(data)
    except Exception as e:  # fail visible but non-blocking so a hook bug cannot brick the session
        print(f"pre_tool_use hook error: {e}", file=sys.stderr)
        return 1
    if not res:
        return 0
    decision, reason, incident = res
    if incident:
        c.log_incident(incident, f"{data.get('tool_name')}: {reason}", data.get("session_id"),
                       c.session_role(data.get("session_id")))
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": decision,
                                             "permissionDecisionReason": reason}}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
