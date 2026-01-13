# Plan2Meal Skill

A ClawdHub skill for managing recipes and grocery lists via Plan2Meal, a React Native recipe app.

## Features

- **Recipe Management**: Add recipes from URLs, search, view, and delete your recipes
- **Grocery Lists**: Create and manage shopping lists with recipes
- **GitHub OAuth**: Secure authentication via GitHub
- **Recipe Extraction**: Automatically fetch recipe metadata from URLs
- **Telegram Formatting**: Pretty-printed output for Telegram

## Setup

1. Install via ClawdHub:
   ```bash
   clawdhub install plan2meal
   ```

2. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. Required environment variables:
   - `CONVEX_URL`: Your Convex deployment URL
   - `GITHUB_CLIENT_ID`: GitHub OAuth App Client ID
   - `GITHUB_CLIENT_SECRET`: GitHub OAuth App Client Secret
   - `CLAWDBOT_URL`: Your ClawdBot URL (for OAuth callback)

## Commands

### Recipe Commands

| Command | Description |
|---------|-------------|
| `plan2meal add <url>` | Fetch recipe metadata from URL and create recipe |
| `plan2meal list` | List your recent recipes |
| `plan2meal search <term>` | Search your recipes |
| `plan2meal show <id>` | Show detailed recipe information |
| `plan2meal delete <id>` | Delete a recipe |

### Grocery List Commands

| Command | Description |
|---------|-------------|
| `plan2meal lists` | List all your grocery lists |
| `plan2meal list-show <id>` | Show grocery list with items |
| `plan2meal list-create <name>` | Create a new grocery list |
| `plan2meal list-add <listId> <recipeId>` | Add recipe to grocery list |

### Help

| Command | Description |
|---------|-------------|
| `plan2meal help` | Show all available commands |

## Usage Examples

### Adding a Recipe

```
plan2meal add https://www.allrecipes.com/recipe/12345/pasta
```

Output:
```
✅ Recipe added successfully!

📖 Recipe Details
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name: Classic Pasta
Source: allrecipes.com
Method: firecrawl-json (credit used)
Time: 15 min prep + 20 min cook

🥘 Ingredients (4 servings)
• 1 lb pasta
• 2 cups marinara sauce
• 1/2 cup parmesan

🔪 Steps
1. Boil water...
```

### Searching Recipes

```
plan2meal search pasta
```

### Creating a Grocery List

```
plan2meal list-create Weekly Shopping
```

### Adding Recipe to List

```
plan2meal list-add <listId> <recipeId>
```

## Recipe Limits

The free tier allows up to **5 recipes**. You'll receive a warning when approaching this limit.

## Authentication

First-time users will be prompted to authenticate via GitHub OAuth. The token is stored securely in your session.

## License

MIT