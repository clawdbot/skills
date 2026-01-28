```
  ╔══════════════════════════════════════╗
  ║   _____ __  __    _    ___ _         ║
  ║  | ____|  \/  |  / \  |_ _| |        ║
  ║  |  _| | |\/| | / _ \  | || |        ║
  ║  | |___| |  | |/ ___ \ | || |___     ║
  ║  |_____|_|  |_/_/   \_\___|_____|    ║
  ║                                      ║
  ║           Best Practices             ║
  ╚══════════════════════════════════════╝
```

# Email Best Practices Skill

A comprehensive agent skill for building production-ready email systems. Covers everything from DNS authentication to webhook processing, with a focus on deliverability, compliance, and reliability.

## Installation

```bash
npx skills add resend/email-best-practices
```

## What This Skill Covers

**Getting Started**
- Planning which emails your app needs (password reset, verification, order confirmations)
- Setting up email authentication (SPF, DKIM, DMARC) so emails reach inboxes

**Sending Emails**
- Transactional email design (subject lines, content structure, mobile-first)
- Marketing email best practices (consent, segmentation, unsubscribe)
- Compliance requirements by region (CAN-SPAM, GDPR, CASL)

**Production Infrastructure**
- Idempotency and retry logic to prevent duplicates
- Webhook processing for delivery events
- Suppression lists and list hygiene automation

## Structure

```
email-best-practices/
├── SKILL.md                             # Start here - routes to the right resource
└── resources/
    ├── deliverability.md                # SPF/DKIM/DMARC, sender reputation
    ├── transactional-emails.md          # Password resets, OTPs, confirmations
    ├── transactional-email-catalog.md   # Email combinations by app type
    ├── marketing-emails.md              # Newsletters, campaigns, consent
    ├── email-capture.md                 # Validation, verification, opt-in
    ├── compliance.md                    # CAN-SPAM, GDPR, CASL
    ├── email-types.md                   # Transactional vs marketing
    ├── sending-reliability.md           # Idempotency, retry logic, errors
    ├── webhooks-events.md               # Delivery events, webhook setup
    └── list-management.md               # Suppression lists, hygiene
```

## Quick Start

Open `SKILL.md` - it has a routing table that directs you to the right resource based on what you need to do.

## License

MIT
