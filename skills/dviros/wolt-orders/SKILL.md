---
name: wolt-orders
slug: wolt-orders
display_name: Wolt Orders 🍔
description: Discover restaurants with advanced filters (cuisine, price, distance, rating, promotions), place single or group orders on Wolt.com, reorder past favorites, track status in real-time, automatically detect delays and contact support, and push rich updates to Slack or other channels.
metadata: {"clawdbot":{"emoji":"🍔","requires":{"config":["browser.enabled"]}}}
user-invocable: true
---


# Wolt Orders 🍔

**Display Name:** Wolt Orders 🍔  
**Slug:** wolt-orders  

This skill provides a full-featured assistant for Wolt.com: smart restaurant discovery with rich filtering, menu browsing, single and group ordering, reordering past orders, real-time tracking, automatic delay detection + support contact, and proactive notifications to Slack or other connected channels.

## Prerequisites
- Browser tool must be enabled (with persistent session support recommended for login).
- User must provide Wolt credentials on first use (email/phone + password or OTP flow). Store session securely via browser cookies/profile.
- Delivery address must be set or provided per order.
- For group orders and notifications, Slack or other channels should be connected via channel_send.
- Always require explicit user confirmation before adding expensive items, finalizing checkout, or placing any order.

## Supported Filters for Restaurant Discovery

| Filter | Description | Example User Input | How to Apply in Browser |
|--------|-------------|--------------------|-------------------------|
| Cuisine/Genre | Specific food types or categories | "Italian", "Sushi", "Burger", "Vegan", "Middle Eastern" | Select cuisine filters on Wolt homepage or search page |
| Price Range | € (cheap) to €€€€ (expensive) | "cheap", "€€", "under 100 ILS" | Use price level filter buttons |
| Max Distance/Delivery Time | Limit by km or minutes | "within 3km", "under 30 min delivery" | Sort by delivery time or use distance filters if available |
| Minimum Rating | Star rating threshold | "4.5 or higher", "only top-rated" | Filter by rating or sort by highest rated |
| Promotions/Discounts | Special offers, free delivery, etc. | "with promo", "free delivery" | Enable "Offers" or "Promotions" filter |
| Dietary/Other | Vegan, gluten-free, halal, etc. | "vegan options", "kosher" | Search keywords or use venue tags |
| Sorting | Best match, rating, distance, delivery time, popularity | "closest first", "fastest delivery" | Use sort dropdown |

## Restaurant Discovery & Recommendation
1. Collect user preferences (cuisine, price, distance, rating, promotions, dietary needs, keywords).
2. Use browser tool to:
   - Navigate to https://wolt.com (auto-detect region, e.g., https://wolt.com/il for Israel).
   - Set or confirm delivery address.
   - Apply all relevant filters and sorting.
   - Perform search if keyword provided.
3. Scrape top 8–12 matching restaurants with: name, cuisines, rating (stars + count), price level, delivery time/fee, distance, current promotions, short description.
4. Present results in a formatted table/list with key details.
5. Offer options: view more results, refine filters, view full menu of a restaurant, or see images/descriptions.
6. If user wants recommendations, prioritize high-rated + fast + matching filters.

## Menu Browsing & Cart Building
1. Navigate to selected restaurant page.
2. Scrape menu by categories (appetizers, mains, drinks, etc.).
3. Present structured menu with item name, description, price, popular tags.
4. Ask user for selections, quantities, customizations (e.g., "no onions", extra cheese).
5. Maintain cart state in conversation.
6. Periodically scrape cart summary for current total, fees, minimum order, estimated delivery.
7. Show updated cart summary after each addition.

## Placing a Single Order
1. Confirm delivery address, payment method (use saved if available).
2. Use browser to add items to cart with exact options.
3. Proceed to checkout, fill any required fields.
4. Show final order summary (items, total, fees, ETA).
5. Require explicit user confirmation ("yes/confirm/place it").
6. Place order.
7. Capture order ID, tracking link, estimated delivery time.
8. Send confirmation + tracking link to user and push to specified channel.

## Placing a Group Order
1. Confirm restaurant, delivery address, and group details (deadline, expected participants).
2. Use browser to start a **Group Order** on Wolt (native feature).
3. Retrieve and share the group order link via channel_send (e.g., Slack thread).
4. Instruct participants to join via link and add their items.
5. Monitor cart periodically (scrape total, participant contributions if visible).
6. When host says "ready to place", finalize checkout and place order (requires host payment).
7. Share final order confirmation, tracking link, and breakdown (if available) with the group.

## Reordering Past Orders
1. Navigate to Wolt account → Orders/History.
2. Scrape recent orders (date, restaurant, total, items summary).
3. Present list of last 5–10 orders.
4. On user selection, use Wolt's "Reorder" button if available, or rebuild cart manually.
5. Proceed as single order with confirmation.

## Tracking an Order
1. Accept order ID or use most recent.
2. Navigate to order tracking page.
3. Scrape current status, ETA, driver info (if en route), map description.
4. Provide rich update (status, time remaining, any notes).
5. Support live polling ("watch mode") in ongoing conversation.

## Handling Delays & Contacting Support
1. During tracking, compare current time to original ETA.
2. If delayed >15–30 min (configurable), alert user and offer to contact support.
3. On approval, navigate to order → Help/Support/Chat.
4. Initiate chat with templated message: "Order #[ID] is delayed. Estimated delivery was [TIME], current status is [STATUS]. Please assist."
5. Relay support responses in real-time.
6. Push delay alerts and support updates to channel.

## Sending Notifications
Use channel_send for all major events:
- Restaurant recommendations
- Cart updates (on request)
- Order confirmation + tracking link
- Status changes
- Delay alerts
- Support interaction summaries

Format messages richly (emojis, bold, links, order ID).

## Safety & Error Handling
- Never place order without explicit "yes/confirm/place" confirmation.
- On browser errors, retry up to 3 times or fall back to manual instructions.
- Respect privacy: do not log full payment details.
- If login expires, prompt for re-authentication.

```

**wolt-orders/thumbnail.png**  
*(Recommended additional file: a 512×512 PNG thumbnail. Suggested image: a stylized Wolt blue bag with food items and a notification bell. You can generate or source one separately.)*

**wolt-orders/examples.md**  
*(Additional file to satisfy "at least one file" requirement beyond SKILL.md)*

```markdown
# Example Invocations

| User Query | Skill Behavior |
|------------|---------------|
| "I'm hungry, find good sushi under €€ within 20 min delivery" | Start discovery with sushi cuisine, €€ price, fast delivery filter |
| "Order pizza from Domino's for me" | Go directly to restaurant, build cart, place single order |
| "Let's do a group order for burgers tonight" | Ask for restaurant/preferences, start group order, share link |
| "Track my last Wolt order" | Fetch most recent order and show live status |
| "My order is late, contact support" | Detect delay, open chat, send message |
| "Reorder my usual shawarma" | List history, identify likely item, reorder with confirmation |
```