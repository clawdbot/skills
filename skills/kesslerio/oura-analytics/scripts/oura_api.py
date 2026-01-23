#!/usr/bin/env python3
"""
Oura Cloud API Wrapper

Usage:
    python oura_api.py sleep --days 7
    python oura_api.py readiness --days 7
    python oura_api.py report --type weekly
"""

import os
import sys
import json
import argparse
import time
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path
from email.utils import parsedate_to_datetime
from enum import Enum

SKILL_DIR = Path(__file__).parent.parent


class OutputMode(Enum):
    """Output format modes for Clawdbot integration"""
    BRIEF = "brief"      # 5-8 line human summary
    JSON = "json"        # Full structured data (default)
    ALERT = "alert"      # Only if something needs attention
    SILENT = "silent"    # Exit code only (for cron)

# Import cache if available (robust path handling)
try:
    # Try relative import first
    from .cache import OuraCache
    CACHE_AVAILABLE = True
except (ImportError, ValueError):
    # Fallback: add scripts dir to path
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from cache import OuraCache
        CACHE_AVAILABLE = True
    except ImportError:
        CACHE_AVAILABLE = False

class OuraClient:
    """Oura Cloud API client"""

    BASE_URL = "https://api.ouraring.com/v2/usercollection"

    def __init__(self, token=None, use_cache=True):
        self.token = token or os.environ.get("OURA_API_TOKEN")
        if not self.token:
            raise ValueError("OURA_API_TOKEN not set. Get it at https://cloud.ouraring.com/personal-access-token")
        self.headers = {"Authorization": f"Bearer {self.token}"}
        
        # Initialize cache
        self.cache = None
        if use_cache and CACHE_AVAILABLE:
            self.cache = OuraCache()

    def _request(self, endpoint, start_date=None, end_date=None, max_retries=3):
        """Make API request using urllib with retry logic and rate limit handling"""
        url = f"{self.BASE_URL}/{endpoint}"
        params = []
        if start_date:
            params.append(f"start_date={start_date}")
        if end_date:
            params.append(f"end_date={end_date}")

        if params:
            url += "?" + "&".join(params)

        req = urllib.request.Request(url, headers=self.headers)
        
        for attempt in range(max_retries):
            try:
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    return data.get("data", [])
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    # Rate limited - respect Retry-After header
                    retry_after_raw = e.headers.get("Retry-After", "60")
                    try:
                        # Try parsing as integer (seconds)
                        wait_time = int(retry_after_raw)
                    except ValueError:
                        # HTTP date format - parse and calculate delta
                        try:
                            retry_date = parsedate_to_datetime(retry_after_raw)
                            wait_time = max(0, int((retry_date - datetime.now()).total_seconds()))
                        except (ValueError, TypeError):
                            # Fallback if parsing fails
                            wait_time = 60
                    
                    if attempt < max_retries - 1:
                        print(f"Rate limited. Waiting {wait_time}s before retry {attempt + 1}/{max_retries}...", file=sys.stderr)
                        time.sleep(wait_time)
                        continue
                raise Exception(f"HTTP Error {e.code}: {e.reason}")
            except urllib.error.URLError as e:
                # Network error - exponential backoff
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # 1s, 2s, 4s
                    print(f"Network error. Retrying in {wait_time}s... ({attempt + 1}/{max_retries})", file=sys.stderr)
                    time.sleep(wait_time)
                    continue
                raise Exception(f"Network Error: {e.reason}")
        
        raise Exception(f"Failed after {max_retries} retries")

    def _get_with_cache(self, endpoint, start_date=None, end_date=None):
        """Get data with cache support (per-day caching)"""
        if not self.cache or not start_date or not end_date:
            # No cache or no date range - fetch directly
            return self._request(endpoint, start_date, end_date)

        # Generate date range
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        date_list = []
        current = start
        while current <= end:
            date_list.append(current.strftime("%Y-%m-%d"))
            current += timedelta(days=1)

        # Check cache for each day
        cached_data = []
        missing_dates = []
        for date_str in date_list:
            cached = self.cache.get(endpoint, date_str)
            if cached is not None:
                cached_data.extend(cached)
            else:
                missing_dates.append(date_str)

        # Fetch missing dates
        if missing_dates:
            # Fetch all missing dates in one API call
            fetch_start = min(missing_dates)
            fetch_end = max(missing_dates)
            fresh_data = self._request(endpoint, fetch_start, fetch_end)
            
            # Cache each day individually
            for item in fresh_data:
                item_date = item.get("day") or item.get("timestamp", "")[:10]
                if item_date:
                    # Cache this day's data
                    day_data = [i for i in fresh_data if (i.get("day") or i.get("timestamp", "")[:10]) == item_date]
                    self.cache.set(endpoint, item_date, day_data)
            
            cached_data.extend(fresh_data)

        # Deduplicate by ID (in case of overlapping date ranges)
        seen_ids = set()
        deduped = []
        for item in cached_data:
            item_id = item.get("id")
            if item_id and item_id not in seen_ids:
                seen_ids.add(item_id)
                deduped.append(item)
            elif not item_id:
                # No ID field - keep item (shouldn't happen with Oura API)
                deduped.append(item)
        
        return deduped

    def sync(self, endpoint, days=7):
        """
        Incrementally sync data for endpoint.
        
        Args:
            endpoint: API endpoint (sleep, daily_readiness, daily_activity)
            days: Number of days to sync (default: 7)
        
        Returns:
            Number of new days cached
        """
        if not self.cache:
            raise ValueError("Cache not available")

        # Get last sync date
        last_sync = self.cache.get_last_sync(endpoint)
        
        if last_sync:
            # Validate: reject future dates (corrupted state)
            today = datetime.now().date()
            try:
                last_sync_date = datetime.strptime(last_sync, "%Y-%m-%d").date()
                if last_sync_date > today:
                    print(f"Warning: last_sync in future ({last_sync}), resetting", file=sys.stderr)
                    last_sync = None
            except ValueError:
                print(f"Warning: invalid last_sync ({last_sync}), resetting", file=sys.stderr)
                last_sync = None
        
        if last_sync:
            # Sync from last sync date to today
            start_date = last_sync
        else:
            # First sync - get last N days
            start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        end_date = datetime.now().strftime("%Y-%m-%d")
        
        # Fetch and cache
        data = self._request(endpoint, start_date, end_date)
        
        # Cache per day
        cached_days = set()
        for item in data:
            item_date = item.get("day") or item.get("timestamp", "")[:10]
            if item_date and item_date not in cached_days:
                day_data = [i for i in data if (i.get("day") or i.get("timestamp", "")[:10]) == item_date]
                self.cache.set(endpoint, item_date, day_data)
                cached_days.add(item_date)
        
        # Update last sync
        self.cache.set_last_sync(endpoint, end_date)
        
        return len(cached_days)

    def get_sleep(self, start_date=None, end_date=None):
        """Fetch sleep data (summary)"""
        return self._get_with_cache("sleep", start_date, end_date)

    def get_daily_sleep(self, start_date=None, end_date=None):
        """Fetch detailed sleep data"""
        return self._get_with_cache("daily_sleep", start_date, end_date)

    def get_readiness(self, start_date=None, end_date=None):
        """Fetch readiness data"""
        return self._get_with_cache("daily_readiness", start_date, end_date)

    def get_activity(self, start_date=None, end_date=None):
        """Fetch activity data"""
        return self._get_with_cache("daily_activity", start_date, end_date)

    def get_hrv(self, start_date=None, end_date=None):
        """Fetch HRV data"""
        return self._request("hrv", start_date, end_date)

    def get_recent_sleep(self, days=2):
        """Fetch and merge recent sleep data (daily + detailed).

        Oura data is processed with delay - get last few days and merge
        daily_sleep scores with detailed sleep data.
        """
        # Oura data is processed with delay - get last few days
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")

        # Get daily sleep scores
        url_daily = f"{self.BASE_URL}/daily_sleep?start_date={start_date}&end_date={end_date}"
        req_daily = urllib.request.Request(url_daily, headers=self.headers)
        with urllib.request.urlopen(req_daily, timeout=10) as resp_daily:
            daily_data = {item["day"]: item for item in json.loads(resp_daily.read().decode("utf-8")).get("data", [])}

        # Get detailed sleep data
        url_sleep = f"{self.BASE_URL}/sleep?start_date={start_date}&end_date={end_date}"
        req_sleep = urllib.request.Request(url_sleep, headers=self.headers)
        with urllib.request.urlopen(req_sleep, timeout=10) as resp_sleep:
            sleep_data = json.loads(resp_sleep.read().decode("utf-8")).get("data", [])

        # Merge: add scores to sleep data
        for item in sleep_data:
            day = item.get("day")
            if day in daily_data:
                item["score"] = daily_data[day].get("score")

        # Return last N entries
        return sleep_data[-days:] if len(sleep_data) >= days else sleep_data

    def get_weekly_summary(self):
        """Fetch weekly sleep summary"""
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        return self.get_sleep(start_date, end_date)


class OuraAnalyzer:
    """Analyze Oura data"""

    def __init__(self, sleep_data=None, readiness_data=None, activity_data=None):
        self.sleep = sleep_data or []
        self.readiness = readiness_data or []
        self.activity = activity_data or []

    @staticmethod
    def seconds_to_hours(seconds):
        """Convert seconds to hours"""
        return round(seconds / 3600, 1) if seconds else None

    @staticmethod
    def calculate_sleep_score(day):
        """Calculate approximate sleep score from available metrics"""
        efficiency = day.get("efficiency", 0)
        duration_sec = day.get("total_sleep_duration", 0)
        duration_hours = duration_sec / 3600 if duration_sec else 0

        # Oura's algorithm approximation:
        eff_score = min(efficiency, 100)
        dur_score = min(duration_hours / 8 * 100, 100)  # 8 hours = 100%

        return round((eff_score * 0.6) + (dur_score * 0.4), 1)

    def average_metric(self, data, metric, convert_to_hours=False):
        """Calculate average of a metric"""
        if not data:
            return None
        values = []
        for d in data:
            val = d.get(metric)
            if val is not None:
                if convert_to_hours:
                    val = self.seconds_to_hours(val)
                values.append(val)
        return round(sum(values) / len(values), 2) if values else None

    def trend(self, data, metric, days=7):
        """Calculate trend over N days"""
        if len(data) < 2:
            return 0
        recent = data[-days:]
        if len(recent) < 2:
            return 0
        first = recent[0].get(metric, 0)
        last = recent[-1].get(metric, 0)
        return round(last - first, 2)

    def summary(self):
        """Generate summary"""
        avg_sleep_hours = self.average_metric(self.sleep, "total_sleep_duration", convert_to_hours=True)
        avg_efficiency = self.average_metric(self.sleep, "efficiency")
        avg_hrv = self.average_metric(self.sleep, "average_hrv")

        # Calculate average sleep score
        sleep_scores = [self.calculate_sleep_score(d) for d in self.sleep]
        avg_sleep_score = round(sum(sleep_scores) / len(sleep_scores), 1) if sleep_scores else None

        # Readiness from dedicated dataset (not nested in sleep)
        avg_readiness = self.average_metric(self.readiness, "score")

        return {
            "avg_sleep_score": avg_sleep_score,
            "avg_readiness_score": avg_readiness,
            "avg_sleep_hours": avg_sleep_hours,
            "avg_sleep_efficiency": avg_efficiency,
            "avg_hrv": avg_hrv,
            "days_tracked": len(self.sleep)
        }


class OuraReporter:
    """Generate Oura reports"""

    def __init__(self, client):
        self.client = client

    def generate_report(self, report_type="weekly", days=None, user_tz=None):
        """Generate report with timezone awareness"""
        if not days:
            days = 7 if report_type == "weekly" else 30

        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        sleep = self.client.get_sleep(start_date, end_date)
        readiness = self.client.get_readiness(start_date, end_date)
        activity = self.client.get_activity(start_date, end_date)

        analyzer = OuraAnalyzer(sleep, readiness, activity)
        summary = analyzer.summary()

        # Get timezone info
        if user_tz is None:
            import os
            user_tz = os.environ.get("USER_TIMEZONE", "America/Los_Angeles")

        # Detect potential travel days (use user-supplied timezone)
        try:
            from timezone_utils import is_travel_day
            travel_days = is_travel_day(sleep, user_tz=user_tz)
            # Convert date objects to strings for JSON serialization
            travel_days = [d.isoformat() for d in travel_days]
        except ImportError:
            travel_days = []

        return {
            "report_type": report_type,
            "period": f"{start_date} to {end_date}",
            "timezone": user_tz,
            "travel_days": travel_days,
            "summary": summary,
            "daily_data": {
                "sleep": sleep,
                "readiness": readiness,
                "activity": activity
            }
        }


def format_output(data, mode: OutputMode = OutputMode.JSON):
    """Format output based on mode"""
    if mode == OutputMode.JSON:
        return json.dumps(data, indent=2)
    
    elif mode == OutputMode.BRIEF:
        # Human-readable brief summary
        if isinstance(data, dict):
            if "summary" in data:
                # Report format
                s = data["summary"]
                lines = [
                    f"📊 {data.get('report_type', 'Report').title()} ({data.get('period', 'N/A')})",
                    f"Sleep: {s.get('avg_sleep_hours', 'N/A')}h avg, {s.get('avg_sleep_score', 'N/A')} score",
                    f"Readiness: {s.get('avg_readiness_score', 'N/A')}",
                    f"Efficiency: {s.get('avg_sleep_efficiency', 'N/A')}%",
                    f"HRV: {s.get('avg_hrv', 'N/A')} ms",
                    f"Days: {s.get('days_tracked', 0)}"
                ]
                if data.get("travel_days"):
                    lines.append(f"Travel: {', '.join(data['travel_days'])}")
                return "\n".join(lines)
            elif "avg_sleep_score" in data or "avg_sleep_hours" in data:
                # Summary command output - prioritize key metrics
                key_order = ["avg_sleep_score", "avg_readiness_score", "avg_sleep_hours", 
                            "avg_sleep_efficiency", "avg_hrv", "days_tracked"]
                lines = []
                for key in key_order:
                    if key in data:
                        lines.append(f"{key}: {data[key]}")
                return "\n".join(lines)
            else:
                # Generic dict - show first 6 items
                lines = [f"{k}: {v}" for k, v in list(data.items())[:6]]
                return "\n".join(lines)
        elif isinstance(data, list):
            return f"{len(data)} records"
        return str(data)
    
    elif mode == OutputMode.ALERT:
        # Only output if something needs attention
        # Handle both nested report summary and flat summary command
        s = data.get("summary", data) if isinstance(data, dict) else {}
        
        # Ensure we are looking at a summary-like object before checking thresholds
        if isinstance(s, dict) and ("avg_sleep_score" in s or "avg_sleep_hours" in s):
            alerts = []
            
            # Check for concerning metrics
            if s.get("avg_sleep_hours") and s["avg_sleep_hours"] < 6:
                alerts.append(f"⚠️  Low sleep: {s['avg_sleep_hours']}h avg")
            if s.get("avg_readiness_score") and s["avg_readiness_score"] < 70:
                alerts.append(f"⚠️  Low readiness: {s['avg_readiness_score']}")
            if s.get("avg_sleep_efficiency") and s["avg_sleep_efficiency"] < 80:
                alerts.append(f"⚠️  Low efficiency: {s['avg_sleep_efficiency']}%")
            
            if alerts:
                return "\n".join(alerts)
        return ""  # No alerts or not a summary
    
    elif mode == OutputMode.SILENT:
        # No output - exit code only
        return ""
    
    return json.dumps(data, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Oura Analytics CLI")
    parser.add_argument("command", choices=["sleep", "daily_sleep", "readiness", "activity", "report", "summary", "comparison", "sync", "cache"],
                       help="Data type to fetch or report type")
    parser.add_argument("--days", type=int, default=7, help="Number of days")
    parser.add_argument("--type", default="weekly", help="Report type")
    parser.add_argument("--token", help="Oura API token")
    parser.add_argument("--timezone", help="User timezone (default: USER_TIMEZONE env or America/Los_Angeles)")
    parser.add_argument("--local-time", action="store_true", help="Show dates in local time instead of UTC")
    parser.add_argument("--endpoint", choices=["sleep", "daily_readiness", "daily_activity", "all"], help="Endpoint for sync/cache commands")
    parser.add_argument("--clear", action="store_true", help="Clear cache (for cache command)")
    parser.add_argument("--no-cache", action="store_true", help="Disable cache for this request")
    parser.add_argument("--format", choices=["json", "brief", "alert", "silent"], default="json", 
                       help="Output format (json=full data, brief=human summary, alert=warnings only, silent=exit code)")

    args = parser.parse_args()

    try:
        use_cache = not args.no_cache
        client = OuraClient(args.token, use_cache=use_cache)
        
        # Parse output mode
        output_mode = OutputMode(args.format)

        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=args.days)).strftime("%Y-%m-%d")

        if args.command == "sleep":
            data = client.get_sleep(start_date, end_date)
            # Optionally convert to local time
            if args.local_time:
                from timezone_utils import get_canonical_day
                for record in data:
                    bedtime_start = record.get("bedtime_start", "")
                    if bedtime_start:
                        _, local_dt = get_canonical_day(bedtime_start, args.timezone)
                        if local_dt:
                            record["local_bedtime_start"] = local_dt.isoformat()
            output = format_output(data, output_mode)
            if output:
                print(output)

        elif args.command == "daily_sleep":
            data = client.get_daily_sleep(start_date, end_date)
            output = format_output(data, output_mode)
            if output:
                print(output)

        elif args.command == "readiness":
            data = client.get_readiness(start_date, end_date)
            output = format_output(data, output_mode)
            if output:
                print(output)

        elif args.command == "activity":
            data = client.get_activity(start_date, end_date)
            output = format_output(data, output_mode)
            if output:
                print(output)

        elif args.command == "summary":
            sleep = client.get_sleep(start_date, end_date)
            readiness = client.get_readiness(start_date, end_date)
            analyzer = OuraAnalyzer(sleep, readiness)
            summary = analyzer.summary()
            output = format_output(summary, output_mode)
            if output:
                print(output)

        elif args.command == "comparison":
            doubled_days = args.days * 2
            start_date_extended = (datetime.now() - timedelta(days=doubled_days)).strftime("%Y-%m-%d")

            sleep = client.get_sleep(start_date_extended, end_date)
            sleep = sorted(sleep, key=lambda x: x.get('day'))
            
            readiness = client.get_readiness(start_date_extended, end_date)
            readiness = sorted(readiness, key=lambda x: x.get('day'))

            current_sleep = sleep[-args.days:] if len(sleep) > 0 else []
            previous_sleep = sleep[:-args.days][-args.days:] if len(sleep) > args.days else []
            
            current_readiness = readiness[-args.days:] if len(readiness) > 0 else []
            previous_readiness = readiness[:-args.days][-args.days:] if len(readiness) > args.days else []

            analyzer_curr = OuraAnalyzer(current_sleep, current_readiness)
            analyzer_prev = OuraAnalyzer(previous_sleep, previous_readiness)

            summary_curr = analyzer_curr.summary()
            summary_prev = analyzer_prev.summary()

            diff = {}
            for key in summary_curr:
                curr_val = summary_curr.get(key)
                prev_val = summary_prev.get(key)
                if isinstance(curr_val, (int, float)) and isinstance(prev_val, (int, float)):
                    diff[key] = round(curr_val - prev_val, 2)
                else:
                    diff[key] = None

            comparison = {
                "current": summary_curr,
                "previous": summary_prev,
                "diff": diff
            }
            output = format_output(comparison, output_mode)
            if output:
                print(output)

        elif args.command == "report":
            reporter = OuraReporter(client)
            report = reporter.generate_report(args.type, args.days, user_tz=args.timezone)
            output = format_output(report, output_mode)
            if output:
                print(output)

        elif args.command == "sync":
            if not CACHE_AVAILABLE:
                print("Error: Cache not available", file=sys.stderr)
                sys.exit(1)
            
            endpoints = ["sleep", "daily_readiness", "daily_activity"] if args.endpoint == "all" else [args.endpoint or "sleep"]
            
            results = {}
            for endpoint in endpoints:
                cached_days = client.sync(endpoint, args.days)
                results[endpoint] = cached_days
                if output_mode != OutputMode.SILENT:
                    print(f"{endpoint}: synced {cached_days} days", file=sys.stderr)
            
            output = format_output(results, output_mode)
            if output:
                print(output)

        elif args.command == "cache":
            if not CACHE_AVAILABLE or not client.cache:
                print("Error: Cache not available", file=sys.stderr)
                sys.exit(1)
            
            if args.clear:
                # Clear cache for endpoint or all
                deleted = client.cache.clear(args.endpoint if args.endpoint != "all" else None)
                print(f"Cleared {deleted} cached files")
            else:
                # Show cache stats
                cache_dir = client.cache.cache_dir
                if cache_dir.exists():
                    stats = {}
                    for endpoint_dir in cache_dir.iterdir():
                        if endpoint_dir.is_dir():
                            files = list(endpoint_dir.glob("*.json"))
                            last_sync = client.cache.get_last_sync(endpoint_dir.name)
                            stats[endpoint_dir.name] = {
                                "cached_days": len(files),
                                "last_sync": last_sync
                            }
                    print(json.dumps(stats, indent=2))
                else:
                    print("Cache empty")

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        print("Set OURA_API_TOKEN environment variable or use --token", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"API Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
