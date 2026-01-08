#!/usr/bin/env python3
"""
Flight tracking CLI - check status, delays, and set alerts.

Usage:
    flights.py status <flight> [--date DATE]
    flights.py search <origin> <dest> [--date DATE] [--airline AIRLINE]
    flights.py track <flight> [--notify]
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Install dependencies: pip install requests beautifulsoup4", file=sys.stderr)
    sys.exit(1)

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

# Airline codes
AIRLINES = {
    "MX": "Breeze Airways",
    "AA": "American Airlines",
    "DL": "Delta",
    "UA": "United",
    "WN": "Southwest",
    "B6": "JetBlue",
    "AS": "Alaska",
    "NK": "Spirit",
    "F9": "Frontier",
}


def get_flightaware_status(flight_number: str, date: str = None) -> dict:
    """Get flight status from FlightAware."""
    # Clean flight number
    flight = flight_number.upper().replace(" ", "")
    
    # Build URL
    url = f"https://www.flightaware.com/live/flight/{flight}"
    if date:
        url += f"/{date}"
    
    headers = {"User-Agent": USER_AGENT}
    
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code != 200:
            return {"error": f"HTTP {resp.status_code}"}
        
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Try to extract flight data
        data = {"flight": flight, "source": "flightaware", "url": url}
        
        # Look for flight status
        status_elem = soup.select_one(".flightPageStatus")
        if status_elem:
            data["status"] = status_elem.get_text(strip=True)
        
        # Look for departure/arrival info
        for row in soup.select(".flightPageSummaryRow"):
            label = row.select_one(".flightPageSummaryLabel")
            value = row.select_one(".flightPageSummaryValue")
            if label and value:
                key = label.get_text(strip=True).lower().replace(" ", "_")
                data[key] = value.get_text(strip=True)
        
        # Try alternate selectors for newer layout
        origin = soup.select_one("[data-origin]")
        dest = soup.select_one("[data-destination]")
        if origin:
            data["origin"] = origin.get("data-origin") or origin.get_text(strip=True)
        if dest:
            data["destination"] = dest.get("data-destination") or dest.get_text(strip=True)
        
        # Look for times in various formats
        time_blocks = soup.select(".flightPageDataBlock")
        for block in time_blocks:
            title = block.select_one(".flightPageDataTitle")
            value = block.select_one(".flightPageDataValue, .flightPageDataTime")
            if title and value:
                key = title.get_text(strip=True).lower().replace(" ", "_")
                data[key] = value.get_text(strip=True)
        
        return data
        
    except Exception as e:
        return {"error": str(e)}


def search_flights_flightaware(origin: str, dest: str, date: str = None, airline: str = None) -> list:
    """Search for flights between airports."""
    origin = origin.upper()
    dest = dest.upper()
    
    # FlightAware route search
    url = f"https://www.flightaware.com/live/findflight?origin={origin}&destination={dest}"
    
    headers = {"User-Agent": USER_AGENT}
    
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        
        flights = []
        
        # FlightAware returns JSON in a JS variable
        import re
        match = re.search(r'FA\.findflight\.resultsContent\s*=\s*(\[.*?\]);', resp.text, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group(1))
                for flight in data:
                    flight_ident = flight.get("flightIdent", "")
                    # Extract flight number from HTML
                    fn_match = re.search(r'>([A-Z]{2,3}\d+)<', flight_ident)
                    flight_num = fn_match.group(1) if fn_match else ""
                    
                    # Filter by airline if specified
                    if airline:
                        airline_upper = airline.upper()
                        if not flight_num.upper().startswith(airline_upper):
                            # Also check MXY for Breeze (MX)
                            if airline_upper == "MX" and not flight_num.upper().startswith("MXY"):
                                continue
                            elif airline_upper != "MX":
                                continue
                    
                    # Only include nonstop flights unless connecting
                    if flight.get("nonstop") != "Nonstop":
                        continue
                    
                    # Clean HTML from status
                    status_raw = flight.get("flightStatus", "")
                    status = re.sub(r'<[^>]+>', '', status_raw).strip()
                    
                    # Clean times
                    dep_time = re.sub(r'<[^>]+>', ' ', flight.get("flightDepartureTime", "")).strip()
                    arr_time = re.sub(r'<[^>]+>', ' ', flight.get("flightArrivalTime", "")).strip()
                    dep_day = re.sub(r'<[^>]+>', '', flight.get("flightDepartureDay", "")).strip()
                    
                    flight_data = {
                        "flight": flight_num,
                        "airline": flight.get("airlineName", ""),
                        "origin": flight.get("origin", ""),
                        "destination": flight.get("destination", ""),
                        "departure": f"{dep_day} {dep_time}",
                        "arrival": arr_time,
                        "status": status,
                        "aircraft": flight.get("aircraftType", ""),
                    }
                    flights.append(flight_data)
            except json.JSONDecodeError:
                pass
        
        return flights
        
    except Exception as e:
        return [{"error": str(e)}]


def get_aviationstack_status(flight_number: str, api_key: str) -> dict:
    """Get flight status from AviationStack API."""
    url = "http://api.aviationstack.com/v1/flights"
    params = {
        "access_key": api_key,
        "flight_iata": flight_number.upper(),
    }
    
    try:
        resp = requests.get(url, params=params, timeout=15)
        data = resp.json()
        
        if data.get("error"):
            return {"error": data["error"].get("message", "API error")}
        
        flights = data.get("data", [])
        if not flights:
            return {"error": "Flight not found"}
        
        flight = flights[0]
        return {
            "flight": flight.get("flight", {}).get("iata"),
            "airline": flight.get("airline", {}).get("name"),
            "origin": flight.get("departure", {}).get("airport"),
            "origin_code": flight.get("departure", {}).get("iata"),
            "destination": flight.get("arrival", {}).get("airport"),
            "dest_code": flight.get("arrival", {}).get("iata"),
            "scheduled_departure": flight.get("departure", {}).get("scheduled"),
            "actual_departure": flight.get("departure", {}).get("actual"),
            "scheduled_arrival": flight.get("arrival", {}).get("scheduled"),
            "actual_arrival": flight.get("arrival", {}).get("actual"),
            "status": flight.get("flight_status"),
            "delay": flight.get("departure", {}).get("delay"),
            "source": "aviationstack",
        }
        
    except Exception as e:
        return {"error": str(e)}


def cmd_status(args):
    """Get flight status."""
    api_key = os.environ.get("AVIATIONSTACK_API_KEY")
    
    # Try AviationStack first if we have a key
    if api_key:
        result = get_aviationstack_status(args.flight, api_key)
        if not result.get("error"):
            print(json.dumps(result, indent=2))
            return
    
    # Fall back to FlightAware scraping
    result = get_flightaware_status(args.flight, args.date)
    print(json.dumps(result, indent=2))


def cmd_search(args):
    """Search for flights."""
    results = search_flights_flightaware(args.origin, args.dest, args.date, args.airline)
    print(json.dumps(results, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Flight tracking CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # status
    p = subparsers.add_parser("status", help="Get flight status")
    p.add_argument("flight", help="Flight number (e.g., MX123, AA100)")
    p.add_argument("--date", help="Date (YYYY-MM-DD)")
    p.set_defaults(func=cmd_status)
    
    # search
    p = subparsers.add_parser("search", help="Search flights by route")
    p.add_argument("origin", help="Origin airport code (e.g., PVD)")
    p.add_argument("dest", help="Destination airport code (e.g., ORF)")
    p.add_argument("--date", help="Date (YYYY-MM-DD)")
    p.add_argument("--airline", help="Airline code filter (e.g., MX)")
    p.set_defaults(func=cmd_search)
    
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
