#!/usr/bin/env bash
# Streaming Buddy Handler v2.0
# Personal streaming assistant with learning preferences
# Usage: handler.sh <command> [args...] <workspace>

set -euo pipefail

# Check dependencies
command -v jq >/dev/null 2>&1 || { echo '{"status":"error","message":"jq required"}'; exit 1; }
command -v curl >/dev/null 2>&1 || { echo '{"status":"error","message":"curl required"}'; exit 1; }

CMD="${1:-status}"
shift || true

# Get workspace (always last argument)
WORKSPACE="${!#:-$(pwd)}"
DATA_DIR="$WORKSPACE/memory/streaming-buddy"
CACHE_DIR="$DATA_DIR/cache"

# Ensure directories exist
mkdir -p "$DATA_DIR" "$CACHE_DIR"

# File paths
PROFILE="$DATA_DIR/profile.json"
CONFIG="$DATA_DIR/config.json"
SERVICES="$DATA_DIR/services.json"
WATCHING="$DATA_DIR/watching.json"
WATCHLIST="$DATA_DIR/watchlist.json"
HISTORY="$DATA_DIR/history.json"
PREFERENCES="$DATA_DIR/preferences.json"

# Initialize files if they don't exist
init_file() {
    local file="$1"
    local default="$2"
    [[ -f "$file" ]] || echo "$default" > "$file"
}

init_file "$CONFIG" '{"tmdbApiKey":"","region":"DE","language":"de-DE"}'
init_file "$SERVICES" '{"active":[],"occasional":[],"region":"DE"}'
init_file "$WATCHING" '{"items":[]}'
init_file "$WATCHLIST" '{"items":[]}'
init_file "$HISTORY" '{"items":[]}'
init_file "$PREFERENCES" '{
  "genres": {"liked": {}, "disliked": {}},
  "themes": {"liked": [], "disliked": []},
  "actors": {"liked": [], "disliked": []},
  "directors": {"liked": [], "disliked": []},
  "moods": {
    "exciting": ["Action", "Thriller", "Science Fiction", "Adventure"],
    "relaxing": ["Comedy", "Animation", "Family", "Documentary"],
    "thoughtful": ["Drama", "Mystery", "History"],
    "scary": ["Horror", "Thriller"],
    "romantic": ["Romance", "Drama"],
    "funny": ["Comedy", "Animation"]
  },
  "avoid": [],
  "updatedAt": null
}'

# Read config
TMDB_API_KEY=$(jq -r '.tmdbApiKey // empty' "$CONFIG" 2>/dev/null || echo "")
LANG=$(jq -r '.language // "de-DE"' "$CONFIG" 2>/dev/null | cut -c1-2)
[[ "$LANG" != "de" && "$LANG" != "en" ]] && LANG="de"
REGION=$(jq -r '.region // "DE"' "$CONFIG" 2>/dev/null)

TMDB_BASE="https://api.themoviedb.org/3"

# ============================================
# TMDB API Functions
# ============================================

tmdb_search() {
    local query="$1"
    local type="${2:-multi}"
    
    [[ -z "$TMDB_API_KEY" ]] && { echo '{"status":"error","message":"TMDB_API_KEY not configured"}'; return 1; }
    
    local encoded_query
    encoded_query=$(echo -n "$query" | jq -sRr @uri)
    
    local cache_key
    cache_key=$(echo -n "${type}-${query}" | md5sum | cut -c1-12)
    local cache_file="$CACHE_DIR/search-${cache_key}.json"
    local cache_age=3600
    
    if [[ -f "$cache_file" ]]; then
        local file_age=$(($(date +%s) - $(stat -c %Y "$cache_file" 2>/dev/null || echo 0)))
        if [[ $file_age -lt $cache_age ]]; then
            cat "$cache_file"
            return 0
        fi
    fi
    
    local url="${TMDB_BASE}/search/${type}?api_key=${TMDB_API_KEY}&query=${encoded_query}&language=de-DE&region=${REGION}"
    local result
    result=$(curl -s --max-time 10 "$url" 2>/dev/null || echo '{"results":[]}')
    
    echo "$result" > "$cache_file"
    echo "$result"
}

tmdb_details() {
    local id="$1"
    local type="$2"
    
    [[ -z "$TMDB_API_KEY" ]] && { echo '{"status":"error","message":"TMDB_API_KEY not configured"}'; return 1; }
    
    local cache_file="$CACHE_DIR/details-${type}-${id}.json"
    local cache_age=86400
    
    if [[ -f "$cache_file" ]]; then
        local file_age=$(($(date +%s) - $(stat -c %Y "$cache_file" 2>/dev/null || echo 0)))
        if [[ $file_age -lt $cache_age ]]; then
            cat "$cache_file"
            return 0
        fi
    fi
    
    local url="${TMDB_BASE}/${type}/${id}?api_key=${TMDB_API_KEY}&language=de-DE&append_to_response=credits,keywords,watch/providers"
    local result
    result=$(curl -s --max-time 10 "$url" 2>/dev/null || echo '{}')
    
    echo "$result" > "$cache_file"
    echo "$result"
}

tmdb_discover() {
    local type="$1"
    local providers="${2:-}"
    local genres="${3:-}"
    local sort="${4:-vote_average.desc}"
    
    [[ -z "$TMDB_API_KEY" ]] && { echo '{"results":[]}'; return 1; }
    
    local cache_key
    cache_key=$(echo -n "${type}-${providers}-${genres}-${sort}" | md5sum | cut -c1-12)
    local cache_file="$CACHE_DIR/discover-${cache_key}.json"
    local cache_age=3600
    
    if [[ -f "$cache_file" ]]; then
        local file_age=$(($(date +%s) - $(stat -c %Y "$cache_file" 2>/dev/null || echo 0)))
        if [[ $file_age -lt $cache_age ]]; then
            cat "$cache_file"
            return 0
        fi
    fi
    
    local url="${TMDB_BASE}/discover/${type}?api_key=${TMDB_API_KEY}&language=de-DE&watch_region=${REGION}&sort_by=${sort}&vote_count.gte=50"
    [[ -n "$providers" ]] && url="${url}&with_watch_providers=${providers// /%20}"
    [[ -n "$genres" ]] && url="${url}&with_genres=${genres// /%20}"
    
    local result
    result=$(curl -s --max-time 10 "$url" 2>/dev/null || echo '{"results":[]}')
    
    echo "$result" > "$cache_file"
    echo "$result"
}

# ============================================
# Helper Functions
# ============================================

get_provider_id() {
    case "${1,,}" in
        apple-tv-plus|appletv|apple|"apple tv+"|"apple tv") echo "350" ;;
        amazon-prime|prime|amazon|"amazon prime") echo "9" ;;
        netflix) echo "8" ;;
        disney-plus|disney|"disney+") echo "337" ;;
        youtube-premium|youtube) echo "188" ;;
        wow|sky) echo "30" ;;
        paramount-plus|paramount|"paramount+") echo "531" ;;
        crunchyroll) echo "283" ;;
        joyn) echo "304" ;;
        rtl|"rtl+") echo "298" ;;
        magenta|magentatv) echo "178" ;;
        mubi) echo "11" ;;
        *) echo "" ;;
    esac
}

get_provider_ids_for_user() {
    local ids=""
    while IFS= read -r svc; do
        local pid
        pid=$(get_provider_id "$svc")
        [[ -n "$pid" ]] && ids="${ids}${ids:+|}${pid}"
    done < <(jq -r '.active[]' "$SERVICES" 2>/dev/null)
    echo "$ids"
}

get_genre_id() {
    local genre="${1,,}"
    case "$genre" in
        action) echo "28" ;;
        adventure|abenteuer) echo "12" ;;
        animation) echo "16" ;;
        comedy|komödie) echo "35" ;;
        crime|krimi) echo "80" ;;
        documentary|dokumentation|doku) echo "99" ;;
        drama) echo "18" ;;
        family|familie) echo "10751" ;;
        fantasy) echo "14" ;;
        history|geschichte) echo "36" ;;
        horror) echo "27" ;;
        music|musik) echo "10402" ;;
        mystery) echo "9648" ;;
        romance|romantik|romanze) echo "10749" ;;
        "science fiction"|sci-fi|scifi) echo "878" ;;
        thriller) echo "53" ;;
        war|krieg) echo "10752" ;;
        western) echo "37" ;;
        *) echo "" ;;
    esac
}

# Calculate match score for a title based on user preferences
calculate_match_score() {
    local genres="$1"
    local keywords="$2"
    local cast="$3"
    local director="$4"
    
    local score=50  # Base score
    local reasons=""
    
    # Genre matching
    while IFS= read -r genre; do
        [[ -z "$genre" ]] && continue
        local liked_weight
        liked_weight=$(jq -r --arg g "$genre" '.genres.liked[$g] // 0' "$PREFERENCES")
        local disliked_weight
        disliked_weight=$(jq -r --arg g "$genre" '.genres.disliked[$g] // 0' "$PREFERENCES")
        
        if [[ "$liked_weight" -gt 0 ]]; then
            score=$((score + liked_weight * 5))
            reasons="${reasons}+Genre:${genre} "
        fi
        if [[ "$disliked_weight" -gt 0 ]]; then
            score=$((score - disliked_weight * 5))
            reasons="${reasons}-Genre:${genre} "
        fi
    done <<< "$genres"
    
    # Theme/keyword matching
    local liked_themes
    liked_themes=$(jq -r '.themes.liked[]' "$PREFERENCES" 2>/dev/null | tr '\n' '|')
    if [[ -n "$liked_themes" && -n "$keywords" ]]; then
        if echo "$keywords" | grep -qiE "$liked_themes"; then
            score=$((score + 15))
            reasons="${reasons}+Theme "
        fi
    fi
    
    # Actor matching
    local liked_actors
    liked_actors=$(jq -r '.actors.liked[]' "$PREFERENCES" 2>/dev/null | tr '\n' '|')
    if [[ -n "$liked_actors" && -n "$cast" ]]; then
        if echo "$cast" | grep -qiE "$liked_actors"; then
            score=$((score + 10))
            reasons="${reasons}+Actor "
        fi
    fi
    
    # Director matching
    local liked_directors
    liked_directors=$(jq -r '.directors.liked[]' "$PREFERENCES" 2>/dev/null | tr '\n' '|')
    if [[ -n "$liked_directors" && -n "$director" ]]; then
        if echo "$director" | grep -qiE "$liked_directors"; then
            score=$((score + 10))
            reasons="${reasons}+Director "
        fi
    fi
    
    # Cap score at 100
    [[ $score -gt 100 ]] && score=100
    [[ $score -lt 0 ]] && score=0
    
    echo "{\"score\":$score,\"reasons\":\"${reasons}\"}"
}

# Update preferences based on a liked/disliked title
update_preferences() {
    local tmdb_id="$1"
    local type="$2"
    local action="$3"  # like or dislike
    local weight="${4:-1}"
    
    # Get title details
    local details
    details=$(tmdb_details "$tmdb_id" "$type")
    
    local title
    title=$(echo "$details" | jq -r '.title // .name // "Unknown"')
    
    # Extract genres
    local genres
    genres=$(echo "$details" | jq -r '[.genres[].name] | join(",")')
    
    # Extract keywords/themes
    local keywords
    keywords=$(echo "$details" | jq -r '[.keywords.keywords[]?.name // .keywords.results[]?.name] | .[0:5] | join(",")')
    
    # Extract top cast
    local cast
    cast=$(echo "$details" | jq -r '[.credits.cast[0:3][]?.name] | join(",")')
    
    # Extract director
    local director
    director=$(echo "$details" | jq -r '[.credits.crew[] | select(.job == "Director")][:1][].name // empty')
    
    # Update preferences based on action
    if [[ "$action" == "like" ]]; then
        # Update genre weights
        IFS=',' read -ra genre_arr <<< "$genres"
        for genre in "${genre_arr[@]}"; do
            [[ -z "$genre" ]] && continue
            jq --arg g "$genre" --argjson w "$weight" \
                '.genres.liked[$g] = ((.genres.liked[$g] // 0) + $w)' \
                "$PREFERENCES" > "$PREFERENCES.tmp" && mv "$PREFERENCES.tmp" "$PREFERENCES"
        done
        
        # Add themes
        IFS=',' read -ra kw_arr <<< "$keywords"
        for kw in "${kw_arr[@]}"; do
            [[ -z "$kw" ]] && continue
            jq --arg t "$kw" \
                'if (.themes.liked | index($t)) then . else .themes.liked += [$t] end' \
                "$PREFERENCES" > "$PREFERENCES.tmp" && mv "$PREFERENCES.tmp" "$PREFERENCES"
        done
        
        # Add actors
        IFS=',' read -ra cast_arr <<< "$cast"
        for actor in "${cast_arr[@]}"; do
            [[ -z "$actor" ]] && continue
            jq --arg a "$actor" \
                'if (.actors.liked | index($a)) then . else .actors.liked += [$a] end' \
                "$PREFERENCES" > "$PREFERENCES.tmp" && mv "$PREFERENCES.tmp" "$PREFERENCES"
        done
        
        # Add director
        if [[ -n "$director" ]]; then
            jq --arg d "$director" \
                'if (.directors.liked | index($d)) then . else .directors.liked += [$d] end' \
                "$PREFERENCES" > "$PREFERENCES.tmp" && mv "$PREFERENCES.tmp" "$PREFERENCES"
        fi
    else
        # Dislike - update genre weights negatively
        IFS=',' read -ra genre_arr <<< "$genres"
        for genre in "${genre_arr[@]}"; do
            [[ -z "$genre" ]] && continue
            jq --arg g "$genre" --argjson w "$weight" \
                '.genres.disliked[$g] = ((.genres.disliked[$g] // 0) + $w)' \
                "$PREFERENCES" > "$PREFERENCES.tmp" && mv "$PREFERENCES.tmp" "$PREFERENCES"
        done
    fi
    
    # Update timestamp
    jq --arg ts "$(date -Iseconds)" '.updatedAt = $ts' "$PREFERENCES" > "$PREFERENCES.tmp" && mv "$PREFERENCES.tmp" "$PREFERENCES"
    
    echo "{\"status\":\"ok\",\"title\":\"$title\",\"action\":\"$action\",\"genres\":\"$genres\",\"themes\":\"$keywords\"}"
}

# ============================================
# Commands
# ============================================

case "$CMD" in
    # ----------------------------------------
    # STATUS
    # ----------------------------------------
    status)
        if [[ ! -f "$PROFILE" ]]; then
            if [[ "$LANG" == "de" ]]; then
                echo '{"status":"ok","setup":false,"message":"Nicht konfiguriert. Starte mit /stream setup."}'
            else
                echo '{"status":"ok","setup":false,"message":"Not configured. Run /stream setup first."}'
            fi
        else
            active_count=$(jq -r '.active | length' "$SERVICES")
            active_list=$(jq -r '.active | join(", ")' "$SERVICES")
            watching_count=$(jq -r '.items | length' "$WATCHING")
            watchlist_count=$(jq -r '.items | length' "$WATCHLIST")
            history_count=$(jq -r '.items | length' "$HISTORY")
            region=$(jq -r '.region // "DE"' "$SERVICES")
            
            current=""
            current_id=""
            if [[ $watching_count -gt 0 ]]; then
                current=$(jq -r '.items[0] | "\(.title) (S\(.season // 1)E\(.episode // 1))"' "$WATCHING")
                current_id=$(jq -r '.items[0].tmdbId' "$WATCHING")
            fi
            
            # Get preference summary
            top_genres=$(jq -r '[.genres.liked | to_entries | sort_by(-.value) | .[0:3][] | .key] | join(", ")' "$PREFERENCES" 2>/dev/null || echo "")
            
            jq -n \
                --argjson activeCount "$active_count" \
                --arg activeList "$active_list" \
                --argjson watchingCount "$watching_count" \
                --argjson watchlistCount "$watchlist_count" \
                --argjson historyCount "$history_count" \
                --arg current "$current" \
                --arg currentId "$current_id" \
                --arg region "$region" \
                --arg lang "$LANG" \
                --arg topGenres "$top_genres" \
                '{
                    status: "ok",
                    setup: true,
                    language: $lang,
                    region: $region,
                    services: {
                        count: $activeCount,
                        list: ($activeList | split(", "))
                    },
                    currentlyWatching: {
                        count: $watchingCount,
                        current: (if $current != "" then $current else null end),
                        currentId: (if $currentId != "" then ($currentId | tonumber) else null end)
                    },
                    watchlistCount: $watchlistCount,
                    historyCount: $historyCount,
                    preferences: {
                        topGenres: (if $topGenres != "" then ($topGenres | split(", ")) else [] end)
                    },
                    commands: (if $lang == "de" then {
                        "/stream": "Status anzeigen",
                        "/stream search <titel>": "Film/Serie suchen",
                        "/stream info <id>": "Details & Verfügbarkeit",
                        "/stream watch <id>": "Anfangen zu schauen",
                        "/stream progress S01E05": "Fortschritt updaten",
                        "/stream done [1-5]": "Fertig + Bewertung",
                        "/stream like [id]": "Gefällt mir → lernt Präferenzen",
                        "/stream dislike [id]": "Gefällt nicht → lernt Präferenzen",
                        "/stream suggest [dienst] [movie|tv]": "Personalisierte Empfehlungen",
                        "/stream mood <stimmung>": "Nach Stimmung suchen (exciting, relaxing, scary...)",
                        "/stream surprise": "Überrasch mich!",
                        "/stream why <id>": "Warum passt das zu mir?",
                        "/stream watchlist": "Merkliste anzeigen",
                        "/stream watchlist add <id>": "Zur Merkliste hinzufügen",
                        "/stream history": "Verlauf anzeigen",
                        "/stream profile": "Mein Geschmacksprofil",
                        "/stream services": "Streaming-Dienste verwalten",
                        "/stream services add <name>": "Dienst hinzufügen",
                        "/stream services remove <name>": "Dienst entfernen"
                    } else {
                        "/stream": "Show status",
                        "/stream search <title>": "Search movie/TV show",
                        "/stream info <id>": "Details & availability",
                        "/stream watch <id>": "Start watching",
                        "/stream progress S01E05": "Update progress",
                        "/stream done [1-5]": "Mark done + rate",
                        "/stream like [id]": "Like → learns preferences",
                        "/stream dislike [id]": "Dislike → learns preferences",
                        "/stream suggest [service] [movie|tv]": "Personalized recommendations",
                        "/stream mood <mood>": "Search by mood (exciting, relaxing, scary...)",
                        "/stream surprise": "Surprise me!",
                        "/stream why <id>": "Why does this match me?",
                        "/stream watchlist": "Show watchlist",
                        "/stream watchlist add <id>": "Add to watchlist",
                        "/stream history": "Show watch history",
                        "/stream profile": "My taste profile",
                        "/stream services": "Manage streaming services",
                        "/stream services add <name>": "Add service",
                        "/stream services remove <name>": "Remove service"
                    } end)
                }'
        fi
        ;;
        
    # ----------------------------------------
    # SETUP
    # ----------------------------------------
    setup)
        if [[ -f "$PROFILE" ]]; then
            echo '{"status":"ok","setup":true,"message":"Already configured. Use /stream services to modify."}'
        else
            echo '{"status":"ok","setup":false,"action":"start_setup","availableServices":["netflix","amazon-prime","disney-plus","apple-tv-plus","youtube-premium","wow","paramount-plus","crunchyroll","joyn","rtl","magenta","mubi"]}'
        fi
        ;;
        
    setup-complete)
        services_list="${1:-}"
        
        echo '{"createdAt":"'"$(date -Iseconds)"'","version":"2.0"}' > "$PROFILE"
        
        IFS=',' read -ra svc_array <<< "$services_list"
        jq -n --argjson svcs "$(printf '%s\n' "${svc_array[@]}" | jq -R . | jq -s .)" \
            '{active: $svcs, occasional: [], region: "DE"}' > "$SERVICES"
        
        echo '{"status":"ok","message":"Setup complete","services":'"$(jq -c '.active' "$SERVICES")"'}'
        ;;
        
    # ----------------------------------------
    # SERVICES
    # ----------------------------------------
    services)
        subcmd="${1:-list}"
        shift || true
        
        case "$subcmd" in
            list)
                jq '{status:"ok", services:.}' "$SERVICES"
                ;;
            add)
                service="${1:-}"
                [[ -z "$service" ]] && { echo '{"status":"error","message":"Service name required"}'; exit 1; }
                jq --arg svc "$service" '.active += [$svc] | .active |= unique' "$SERVICES" > "$SERVICES.tmp"
                mv "$SERVICES.tmp" "$SERVICES"
                echo '{"status":"ok","message":"Service added","service":"'"$service"'"}'
                ;;
            remove)
                service="${1:-}"
                jq --arg svc "$service" '.active -= [$svc]' "$SERVICES" > "$SERVICES.tmp"
                mv "$SERVICES.tmp" "$SERVICES"
                echo '{"status":"ok","message":"Service removed","service":"'"$service"'"}'
                ;;
            *)
                jq '{status:"ok", services:.}' "$SERVICES"
                ;;
        esac
        ;;
        
    # ----------------------------------------
    # SEARCH
    # ----------------------------------------
    search)
        query="${1:-}"
        [[ -z "$query" ]] && { echo '{"status":"error","message":"Search query required"}'; exit 1; }
        
        result=$(tmdb_search "$query" "multi")
        
        echo "$result" | jq '{
            status: "ok",
            query: "'"$query"'",
            results: [.results[:10][] | select(.media_type == "movie" or .media_type == "tv") | {
                id: .id,
                title: (.title // .name),
                type: .media_type,
                year: ((.release_date // .first_air_date // "")[:4]),
                rating: ((.vote_average // 0) | . * 10 | round / 10),
                overview: (.overview[:200] + (if (.overview | length) > 200 then "..." else "" end)),
                poster: (if .poster_path then "https://image.tmdb.org/t/p/w200" + .poster_path else null end)
            }]
        }'
        ;;
        
    # ----------------------------------------
    # INFO
    # ----------------------------------------
    info)
        tmdb_id="${1:-}"
        type="${2:-tv}"
        
        [[ -z "$tmdb_id" ]] && { echo '{"status":"error","message":"TMDB ID required"}'; exit 1; }
        
        details=$(tmdb_details "$tmdb_id" "$type")
        
        # Get availability
        availability=$(echo "$details" | jq --arg region "$REGION" '
            .["watch/providers"].results[$region] // {} |
            {
                flatrate: [.flatrate[]?.provider_name] | unique,
                rent: [.rent[]?.provider_name] | unique,
                buy: [.buy[]?.provider_name] | unique
            }
        ')
        
        # Get user services for matching
        user_services=$(jq -r '.active | map(ascii_downcase) | join("|")' "$SERVICES")
        
        # Extract data for match calculation
        genres=$(echo "$details" | jq -r '[.genres[].name] | join("\n")')
        keywords=$(echo "$details" | jq -r '[.keywords.keywords[]?.name // .keywords.results[]?.name] | join(",")')
        cast=$(echo "$details" | jq -r '[.credits.cast[0:5][]?.name] | join(",")')
        director=$(echo "$details" | jq -r '[.credits.crew[] | select(.job == "Director")][:1][].name // empty')
        
        # Calculate match score
        match_result=$(calculate_match_score "$genres" "$keywords" "$cast" "$director")
        match_score=$(echo "$match_result" | jq -r '.score')
        
        echo "$details" | jq --argjson avail "$availability" --argjson match "$match_score" --arg cast "$cast" --arg director "$director" --arg keywords "$keywords" '{
            status: "ok",
            id: .id,
            title: (.title // .name),
            originalTitle: (.original_title // .original_name),
            type: (if .title then "movie" else "tv" end),
            year: ((.release_date // .first_air_date // "")[:4]),
            rating: .vote_average,
            voteCount: .vote_count,
            overview: .overview,
            genres: [.genres[].name],
            runtime: (.runtime // .episode_run_time[0] // null),
            seasons: (.number_of_seasons // null),
            episodes: (.number_of_episodes // null),
            status: .status,
            poster: (if .poster_path then "https://image.tmdb.org/t/p/w500" + .poster_path else null end),
            backdrop: (if .backdrop_path then "https://image.tmdb.org/t/p/w1280" + .backdrop_path else null end),
            cast: ($cast | split(",") | .[0:5]),
            director: (if $director != "" then $director else null end),
            themes: ($keywords | split(",") | .[0:5]),
            availability: $avail,
            matchScore: $match
        }'
        ;;
        
    # ----------------------------------------
    # WATCH (start tracking)
    # ----------------------------------------
    watch)
        tmdb_id="${1:-}"
        type="${2:-tv}"
        
        [[ -z "$tmdb_id" ]] && { echo '{"status":"error","message":"TMDB ID required"}'; exit 1; }
        
        details=$(tmdb_details "$tmdb_id" "$type")
        title=$(echo "$details" | jq -r '.title // .name')
        seasons=$(echo "$details" | jq -r '.number_of_seasons // 1')
        episodes=$(echo "$details" | jq -r '.number_of_episodes // 1')
        genres=$(echo "$details" | jq -c '[.genres[].name]')
        
        # Get service it's available on
        service=$(echo "$details" | jq -r --arg region "$REGION" '.["watch/providers"].results[$region].flatrate[0].provider_name // "Unknown"')
        
        entry=$(jq -n \
            --arg id "$tmdb_id" \
            --arg title "$title" \
            --arg type "$type" \
            --argjson seasons "$seasons" \
            --argjson episodes "$episodes" \
            --argjson genres "$genres" \
            --arg service "$service" \
            '{
                tmdbId: ($id | tonumber),
                title: $title,
                type: $type,
                season: 1,
                episode: 1,
                totalSeasons: $seasons,
                totalEpisodes: $episodes,
                genres: $genres,
                service: $service,
                startedAt: (now | strftime("%Y-%m-%d")),
                updatedAt: (now | strftime("%Y-%m-%d"))
            }')
        
        # Add to front of watching list (remove if already exists)
        jq --argjson entry "$entry" '.items = [$entry] + [.items[] | select(.tmdbId != ($entry.tmdbId))]' "$WATCHING" > "$WATCHING.tmp"
        mv "$WATCHING.tmp" "$WATCHING"
        
        echo "$entry" | jq '{status:"ok", message:"Started watching", item:.}'
        ;;
        
    # ----------------------------------------
    # PROGRESS
    # ----------------------------------------
    progress)
        progress="${1:-}"
        
        if [[ "$progress" =~ ^[Ss]([0-9]+)[Ee]([0-9]+)$ ]]; then
            season="${BASH_REMATCH[1]}"
            episode="${BASH_REMATCH[2]}"
        else
            echo '{"status":"error","message":"Invalid format. Use S01E05"}'
            exit 1
        fi
        
        jq --argjson s "$((10#$season))" --argjson e "$((10#$episode))" '
            .items[0].season = $s |
            .items[0].episode = $e |
            .items[0].updatedAt = (now | strftime("%Y-%m-%d"))
        ' "$WATCHING" > "$WATCHING.tmp"
        mv "$WATCHING.tmp" "$WATCHING"
        
        jq '{status:"ok", message:"Progress updated", current:.items[0]}' "$WATCHING"
        ;;
        
    # ----------------------------------------
    # DONE (finish watching + rate)
    # ----------------------------------------
    done)
        rating="${1:-0}"
        notes="${2:-}"
        
        current=$(jq '.items[0]' "$WATCHING")
        
        if [[ "$current" == "null" || -z "$current" ]]; then
            echo '{"status":"error","message":"Nothing currently watching"}'
            exit 1
        fi
        
        # Add to history with rating
        history_entry=$(echo "$current" | jq --argjson rating "$rating" --arg notes "$notes" '
            . + {
                rating: $rating,
                notes: $notes,
                finishedAt: (now | strftime("%Y-%m-%d"))
            }
        ')
        
        jq --argjson entry "$history_entry" '.items = [$entry] + .items' "$HISTORY" > "$HISTORY.tmp"
        mv "$HISTORY.tmp" "$HISTORY"
        
        # Remove from watching
        jq 'del(.items[0])' "$WATCHING" > "$WATCHING.tmp"
        mv "$WATCHING.tmp" "$WATCHING"
        
        # Auto-learn from rating
        tmdb_id=$(echo "$history_entry" | jq -r '.tmdbId')
        type=$(echo "$history_entry" | jq -r '.type')
        
        if [[ "$rating" -ge 4 ]]; then
            update_preferences "$tmdb_id" "$type" "like" "$rating" > /dev/null 2>&1
        elif [[ "$rating" -le 2 && "$rating" -gt 0 ]]; then
            update_preferences "$tmdb_id" "$type" "dislike" "1" > /dev/null 2>&1
        fi
        
        echo "$history_entry" | jq '{status:"ok", message:"Marked as done", learned:(if .rating >= 4 then "liked" elif .rating <= 2 and .rating > 0 then "disliked" else "neutral" end), item:.}'
        ;;
        
    # ----------------------------------------
    # LIKE
    # ----------------------------------------
    like)
        tmdb_id="${1:-}"
        type="${2:-}"
        
        # If no ID provided, use current watching
        if [[ -z "$tmdb_id" || "$tmdb_id" == "$WORKSPACE" ]]; then
            tmdb_id=$(jq -r '.items[0].tmdbId // empty' "$WATCHING")
            type=$(jq -r '.items[0].type // "tv"' "$WATCHING")
        fi
        
        [[ -z "$type" ]] && type="tv"
        [[ -z "$tmdb_id" || "$tmdb_id" == "null" ]] && { echo '{"status":"error","message":"No ID provided and nothing currently watching"}'; exit 1; }
        
        result=$(update_preferences "$tmdb_id" "$type" "like" "2")
        echo "$result"
        ;;
        
    # ----------------------------------------
    # DISLIKE
    # ----------------------------------------
    dislike)
        tmdb_id="${1:-}"
        type="${2:-}"
        
        if [[ -z "$tmdb_id" || "$tmdb_id" == "$WORKSPACE" ]]; then
            tmdb_id=$(jq -r '.items[0].tmdbId // empty' "$WATCHING")
            type=$(jq -r '.items[0].type // "tv"' "$WATCHING")
        fi
        
        [[ -z "$type" ]] && type="tv"
        [[ -z "$tmdb_id" || "$tmdb_id" == "null" ]] && { echo '{"status":"error","message":"No ID provided and nothing currently watching"}'; exit 1; }
        
        result=$(update_preferences "$tmdb_id" "$type" "dislike" "1")
        echo "$result"
        ;;
        
    # ----------------------------------------
    # SUGGEST (personalized recommendations)
    # ----------------------------------------
    suggest)
        filter_service="${1:-}"
        filter_type="${2:-}"
        
        # Build provider filter
        if [[ -n "$filter_service" ]]; then
            provider_ids=$(get_provider_id "$filter_service")
        else
            provider_ids=$(get_provider_ids_for_user)
        fi
        
        # Get preferred genres
        preferred_genres=$(jq -r '[.genres.liked | to_entries | sort_by(-.value) | .[0:3][] | .key] | join(",")' "$PREFERENCES" 2>/dev/null || echo "")
        
        # Convert genre names to IDs
        genre_ids=""
        if [[ -n "$preferred_genres" ]]; then
            IFS=',' read -ra genre_arr <<< "$preferred_genres"
            for g in "${genre_arr[@]}"; do
                gid=$(get_genre_id "$g")
                [[ -n "$gid" ]] && genre_ids="${genre_ids}${genre_ids:+,}${gid}"
            done
        fi
        
        types=("movie" "tv")
        [[ "$filter_type" == "movie" ]] && types=("movie")
        [[ "$filter_type" == "tv" ]] && types=("tv")
        
        all_results="[]"
        
        for type in "${types[@]}"; do
            # Discover with user preferences
            type_results=$(tmdb_discover "$type" "$provider_ids" "$genre_ids" "vote_average.desc")
            
            extracted=$(echo "$type_results" | jq --arg type "$type" '[.results[:8][] | {
                id: .id,
                title: (.title // .name),
                type: $type,
                year: ((.release_date // .first_air_date // "")[:4]),
                rating: ((.vote_average // 0) | . * 10 | round / 10),
                overview: (.overview[:150] + (if (.overview | length) > 150 then "..." else "" end)),
                genres: [.genre_ids[]] 
            }]')
            
            all_results=$(echo "$all_results" "$extracted" | jq -s 'add')
        done
        
        # Filter out already watched
        watched_ids=$(jq -r '[.items[].tmdbId] | join(",")' "$HISTORY" 2>/dev/null || echo "")
        
        # Sort by rating and limit
        final_results=$(echo "$all_results" | jq --arg watched "$watched_ids" '
            [.[] | select(.id as $id | ($watched | split(",") | map(tonumber? // 0) | index($id) | not))] |
            sort_by(-.rating) |
            .[0:10]
        ')
        
        jq -n \
            --argjson results "$final_results" \
            --arg service "$filter_service" \
            --arg type "$filter_type" \
            --arg genres "$preferred_genres" \
            --arg lang "$LANG" \
            '{
                status: "ok",
                filter: {
                    service: (if $service != "" then $service else "all" end),
                    type: (if $type != "" then $type else "all" end)
                },
                basedOn: {
                    preferredGenres: (if $genres != "" then ($genres | split(",")) else [] end)
                },
                language: $lang,
                results: $results
            }'
        ;;
        
    # ----------------------------------------
    # MOOD (mood-based suggestions)
    # ----------------------------------------
    mood)
        mood="${1:-}"
        filter_type="${2:-}"
        
        [[ -z "$mood" ]] && { echo '{"status":"error","message":"Mood required (exciting, relaxing, thoughtful, scary, romantic, funny)"}'; exit 1; }
        
        # Get genres for mood
        mood_genres=$(jq -r --arg m "${mood,,}" '.moods[$m] // [] | join(",")' "$PREFERENCES")
        
        if [[ -z "$mood_genres" || "$mood_genres" == "null" ]]; then
            echo '{"status":"error","message":"Unknown mood. Try: exciting, relaxing, thoughtful, scary, romantic, funny"}'
            exit 1
        fi
        
        # Convert to genre IDs (use | for OR matching)
        genre_ids=""
        IFS=',' read -ra genre_arr <<< "$mood_genres"
        for g in "${genre_arr[@]}"; do
            gid=$(get_genre_id "$g")
            [[ -n "$gid" ]] && genre_ids="${genre_ids}${genre_ids:+|}${gid}"
        done
        
        provider_ids=$(get_provider_ids_for_user)
        
        types=("movie" "tv")
        [[ "$filter_type" == "movie" ]] && types=("movie")
        [[ "$filter_type" == "tv" ]] && types=("tv")
        
        all_results="[]"
        
        for type in "${types[@]}"; do
            type_results=$(tmdb_discover "$type" "$provider_ids" "$genre_ids" "popularity.desc")
            
            extracted=$(echo "$type_results" | jq --arg type "$type" '[.results[:5][] | {
                id: .id,
                title: (.title // .name),
                type: $type,
                year: ((.release_date // .first_air_date // "")[:4]),
                rating: ((.vote_average // 0) | . * 10 | round / 10),
                overview: (.overview[:150] + (if (.overview | length) > 150 then "..." else "" end))
            }]')
            
            all_results=$(echo "$all_results" "$extracted" | jq -s 'add | sort_by(-.rating) | .[0:10]')
        done
        
        jq -n \
            --argjson results "$all_results" \
            --arg mood "$mood" \
            --arg genres "$mood_genres" \
            '{
                status: "ok",
                mood: $mood,
                genres: ($genres | split(",")),
                results: $results
            }'
        ;;
        
    # ----------------------------------------
    # SURPRISE (random recommendation)
    # ----------------------------------------
    surprise)
        provider_ids=$(get_provider_ids_for_user)
        
        # Random type
        types=("movie" "tv")
        type="${types[$RANDOM % 2]}"
        
        # Get popular titles
        results=$(tmdb_discover "$type" "$provider_ids" "" "popularity.desc")
        
        # Pick random from top 20
        count=$(echo "$results" | jq '.results | length')
        [[ "$count" -eq 0 ]] && { echo '{"status":"error","message":"No results found"}'; exit 1; }
        [[ "$count" -gt 20 ]] && count=20
        [[ "$count" -lt 1 ]] && count=1
        random_idx=$((RANDOM % count))
        
        pick=$(echo "$results" | jq --argjson idx "$random_idx" --arg type "$type" '
            if .results[$idx] then
                .results[$idx] | {
                    id: .id,
                    title: (.title // .name),
                    type: $type,
                    year: ((.release_date // .first_air_date // "")[:4]),
                    rating: ((.vote_average // 0) | . * 10 | round / 10),
                    overview: .overview,
                    poster: (if .poster_path then "https://image.tmdb.org/t/p/w500" + .poster_path else null end)
                }
            else
                .results[0] | {
                    id: .id,
                    title: (.title // .name),
                    type: $type,
                    year: ((.release_date // .first_air_date // "")[:4]),
                    rating: ((.vote_average // 0) | . * 10 | round / 10),
                    overview: .overview,
                    poster: (if .poster_path then "https://image.tmdb.org/t/p/w500" + .poster_path else null end)
                }
            end
        ')
        
        jq -n --argjson pick "$pick" '{
            status: "ok",
            message: "Surprise!",
            recommendation: $pick
        }'
        ;;
        
    # ----------------------------------------
    # WHY (explain match)
    # ----------------------------------------
    why)
        tmdb_id="${1:-}"
        type="${2:-tv}"
        
        [[ -z "$tmdb_id" ]] && { echo '{"status":"error","message":"TMDB ID required"}'; exit 1; }
        
        details=$(tmdb_details "$tmdb_id" "$type")
        
        title=$(echo "$details" | jq -r '.title // .name')
        genres=$(echo "$details" | jq -r '[.genres[].name] | join("\n")')
        keywords=$(echo "$details" | jq -r '[.keywords.keywords[]?.name // .keywords.results[]?.name] | .[0:10] | join(",")')
        cast=$(echo "$details" | jq -r '[.credits.cast[0:5][]?.name] | join(",")')
        director=$(echo "$details" | jq -r '[.credits.crew[] | select(.job == "Director")][:1][].name // empty')
        
        # Build detailed match explanation
        reasons=()
        
        # Check genre matches
        while IFS= read -r genre; do
            [[ -z "$genre" ]] && continue
            liked_weight=$(jq -r --arg g "$genre" '.genres.liked[$g] // 0' "$PREFERENCES")
            if [[ "$liked_weight" -gt 0 ]]; then
                reasons+=("✓ Genre \"$genre\" (du magst das, Score: +$liked_weight)")
            fi
        done <<< "$genres"
        
        # Check theme matches
        liked_themes=$(jq -r '.themes.liked[]' "$PREFERENCES" 2>/dev/null)
        if [[ -n "$liked_themes" && -n "$keywords" ]]; then
            while IFS= read -r theme; do
                if echo "$keywords" | grep -qi "$theme"; then
                    reasons+=("✓ Theme \"$theme\" passt zu deinen Vorlieben")
                fi
            done <<< "$liked_themes"
        fi
        
        # Check actor matches
        liked_actors=$(jq -r '.actors.liked[]' "$PREFERENCES" 2>/dev/null)
        if [[ -n "$liked_actors" && -n "$cast" ]]; then
            while IFS= read -r actor; do
                if echo "$cast" | grep -qi "$actor"; then
                    reasons+=("✓ Mit $actor (einer deiner Favoriten)")
                fi
            done <<< "$liked_actors"
        fi
        
        # Check director matches
        liked_directors=$(jq -r '.directors.liked[]' "$PREFERENCES" 2>/dev/null)
        if [[ -n "$liked_directors" && -n "$director" ]]; then
            while IFS= read -r dir; do
                if echo "$director" | grep -qi "$dir"; then
                    reasons+=("✓ Regie: $director (einer deiner Favoriten)")
                fi
            done <<< "$liked_directors"
        fi
        
        # Check availability
        available_on=$(echo "$details" | jq -r --arg region "$REGION" '[.["watch/providers"].results[$region].flatrate[]?.provider_name] | join(", ")')
        user_services=$(jq -r '.active | join("|")' "$SERVICES")
        if [[ -n "$available_on" ]] && echo "$available_on" | grep -qiE "$user_services"; then
            reasons+=("✓ Verfügbar auf deinen Diensten: $available_on")
        fi
        
        # Find similar titles from history
        similar=$(jq -r --arg genres "$genres" '[.items[] | select(.rating >= 4) | select(.genres as $g | ($genres | split("\n")) | any(. as $x | $g | index($x)))] | .[0:2] | .[] | "• \(.title) (⭐\(.rating))"' "$HISTORY" 2>/dev/null | head -3)
        
        reasons_json=$(printf '%s\n' "${reasons[@]}" | jq -R . | jq -s .)
        
        jq -n \
            --arg title "$title" \
            --arg id "$tmdb_id" \
            --argjson reasons "$reasons_json" \
            --arg similar "$similar" \
            --arg genres "$genres" \
            --arg themes "$keywords" \
            --arg cast "$cast" \
            --arg director "$director" \
            '{
                status: "ok",
                title: $title,
                id: ($id | tonumber),
                matchReasons: $reasons,
                similarToYourFavorites: (if $similar != "" then ($similar | split("\n")) else [] end),
                details: {
                    genres: ($genres | split("\n") | map(select(. != ""))),
                    themes: ($themes | split(",") | map(select(. != "")) | .[0:5]),
                    cast: ($cast | split(",") | map(select(. != ""))),
                    director: (if $director != "" then $director else null end)
                }
            }'
        ;;
        
    # ----------------------------------------
    # PROFILE (show taste profile)
    # ----------------------------------------
    profile)
        jq '{
            status: "ok",
            profile: {
                topGenres: [.genres.liked | to_entries | sort_by(-.value) | .[0:5][] | {genre: .key, score: .value}],
                avoidGenres: [.genres.disliked | to_entries | sort_by(-.value) | .[0:3][] | {genre: .key, score: .value}],
                likedThemes: .themes.liked[0:10],
                likedActors: .actors.liked[0:10],
                likedDirectors: .directors.liked[0:5],
                moodMappings: .moods,
                updatedAt: .updatedAt
            }
        }' "$PREFERENCES"
        ;;
        
    # ----------------------------------------
    # WATCHLIST
    # ----------------------------------------
    watchlist)
        subcmd="${1:-list}"
        shift || true
        
        case "$subcmd" in
            list)
                jq '{status:"ok", count: (.items | length), watchlist:.items}' "$WATCHLIST"
                ;;
            add)
                tmdb_id="${1:-}"
                type="${2:-tv}"
                
                [[ -z "$tmdb_id" ]] && { echo '{"status":"error","message":"TMDB ID required"}'; exit 1; }
                
                details=$(tmdb_details "$tmdb_id" "$type")
                title=$(echo "$details" | jq -r '.title // .name')
                year=$(echo "$details" | jq -r '(.release_date // .first_air_date // "")[:4]')
                
                entry=$(jq -n --arg id "$tmdb_id" --arg title "$title" --arg type "$type" --arg year "$year" '{
                    tmdbId: ($id | tonumber),
                    title: $title,
                    type: $type,
                    year: $year,
                    addedAt: (now | strftime("%Y-%m-%d"))
                }')
                
                # Add if not already in list
                jq --argjson entry "$entry" '
                    if [.items[].tmdbId] | index($entry.tmdbId) then .
                    else .items += [$entry]
                    end
                ' "$WATCHLIST" > "$WATCHLIST.tmp"
                mv "$WATCHLIST.tmp" "$WATCHLIST"
                
                echo '{"status":"ok","message":"Added to watchlist","title":"'"$title"'"}'
                ;;
            remove)
                tmdb_id="${1:-}"
                jq --arg id "$tmdb_id" '.items |= map(select(.tmdbId != ($id | tonumber)))' "$WATCHLIST" > "$WATCHLIST.tmp"
                mv "$WATCHLIST.tmp" "$WATCHLIST"
                echo '{"status":"ok","message":"Removed from watchlist"}'
                ;;
            *)
                jq '{status:"ok", count: (.items | length), watchlist:.items}' "$WATCHLIST"
                ;;
        esac
        ;;
        
    # ----------------------------------------
    # HISTORY
    # ----------------------------------------
    history)
        limit="${1:-10}"
        [[ "$limit" == "$WORKSPACE" ]] && limit=10
        jq --argjson limit "$limit" '{
            status: "ok",
            total: (.items | length),
            avgRating: (if (.items | length) > 0 then (([.items[].rating | select(. > 0)] | if length > 0 then add / length | . * 10 | round / 10 else null end)) else null end),
            items: [.items[:$limit][] | {title, type, rating, finishedAt}]
        }' "$HISTORY"
        ;;
        
    # ----------------------------------------
    # HELP / UNKNOWN
    # ----------------------------------------
    help)
        if [[ "$LANG" == "de" ]]; then
            echo '{"status":"ok","message":"Verfügbare Befehle: status, setup, search, info, watch, progress, done, like, dislike, suggest, mood, surprise, why, watchlist, history, profile, services"}'
        else
            echo '{"status":"ok","message":"Available commands: status, setup, search, info, watch, progress, done, like, dislike, suggest, mood, surprise, why, watchlist, history, profile, services"}'
        fi
        ;;
        
    *)
        echo '{"status":"error","message":"Unknown command: '"$CMD"'. Use help for available commands."}'
        exit 1
        ;;
esac
