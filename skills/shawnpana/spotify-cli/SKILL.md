# Spotify CLI

A simple command-line interface for controlling Spotify playback from a Raspberry Pi (or any Linux system).

## Requirements

- Python 3
- Spotify Premium account
- `spotipy` Python library
- Spotify app open on another device (phone, computer, or web player)

## Installation

### 1. Install dependencies

```bash
pip3 install spotipy --break-system-packages
```

### 2. Create a Spotify Developer App

1. Go to https://developer.spotify.com/dashboard
2. Log in and click "Create App"
3. Set Redirect URI to `http://127.0.0.1:8888/callback`
4. Copy the **Client ID** and **Client Secret**

### 3. Create config file

```bash
mkdir -p ~/.config/spotify-cli
cat << EOF > ~/.config/spotify-cli/config
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
EOF
```

The script automatically loads credentials from `~/.config/spotify-cli/config`.

### 4. Install the script

```bash
sudo cp spotify /usr/local/bin/spotify
sudo chmod +x /usr/local/bin/spotify
```

### 5. Authenticate

Run any command (e.g., `spotify status`). On first run, you'll get a URL to open in your browser. After authorizing, copy the redirect URL (even if the page doesn't load) and paste it when prompted.

## Commands

| Command | Description |
|---------|-------------|
| `spotify search <query>` | Search for songs (shows top 5 results) |
| `spotify play <song>` | Search and play a song |
| `spotify pause` | Pause playback |
| `spotify resume` | Resume playback |
| `spotify next` | Skip to next track |
| `spotify prev` | Previous track |
| `spotify status` | Show currently playing track |
| `spotify devices` | List available Spotify devices |

## Examples

```bash
# Search for a song
spotify search "stairway to heaven"

# Play a song (tip: include artist for better results)
spotify play "stairway to heaven led zeppelin"

# Check what's playing
spotify status

# Control playback
spotify pause
spotify resume
spotify next
```

## Best Practices (for AI agents)

When using this tool on behalf of a user:

1. **Always search first** before playing. Use `spotify search "query"` to see results.
2. **Verify the match** - confirm with the user that the search results match what they were looking for.
3. **Then play** - once confirmed, use `spotify play "exact song name artist"` with the correct title/artist from the search results.

This avoids playing the wrong song due to Spotify's fuzzy search matching.

**Example workflow:**
```bash
# User asks: "play voice actor u projected 2"

# Step 1: Search first
spotify search "voice actor u projected 2"
# Results show: "U Projected 2 - Voice Actor, Yarrow.co"

# Step 2: Confirm with user that this is the right song

# Step 3: Play with exact match
spotify play "U Projected 2 Voice Actor"
```

## Notes

- This CLI controls playback on an existing Spotify session. You need Spotify open on another device (phone, computer, or https://open.spotify.com).
- The CLI sends commands to that device - audio plays there, not on the Pi.
- Requires Spotify Premium for playback control.

## Troubleshooting

### "No active device found"
Open Spotify on your phone/computer and play something, then try again.

### "No devices found"
Make sure Spotify is open on at least one device and logged into the same account.

### Auth token expired
Delete `~/.cache-*` files and re-authenticate.
