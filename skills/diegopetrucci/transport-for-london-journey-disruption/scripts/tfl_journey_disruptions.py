#!/usr/bin/env python3
import argparse
import datetime
import json
import os
import sys
import urllib.parse
import urllib.request

BASE_URL = "https://api.tfl.gov.uk"


def _env_params():
    params = {}
    app_id = os.environ.get("TFL_APP_ID")
    app_key = os.environ.get("TFL_APP_KEY")
    if app_id:
        params["app_id"] = app_id
    if app_key:
        params["app_key"] = app_key
    return params


def _build_url(path, params=None):
    url = BASE_URL + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    return url


def _http_get_json(path, params=None):
    url = _build_url(path, params)
    req = urllib.request.Request(url, headers={"User-Agent": "tfl-journey-disruption-skill"})
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def _print_disambiguation(side, disambig):
    options = disambig.get("disambiguationOptions", [])
    if not options:
        return False
    print(f"{side} location is ambiguous. Pick one and retry:")
    for opt in options[:10]:
        place = opt.get("place", {})
        name = place.get("commonName") or opt.get("parameterValue")
        print(f"- {name} -> {opt.get('parameterValue')}")
    return True


def _extract_line_ids(legs):
    line_ids = set()
    for leg in legs:
        mode = (leg.get("mode") or {}).get("id")
        if mode == "walking":
            continue
        line = leg.get("line") or {}
        if line.get("id"):
            line_ids.add(line["id"])
        for opt in (leg.get("routeOptions") or []):
            line_identifier = opt.get("lineIdentifier")
            if isinstance(line_identifier, dict) and line_identifier.get("id"):
                line_ids.add(line_identifier["id"])
            elif isinstance(line_identifier, str):
                line_ids.add(line_identifier)
    return sorted(line_ids)


def _summarize_leg(leg):
    mode = (leg.get("mode") or {}).get("id")
    instruction = (leg.get("instruction") or {}).get("summary")
    direction = ""
    line_id = None
    line_name = None

    line = leg.get("line") or {}
    if line.get("id"):
        line_id = line["id"]
    if line.get("name"):
        line_name = line["name"]

    for opt in (leg.get("routeOptions") or []):
        line_identifier = opt.get("lineIdentifier")
        if isinstance(line_identifier, dict):
            if not line_id and line_identifier.get("id"):
                line_id = line_identifier["id"]
            if not line_name and line_identifier.get("name"):
                line_name = line_identifier["name"]
        if not line_name and opt.get("name"):
            line_name = opt.get("name")
        directions = opt.get("directions") or []
        if directions and not direction:
            direction = directions[0]

    return {
        "mode": mode,
        "instruction": instruction,
        "line_id": line_id,
        "line_name": line_name,
        "direction": direction,
        "departure": leg.get("departureTime"),
        "arrival": leg.get("arrivalTime"),
    }


def _fetch_line_status(line_ids, base_params):
    if not line_ids:
        return {}
    joined = ",".join(line_ids)
    path = "/Line/{}/Status".format(urllib.parse.quote(joined, safe=","))
    data = _http_get_json(path, base_params)
    statuses = {}
    for line in data:
        line_id = line.get("id") or line.get("name")
        statuses[line_id] = {
            "name": line.get("name") or line_id,
            "statuses": line.get("lineStatuses") or [],
        }
    return statuses


def _issues_for_line_status(line_statuses):
    issues = []
    for st in line_statuses:
        desc = st.get("statusSeverityDescription")
        reason = st.get("reason")
        if desc and desc.lower() != "good service":
            issues.append({"status": desc, "reason": reason})
        elif reason:
            issues.append({"status": desc or "Advisory", "reason": reason})
    return issues


def _print_journey(journey, statuses_by_line):
    duration = journey.get("duration")
    depart = journey.get("startDateTime")
    arrive = journey.get("arrivalDateTime")
    legs = journey.get("legs", [])

    print(f"Duration: {duration} min")
    if depart and arrive:
        print(f"Time: {depart} -> {arrive}")

    for leg in legs:
        summary = _summarize_leg(leg)
        mode = summary.get("mode") or ""
        instruction = summary.get("instruction") or ""
        line_name = summary.get("line_name") or summary.get("line_id")
        direction = summary.get("direction")
        if mode == "walking":
            label = "Walk"
        else:
            label = line_name or mode
        if direction:
            print(f"- {label} towards {direction}: {instruction}")
        else:
            print(f"- {label}: {instruction}")

    line_ids = _extract_line_ids(legs)
    issues = []
    for line_id in line_ids:
        status = statuses_by_line.get(line_id)
        if not status:
            continue
        line_issues = _issues_for_line_status(status.get("statuses", []))
        for issue in line_issues:
            issues.append({"line": status["name"], **issue})

    if issues:
        print("Disruptions:")
        for issue in issues:
            reason = issue.get("reason")
            if reason:
                print(f"- {issue['line']}: {issue['status']} | {reason}")
            else:
                print(f"- {issue['line']}: {issue['status']}")
    else:
        print("Disruptions: none detected")

    return issues


def main():
    parser = argparse.ArgumentParser(
        description="Plan a TfL journey and check for line disruptions."
    )
    parser.add_argument("locations", nargs="*", help="from and to locations")
    parser.add_argument("--from", dest="from_location", help="start location")
    parser.add_argument("--to", dest="to_location", help="end location")
    parser.add_argument("--date", help="YYYYMMDD")
    parser.add_argument("--time", help="HHMM")
    parser.add_argument("--time-is", choices=["Depart", "Arrive"], help="Depart or Arrive")
    parser.add_argument("--depart-at", help="HHMM")
    parser.add_argument("--arrive-by", help="HHMM")
    parser.add_argument("--max-journeys", type=int, default=3)

    args = parser.parse_args()

    if len(args.locations) > 2:
        parser.error("Too many positional arguments. Use: FROM TO")

    from_location = args.from_location or (args.locations[0] if len(args.locations) > 0 else None)
    to_location = args.to_location or (args.locations[1] if len(args.locations) > 1 else None)

    if not from_location or not to_location:
        parser.error("Missing FROM or TO. Provide positional args or --from/--to.")

    if args.depart_at and args.arrive_by:
        parser.error("Use only one of --depart-at or --arrive-by.")

    if args.depart_at:
        if args.time or args.time_is:
            parser.error("--depart-at conflicts with --time/--time-is.")
        args.time = args.depart_at
        args.time_is = "Depart"
    if args.arrive_by:
        if args.time or args.time_is:
            parser.error("--arrive-by conflicts with --time/--time-is.")
        args.time = args.arrive_by
        args.time_is = "Arrive"

    params = _env_params()
    if args.date:
        params["date"] = args.date
    if args.time:
        params["time"] = args.time
    if args.time_is:
        params["timeIs"] = args.time_is

    from_encoded = urllib.parse.quote(from_location, safe=",")
    to_encoded = urllib.parse.quote(to_location, safe=",")
    path = f"/Journey/JourneyResults/{from_encoded}/to/{to_encoded}"

    try:
        data = _http_get_json(path, params)
    except Exception as exc:
        print(f"Error fetching journey results: {exc}", file=sys.stderr)
        return 1

    disambig = False
    if _print_disambiguation("From", data.get("fromLocationDisambiguation", {})):
        disambig = True
    if _print_disambiguation("To", data.get("toLocationDisambiguation", {})):
        disambig = True
    if disambig:
        return 2

    journeys = data.get("journeys", [])
    if not journeys:
        print("No journeys returned.")
        return 1

    journeys = journeys[: max(1, args.max_journeys)]

    # Collect line IDs across all candidate journeys
    line_ids = set()
    for journey in journeys:
        line_ids.update(_extract_line_ids(journey.get("legs", [])))

    statuses_by_line = _fetch_line_status(sorted(line_ids), params)

    # Evaluate top journey first
    print(f"From: {from_location}")
    print(f"To: {to_location}")
    if args.date:
        print(f"Date: {args.date}")
    if args.time:
        time_is = args.time_is or "Depart"
        print(f"Time: {args.time} ({time_is})")
    print("")

    top = journeys[0]
    top_issues = _print_journey(top, statuses_by_line)

    if not top_issues:
        print("\nRecommended route: no active disruptions detected.")
        return 0

    # If disrupted, show alternatives
    if len(journeys) == 1:
        print("\nTop route has disruptions. No alternative routes returned.")
        print("Try increasing --max-journeys or adjusting time/date.")
        return 0

    print("\nTop route has disruptions. Alternatives:")
    for idx, journey in enumerate(journeys[1:3], start=2):
        print("")
        print(f"Option {idx}:")
        issues = _print_journey(journey, statuses_by_line)
        if not issues:
            print("Note: no active disruptions detected for this option.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
