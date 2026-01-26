# Detection Rules Reference

## Recurring Charge Detection

A charge is considered recurring if:

### Frequency Rules
- Same normalized merchant appears >= 2 times in last 90 days
- Amounts are similar within `max(2.00, 0.05 * abs(amount))`
- Cadence matches one of:
  - Weekly: 5-9 days between charges
  - Monthly: 25-35 days between charges
  - Yearly: 330-400 days between charges

### Subscription Keywords
Automatic recurring detection for these merchants:
- NETFLIX, SPOTIFY, APPLE.COM/BILL, GOOGLE, ICLOUD
- ADOBE, MICROSOFT, DROPBOX, NOTION, SLACK
- OPENAI, CHATGPT, GITHUB, FIGMA
- HULU, DISNEY, HBO, PARAMOUNT, PEACOCK
- YOUTUBE, TWITCH, PATREON, SUBSTACK, MEDIUM
- ZOOM, ATLASSIAN, JIRA, ASANA, MONDAY
- AWS, AZURE, DIGITALOCEAN, HEROKU, VERCEL
- CANVA, GRAMMARLY, LASTPASS, 1PASSWORD
- NORDVPN, EXPRESSVPN, AUDIBLE, KINDLE
- PELOTON, STRAVA, HEADSPACE, CALM, DUOLINGO

## Unexpected Charge Detection

### 1. New Merchant (MEDIUM severity)
- First time seeing this merchant in history
- AND `abs(amount) > 30`
- Not in known recurring list

### 2. Amount Spike (HIGH severity)
- `abs(amount) > baseline * 1.8`
- AND `(amount - baseline) > 25`
- Baseline = average of last 20 charges from same merchant

### 3. Duplicate (HIGH severity)
- Same normalized merchant name
- Same amount (exact match)
- Within 0-2 days of each other

### 4. Fee-like (LOW severity)
- Description contains keywords:
  - FEE, COMMISSION, FX, ATM, OVERDRAFT, LATE
  - PENALTY, SERVICE CHARGE, MAINTENANCE
  - ANNUAL FEE, MONTHLY FEE, INTEREST
  - FINANCE CHARGE, CASH ADVANCE
  - FOREIGN TRANSACTION, WIRE TRANSFER
  - INSUFFICIENT FUNDS, NSF, RETURNED ITEM
- AND `abs(amount) > 3`

### 5. Currency Anomaly (LOW/MEDIUM severity)
- Transaction currency differs from main account currency
- Currency appears <= 2 times in statement
- MEDIUM if DCC indicators present:
  - DCC, DYNAMIC CURRENCY, CONVERSION FEE
  - EXCHANGE RATE, CURRENCY CONVERSION

### 6. Missing Refund (MEDIUM severity)
- Description contains dispute keywords:
  - DISPUTE, CHARGEBACK, UNAUTHORIZED, FRAUD
- No matching positive amount within 14 days
- Charge amount > 50

## Merchant Normalization

### Prefixes Removed
- POS, DEBIT, CREDIT, ACH, WIRE, CHECK
- PURCHASE, PAYMENT, TRANSFER, DEPOSIT
- CARD, VISA, MC, MASTERCARD, AMEX
- SQ *, SQUARE *, PAYPAL *, STRIPE, VENMO
- TST*, SP, DD

### Suffixes Removed
- Transaction IDs (6+ digit sequences)
- Reference numbers (REF #...)
- Location info (State + ZIP)
- Trailing asterisks and dashes

### Output
- Title case for readability
- Collapsed whitespace
