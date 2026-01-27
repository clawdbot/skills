---
name: standard-agentic-commerce-engine
version: 1.2.4
description: A production-ready universal engine for Agentic Commerce. This tool enables autonomous agents to interact with any compatible headless e-commerce backend through a standardized protocol. It provides out-of-the-box support for discovery, cart operations, and secure user management.
tags: [ecommerce, shopping-agent, commerce-engine, standard-protocol, headless-commerce, agentic-web]
---

# Standard Agentic Commerce Engine

The **Standard Agentic Commerce Engine** is a production-ready bridge connecting autonomous agents with modern e-commerce backends. By providing a unified, high-precision interface, it allows any digital storefront to become "Agent-Native" instantly.

GitHub Repository: https://github.com/NowLoadY/agent-commerce-engine

## Reference Case: Lafeitu

For a production-grade implementation example using this engine, see the [Lafeitu Gourmet Skill](https://clawdhub.com/NowLoadY/agentic-spicy-food). It demonstrates the engine specialized for a real-world artisanal food brand.

---

## 🛠 Tool Priority & Fallback Strategy

To provide the most accurate and efficient experience, follow this priority sequence:

1.  **API First (Primary)**: Always attempt to use the `commerce.py` script first. It provides structured, high-precision data. Configure it via environment variables (`COMMERCE_URL`).
2.  **Stateless Headers**: Rely on the engine's built-in header management (`x-user-account`, `x-visitor-id`) to maintain session integrity without cookies.
3.  **Self-Correction**: If the API returns a 404 for a specific slug discovered via browser, prioritize the API's `search` results as the source of truth for the backend.

---

## 🧠 Agent Operational Logic

Follow these logical flows to ensure a high-quality user experience:

### 1. Product Discovery & Validation
**Goal**: Ensure the item exists and find the correct specifications before taking action.
- **Action**: Always run `search` or `list` before adding to cart.
- **Logic**: Use the API to discover the correct `slug` and valid `gram`/variant values. 
- **Refinement**: If multiple results are found, ask the user to specify based on the returned attributes.

### 2. Authentication & Profile Flow
**Goal**: Manage user privacy and session data.
- **Logic**: The API is stateless. Actions requiring identity will return `401 Unauthorized` if credentials aren't saved.
- **Commands**:
    1. View profile: `python3 scripts/commerce.py get-profile`
    2. Update details: `python3 scripts/commerce.py update-profile --name "Name" --address "..."`
- **Required Data**: Respect the schema of the specific brand's backend.

### 3. Registration Flow
**Goal**: Handle new users.
- **Trigger**: When an action returns "User Not Found".
- **Instruction**: Guide the user to the store's registration URL (often found in brand metadata).

### 4. Shopping Cart Management
**Goal**: Precise modification of the user's shopping session.
- **Logic**: The engine supports incrementing quantities or setting absolute values.
- **Commands**:
    - **Add**: `python3 scripts/commerce.py add-cart <slug> --gram <G> --quantity <Q>`
    - **Update**: `python3 scripts/commerce.py update-cart <slug> --gram <G> --quantity <Q>`
    - **Remove**: `python3 scripts/commerce.py remove-cart <slug> --gram <G>`
- **Validation**: Gram/variant values must be strictly chosen from the product's available options list.

### 5. Brand Information & Storytelling
**Goal**: Access brand identity and support data.
- **Logic**: Use the `brand-info` interface to retrieve narrative content.
- **Tooling**:
    - `python3 scripts/commerce.py brand-story`: Get the narrative/mission.
    - `python3 scripts/commerce.py company-info`: Get formal details.
    - `python3 scripts/commerce.py contact-info`: Get customer support channels.

---

## 🚀 Capabilities Summary

- **`search` / `list`**: Product discovery and inventory scan.
- **`get`**: Deep dive into product specifications, variants, and pricing.
- **`promotions`**: Current business rules, shipping thresholds, and active offers.
- **`cart`**: Complete session summary including VIP discounts and tax/shipping estimates.
- **`add-cart` / `update-cart` / `remove-cart`**: Atomic cart control.
- **`get-profile` / `update-profile`**: Personalization and fulfillment data.
- **`brand-story` / `company-info` / `contact-info`**: Brand context and support.
- **`orders`**: Real-time tracking and purchase history.

---

## 💻 CLI Configuration & Examples

```bash
# Setup
export COMMERCE_URL="https://api.yourbrand.com/v1"
export COMMERCE_BRAND_ID="brand_slug"

# Actions
python3 scripts/commerce.py list
python3 scripts/commerce.py search "item"
python3 scripts/commerce.py get <slug>
python3 scripts/commerce.py add-cart <slug> --gram <variant>
```

---

## 🤖 Troubleshooting & Debugging

- **Status Code 401**: Credentials missing or expired. Recommend `login`.
- **Status Code 404**: Resource not found. Verify `slug` via `search`.
- **Connection Error**: Verify `COMMERCE_URL` environment variable is correct and the endpoint is reachable.
