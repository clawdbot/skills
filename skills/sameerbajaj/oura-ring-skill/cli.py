#!/usr/bin/env python3
"""Oura Ring (V2 API) CLI.

Commands:
  - readiness: fetch most recent daily readiness
  - sleep:     fetch most recent daily sleep
  - trends:    fetch last 7 days of readiness (handles pagination)

Auth:
  Loads OURA_TOKEN from a .env file (python-dotenv) or from environment.

This is intended to be a small, public-facing reference implementation.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

try:
    import requests  # type: ignore
except ModuleNotFoundError:  # Allows --mock usage without deps installed
    requests = None  # type: ignore

try:
    from dotenv import find_dotenv, load_dotenv  # type: ignore
except ModuleNotFoundError:  # Allows --mock usage without deps installed
    find_dotenv = None  # type: ignore
    load_dotenv = None  # type: ignore

DEFAULT_BASE_URL = "https://api.ouraring.com/v2/usercollection"


class OuraError(RuntimeError):
    pass


def _iso_date(d: _dt.date) -> str:
    return d.strftime("%Y-%m-%d")


def _today_local() -> _dt.date:
    return _dt.date.today()


def _truncate(s: str, n: int = 600) -> str:
    s = s or ""
    return s if len(s) <= n else (s[:n] + "…")


@dataclass
class OuraClient:
    token: str
    base_url: str = DEFAULT_BASE_URL
    timeout_s: float = 20.0
    max_retries: int = 3

    def __post_init__(self) -> None:
        if requests is None:
            raise OuraError(
                "Missing dependency 'requests'. Install requirements.txt (preferably in a venv)."
            )
        self._session = requests.Session()

    def get_json(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = self.base_url.rstrip("/") + "/" + path.lstrip("/")
        # Oura V2 sometimes uses different base paths for detailed data
        # If the path is 'sleep' or 'readiness' or 'heartrate', it might be at /v2/usercollection/
        # but let's check if we need to adjust based on the endpoint.
        headers = {"Authorization": f"Bearer {self.token}", "Accept": "application/json"}

        for attempt in range(self.max_retries + 1):
            try:
                resp = self._session.get(url, headers=headers, params=params, timeout=self.timeout_s)
            except requests.RequestException as e:
                if attempt < self.max_retries:
                    time.sleep(0.75 * (2**attempt))
                    continue
                raise OuraError(f"Request failed: {e}") from e

            if resp.status_code in (429, 500, 502, 503, 504) and attempt < self.max_retries:
                retry_after = resp.headers.get("Retry-After")
                if retry_after and retry_after.isdigit():
                    time.sleep(float(retry_after))
                else:
                    time.sleep(0.75 * (2**attempt))
                continue

            if not resp.ok:
                raise OuraError(f"HTTP {resp.status_code} calling {url}: {_truncate(resp.text)}")

            try:
                data = resp.json()
            except ValueError as e:
                raise OuraError(f"Non-JSON response from {url}: {_truncate(resp.text)}") from e

            if not isinstance(data, dict):
                raise OuraError(f"Unexpected response type from {url}: {type(data).__name__}")
            return data

        raise OuraError("Request failed after retries")


def _load_token(env_file: Optional[str]) -> Tuple[str, str]:
    """Returns (token, env_source)."""
    if load_dotenv is None or find_dotenv is None:
        raise OuraError(
            "Missing dependency 'python-dotenv'. Install requirements.txt (preferably in a venv)."
        )

    if env_file:
        load_dotenv(env_file, override=False)
        source = env_file
    else:
        dotenv_path = find_dotenv(usecwd=True)
        if dotenv_path:
            load_dotenv(dotenv_path, override=False)
            source = dotenv_path
        else:
            source = "environment"

    token = os.getenv("OURA_TOKEN", "").strip()
    if not token:
        token = os.getenv("OURA_PERSONAL_ACCESS_TOKEN", "").strip()

    if not token:
        raise OuraError(
            "Missing OURA_TOKEN. Put it in a .env file (recommended) or export it in your shell."
        )
    return token, source


def _paginate(client: OuraClient, endpoint: str, params: Dict[str, Any]) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    next_token: Optional[str] = None

    while True:
        p = dict(params)
        if next_token:
            p["next_token"] = next_token

        payload = client.get_json(endpoint, params=p)
        batch = payload.get("data")
        if batch is None:
            batch = payload.get("items") or payload.get("records") or []

        if not isinstance(batch, list):
            raise OuraError(f"Unexpected pagination payload: 'data' is {type(batch).__name__}")

        items.extend([x for x in batch if isinstance(x, dict)])

        next_token = payload.get("next_token") or payload.get("nextToken")
        if not next_token:
            break

    return items


def _pick_latest_by_day(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not items:
        raise OuraError("No data returned for the requested date range.")

    def key(it: Dict[str, Any]) -> str:
        day = it.get("day") or it.get("date") or ""
        return str(day)

    return sorted(items, key=key)[-1]


def _mock_daily_readiness(today: _dt.date) -> Dict[str, Any]:
    day = _iso_date(today)
    return {
        "data": [
            {
                "day": day,
                "score": 85,
                "contributors": {
                    "sleep_balance": 82,
                    "hrv_balance": 79,
                    "resting_heart_rate": 88,
                    "activity_balance": 74,
                    "recovery_index": 80,
                },
            }
        ],
        "next_token": None,
    }


def _mock_daily_sleep(today: _dt.date) -> Dict[str, Any]:
    day = _iso_date(today)
    return {
        "data": [
            {
                "day": day,
                "score": 79,
                "total_sleep_duration": 7 * 3600 + 22 * 60,
                "contributors": {
                    "total_sleep": 78,
                    "deep_sleep": 72,
                    "rem_sleep": 76,
                    "sleep_efficiency": 81,
                    "latency": 70,
                },
            }
        ],
        "next_token": None,
    }


def _mock_trends(today: _dt.date) -> Dict[str, Any]:
    data = []
    for i in range(6, -1, -1):
        d = today - _dt.timedelta(days=i)
        data.append({"day": _iso_date(d), "score": 75 + (6 - i)})
    return {"data": data, "next_token": None}


def cmd_readiness(args: argparse.Namespace) -> Dict[str, Any]:
    today = _today_local()
    if args.mock:
        item = _pick_latest_by_day(_mock_daily_readiness(today)["data"])
        return {"type": "daily_readiness", "item": item, "source": "mock"}

    token, source = _load_token(args.env_file)
    base_url = args.base_url or os.getenv("OURA_BASE_URL") or DEFAULT_BASE_URL
    client = OuraClient(token=token, base_url=base_url, timeout_s=args.timeout)

    start = today - _dt.timedelta(days=args.lookback_days)
    items = _paginate(
        client, "daily_readiness", {"start_date": _iso_date(start), "end_date": _iso_date(today)}
    )
    item = _pick_latest_by_day(items)
    return {"type": "daily_readiness", "item": item, "source": source}


def cmd_sleep(args: argparse.Namespace) -> Dict[str, Any]:
    today = _today_local()
    if args.mock:
        item = _pick_latest_by_day(_mock_daily_sleep(today)["data"])
        return {"type": "daily_sleep", "item": item, "source": "mock"}

    token, source = _load_token(args.env_file)
    base_url = args.base_url or os.getenv("OURA_BASE_URL") or DEFAULT_BASE_URL
    client = OuraClient(token=token, base_url=base_url, timeout_s=args.timeout)

    start = today - _dt.timedelta(days=args.lookback_days)
    
    # 1. Fetch Summary (Score)
    items = _paginate(
        client, "daily_sleep", {"start_date": _iso_date(start), "end_date": _iso_date(today)}
    )
    summary = _pick_latest_by_day(items)
    
    # 2. Fetch Detailed (Duration, RHR, HRV)
    sessions = _paginate(
        client, "sleep", {"start_date": _iso_date(start), "end_date": _iso_date(today)}
    )
    detail = _pick_latest_by_day(sessions)
    
    return {"type": "daily_sleep", "item": summary, "detail": detail, "source": source}


def cmd_trends(args: argparse.Namespace) -> Dict[str, Any]:
    today = _today_local()
    start = today - _dt.timedelta(days=6)

    if args.mock:
        payload = _mock_trends(today)
        return {
            "type": "readiness_trends",
            "start_date": _iso_date(start),
            "end_date": _iso_date(today),
            "items": payload["data"],
            "source": "mock",
        }

    token, source = _load_token(args.env_file)
    base_url = args.base_url or os.getenv("OURA_BASE_URL") or DEFAULT_BASE_URL
    client = OuraClient(token=token, base_url=base_url, timeout_s=args.timeout)

    # 1. Readiness Scores
    items = _paginate(
        client, "daily_readiness", {"start_date": _iso_date(start), "end_date": _iso_date(today)}
    )
    items_sorted = sorted(items, key=lambda x: str(x.get("day") or x.get("date") or ""))

    # 2. Heart Rate / HRV Trend (from sleep sessions)
    sessions = _paginate(
        client, "sleep", {"start_date": _iso_date(start), "end_date": _iso_date(today)}
    )
    sessions_sorted = sorted(sessions, key=lambda x: str(x.get("day") or x.get("date") or ""))

    return {
        "type": "readiness_trends",
        "start_date": _iso_date(start),
        "end_date": _iso_date(today),
        "items": items_sorted,
        "sessions": sessions_sorted,
        "source": source,
    }


def cmd_resilience(args: argparse.Namespace) -> Dict[str, Any]:
    today = _today_local()
    if args.mock:
        return {"type": "daily_resilience", "item": {"day": _iso_date(today), "level": "EXTERNALLY_RECOVERED"}, "source": "mock"}

    token, source = _load_token(args.env_file)
    base_url = args.base_url or os.getenv("OURA_BASE_URL") or DEFAULT_BASE_URL
    client = OuraClient(token=token, base_url=base_url, timeout_s=args.timeout)

    start = today - _dt.timedelta(days=7)
    items = _paginate(client, "daily_resilience", {"start_date": _iso_date(start), "end_date": _iso_date(today)})
    item = _pick_latest_by_day(items)
    return {"type": "daily_resilience", "item": item, "source": source}


def cmd_stress(args: argparse.Namespace) -> Dict[str, Any]:
    today = _today_local()
    if args.mock:
        return {"type": "daily_stress", "item": {"day": _iso_date(today), "stress_high": 10}, "source": "mock"}

    token, source = _load_token(args.env_file)
    base_url = args.base_url or os.getenv("OURA_BASE_URL") or DEFAULT_BASE_URL
    client = OuraClient(token=token, base_url=base_url, timeout_s=args.timeout)

    start = today - _dt.timedelta(days=7)
    items = _paginate(client, "daily_stress", {"start_date": _iso_date(start), "end_date": _iso_date(today)})
    item = _pick_latest_by_day(items)
    return {"type": "daily_stress", "item": item, "source": source}


def _emit(payload: Dict[str, Any], fmt: str, pretty: bool) -> None:
    if fmt == "json":
        json.dump(payload, sys.stdout, indent=2 if pretty else None, sort_keys=pretty)
        sys.stdout.write("\n")
        return

    t = payload.get("type")
    if t == "daily_readiness":
        it = payload.get("item") or {}
        sys.stdout.write(f"{it.get('day','?')} readiness_score={it.get('score')}\n")
    elif t == "daily_sleep":
        it = payload.get("item") or {}
        dur = it.get("total_sleep_duration")
        if isinstance(dur, (int, float)):
            h = int(dur) // 3600
            m = (int(dur) % 3600) // 60
            dur_s = f"{h}h{m:02d}m"
        else:
            dur_s = "?"
        sys.stdout.write(
            f"{it.get('day','?')} sleep_score={it.get('score')} total_sleep={dur_s}\n"
        )
    elif t == "readiness_trends":
        for it in payload.get("items") or []:
            if isinstance(it, dict):
                sys.stdout.write(f"{it.get('day','?')} readiness_score={it.get('score')}\n")
    elif t == "daily_resilience":
        it = payload.get("item") or {}
        sys.stdout.write(f"{it.get('day','?')} resilience_level={it.get('level')}\n")
    elif t == "daily_stress":
        it = payload.get("item") or {}
        sys.stdout.write(f"{it.get('day','?')} stress_high={it.get('stress_high')} stress_score={it.get('stress_score')}\n")
    else:
        sys.stdout.write(str(payload) + "\n")


def build_parser() -> argparse.ArgumentParser:
    # Global flags must come before the subcommand (standard argparse behavior).
    p = argparse.ArgumentParser(prog="oura", description="Oura Ring V2 API CLI")
    p.add_argument(
        "--env-file",
        help="Path to .env file containing OURA_TOKEN (default: search parents for .env)",
        default=None,
    )
    p.add_argument(
        "--base-url",
        help=f"Override API base URL (default: {DEFAULT_BASE_URL})",
        default=None,
    )
    p.add_argument("--timeout", type=float, default=20.0, help="Request timeout in seconds")
    p.add_argument(
        "--format",
        choices=["json", "text"],
        default="text" if sys.stdout.isatty() else "json",
        help="Output format",
    )
    p.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    p.add_argument("--mock", action="store_true", help="Emit example payloads (no network)")

    sub = p.add_subparsers(dest="command", required=True)

    pr = sub.add_parser("readiness", help="Fetch most recent daily readiness")
    pr.add_argument(
        "--lookback-days",
        type=int,
        default=14,
        help="How many days back to search to find the latest record",
    )
    pr.set_defaults(func=cmd_readiness)

    ps = sub.add_parser("sleep", help="Fetch most recent daily sleep")
    ps.add_argument(
        "--lookback-days",
        type=int,
        default=14,
        help="How many days back to search to find the latest record",
    )
    ps.set_defaults(func=cmd_sleep)

    pt = sub.add_parser("trends", help="Fetch last 7 days of readiness (paginated)")
    pt.set_defaults(func=cmd_trends)

    pre = sub.add_parser("resilience", help="Fetch latest daily resilience")
    pre.set_defaults(func=cmd_resilience)

    pst = sub.add_parser("stress", help="Fetch latest daily stress")
    pst.set_defaults(func=cmd_stress)

    return p


def main(argv: Optional[List[str]] = None) -> int:
    try:
        args = build_parser().parse_args(argv)
        payload = args.func(args)
        _emit(payload, fmt=args.format, pretty=bool(args.pretty))
        return 0
    except KeyboardInterrupt:
        return 130
    except OuraError as e:
        sys.stderr.write(f"Error: {e}\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
