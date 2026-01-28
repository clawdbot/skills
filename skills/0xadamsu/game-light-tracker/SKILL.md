---
name: game-light-tracker
description: Track live NFL, NBA, NHL, or MLB games and automatically change Hue light colors based on which team is leading. Use when user wants to sync smart lights with live sports scores for visual game tracking. Supports NFL, NBA, NHL, and MLB games with customizable team colors.
---

# Game Light Tracker

Automatically sync your Hue lights with live sports scores. When the lead changes, your lights change color to match the leading team.

## Quick Start

**Basic usage:**
```
Track the [Team A] vs [Team B] game and change my [light name] to [color1] when [Team A] leads and [color2] when [Team B] leads
```

**Examples:**
- "Track the Rams vs Seahawks game and change my backlight to blue when Rams lead, green when Seahawks lead" (NFL)
- "Monitor the Lakers vs Celtics game, purple for Lakers, green for Celtics" (NBA)
- "Watch the Rangers vs Devils game - blue for Rangers, red for Devils" (NHL)
- "Track the Yankees vs Red Sox game, make my living room light blue for Yankees, red for Red Sox" (MLB)

## How It Works

1. Fetches live scores from ESPN API every 20 seconds
2. Detects lead changes
3. Changes specified Hue light color via Home Assistant
4. Includes auto-restart keeper to prevent timeouts
5. Optional: Adds third color for tied games

## Setup Requirements

- Home Assistant with Hue lights configured
- Home Assistant API token (stored in `.homeassistant-config.json`)
- Light entity ID from Home Assistant

## Scripts

### `game-tracker.ps1`
Main monitoring script that tracks a specific game and updates lights.

**Usage:**
```powershell
.\game-tracker.ps1 -Sport "nfl" -Team1 "LAR" -Team2 "SEA" -Light "light.backlight" -Color1 "0,0,255" -Color2 "0,100,0" [-TiedColor "255,0,0"]
```

**Parameters:**
- `-Sport`: "nfl", "nba", "nhl", or "mlb"
- `-Team1`: First team abbreviation
- `-Team2`: Second team abbreviation
- `-Light`: Home Assistant light entity ID
- `-Color1`: RGB color for Team1 (comma-separated, e.g., "0,0,255" for blue)
- `-Color2`: RGB color for Team2 (comma-separated, e.g., "0,100,0" for dark green)
- `-TiedColor`: (Optional) RGB color when game is tied

### `keeper.ps1`
Auto-restart supervisor that prevents 30-minute timeout crashes.

**Usage:**
```powershell
.\keeper.ps1 -TrackerScript "game-tracker.ps1" -RestartInterval 25
```

**Parameters:**
- `-TrackerScript`: Path to the game-tracker.ps1 script
- `-RestartInterval`: Minutes between restarts (default: 25)

## Common Team Abbreviations

**NFL:**
- Rams: LAR, Seahawks: SEA, Chiefs: KC, Bills: BUF, Patriots: NE
- Cowboys: DAL, Eagles: PHI, 49ers: SF, Packers: GB, Bears: CHI
- [Full list: https://www.espn.com/nfl/teams]

**NBA:**
- Lakers: LAL, Celtics: BOS, Warriors: GS, Knicks: NY, Bulls: CHI
- Heat: MIA, Nets: BKN, 76ers: PHI, Bucks: MIL, Mavericks: DAL
- Nuggets: DEN, Suns: PHX, Clippers: LAC, Raptors: TOR
- [Full list: https://www.espn.com/nba/teams]

**NHL:**
- Rangers: NYR, Devils: NJ, Bruins: BOS, Maple Leafs: TOR, Canadiens: MTL
- Penguins: PIT, Capitals: WSH, Flyers: PHI, Lightning: TB, Panthers: FLA
- Red Wings: DET, Blackhawks: CHI, Avalanche: COL, Golden Knights: VGK
- [Full list: https://www.espn.com/nhl/teams]

**MLB:**
- Yankees: NYY, Red Sox: BOS, Dodgers: LAD, Giants: SF, Mets: NYM
- Cubs: CHC, Cardinals: STL, Astros: HOU, Braves: ATL, Phillies: PHI
- [Full list: https://www.espn.com/mlb/teams]

## Common RGB Colors

- **Blue**: 0,0,255
- **Red**: 255,0,0
- **Green**: 0,255,0
- **Dark Green**: 0,100,0
- **Orange**: 255,165,0
- **Purple**: 128,0,128
- **Yellow**: 255,255,0
- **White**: 255,255,255

## Workflow

When user requests game tracking:

1. **Identify sport and teams:**
   - Extract sport (NFL/NBA/NHL/MLB)
   - Get team abbreviations from user or look up from team names

2. **Get light and color preferences:**
   - Ask for light entity ID (or read from Home Assistant config)
   - Get desired RGB colors for each team
   - Optional: Ask if they want a tied-game color

3. **Load Home Assistant config:**
   ```powershell
   $config = Get-Content ".homeassistant-config.json" | ConvertFrom-Json
   $token = $config.token
   $url = $config.url
   ```

4. **Start game tracker:**
   ```powershell
   .\scripts\game-tracker.ps1 -Sport "nfl" -Team1 "LAR" -Team2 "SEA" -Light "light.backlight" -Color1 "0,0,255" -Color2 "0,100,0" -TiedColor "255,0,0"
   ```

5. **Start keeper for auto-restart:**
   ```powershell
   Start-Process powershell -ArgumentList "-File keeper.ps1 -TrackerScript 'game-tracker.ps1'" -WindowStyle Hidden
   ```

6. **Confirm to user:**
   - Tell them monitoring is active
   - Show current score if available
   - Explain color scheme
   - Tell them how to stop it

## Stopping the Tracker

To stop monitoring:
```powershell
Get-Process powershell | Where-Object { $_.CommandLine -like "*game-tracker.ps1*" -or $_.CommandLine -like "*keeper.ps1*" } | Stop-Process -Force
```

## Troubleshooting

**Light not changing:**
- Verify Home Assistant token is valid
- Check light entity ID is correct
- Ensure Home Assistant is accessible at the configured URL

**Script crashes:**
- Keeper should auto-restart it
- Check ESPN API is accessible
- Verify team abbreviations are correct

**Wrong team colors:**
- Double-check RGB values (must be 0-255, comma-separated)
- Ensure colors are assigned to correct teams
