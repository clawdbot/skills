---
name: paypal
description: PayPal payment integration. Send money, create invoices, and manage PayPal transactions.
metadata: {"clawdbot":{"emoji":"🅿️","always":true,"requires":{"bins":["curl","jq"]},"primaryEnv":"PAYPAL_CLIENT_ID"}}
---

# PayPal 🅿️

PayPal payment platform integration.

## Setup

```bash
export PAYPAL_CLIENT_ID="your_client_id"
export PAYPAL_SECRET="your_secret"
```

## Features

- Send payments
- Create invoices
- Request money
- Transaction history
- Refunds

## Usage Examples

```
"Send $25 to user@email.com via PayPal"
"Create PayPal invoice for $100"
"Show my PayPal balance"
```
