# API Notes

- Desktop API docs: https://developers.beeper.com/desktop-api
- Base URL: http://localhost:23373 (Beeper Desktop must be running).

## Search behavior

- Message search is literal word match (not semantic).
- Global search uses `/v1/search` for chats/groups.
- Message pagination for global search uses `/v1/messages/search` when `--messages-*` flags are set.

## Pagination

- Chats list returns `newestCursor` and `oldestCursor`.
- Messages list uses the last item's `sortKey` as the cursor.
- Message search returns `oldestCursor`/`newestCursor` for paging.
