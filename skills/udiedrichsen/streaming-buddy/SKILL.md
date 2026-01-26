---
name: streaming-buddy
version: 2.0.0
description: "Personal streaming assistant with learning preferences. Tracks what you're watching, learns your taste, and suggests what to watch next based on your services, mood, and preferences. Use when asked about movies, TV shows, streaming services, what to watch, or tracking viewing progress. Triggers: /stream, 'what should I watch', 'recommend something', mentioning Netflix/Prime/Disney+/Apple TV+, asking about series/seasons/episodes, mood-based requests like 'something exciting'."
author: clawdbot
license: MIT
metadata:
  clawdbot:
    emoji: "📺"
    triggers: ["/stream"]
    requires:
      bins: ["jq", "curl"]
      env: ["TMDB_API_KEY"]
  tags: ["streaming", "movies", "tv-shows", "recommendations", "entertainment", "learning", "preferences"]
---

# Streaming Buddy 📺

Personal streaming assistant that learns your taste, tracks your watching habits, and suggests what to watch next.

## Features

- **Search & Info**: Find movies/TV shows with TMDB data
- **Watch Tracking**: Track what you're currently watching with progress
- **Learning System**: Learns your preferences from likes/dislikes/ratings
- **Smart Recommendations**: Personalized suggestions based on your taste
- **Mood-Based Search**: Find content by mood (exciting, relaxing, scary, etc.)
- **Availability Check**: Shows which of your services has the content
- **Match Explanation**: Explains why a title matches your preferences

## Commands

| Command | Action |
|---------|--------|
| `/stream` | Show status with all commands |
| `/stream search <title>` | Search for movies/TV shows |
| `/stream info <id> [tv\|movie]` | Detailed info + availability |
| `/stream watch <id> [tv\|movie]` | Start tracking a title |
| `/stream progress S01E05` | Update progress on current show |
| `/stream done [1-5]` | Mark as finished + rate (auto-learns) |
| `/stream like [id]` | Mark as liked → learns preferences |
| `/stream dislike [id]` | Mark as disliked → learns preferences |
| `/stream suggest [service] [tv\|movie]` | Personalized recommendations |
| `/stream mood <mood>` | Search by mood |
| `/stream surprise` | Random recommendation |
| `/stream why <id>` | Explain why this matches you |
| `/stream watchlist` | Show watchlist |
| `/stream watchlist add <id>` | Add to watchlist |
| `/stream history` | View watch history |
| `/stream profile` | Show your taste profile |
| `/stream services` | Manage streaming services |
| `/stream services add <name>` | Add a service |
| `/stream services remove <name>` | Remove a service |

## Mood Options

| Mood | Genres |
|------|--------|
| `exciting` | Action, Thriller, Sci-Fi, Adventure |
| `relaxing` | Comedy, Animation, Family, Documentary |
| `thoughtful` | Drama, Mystery, History |
| `scary` | Horror, Thriller |
| `romantic` | Romance, Drama |
| `funny` | Comedy, Animation |

## Supported Services

- `netflix`, `amazon-prime`, `disney-plus`, `apple-tv-plus`
- `youtube-premium`, `wow`, `paramount-plus`, `crunchyroll`
- `joyn`, `rtl`, `magenta`, `mubi`

## Learning System

The skill learns your preferences from:

1. **Ratings**: When you finish with `/stream done [1-5]`:
   - Rating 4-5: Adds genres/themes/actors to "liked"
   - Rating 1-2: Adds genres to "avoided"

2. **Explicit Feedback**: `/stream like` and `/stream dislike`:
   - Extracts genres, themes, actors, directors
   - Updates preference weights

3. **Preference Profile** includes:
   - Genre preferences (weighted scores)
   - Liked/disliked themes
   - Favorite actors & directors
   - Custom mood mappings

## Handler Usage

```bash
# Core commands
handler.sh status $WORKSPACE
handler.sh search "severance" $WORKSPACE
handler.sh info 95396 tv $WORKSPACE
handler.sh watch 95396 tv $WORKSPACE
handler.sh progress S01E05 $WORKSPACE
handler.sh done 5 "Great show!" $WORKSPACE

# Learning commands
handler.sh like $WORKSPACE                    # Like current watching
handler.sh like 12345 movie $WORKSPACE        # Like specific title
handler.sh dislike $WORKSPACE
handler.sh why 95396 tv $WORKSPACE
handler.sh profile $WORKSPACE

# Recommendation commands
handler.sh suggest $WORKSPACE                 # All services, all types
handler.sh suggest prime movie $WORKSPACE     # Prime movies only
handler.sh mood exciting $WORKSPACE
handler.sh mood relaxing tv $WORKSPACE
handler.sh surprise $WORKSPACE

# List commands
handler.sh watchlist list $WORKSPACE
handler.sh watchlist add 12345 tv $WORKSPACE
handler.sh history $WORKSPACE

# Service management
handler.sh services list $WORKSPACE
handler.sh services add netflix $WORKSPACE
handler.sh services remove netflix $WORKSPACE
```

## Data Files

All data stored in `$WORKSPACE/memory/streaming-buddy/`:

| File | Purpose |
|------|---------|
| `config.json` | TMDB API key, region, language |
| `profile.json` | User profile metadata |
| `services.json` | Active streaming services |
| `preferences.json` | Learned taste preferences |
| `watching.json` | Currently watching |
| `watchlist.json` | Want to watch list |
| `history.json` | Watched + ratings |
| `cache/*.json` | API response cache (24h) |

## Setup

1. Get TMDB API key: https://www.themoviedb.org/settings/api
2. Store in `memory/streaming-buddy/config.json`:
   ```json
   {
     "tmdbApiKey": "your_api_key",
     "region": "DE",
     "language": "de-DE"
   }
   ```
3. Run `/stream setup` to configure services

## Conversation Examples

**Mood-based search:**
```
User: I want something exciting tonight
Bot: 🎬 Exciting picks for you:
     1. Reacher S3 (Prime) ⭐8.5
     2. Jack Ryan (Prime) ⭐8.1
     ...
```

**Learning from feedback:**
```
User: /stream done 5
Bot: ✅ Severance marked as done (⭐5)
     📚 Learned: +Drama, +Mystery, +Sci-Fi
     Actors: Adam Scott, Britt Lower saved to favorites
```

**Explaining recommendations:**
```
User: /stream why 95396
Bot: 🎯 Why Severance matches you:
     ✓ Genre "Drama" (you like this, +2)
     ✓ Genre "Mystery" (you like this, +2)
     ✓ Theme "office" in your preferences
     ✓ With Adam Scott (your favorite)
     Similar to: Fallout ⭐5
```

## Language Support

- Language detected from `config.json` (`language: "de-DE"` or `"en"`)
- All output adapts to configured language
- Commands work in any language

## Requirements

- `jq` (JSON processor)
- `curl` (HTTP client)
- `bash` 4.0+
- TMDB API key (free)

## References

- [services.md](references/services.md) — Full list of streaming services
- [tmdb-api.md](references/tmdb-api.md) — TMDB API usage
- [justwatch.md](references/justwatch.md) — Availability data integration
