---
name: office-quotes
description: Generate random quotes from The Office (US). Provides access to 326 offline quotes plus online mode with SVG cards, character avatars, and full episode metadata via the akashrajpurohit API. Use for fun, icebreakers, or any task requiring The Office quotes.
---

# office-quotes Skill

Generate random quotes from The Office (US) TV show.

## Tools

### office_quote

**Description:** Generate a random quote from The Office (US).

**Parameters:**
- `mode` (optional, default: "offline"): Quote mode - "offline" for 326 local quotes, "api" for online SVG card generation
- `theme` (optional, default: "dark"): SVG theme when using api mode - "dark" or "light"
- `include_image` (optional, default: false): When true, returns SVG image URL instead of rendered SVG

**Examples:**
```typescript
// Random offline quote
await office_quote({});

// Random quote with SVG card (dark theme)
await office_quote({ mode: "api" });

// SVG image URL (for embedding)
await office_quote({ mode: "api", include_image: true });

// Light theme SVG
await office_quote({ mode: "api", theme: "light" });
```

## Offline Mode (Default)

326 quotes sourced from the Raycast Office Quotes extension. Always works, no network required.

## Online Mode

Unlimited quotes from the the-office-api by Akash Rajpurohit. Returns SVG cards with character avatars and animations.

## Episode Lookup

Use external fetch or browser for episode metadata:
- `https://officeapi.akashrajpurohit.com/season/{season}` - Season overview
- `https://officeapi.akashrajpurohit.com/season/{season}/episode/{episode}` - Specific episode

## Quote Examples

> "Would I rather be feared or loved? Easy. Both. I want people to be afraid of how much they love me." — Michael Scott

> "Bears. Beets. Battlestar Galactica." — Jim Halpert

> "Whenever I'm about to do something, I think, 'Would an idiot do that?' And if they would, I do not do that thing." — Dwight Schrute
