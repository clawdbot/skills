# Overseerr Request Media Skill

## Purpose
Request a movie or TV show using the user's Overseerr instance. Overseerr forwards the request to Sonarr/Radarr.

## Requirements
Environment variables:
- OVERSEERR_URL (example: https://overseerr.yourdomain.com)
- OVERSEERR_API_KEY

Authentication header:
- X-Api-Key: $OVERSEERR_API_KEY

Overseerr can detect if media is already available or already requested based on your configured Plex + Sonarr/Radarr connections.

## What this skill handles
User examples:
- "Request Interstellar"
- "Add Interstellar to overseerr"
- "Request Reacher season 2"
- "Request The Office seasons 2-4"

## Workflow (ALWAYS FOLLOW)

### 1) Parse the user's request
Extract:
- Title
- Optional type hint: movie or tv
- Optional season request:
  - "season 2"
  - "seasons 1-3"
  - "season 1 and 4"

### 2) Search Overseerr
GET:
$OVERSEERR_URL/api/v1/search?query=<urlencoded title>

Example:
curl -s -H "X-Api-Key: $OVERSEERR_API_KEY" \
"$OVERSEERR_URL/api/v1/search?query=interstellar"

### 3) Clarify if the result is ambiguous (movie vs show with same name)
If the search results include BOTH:
- a movie match AND
- a tv match
with the same (or extremely similar) title,

THEN ask the user to choose before requesting.

Show 2-4 options max, like:
- Movie: Title (Year)
- TV: Title (Year)

If the user provided an obvious hint like "movie", "show", "tv", "season 2", then pick the matching type automatically.

### 4) Pick the best match
Rules:
- Prefer exact title match
- Prefer the highest popularity match when multiple results exist
- Respect the user's type hint if provided (movie vs tv)

### 5) Check if it already exists (available or already requested)
Before creating a request:
- Inspect the selected result for availability/request status info returned by Overseerr (library/availability/request indicators).
- If it indicates the media is already available in the library:
  - Do NOT request it
  - Reply: "Already available ✅"
- If it indicates the media is already requested (pending/processing/approved/requested):
  - Do NOT request it again
  - Reply: "Already requested ✅"

If the API response does NOT clearly indicate status:
- Proceed with creating the request
- If the POST fails due to duplicate/existing request, reply "Already requested ✅"

### 6) Create the request
POST:
$OVERSEERR_URL/api/v1/request

Movie JSON:
{
  "mediaType": "movie",
  "mediaId": <tmdbId>
}

TV JSON (full series):
{
  "mediaType": "tv",
  "mediaId": <tmdbId>
}

TV JSON (specific seasons):
{
  "mediaType": "tv",
  "mediaId": <tmdbId>,
  "seasons": [2,3]
}

Examples:

Movie:
curl -s -X POST \
-H "X-Api-Key: $OVERSEERR_API_KEY" \
-H "Content-Type: application/json" \
"$OVERSEERR_URL/api/v1/request" \
-d '{"mediaType":"movie","mediaId":157336}'

TV (full):
curl -s -X POST \
-H "X-Api-Key: $OVERSEERR_API_KEY" \
-H "Content-Type: application/json" \
"$OVERSEERR_URL/api/v1/request" \
-d '{"mediaType":"tv","mediaId":71912}'

TV (season 2):
curl -s -X POST \
-H "X-Api-Key: $OVERSEERR_API_KEY" \
-H "Content-Type: application/json" \
"$OVERSEERR_URL/api/v1/request" \
"$OVERSEERR_URL/api/v1/request" \
-d '{"mediaType":"tv","mediaId":71912,"seasons":[2]}'

### 7) Respond cleanly
- Confirm what was requested
- If TV request was partial, list seasons
- If already requested/available, say so
- If no results, ask for alternate spelling or more context

## Output style
Short confirmations:
- "✅ Requested: Interstellar (2014)"
- "✅ Requested: Reacher (Season 2)"
- "Already requested ✅"
- "Already available ✅"

## Error handling
- If search returns 0 results:
  - Ask for alternate title or year
- If multiple equally good matches remain:
  - Ask the user to pick from 2-4 options