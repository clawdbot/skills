#!/usr/bin/env python3
"""track17.py

A small, dependency-free CLI for tracking parcels via the 17TRACK Tracking API v2.2.

Designed to be used by Clawdbot as a "skill" helper script.

Key features
- Stores tracked packages in a local SQLite database.
- Registers tracking numbers with 17TRACK.
- Polls current status (sync) and updates local DB.
- Ingests 17TRACK webhook deliveries (from stdin/files/inbox) and updates local DB.
- Includes a tiny webhook HTTP server (stdlib) that can spool payloads into the inbox.

Environment
- TRACK17_TOKEN (required for API calls) : 17TRACK API token (header: 17token)
- TRACK17_WEBHOOK_SECRET (optional)      : webhook signature key (verify SHA256(body + "/" + key))
- TRACK17_DATA_DIR (optional)            : override data directory (db + inbox + cache)
- TRACK17_WORKSPACE_DIR (optional)       : override workspace directory (default data dir becomes <workspace>/packages/track17)
- TRACK17_LANG (optional)                : default translation language, e.g. "en" (default: "en")

Storage
By default, data is stored under:
  <workspace>/packages/track17/

Where <workspace> is auto-detected as the parent directory of the nearest
"skills" directory that contains this skill. For example, if this skill lives at:
  /clawd/skills/track17/
then data is stored at:
  /clawd/packages/track17/

Inside the data dir:
  - track17.sqlite3
  - inbox/ (raw webhook payloads)
  - processed/ (already processed webhook payloads)
  - cache/carriers.json (optional carrier list cache)

Notes
- This script intentionally uses only the Python standard library.
- All timestamps are stored as ISO 8601 strings.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import http.server
import json
import os
import pathlib
import re
import shutil
import sqlite3
import sys
import textwrap
import time
import urllib.error
import urllib.request
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

API_BASE = "https://api.17track.net/track/v2.2"
CARRIERS_URL = "https://res.17track.net/asset/carrier/info/apicarrier.all.json"


def _utc_now_iso() -> str:
    return _dt.datetime.now(tz=_dt.timezone.utc).replace(microsecond=0).isoformat()


def _expand(path: str) -> str:
    return os.path.expandvars(os.path.expanduser(path))


def resolve_workspace_dir() -> pathlib.Path:
    """Best-effort workspace root detection.

    Priority:
      1) TRACK17_WORKSPACE_DIR (explicit override)
      2) CLAWDBOT_WORKSPACE_DIR (if your host environment sets it)
      3) Walk upwards from this script to find a parent directory named "skills".
         The workspace is the parent of that "skills" directory.
      4) Current working directory.
    """

    env_override = os.environ.get("TRACK17_WORKSPACE_DIR") or os.environ.get("CLAWDBOT_WORKSPACE_DIR")
    if env_override:
        return pathlib.Path(_expand(env_override)).resolve()

    # Try to infer from where this skill is installed.
    here = pathlib.Path(__file__).resolve()
    for parent in here.parents:
        if parent.name == "skills":
            # .../<workspace>/skills/track17/...
            return parent.parent.resolve()

    # Fallback: run-local usage.
    return pathlib.Path.cwd().resolve()


def resolve_data_dir() -> pathlib.Path:
    """Resolve where we store the sqlite db + inbox.

    Priority:
      1) TRACK17_DATA_DIR
      2) <workspace>/packages/track17 (workspace auto-detected)
    """

    override = os.environ.get("TRACK17_DATA_DIR")
    if override:
        return pathlib.Path(_expand(override)).resolve()

    return resolve_workspace_dir() / "packages" / "track17"


def paths() -> Dict[str, pathlib.Path]:
    base = resolve_data_dir()
    return {
        "base": base,
        "db": base / "track17.sqlite3",
        "inbox": base / "inbox",
        "processed": base / "processed",
        "cache": base / "cache",
        "carriers": base / "cache" / "carriers.json",
    }


def ensure_dirs() -> Dict[str, pathlib.Path]:
    p = paths()
    p["base"].mkdir(parents=True, exist_ok=True)
    p["inbox"].mkdir(parents=True, exist_ok=True)
    p["processed"].mkdir(parents=True, exist_ok=True)
    p["cache"].mkdir(parents=True, exist_ok=True)
    return p


def connect_db(db_path: pathlib.Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    # Reasonable defaults for a small personal DB.
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = NORMAL;")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS packages (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL,

          label TEXT,

          number TEXT NOT NULL,
          carrier INTEGER NOT NULL DEFAULT 0,
          param TEXT NOT NULL DEFAULT "",
          tag TEXT NOT NULL DEFAULT "",
          lang TEXT NOT NULL DEFAULT "en",

          api_registered INTEGER NOT NULL DEFAULT 0,

          tracking_status TEXT,
          package_status TEXT,

          last_status TEXT,
          last_sub_status TEXT,
          last_event_time_utc TEXT,
          last_event_desc TEXT,
          last_location TEXT,

          last_update_at TEXT,
          last_payload_sha TEXT,

          archived INTEGER NOT NULL DEFAULT 0,

          UNIQUE(number, carrier, param)
        );

        CREATE TABLE IF NOT EXISTS events (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          package_id INTEGER NOT NULL,
          provider_key INTEGER,
          time_utc TEXT,
          time_iso TEXT,
          description TEXT,
          location TEXT,
          stage TEXT,
          sub_status TEXT,
          raw_json TEXT,
          event_hash TEXT NOT NULL,
          created_at TEXT NOT NULL,
          UNIQUE(package_id, event_hash),
          FOREIGN KEY(package_id) REFERENCES packages(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS payloads (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          received_at TEXT NOT NULL,
          source TEXT NOT NULL,
          event_type TEXT,
          number TEXT,
          carrier INTEGER,
          signature TEXT,
          signature_valid INTEGER,
          sha256 TEXT NOT NULL UNIQUE,
          raw_json TEXT NOT NULL
        );
        """
    )
    conn.commit()


class Track17Error(RuntimeError):
    pass


def _http_json_post(url: str, token: str, payload: Optional[Any]) -> Dict[str, Any]:
    """POST JSON to 17TRACK and decode JSON response."""

    data_bytes: Optional[bytes]
    if payload is None:
        data_bytes = None
    else:
        data_bytes = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data_bytes,
        headers={
            "Content-Type": "application/json",
            "17token": token,
            "User-Agent": "track17-skill/1.0 (+https://docs.clawd.bot/tools/skills)",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read()
    except urllib.error.HTTPError as e:
        body = e.read() if hasattr(e, "read") else b""
        raise Track17Error(f"HTTP {e.code} from 17TRACK: {body[:500]!r}") from e
    except urllib.error.URLError as e:
        raise Track17Error(f"Network error talking to 17TRACK: {e}") from e

    try:
        return json.loads(body.decode("utf-8"))
    except Exception as e:
        raise Track17Error(f"Could not parse JSON from 17TRACK: {body[:500]!r}") from e


def _api_token(required: bool = True) -> Optional[str]:
    tok = os.environ.get("TRACK17_TOKEN")
    if required and not tok:
        raise Track17Error(
            "TRACK17_TOKEN is not set. Configure it in clawdbot.json under skills.entries.track17.apiKey "
            "(or export it in your shell)."
        )
    return tok


def api_register(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    token = _api_token(True)
    assert token is not None
    return _http_json_post(f"{API_BASE}/register", token, items)


def api_gettrackinfo(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    token = _api_token(True)
    assert token is not None
    return _http_json_post(f"{API_BASE}/gettrackinfo", token, items)


def api_getquota() -> Dict[str, Any]:
    token = _api_token(True)
    assert token is not None
    # Docs say "no parameter needed"; we send an empty body.
    return _http_json_post(f"{API_BASE}/getquota", token, None)


def api_stoptrack(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    token = _api_token(True)
    assert token is not None
    return _http_json_post(f"{API_BASE}/stoptrack", token, items)


def api_retrack(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    token = _api_token(True)
    assert token is not None
    return _http_json_post(f"{API_BASE}/retrack", token, items)


def api_changeinfo(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    token = _api_token(True)
    assert token is not None
    return _http_json_post(f"{API_BASE}/changeinfo", token, items)


def api_deletetrack(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    token = _api_token(True)
    assert token is not None
    return _http_json_post(f"{API_BASE}/deletetrack", token, items)


def _normalise_number(n: str) -> str:
    return re.sub(r"\s+", "", n.strip())


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compute_webhook_signature(raw_body: bytes, secret: str) -> str:
    """17TRACK webhook signature: SHA256( body + "/" + key )."""

    blob = raw_body.decode("utf-8") + "/" + secret
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def guess_signature_header(headers: Dict[str, str]) -> Optional[Tuple[str, str]]:
    """Try common header names for 17TRACK webhook signatures.

    The 17TRACK docs say the signature is sent in a request header, but they don't
    consistently name it in all snippets. We accept a few variants.
    """

    candidates = [
        "signature",
        "Signature",
        "SIGNATURE",
        "sign",
        "Sign",
        "x-signature",
        "X-Signature",
        "x-17track-signature",
        "X-17Track-Signature",
    ]
    for key in candidates:
        if key in headers and headers[key]:
            return key, headers[key]

    # Some servers normalise to Title-Case. Do a case-insensitive scan.
    lower = {k.lower(): (k, v) for k, v in headers.items()}
    for key in ["signature", "sign", "x-signature", "x-17track-signature"]:
        if key in lower and lower[key][1]:
            return lower[key][0], lower[key][1]

    return None


def upsert_package(
    conn: sqlite3.Connection,
    *,
    number: str,
    carrier: int,
    param: str,
    label: Optional[str] = None,
    tag: Optional[str] = None,
    lang: Optional[str] = None,
    api_registered: Optional[bool] = None,
) -> sqlite3.Row:
    now = _utc_now_iso()
    number_n = _normalise_number(number)
    param_n = param or ""
    carrier_n = int(carrier or 0)

    existing = conn.execute(
        "SELECT * FROM packages WHERE number = ? AND carrier = ? AND param = ?",
        (number_n, carrier_n, param_n),
    ).fetchone()

    if existing:
        fields: List[str] = []
        values: List[Any] = []
        if label is not None:
            fields.append("label = ?")
            values.append(label)
        if tag is not None:
            fields.append("tag = ?")
            values.append(tag)
        if lang is not None:
            fields.append("lang = ?")
            values.append(lang)
        if api_registered is not None:
            fields.append("api_registered = ?")
            values.append(1 if api_registered else 0)

        fields.append("updated_at = ?")
        values.append(now)

        if fields:
            values.extend([number_n, carrier_n, param_n])
            conn.execute(
                f"UPDATE packages SET {', '.join(fields)} WHERE number = ? AND carrier = ? AND param = ?",
                tuple(values),
            )
            conn.commit()

        return conn.execute(
            "SELECT * FROM packages WHERE id = ?",
            (existing["id"],),
        ).fetchone()

    conn.execute(
        """
        INSERT INTO packages (
          created_at, updated_at,
          label, number, carrier, param, tag, lang,
          api_registered
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            now,
            now,
            label,
            number_n,
            carrier_n,
            param_n,
            tag or "",
            lang or (os.environ.get("TRACK17_LANG") or "en"),
            1 if api_registered else 0,
        ),
    )
    conn.commit()
    return conn.execute(
        "SELECT * FROM packages WHERE number = ? AND carrier = ? AND param = ?",
        (number_n, carrier_n, param_n),
    ).fetchone()


def find_package(conn: sqlite3.Connection, key: str) -> Optional[sqlite3.Row]:
    """Find a package by id or tracking number."""

    k = key.strip()
    if k.isdigit():
        row = conn.execute("SELECT * FROM packages WHERE id = ?", (int(k),)).fetchone()
        if row:
            return row

    # try number exact (normalised)
    n = _normalise_number(k)
    row = conn.execute(
        "SELECT * FROM packages WHERE number = ? ORDER BY id DESC LIMIT 1",
        (n,),
    ).fetchone()
    return row


def list_packages(conn: sqlite3.Connection, include_archived: bool = False) -> List[sqlite3.Row]:
    if include_archived:
        q = "SELECT * FROM packages ORDER BY archived ASC, updated_at DESC"
        return list(conn.execute(q).fetchall())
    q = "SELECT * FROM packages WHERE archived = 0 ORDER BY updated_at DESC"
    return list(conn.execute(q).fetchall())


def _safe_get(d: Any, path: Sequence[Any], default: Any = None) -> Any:
    cur = d
    for p in path:
        try:
            if isinstance(cur, dict):
                cur = cur[p]
            elif isinstance(cur, list) and isinstance(p, int):
                cur = cur[p]
            else:
                return default
        except Exception:
            return default
    return cur


def extract_latest_fields(track_info: Dict[str, Any]) -> Dict[str, Optional[str]]:
    latest_status = _safe_get(track_info, ["latest_status"], {}) or {}
    latest_event = _safe_get(track_info, ["latest_event"], {}) or {}

    status = latest_status.get("status")
    sub_status = latest_status.get("sub_status")

    evt_time = latest_event.get("time_utc") or latest_event.get("time_iso")
    evt_desc = latest_event.get("description_translation") or latest_event.get("description")
    if isinstance(evt_desc, dict):
        evt_desc = evt_desc.get("description") or evt_desc.get("translated")

    evt_loc = latest_event.get("location")
    if isinstance(evt_loc, dict):
        # best-effort
        evt_loc = evt_loc.get("address") or evt_loc.get("city") or evt_loc.get("country")

    return {
        "last_status": str(status) if status is not None else None,
        "last_sub_status": str(sub_status) if sub_status is not None else None,
        "last_event_time_utc": str(evt_time) if evt_time is not None else None,
        "last_event_desc": str(evt_desc) if evt_desc is not None else None,
        "last_location": str(evt_loc) if evt_loc is not None else None,
    }


def iter_events(track_info: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    providers = _safe_get(track_info, ["tracking", "providers"], [])
    if not isinstance(providers, list):
        return []

    for p in providers:
        if not isinstance(p, dict):
            continue
        provider_key = p.get("key")
        events = p.get("events") or []
        if not isinstance(events, list):
            continue
        for e in events:
            if not isinstance(e, dict):
                continue
            out = dict(e)
            out["_provider_key"] = provider_key
            yield out


def event_hash(event: Dict[str, Any]) -> str:
    provider_key = str(event.get("_provider_key") or "")
    time_utc = str(event.get("time_utc") or event.get("time_iso") or "")
    desc = event.get("description_translation")
    if isinstance(desc, dict):
        desc = desc.get("description")
    if desc is None:
        desc = event.get("description")
    desc_s = str(desc or "")
    loc = event.get("location")
    if isinstance(loc, dict):
        loc = loc.get("address") or loc.get("city") or loc.get("country")
    loc_s = str(loc or "")

    raw = "|".join([provider_key, time_utc, desc_s, loc_s])
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()


def store_payload(
    conn: sqlite3.Connection,
    *,
    raw_body: bytes,
    source: str,
    event_type: Optional[str],
    number: Optional[str],
    carrier: Optional[int],
    signature: Optional[str],
    signature_valid: Optional[bool],
) -> str:
    sha = _sha256_hex(raw_body)

    try:
        conn.execute(
            """
            INSERT INTO payloads (received_at, source, event_type, number, carrier, signature, signature_valid, sha256, raw_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                _utc_now_iso(),
                source,
                event_type,
                number,
                carrier,
                signature,
                1 if signature_valid else (0 if signature_valid is not None else None),
                sha,
                raw_body.decode("utf-8", errors="replace"),
            ),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        # Duplicate payload (same SHA256). Ignore.
        pass

    return sha


def apply_update_from_trackinfo(
    conn: sqlite3.Connection,
    *,
    package_row: sqlite3.Row,
    response_item: Dict[str, Any],
    raw_payload_sha: Optional[str],
    source: str,
) -> Tuple[bool, str]:
    """Apply a gettrackinfo item or webhook payload to local DB.

    Returns: (changed, summary)
    """

    pkg_id = int(package_row["id"])

    tracking_status = response_item.get("tracking_status")
    package_status = response_item.get("package_status")

    track_info = response_item.get("track_info")
    if not isinstance(track_info, dict):
        track_info = {}

    latest = extract_latest_fields(track_info)

    # Determine if this update is new
    prev = conn.execute("SELECT * FROM packages WHERE id = ?", (pkg_id,)).fetchone()
    prev_sha = prev["last_payload_sha"] if prev else None

    changed = False
    if raw_payload_sha and raw_payload_sha != prev_sha:
        changed = True

    # Also consider event change if payload_sha is missing
    if not raw_payload_sha:
        for k in ["last_event_time_utc", "last_event_desc", "last_status", "last_sub_status"]:
            if prev and latest.get(k) and latest.get(k) != prev.get(k):
                changed = True
                break

    now = _utc_now_iso()

    conn.execute(
        """
        UPDATE packages
        SET updated_at = ?,
            tracking_status = ?,
            package_status = ?,
            last_status = ?,
            last_sub_status = ?,
            last_event_time_utc = ?,
            last_event_desc = ?,
            last_location = ?,
            last_update_at = ?,
            last_payload_sha = ?
        WHERE id = ?
        """,
        (
            now,
            str(tracking_status) if tracking_status is not None else prev["tracking_status"],
            str(package_status) if package_status is not None else prev["package_status"],
            latest.get("last_status") or prev["last_status"],
            latest.get("last_sub_status") or prev["last_sub_status"],
            latest.get("last_event_time_utc") or prev["last_event_time_utc"],
            latest.get("last_event_desc") or prev["last_event_desc"],
            latest.get("last_location") or prev["last_location"],
            now,
            raw_payload_sha or prev_sha,
            pkg_id,
        ),
    )

    # Store events (best-effort)
    inserted_events = 0
    for e in iter_events(track_info):
        eh = event_hash(e)
        try:
            conn.execute(
                """
                INSERT INTO events (
                  package_id, provider_key, time_utc, time_iso, description, location,
                  stage, sub_status, raw_json, event_hash, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    pkg_id,
                    e.get("_provider_key"),
                    e.get("time_utc"),
                    e.get("time_iso"),
                    (e.get("description_translation", {}) or {}).get("description")
                    if isinstance(e.get("description_translation"), dict)
                    else e.get("description_translation")
                    or e.get("description"),
                    json.dumps(e.get("location"), ensure_ascii=False) if isinstance(e.get("location"), dict) else e.get("location"),
                    e.get("stage"),
                    e.get("sub_status"),
                    json.dumps(e, ensure_ascii=False),
                    eh,
                    now,
                ),
            )
            inserted_events += 1
        except sqlite3.IntegrityError:
            pass

    conn.commit()

    # Summary
    label = package_row["label"] or package_row["number"]
    status = latest.get("last_status") or package_status or tracking_status or "unknown"
    event_desc = latest.get("last_event_desc")
    event_time = latest.get("last_event_time_utc")

    bits = [f"{label}: {status}"]
    if event_time:
        bits.append(f"@ {event_time}")
    if event_desc:
        bits.append(f"- {event_desc}")

    summary = " ".join(bits)

    if inserted_events and changed:
        summary += f" (+{inserted_events} events)"

    if source == "webhook":
        summary = "[webhook] " + summary

    return changed, summary


def _parse_gettrackinfo_response_items(resp: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    code = resp.get("code")
    if code not in (0, "0"):
        raise Track17Error(f"17TRACK API error code: {code} ({resp})")

    data = resp.get("data") or {}
    accepted = data.get("accepted") or []
    rejected = data.get("rejected") or []
    if not isinstance(accepted, list):
        accepted = []
    if not isinstance(rejected, list):
        rejected = []
    return accepted, rejected


def cmd_init(args: argparse.Namespace) -> int:
    p = ensure_dirs()
    conn = connect_db(p["db"])
    init_db(conn)
    print("Initialised track17 storage:")
    print(f"  data_dir: {p['base']}")
    print(f"  db:       {p['db']}")
    print(f"  inbox:    {p['inbox']}")
    print(f"  cache:    {p['cache']}")
    return 0


def cmd_add(args: argparse.Namespace) -> int:
    p = ensure_dirs()
    conn = connect_db(p["db"])
    init_db(conn)

    number = _normalise_number(args.number)
    carrier = int(args.carrier or 0)
    param = args.param or ""
    label = args.label
    tag = args.tag or (label[:32] if label else "")
    lang = args.lang or (os.environ.get("TRACK17_LANG") or "en")

    row = upsert_package(
        conn,
        number=number,
        carrier=carrier,
        param=param,
        label=label,
        tag=tag,
        lang=lang,
        api_registered=False,
    )

    # Register with API
    payload_item: Dict[str, Any] = {"number": number}
    if carrier:
        payload_item["carrier"] = carrier
    if tag:
        payload_item["tag"] = tag
    if param:
        payload_item["param"] = param
    if lang:
        payload_item["lang"] = lang

    resp = api_register([payload_item])
    accepted, rejected = _parse_gettrackinfo_response_items(resp)

    if rejected:
        err = rejected[0].get("error") or {}
        code = err.get("code")
        msg = err.get("message")
        raise Track17Error(f"Register failed for {number}: {code} {msg}")

    # Update carrier from accepted response (17TRACK may correct it)
    acc0 = accepted[0]
    new_carrier = int(acc0.get("carrier") or carrier or 0)

    # If we registered with carrier=0, we need to move the row to the real carrier.
    if int(row["carrier"]) != new_carrier:
        # Merge strategy:
        # - If a row already exists for (number,new_carrier,param), keep it and archive/remove the old.
        existing = conn.execute(
            "SELECT * FROM packages WHERE number=? AND carrier=? AND param=?",
            (number, new_carrier, param),
        ).fetchone()
        if existing:
            # Prefer the existing, but update its label/tag/lang if missing.
            upsert_package(
                conn,
                number=number,
                carrier=new_carrier,
                param=param,
                label=label or existing["label"],
                tag=tag or existing["tag"],
                lang=lang or existing["lang"],
                api_registered=True,
            )
            # Archive the old (carrier=0) row.
            conn.execute("UPDATE packages SET archived=1, updated_at=? WHERE id=?", (_utc_now_iso(), row["id"]))
            conn.commit()
            row = existing
        else:
            conn.execute(
                "UPDATE packages SET carrier=?, api_registered=1, updated_at=? WHERE id=?",
                (new_carrier, _utc_now_iso(), row["id"]),
            )
            conn.commit()

    else:
        conn.execute(
            "UPDATE packages SET api_registered=1, updated_at=? WHERE id=?",
            (_utc_now_iso(), row["id"]),
        )
        conn.commit()

    print(f"Added package #{row['id']}:")
    print(f"  label:   {label or ''}")
    print(f"  number:  {number}")
    print(f"  carrier: {new_carrier}")
    if param:
        print(f"  param:   {param}")
    if tag:
        print(f"  tag:     {tag}")
    print("Registered with 17TRACK.")

    # Optionally fetch immediate status
    if args.status:
        return cmd_status(argparse.Namespace(key=str(row["id"]), refresh=True, events=10, json=False))

    return 0


def _fmt_row_short(r: sqlite3.Row) -> str:
    label = r["label"] or ""
    num = r["number"]
    car = r["carrier"]
    status = r["last_status"] or r["package_status"] or r["tracking_status"] or ""
    evt_time = r["last_event_time_utc"] or ""
    evt_desc = r["last_event_desc"] or ""

    left = f"#{r['id']:<3}"
    lab = (label[:24] + "…") if len(label) > 25 else label
    return f"{left} {lab:<26} {num:<18} c={car:<5} {status:<12} {evt_time:<20} {evt_desc[:60]}"


def cmd_list(args: argparse.Namespace) -> int:
    p = ensure_dirs()
    conn = connect_db(p["db"])
    init_db(conn)

    rows = list_packages(conn, include_archived=args.all)
    if not rows:
        print("No packages tracked yet. Use: track17 add <number> --label ...")
        return 0

    print("Tracked packages:")
    print("#    Label                      Number             Carrier Status       Last event time       Last event")
    print("-" * 110)
    for r in rows:
        if not args.all and r["archived"]:
            continue
        print(_fmt_row_short(r))
    return 0


def _build_trackinfo_items(rows: List[sqlite3.Row]) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for r in rows:
        num = r["number"]
        carrier = int(r["carrier"] or 0)
        param = r["param"] or ""
        lang = r["lang"] or (os.environ.get("TRACK17_LANG") or "en")

        it: Dict[str, Any] = {"number": num}
        if carrier:
            it["carrier"] = carrier
        if param:
            it["param"] = param
        if lang:
            it["lang"] = lang
        items.append(it)
    return items


def cmd_sync(args: argparse.Namespace) -> int:
    p = ensure_dirs()
    conn = connect_db(p["db"])
    init_db(conn)

    rows = list_packages(conn, include_archived=False)
    if args.active_only:
        rows = [r for r in rows if (r["tracking_status"] or "").lower() != "stopped"]

    if not rows:
        print("No packages to sync.")
        return 0

    items = _build_trackinfo_items(rows)

    # API supports max 40 items per call.
    CHUNK = 40
    changed_summaries: List[str] = []
    rejected_total: List[Dict[str, Any]] = []

    for i in range(0, len(items), CHUNK):
        batch = items[i : i + CHUNK]
        resp = api_gettrackinfo(batch)
        accepted, rejected = _parse_gettrackinfo_response_items(resp)
        rejected_total.extend(rejected)

        # Apply accepted items
        for acc in accepted:
            num = _normalise_number(str(acc.get("number") or ""))
            car = int(acc.get("carrier") or 0)

            # Find matching package row; if multiple, pick the newest.
            pkg = conn.execute(
                "SELECT * FROM packages WHERE number=? AND carrier=? ORDER BY id DESC LIMIT 1",
                (num, car),
            ).fetchone()
            if not pkg:
                # Unknown locally; create minimal row (use tag if present).
                pkg = upsert_package(
                    conn,
                    number=num,
                    carrier=car,
                    param=str(acc.get("param") or ""),
                    label=None,
                    tag=str(acc.get("tag") or ""),
                    lang=str(acc.get("lang") or "en"),
                    api_registered=True,
                )

            raw_payload_sha = None
            try:
                raw_payload_sha = hashlib.sha256(json.dumps(acc, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
            except Exception:
                pass

            changed, summary = apply_update_from_trackinfo(
                conn,
                package_row=pkg,
                response_item=acc,
                raw_payload_sha=raw_payload_sha,
                source="poll",
            )
            if changed:
                changed_summaries.append(summary)

    # Output
    if rejected_total:
        print(f"Some items were rejected by 17TRACK ({len(rejected_total)}):")
        for r in rejected_total[:10]:
            num = r.get("number")
            err = r.get("error") or {}
            print(f"  - {num}: {err.get('code')} {err.get('message')}")
        if len(rejected_total) > 10:
            print(f"  ... ({len(rejected_total) - 10} more)")

    if not changed_summaries:
        print(f"Sync complete. No changes ({len(rows)} packages checked).")
        return 0

    print(f"Sync complete. {len(changed_summaries)} package(s) updated:")
    for s in changed_summaries:
        print(f"- {s}")

    return 0


def cmd_status(args: argparse.Namespace) -> int:
    p = ensure_dirs()
    conn = connect_db(p["db"])
    init_db(conn)

    pkg = find_package(conn, args.key)
    if not pkg:
        print(f"Package not found: {args.key}")
        return 2

    # Optionally refresh from API.
    if args.refresh:
        items = _build_trackinfo_items([pkg])
        resp = api_gettrackinfo(items)
        accepted, rejected = _parse_gettrackinfo_response_items(resp)
        if rejected:
            err = rejected[0].get("error") or {}
            raise Track17Error(f"Refresh failed: {err.get('code')} {err.get('message')}")
        if accepted:
            acc = accepted[0]
            raw_payload_sha = hashlib.sha256(json.dumps(acc, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
            _, _ = apply_update_from_trackinfo(conn, package_row=pkg, response_item=acc, raw_payload_sha=raw_payload_sha, source="poll")
            pkg = find_package(conn, str(pkg["id"])) or pkg

    if args.json:
        # Include recent events.
        ev = conn.execute(
            "SELECT * FROM events WHERE package_id=? ORDER BY time_utc DESC, id DESC LIMIT ?",
            (pkg["id"], args.events),
        ).fetchall()
        out = {k: pkg[k] for k in pkg.keys()}
        out["events"] = [dict(r) for r in ev]
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 0

    print(f"Package #{pkg['id']}")
    if pkg["label"]:
        print(f"Label: {pkg['label']}")
    print(f"Number:  {pkg['number']}")
    print(f"Carrier:  {pkg['carrier']}")
    if pkg["param"]:
        print(f"Param:   {pkg['param']}")
    if pkg["tag"]:
        print(f"Tag:     {pkg['tag']}")
    print(f"Tracking status: {pkg['tracking_status']}")
    print(f"Package status:  {pkg['package_status']}")
    print(f"Latest status:   {pkg['last_status']} (sub: {pkg['last_sub_status']})")
    print(f"Latest event:    {pkg['last_event_time_utc']} - {pkg['last_event_desc']}")
    if pkg["last_location"]:
        print(f"Location:        {pkg['last_location']}")
    print(f"Last updated:    {pkg['last_update_at']}")

    ev = conn.execute(
        "SELECT * FROM events WHERE package_id=? ORDER BY time_utc DESC, id DESC LIMIT ?",
        (pkg["id"], args.events),
    ).fetchall()
    if ev:
        print("")
        print(f"Recent events (max {args.events}):")
        for r in ev:
            t = r["time_utc"] or r["time_iso"] or ""
            d = r["description"] or ""
            loc = r["location"] or ""
            if isinstance(loc, str) and loc.startswith("{"):
                # stored json string for dict location
                try:
                    loc_obj = json.loads(loc)
                    loc = loc_obj.get("address") or loc_obj.get("city") or loc_obj.get("country") or ""
                except Exception:
                    pass
            print(f"- {t} {d} {('(' + loc + ')') if loc else ''}")

    return 0


def cmd_stop(args: argparse.Namespace) -> int:
    p = ensure_dirs()
    conn = connect_db(p["db"])
    init_db(conn)

    pkg = find_package(conn, args.key)
    if not pkg:
        print(f"Package not found: {args.key}")
        return 2

    num = pkg["number"]
    car = int(pkg["carrier"] or 0)

    payload = [{"number": num}]
    if car:
        payload[0]["carrier"] = car

    resp = api_stoptrack(payload)
    accepted, rejected = _parse_gettrackinfo_response_items(resp)
    if rejected:
        err = rejected[0].get("error") or {}
        raise Track17Error(f"Stop failed: {err.get('code')} {err.get('message')}")

    conn.execute(
        "UPDATE packages SET tracking_status='Stopped', updated_at=? WHERE id=?",
        (_utc_now_iso(), pkg["id"]),
    )
    conn.commit()

    print(f"Stopped tracking for #{pkg['id']} ({num}, carrier {car}).")
    return 0


def cmd_retrack(args: argparse.Namespace) -> int:
    p = ensure_dirs()
    conn = connect_db(p["db"])
    init_db(conn)

    pkg = find_package(conn, args.key)
    if not pkg:
        print(f"Package not found: {args.key}")
        return 2

    num = pkg["number"]
    car = int(pkg["carrier"] or 0)

    payload = [{"number": num}]
    if car:
        payload[0]["carrier"] = car

    resp = api_retrack(payload)
    accepted, rejected = _parse_gettrackinfo_response_items(resp)
    if rejected:
        err = rejected[0].get("error") or {}
        raise Track17Error(f"Retrack failed: {err.get('code')} {err.get('message')}")

    conn.execute(
        "UPDATE packages SET tracking_status='Tracking', updated_at=? WHERE id=?",
        (_utc_now_iso(), pkg["id"]),
    )
    conn.commit()

    print(f"Restarted tracking for #{pkg['id']} ({num}, carrier {car}).")
    return 0


def cmd_remove(args: argparse.Namespace) -> int:
    p = ensure_dirs()
    conn = connect_db(p["db"])
    init_db(conn)

    pkg = find_package(conn, args.key)
    if not pkg:
        print(f"Package not found: {args.key}")
        return 2

    if args.delete_remote:
        payload = [{"number": pkg["number"]}]
        car = int(pkg["carrier"] or 0)
        if car:
            payload[0]["carrier"] = car
        resp = api_deletetrack(payload)
        accepted, rejected = _parse_gettrackinfo_response_items(resp)
        if rejected:
            err = rejected[0].get("error") or {}
            raise Track17Error(f"Remote delete failed: {err.get('code')} {err.get('message')}")

    conn.execute("DELETE FROM packages WHERE id=?", (pkg["id"],))
    conn.commit()
    print(f"Removed package #{pkg['id']} from local DB.")
    return 0


def cmd_quota(args: argparse.Namespace) -> int:
    _ = ensure_dirs()
    resp = api_getquota()
    code = resp.get("code")
    if code not in (0, "0"):
        raise Track17Error(f"17TRACK API error code: {code} ({resp})")
    data = resp.get("data") or {}
    print(json.dumps(data, indent=2, ensure_ascii=False))
    return 0


def cmd_carriers_update(args: argparse.Namespace) -> int:
    p = ensure_dirs()
    dest = p["carriers"]

    try:
        with urllib.request.urlopen(CARRIERS_URL, timeout=30) as resp:
            body = resp.read()
    except Exception as e:
        raise Track17Error(f"Failed to download carrier list: {e}") from e

    dest.write_bytes(body)
    print(f"Saved carrier list to {dest}")
    return 0


def cmd_carriers_search(args: argparse.Namespace) -> int:
    p = ensure_dirs()
    src = p["carriers"]
    if not src.exists():
        print("Carrier cache not found. Run: track17 carriers-update")
        return 2

    data = json.loads(src.read_text("utf-8"))
    q = args.query.lower().strip()

    # The carrier JSON schema is not documented in detail here; we do a best-effort search.
    matches: List[Tuple[str, Any]] = []
    if isinstance(data, list):
        for item in data:
            if not isinstance(item, dict):
                continue
            name = str(item.get("name") or item.get("en") or item.get("cn") or "")
            code = item.get("key") or item.get("code") or item.get("id")
            hay = f"{name} {code}".lower()
            if q in hay:
                matches.append((name, code))
    elif isinstance(data, dict):
        # sometimes top-level has "data".
        arr = data.get("data") if isinstance(data.get("data"), list) else None
        if arr:
            for item in arr:
                if not isinstance(item, dict):
                    continue
                name = str(item.get("name") or item.get("en") or item.get("cn") or "")
                code = item.get("key") or item.get("code") or item.get("id")
                hay = f"{name} {code}".lower()
                if q in hay:
                    matches.append((name, code))

    if not matches:
        print("No carrier matches.")
        return 0

    print(f"Found {len(matches)} carrier(s):")
    for name, code in matches[:50]:
        print(f"- {code}: {name}")
    if len(matches) > 50:
        print(f"... ({len(matches) - 50} more)")
    return 0


def parse_webhook_payload(raw_body: bytes) -> Dict[str, Any]:
    try:
        return json.loads(raw_body.decode("utf-8"))
    except Exception as e:
        raise Track17Error(f"Invalid JSON payload: {e}") from e


def ingest_payload(
    conn: sqlite3.Connection,
    *,
    raw_body: bytes,
    headers: Optional[Dict[str, str]] = None,
    source: str,
    secret: Optional[str],
) -> Tuple[bool, str]:
    """Ingest a webhook (or webhook-like) payload."""

    headers = headers or {}

    sig_pair = guess_signature_header(headers)
    sig_header_name = sig_pair[0] if sig_pair else None
    sig_value = sig_pair[1] if sig_pair else None

    sig_valid: Optional[bool] = None
    if secret and sig_value:
        expected = compute_webhook_signature(raw_body, secret)
        sig_valid = expected.lower() == sig_value.lower()

    payload_sha = store_payload(
        conn,
        raw_body=raw_body,
        source=source,
        event_type=None,
        number=None,
        carrier=None,
        signature=sig_value,
        signature_valid=sig_valid,
    )

    payload = parse_webhook_payload(raw_body)

    # 17TRACK webhook structure: { event: "TRACKING_UPDATED", data: {...} }
    event_type = payload.get("event")
    data = payload.get("data")

    # Update payload record with extracted basics (best-effort)
    number = None
    carrier = None
    if isinstance(data, dict):
        number = data.get("number")
        carrier = data.get("carrier")

    conn.execute(
        "UPDATE payloads SET event_type=?, number=?, carrier=? WHERE sha256=?",
        (event_type, number, carrier, payload_sha),
    )
    conn.commit()

    if not isinstance(data, dict):
        return False, f"Stored payload {payload_sha} (no data object)"

    number_s = _normalise_number(str(data.get("number") or ""))
    carrier_i = int(data.get("carrier") or 0)
    tag = str(data.get("tag") or "")
    param = str(data.get("param") or "")

    # Ensure package exists
    pkg = conn.execute(
        "SELECT * FROM packages WHERE number=? AND carrier=? AND param=? ORDER BY id DESC LIMIT 1",
        (number_s, carrier_i, param),
    ).fetchone()

    if not pkg:
        pkg = upsert_package(
            conn,
            number=number_s,
            carrier=carrier_i,
            param=param,
            label=None,
            tag=tag,
            lang=os.environ.get("TRACK17_LANG") or "en",
            api_registered=True,
        )

    # Use the data object as the response item; it includes track_info.
    changed, summary = apply_update_from_trackinfo(
        conn,
        package_row=pkg,
        response_item=data,
        raw_payload_sha=payload_sha,
        source=source,
    )

    if secret and sig_value:
        validity = "valid" if sig_valid else "INVALID"
        summary = f"[{validity} signature via {sig_header_name}] " + summary
    elif secret and not sig_value:
        summary = "[no signature header] " + summary

    return changed, summary


def cmd_ingest_webhook(args: argparse.Namespace) -> int:
    p = ensure_dirs()
    conn = connect_db(p["db"])
    init_db(conn)

    raw_body: bytes
    if args.file:
        raw_body = pathlib.Path(args.file).read_bytes()
    else:
        raw_body = sys.stdin.buffer.read()

    secret = args.secret or os.environ.get("TRACK17_WEBHOOK_SECRET")

    changed, summary = ingest_payload(conn, raw_body=raw_body, headers={}, source="webhook", secret=secret)

    print(summary)
    return 0


def cmd_process_inbox(args: argparse.Namespace) -> int:
    p = ensure_dirs()
    conn = connect_db(p["db"])
    init_db(conn)

    secret = args.secret or os.environ.get("TRACK17_WEBHOOK_SECRET")

    inbox = p["inbox"]
    files = sorted([f for f in inbox.glob("*.json") if f.is_file()])
    if not files:
        print("Inbox is empty.")
        return 0

    changed_count = 0
    summaries: List[str] = []

    for f in files:
        raw = f.read_bytes()
        # We store headers separately in a sidecar .headers.json (optional)
        headers: Dict[str, str] = {}
        sidecar = f.with_suffix(".headers.json")
        if sidecar.exists():
            try:
                headers = json.loads(sidecar.read_text("utf-8"))
            except Exception:
                headers = {}

        try:
            changed, summary = ingest_payload(conn, raw_body=raw, headers=headers, source="webhook", secret=secret)
            if changed:
                changed_count += 1
                summaries.append(summary)

            # Move processed files
            dest = p["processed"] / f.name
            f.rename(dest)
            if sidecar.exists():
                sidecar.rename(p["processed"] / sidecar.name)
        except Exception as e:
            print(f"Failed to process {f.name}: {e}")

    print(f"Processed {len(files)} inbox payload(s). Updated {changed_count} package(s).")
    for s in summaries[:20]:
        print(f"- {s}")
    if len(summaries) > 20:
        print(f"... ({len(summaries) - 20} more)")

    return 0


class _WebhookHandler(http.server.BaseHTTPRequestHandler):
    server_version = "track17-webhook/1.0"

    def do_POST(self) -> None:  # noqa: N802
        server: "WebhookServer" = self.server  # type: ignore[assignment]

        try:
            length = int(self.headers.get("Content-Length") or "0")
        except ValueError:
            length = 0

        raw_body = self.rfile.read(length) if length > 0 else self.rfile.read()

        # Basic response first to keep provider happy.
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b"{\"ok\":true}\n")

        # Then spool payload to disk.
        server.spool(raw_body, dict(self.headers))

    def log_message(self, fmt: str, *args: Any) -> None:
        # Quiet by default; use --verbose to see logs.
        server: "WebhookServer" = self.server  # type: ignore[assignment]
        if getattr(server, "verbose", False):
            super().log_message(fmt, *args)


class WebhookServer(http.server.ThreadingHTTPServer):
    def __init__(
        self,
        server_address: Tuple[str, int],
        RequestHandlerClass: type[_WebhookHandler],
        *,
        inbox_dir: pathlib.Path,
        verbose: bool = False,
        max_files: int = 5000,
    ):
        super().__init__(server_address, RequestHandlerClass)
        self.inbox_dir = inbox_dir
        self.verbose = verbose
        self.max_files = max_files

    def spool(self, raw_body: bytes, headers: Dict[str, str]) -> None:
        ts = _dt.datetime.now(tz=_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        sha = _sha256_hex(raw_body)[:16]
        fname = f"{ts}_{sha}.json"
        fpath = self.inbox_dir / fname

        # Don't overwrite existing.
        if fpath.exists():
            return

        # Very small backpressure: if inbox is huge, drop oldest processed files.
        try:
            existing = sorted(self.inbox_dir.glob("*.json"))
            if len(existing) >= self.max_files:
                for old in existing[: max(0, len(existing) - self.max_files + 1)]:
                    try:
                        old.unlink()
                        side = old.with_suffix(".headers.json")
                        if side.exists():
                            side.unlink()
                    except Exception:
                        pass
        except Exception:
            pass

        fpath.write_bytes(raw_body)
        (self.inbox_dir / f"{fpath.stem}.headers.json").write_text(json.dumps(headers), "utf-8")

        if self.verbose:
            print(f"Spooled webhook payload to {fpath}")


def cmd_webhook_server(args: argparse.Namespace) -> int:
    p = ensure_dirs()

    bind = args.bind
    port = int(args.port)

    httpd = WebhookServer((bind, port), _WebhookHandler, inbox_dir=p["inbox"], verbose=args.verbose)

    print(f"Webhook server listening on http://{bind}:{port}/")
    print(f"Spooling JSON payloads into: {p['inbox']}")
    print("Press Ctrl+C to stop.")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()

    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="track17",
        description="Track parcels via 17TRACK (local SQLite DB + polling + webhook ingestion).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """
            Examples:
              track17 init
              track17 add RR123456789CN --label "New headphones"
              track17 list
              track17 sync
              track17 status 1 --refresh
              track17 webhook-server --bind 127.0.0.1 --port 8789
            """
        ),
    )

    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init", help="Initialise DB and data directories")
    s.set_defaults(fn=cmd_init)

    s = sub.add_parser("add", help="Add + register a tracking number")
    s.add_argument("number", help="Tracking number")
    s.add_argument("--label", help="Friendly label")
    s.add_argument("--carrier", type=int, help="Carrier code (optional; 0 means auto-detect)")
    s.add_argument("--param", help="Additional parameter (postcode, phone last4, etc.)")
    s.add_argument("--tag", help="17TRACK tag (defaults to label if provided)")
    s.add_argument("--lang", help="Translation language code (default: TRACK17_LANG or 'en')")
    s.add_argument("--status", action="store_true", help="Fetch status immediately after adding")
    s.set_defaults(fn=cmd_add)

    s = sub.add_parser("list", help="List locally tracked packages")
    s.add_argument("--all", action="store_true", help="Include archived rows")
    s.set_defaults(fn=cmd_list)

    s = sub.add_parser("sync", help="Poll 17TRACK for updates for all packages")
    s.add_argument("--active-only", action="store_true", help="Only packages not marked as Stopped")
    s.set_defaults(fn=cmd_sync)

    s = sub.add_parser("status", help="Show status for one package")
    s.add_argument("key", help="Package id or tracking number")
    s.add_argument("--refresh", action="store_true", help="Fetch latest status from 17TRACK")
    s.add_argument("--events", type=int, default=10, help="How many recent events to show")
    s.add_argument("--json", action="store_true", help="Output JSON")
    s.set_defaults(fn=cmd_status)

    s = sub.add_parser("stop", help="Stop tracking a package at 17TRACK")
    s.add_argument("key", help="Package id or tracking number")
    s.set_defaults(fn=cmd_stop)

    s = sub.add_parser("retrack", help="Restart tracking for a stopped package")
    s.add_argument("key", help="Package id or tracking number")
    s.set_defaults(fn=cmd_retrack)

    s = sub.add_parser("remove", help="Remove a package from local DB")
    s.add_argument("key", help="Package id or tracking number")
    s.add_argument("--delete-remote", action="store_true", help="Also delete the tracking number at 17TRACK")
    s.set_defaults(fn=cmd_remove)

    s = sub.add_parser("quota", help="Show 17TRACK API quota info")
    s.set_defaults(fn=cmd_quota)

    s = sub.add_parser("carriers-update", help="Download carrier list cache (for looking up carrier codes)")
    s.set_defaults(fn=cmd_carriers_update)

    s = sub.add_parser("carriers-search", help="Search carrier list cache")
    s.add_argument("query", help="Search query (name/code)")
    s.set_defaults(fn=cmd_carriers_search)

    s = sub.add_parser("ingest-webhook", help="Ingest a single webhook payload (stdin or --file)")
    s.add_argument("--file", help="Read payload JSON from this file instead of stdin")
    s.add_argument("--secret", help="Webhook secret (or set TRACK17_WEBHOOK_SECRET)")
    s.set_defaults(fn=cmd_ingest_webhook)

    s = sub.add_parser("process-inbox", help="Process all spooled payloads in the inbox directory")
    s.add_argument("--secret", help="Webhook secret (or set TRACK17_WEBHOOK_SECRET)")
    s.set_defaults(fn=cmd_process_inbox)

    s = sub.add_parser("webhook-server", help="Run a simple HTTP server to receive 17TRACK webhooks")
    s.add_argument("--bind", default="127.0.0.1", help="Bind address (default: 127.0.0.1)")
    s.add_argument("--port", default=8789, type=int, help="Port (default: 8789)")
    s.add_argument("--verbose", action="store_true", help="Verbose request logging")
    s.set_defaults(fn=cmd_webhook_server)

    return p


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        return int(args.fn(args))
    except Track17Error as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Interrupted.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
