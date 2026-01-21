---
name: checkers-sixty60
description: Shop on Checkers.co.za Sixty60 delivery service via browser automation. Use when the user asks to shop for groceries, add items to cart, order from Checkers, or manage their Checkers shopping basket. Handles delivery type selection, product search, backup preferences, regular item reordering, and deal evaluation.
---

# Checkers Sixty60 Shopping

Guide for shopping on Checkers.co.za using browser automation, focused on Sixty60 quick delivery.

## Delivery Types

Checkers offers two delivery options:

1. **Sixty60** (scooter icon 🛵) - Quick shop and delivery, **maximum 40 items**
2. **Hyper** (van icon 🚚) - Bulk shopping and larger items

**Default to Sixty60 delivery** unless the user specifically requests bulk/hyper shopping.

## Cart Structure

The cart has two sections:
- **Top section**: Sixty60 items
- **Bottom section**: Hyper items (generally ignore this section)

## Shopping Workflow

### 1. Filter for Sixty60 Items (Recommended)

Click the **Sixty60 icon** next to "Shop By Delivery" in the navigation to show only Sixty60-eligible items.

⚠️ **Important**: This is a toggle button. If already active, clicking again will deactivate the filter.

### 2. Search and Add Items

- Each item shows either a Sixty60 icon or Hyper icon at the bottom of the product card
- When Sixty60 filter is active, only compatible items are shown
- Look for deal badges under item images (e.g., "save R5", "buy 2 for R150")

### 3. Product Selection Strategy

When choosing between similar products:
- **Prefer Vitality products** when price is equal or similar (identifiable by Vitality logo at top-left of product card) - user earns points on these
- Choose the **cheaper option** after considering any sales/deals
- Evaluate bundle deals (e.g., "buy 2 for X") to determine if worth purchasing
- Consider unit price, not just total price

**Selection priority** (highest to lowest):
1. Vitality product at same or lower price
2. Lower price (considering deals)
3. Better unit price

### 4. Adding Items to Cart (Error Handling)

⚠️ **Critical**: Always wait for UI to update after clicking Add/+/- buttons.

**Process**:
1. Click the Add button or +/- button
2. Take a new snapshot to verify the update
3. Check the item counter on the product card shows the expected quantity
4. If an error alert appears, report it to the user
5. If the quantity doesn't match expected, try again or report the issue

**Common errors**:
- "Failed to validate your 60min item" - temporary stock/delivery issue
- Items may not add if out of stock or delivery incompatible

**Never assume success** - always verify the cart state after each operation.

### 5. Backup Preferences

Each cart item can have a backup in case of out-of-stock:
- Select a backup product OR
- Select **"I don't want a backup"** if no substitute is acceptable

**Note**: Items ordered before remember their backup preference, making reordering efficient.

## Shop Your Regulars

Access previously purchased items to reorder efficiently:

1. Click **"My Shop"** in navigation
2. Click **"Shop Your Regulars"** (or navigate to `/my-shop/shop-your-regulars`)

**Features**:
- Shows all previously ordered items
- Items retain their backup preferences
- Cannot search within regulars (limitation)
- Can filter using the filter dropdown
- Can sort items

**Best practice**: When user mentions common grocery items they regularly buy, check regulars first.

## Deals and Promotions

Deal badges appear under item images showing:
- Flat discounts: "save R5"
- Bundle deals: "buy 2 for R150"
- Percentage off: "30% off"

Evaluate deals by:
- Comparing unit price vs. regular price
- Checking if bundle quantity matches user needs
- Considering if deal item is equivalent to preferred brand

## Cart Management

- Maximum **40 items** per Sixty60 order
- Cart shows running total in top-right (e.g., "R52.98")
- Can increase/decrease quantities using +/- buttons
- Remove items by reducing quantity to zero

## Navigation Tips

- Search bar at top: Use for specific products
- "Shop by Department": Browse by category
- Check basket icon for current total and item count
- Address shown at top - delivery location confirmation
