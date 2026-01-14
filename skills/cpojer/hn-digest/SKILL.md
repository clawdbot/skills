---
name: hn-digest
description: "Fetch and send Hacker News front-page posts on demand. Use when the user asks for HN, says 'hn', 'pull HN', 'hn 10', or specifies a topic like 'hn health', 'hn hacking', or 'hn tech'. Sends N (default 5) posts as individual messages with Title + Link. Exclude crypto."
---

# HN Digest

## Command format

Interpret a user message that starts with `hn` as a request for a Hacker News front-page digest.

Supported forms:

- `hn` → default 5 posts
- `hn <n>` → n posts
- `hn <topic>` → filter/boost by topic
- `hn <n> <topic>` → both
- If the user asks for “more” after already seeing some (e.g. “show me top 10–15 since we already did top 10”), treat it as an offset request and use `--offset` (e.g. offset 10, count 10).

Topics:

- `tech` (default)
- `health`
- `hacking`
- `life` / `lifehacks`

## Output requirements

- Do **not** send any extra commentary/preamble/epilogue.
- Send results as **individual messages**.
- Each post message must be exactly:
  - first line: the post title
  - second line: `<age> · <commentCount> comments` (age like `45m ago`, `6h ago`, `3d ago`)
  - third line: the Hacker News comments link (`https://news.ycombinator.com/item?id=...`)
- After the post messages, send **one final message** that is the generated image.
  - If the chat provider requires non-empty text for media, use a minimal caption `.`.
- Hard exclude crypto.

## Procedure

1. Parse `n` and `topic` from the user message.
2. Fetch + rank items:
   - Run `node skills/hn-digest/scripts/hn.mjs --count <n> --offset <offset> --topic <topic> --format json`.
   - Default `offset` is 0 unless the user explicitly asks for “more/next” after a previous batch.
3. Send results as **N individual messages** in the required 3-line format.
4. Then generate a **delightful mood image** via Nano Banana, inspired by the posts you just sent:
   - Use `skills/hn-digest/scripts/mood_prompt.mjs` to build a prompt from the JSON items.
   - Add 3–4 subtle Easter eggs derived from the post themes (no text/logos; keep it fun).
   - Generate and attach the image by running:
     - `skills/hn-digest/scripts/generate_mood_nano_banana.sh ./tmp/hn-mood/hn-mood.png <topic> <n> <offset>`
   - Send the generated image as one additional message.

If fetching/ranking fails or returns 0 items:
- Use `https://news.ycombinator.com/` in the browser tool, pick N non-crypto items by judgment, and send them in the same 3-line format.
- Still generate a mood image (general “HN tech deep dives” vibe) with a banana Easter egg.
