# Refund Template Reference

Templates are generated for HIGH and MEDIUM severity flags only.
All templates avoid apostrophes per spec.

## Template Types

### Email
Full formal email with subject line. Best for:
- First contact with merchant
- Documentation trail
- Larger amounts

### Chat
Short message for live support. Best for:
- Quick resolution
- Real-time support
- Smaller amounts

### Dispute
Formal bank dispute form text. Best for:
- Unauthorized charges
- Failed merchant resolution
- Fraud cases

## Tone Variants

### Concise (default)
- Direct and professional
- States facts clearly
- Requests action politely

### Firm
- Assertive language
- References consumer rights
- Sets deadlines
- Mentions escalation options

### Friendly
- Warm and polite
- Assumes good faith
- Asks for help
- Thanks in advance

## Template Placeholders

Templates include these placeholders for user to fill:

| Placeholder | Description |
|------------|-------------|
| `[YOUR NAME]` | Customer name |
| `[CARD ENDING IN XXXX]` | Last 4 digits of card |
| `[YOUR PHONE NUMBER]` | Contact phone |
| `[IF AVAILABLE]` | Reference number if known |

## Reason Text by Flag Type

### Duplicate
> This appears to be a duplicate charge. I was charged twice for the same transaction.

### Amount Spike
> This charge is significantly higher than my usual charges with this merchant. I believe there may be a billing error.

### New Merchant
> I do not recognize this merchant and did not authorize this transaction.

### Fee-like
> This fee was not disclosed or agreed upon. I am requesting a refund of this charge.

### Currency Anomaly
> This transaction was processed in an unexpected currency. I may have been subject to unauthorized currency conversion.

### Missing Refund
> I previously disputed this charge but have not received the refund. I am following up on this matter.

## Dispute Categories

| Flag Type | Dispute Category |
|-----------|-----------------|
| Duplicate | Duplicate Transaction |
| Amount Spike | Incorrect Amount Charged |
| New Merchant | Unauthorized Transaction / Fraud |
| Fee-like | Unauthorized Fee |
| Currency Anomaly | Currency/Conversion Error |
| Missing Refund | Refund Not Received |

## Example Email (Concise)

```
Subject: Refund Request - $29.99 charge on January 12, 2026

Hello,

I am requesting a refund for the following transaction:

Merchant: Amazon
Amount: $29.99
Date: January 12, 2026

Reason: This appears to be a duplicate charge. I was charged twice for the same transaction.

Please process this refund at your earliest convenience.

Thank you.
```

## Example Chat (Firm)

```
I need to dispute a charge immediately. $29.99 from Amazon on January 12, 2026. This is a duplicate charge. I need this refunded today or I will file a formal dispute.
```

## Example Dispute (Friendly)

```
Hi,

I would like to file a dispute for a charge on my account.

Here are the details:
- Merchant: Amazon
- Amount: $29.99
- Date: January 12, 2026
- My card ends in: [XXXX]

Reason for dispute: Duplicate Transaction

What happened: This appears to be a duplicate charge. I was charged twice for the same transaction.

I would appreciate it if you could look into this and help me get a refund. Please let me know if you need any additional information from me.

Thank you for your help!

[YOUR NAME]
[YOUR PHONE NUMBER]
```
