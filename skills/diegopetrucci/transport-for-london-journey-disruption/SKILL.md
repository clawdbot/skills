---
name: tfl-journey-disruption
description: Plan TfL journeys from start/end/time, resolve locations (prefer postcodes), and warn about disruptions; suggest alternatives when disrupted.
---

# TfL Journey Planner + Disruption Checks

Use this skill when the user wants a TfL journey plan and needs disruption awareness.

Reference: https://tfl.gov.uk/info-for/open-data-users/api-documentation

## Script helper

Use `scripts/tfl_journey_disruptions.py` for a quick journey + disruption check.

Examples:

```bash
python3 scripts/tfl_journey_disruptions.py \"940GZZLUSTD\" \"W1F 9LD\" --depart-at 0900
python3 scripts/tfl_journey_disruptions.py --from \"Stratford\" --to \"W1F 9LD\" --arrive-by 1800
```

Notes:
- If the API returns disambiguation options, pick one and retry with its `parameterValue`.
- If you have TfL API keys, set `TFL_APP_ID` and `TFL_APP_KEY` in the environment.

## Inputs to collect

- From: postcode, stop/station name, place name, or lat,lon
- To: postcode, stop/station name, place name, or lat,lon
- Time + intent: depart at or arrive by (and date if not explicit)
- Optional: mode or accessibility constraints if the user mentions them

If any of these are missing or ambiguous, ask the user for clarification.

## Resolve locations

Prefer postcodes when available. Otherwise, resolve place names and stations:

- If input looks like a UK postcode, use it directly as `{from}` or `{to}`.
- If input is lat,lon, use as-is.
- If input is a stop or station name, try `StopPoint/Search/{query}` and choose a hub or the relevant NaPTAN ID.
- If the search or journey result returns disambiguation, show the top options (common name + parameterValue) and ask the user to pick.
- When unsure, ask a clarifying question rather than guessing.

## Plan journeys

Call:

`/Journey/JourneyResults/{from}/to/{to}?date=YYYYMMDD&time=HHMM&timeIs=Depart|Arrive`

Guidelines:
- If the user says "arrive by" use `timeIs=Arrive`; otherwise default to `Depart`.
- If the date is not provided, ask. If the user implies "now", you can omit date/time.

## Extract candidate routes

From the response, take the first 1-3 journeys. For each, capture:
- Duration and arrival time
- Public transport legs (mode, line name, direction)
- Line IDs for disruption checks

Line IDs usually appear in `leg.routeOptions[].lineIdentifier.id` or `leg.line.id`. Ignore walking legs.

## Disruption checks

For each journey, collect unique line IDs and call:

`/Line/{ids}/Status`

Treat a route as disrupted if any line status is not "Good Service" or includes a reason. Summarize the severity and reason.

Optionally, check station-specific issues with `/StopPoint/{id}/Disruption` when relevant.

## Response strategy

- If the top route has no disruptions, recommend it and say no active disruptions were found.
- If the top route is disrupted, warn first, then propose 1-2 alternative routes from other journeys.
- If all routes are disrupted, still recommend the best option but list the disruption warnings and alternatives.
- If the journey is for a future time (later today or another day), note that disruption statuses are current and may change by the travel time (for example: "Minor Delays now; this may change by morning").
- Always invite the user to confirm a route or provide clarifications.
