# TMDB API Reference

## Getting API Key

1. Create account: https://www.themoviedb.org/signup
2. Go to Settings → API
3. Request API key (choose "Developer" → personal use)
4. Copy API Key (v3 auth)

## Endpoints Used

### Search Multi (Movies + TV)
```
GET /search/multi?api_key={key}&query={query}&language=de-DE
```

Response:
```json
{
  "results": [
    {
      "id": 106379,
      "media_type": "tv",
      "name": "Fallout",
      "first_air_date": "2024-04-10",
      "vote_average": 8.5,
      "overview": "...",
      "poster_path": "/path.jpg"
    }
  ]
}
```

### TV Show Details
```
GET /tv/{id}?api_key={key}&language=de-DE&append_to_response=credits,watch/providers
```

Response includes:
- Basic info (name, overview, genres)
- Seasons and episodes count
- Cast and crew (credits)
- Streaming availability (watch/providers)

### Movie Details
```
GET /movie/{id}?api_key={key}&language=de-DE&append_to_response=credits,watch/providers
```

### Discover (for recommendations)
```
GET /discover/tv?api_key={key}&language=de-DE&with_genres={genre_ids}&watch_region=DE&with_watch_providers={provider_ids}&sort_by=vote_average.desc
```

## Watch Providers

The `watch/providers` response includes availability by region:

```json
{
  "watch/providers": {
    "results": {
      "DE": {
        "flatrate": [
          {"provider_id": 9, "provider_name": "Amazon Prime Video"}
        ],
        "rent": [...],
        "buy": [...]
      }
    }
  }
}
```

## Genre IDs

| Genre | TV ID | Movie ID |
|-------|-------|----------|
| Action & Adventure | 10759 | 28 |
| Animation | 16 | 16 |
| Comedy | 35 | 35 |
| Crime | 80 | 80 |
| Documentary | 99 | 99 |
| Drama | 18 | 18 |
| Family | 10751 | 10751 |
| Fantasy | 10765 | 14 |
| Horror | - | 27 |
| Mystery | 9648 | 9648 |
| Romance | - | 10749 |
| Sci-Fi & Fantasy | 10765 | 878 |
| Thriller | - | 53 |
| War & Politics | 10768 | 10752 |
| Western | 37 | 37 |

## Rate Limits

- 40 requests per 10 seconds
- Cache responses for at least 1 hour (search) or 24 hours (details)

## Image URLs

Base URL: `https://image.tmdb.org/t/p/`

Sizes:
- Poster: `w92`, `w154`, `w185`, `w342`, `w500`, `w780`, `original`
- Backdrop: `w300`, `w780`, `w1280`, `original`
- Profile: `w45`, `w185`, `h632`, `original`
