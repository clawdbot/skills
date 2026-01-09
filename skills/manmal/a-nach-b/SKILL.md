---
name: anachb
description: Austrian public transport (VOR AnachB) for all of Austria. Query real-time departures, search stations/stops, plan routes between locations, and check service disruptions. Use when asking about Austrian trains, buses, trams, metro (U-Bahn), or directions involving public transport in Austria.
---

# VOR AnachB - Austrian Public Transport API

Query Austrian public transport for real-time departures, route planning, and service disruptions using the HAFAS API.

## Quick Reference

| Script | Purpose |
|--------|---------|
| `search.sh` | Find stations/stops by name |
| `departures.sh` | Real-time departures at a station |
| `route.sh` | Plan a trip between two locations |
| `disruptions.sh` | Current service disruptions |

**API:** HAFAS (Hacon Fahrplan-Auskunfts-System)  
**Endpoint:** `https://vao.demo.hafas.de/gate`

---

## 1. Search Stations/Stops

Find station IDs by name:

```bash
./search.sh "Stephansplatz"
./search.sh "Wien Hauptbahnhof"
./search.sh "Linz"
./search.sh "Salzburg Hbf"
```

Returns station names, IDs (extId), and coordinates.

**Response fields:**
- `name`: Station name
- `extId`: Station ID for use in other queries
- `type`: S (Station), A (Address), P (POI)
- `coordinates`: WGS84 coordinates (lon/lat in 1e-6 format)

---

## 2. Real-Time Departures

Get next departures from a station:

```bash
./departures.sh <station-id> [count]

# Examples:
./departures.sh 490132000        # Wien Stephansplatz, 10 departures
./departures.sh 490132000 20     # Wien Stephansplatz, 20 departures
./departures.sh 490060200        # Wien Hauptbahnhof
./departures.sh 444130000        # Linz Hbf
./departures.sh 455000100        # Salzburg Hbf
```

**Response fields:**
- `line`: Line name (U1, S1, RJ, etc.)
- `direction`: Final destination
- `departure`: Scheduled departure time
- `delay`: Delay in minutes (if any)
- `platform`: Platform/track number

---

## 3. Route Planning

Plan a trip between two stations:

```bash
./route.sh <from-id> <to-id> [results]

# Examples:
./route.sh 490132000 490060200        # Stephansplatz → Hauptbahnhof
./route.sh 490132000 444130000 5      # Wien → Linz, 5 results
./route.sh "Graz Hbf" "Wien Hbf"      # Search by name (slower)
```

**Response fields:**
- `departure`: Departure time
- `arrival`: Arrival time
- `duration`: Trip duration
- `changes`: Number of transfers
- `legs`: Array of trip segments with line info

---

## 4. Disruptions

Check current service disruptions:

```bash
./disruptions.sh [category]

# Examples:
./disruptions.sh            # All disruptions
./disruptions.sh TRAIN      # Train disruptions only
./disruptions.sh BUS        # Bus disruptions only
```

---

## Common Station IDs

| Station | ID |
|---------|-----|
| Wien Stephansplatz | 490132000 |
| Wien Hauptbahnhof | 490134900 |
| Wien Westbahnhof | 490024300 |
| Wien Praterstern | 490056100 |
| Wien Karlsplatz | 490024600 |
| Wien Schwedenplatz | 490119500 |
| Linz Hbf | 444116400 |
| Salzburg Hbf | 455000200 |
| Graz Hbf | 460086000 |
| Innsbruck Hbf | 481070100 |
| Klagenfurt Hbf | 492019500 |
| St. Pölten Hbf | 431543300 |
| Wiener Neustadt Hbf | 430521000 |
| Krems a.d. Donau | 431046400 |

**Tip:** Always use `./search.sh` to find the correct station ID.

---

## Transport Types

| Code | Type |
|------|------|
| ICE/RJ/RJX | High-speed trains |
| IC/EC | InterCity/EuroCity |
| REX/R | Regional Express/Regional |
| S | S-Bahn (suburban rail) |
| U | U-Bahn (Vienna metro) |
| STR | Tram/Straßenbahn |
| BUS | Bus |
| AST | Demand-responsive transport |

---

## API Details (for advanced usage)

The scripts use the HAFAS JSON API. For custom queries:

```bash
curl -s -X POST "https://vao.demo.hafas.de/gate" \
  -H "Content-Type: application/json" \
  -d '{
    "svcReqL": [{
      "req": { ... },
      "meth": "METHOD_NAME",
      "id": "1|1|"
    }],
    "client": {"id": "VAO", "v": "1", "type": "AND", "name": "nextgen"},
    "ver": "1.73",
    "lang": "de",
    "auth": {"aid": "nextgen", "type": "AID"}
  }'
```

**Available methods:**
- `LocMatch` - Location/station search
- `StationBoard` - Departures/arrivals
- `TripSearch` - Route planning
- `HimSearch` - Disruptions/service messages
- `JourneyDetails` - Details of a specific journey

---

## Tips

1. **Find station IDs first**: Always use `search.sh` to find the correct station ID before querying departures or routes.

2. **Station vs Stop**: Major stations have multiple platforms - the main station ID covers all platforms.

3. **Real-time data**: Departures include real-time delays when available.

4. **Austria-wide**: This API covers all Austrian public transport, not just Vienna.

5. **Cross-border**: Some routes extend to neighboring countries (Germany, Czech Republic, etc.).
