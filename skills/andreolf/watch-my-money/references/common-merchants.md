# Common Merchant Mappings

Override rules for merchants that are hard to auto-categorize.

## Swiss Merchants

| Merchant Pattern | Category | Notes |
|-----------------|----------|-------|
| COOP, COOP CITY | groceries | Swiss supermarket chain |
| MIGROS, M-BUDGET | groceries | Swiss supermarket chain |
| DENNER | groceries | Discount supermarket |
| ALDI SUISSE | groceries | Discount supermarket |
| LIDL | groceries | Discount supermarket |
| MANOR | shopping | Department store (not Manor Food) |
| MANOR FOOD | groceries | Food section of Manor |
| SBB, CFF, FFS | transport | Swiss Federal Railways |
| POSTFINANCE | transfers | Swiss postal bank |
| TWINT | transfers | Swiss mobile payment |
| SWISSCOM | utilities | Telecom |
| SUNRISE | utilities | Telecom |
| SALT | utilities | Telecom |
| EWZ | utilities | Zurich electricity |
| CSS, HELSANA, SWICA | health | Health insurance |
| CEMBRA | other | Credit card fees |

## International Merchants

| Merchant Pattern | Category | Notes |
|-----------------|----------|-------|
| AMAZON | shopping | Unless clearly groceries |
| APPLE.COM/BILL | subscriptions | App Store, iCloud, etc |
| GOOGLE *SERVICES | subscriptions | Google One, YouTube Premium |
| PAYPAL *SPOTIFY | subscriptions | Spotify via PayPal |
| NETFLIX.COM | subscriptions | Streaming |
| UBER, UBER EATS | transport OR eating_out | Check amount: <20 = transport |
| BOOKING.COM | travel | Hotels |
| AIRBNB | travel | Accommodation |
| RYANAIR, EASYJET | travel | Budget airlines |

## Ambiguous Merchants

These need user confirmation:

| Merchant | Could Be | Disambiguation |
|----------|----------|----------------|
| STARBUCKS | eating_out OR groceries | In-store = eating_out, beans = groceries |
| IKEA | shopping OR eating_out | Check amount: >50 = shopping |
| GAS STATION | transport OR groceries | Shop purchases vs fuel |
| PHARMACY | health OR groceries | Meds = health, toiletries = groceries |

## Adding Overrides

When user categorizes a merchant, save to state:

```bash
python -m watch_my_money set-merchant "WEIRD MERCHANT NAME" --category shopping
```

Or interactively during `analyze`:
```
Unknown merchant: ACME CORP (3 transactions, 450 CHF)
Category? [groceries/shopping/other/skip]: shopping
→ Saved override for future runs
```
