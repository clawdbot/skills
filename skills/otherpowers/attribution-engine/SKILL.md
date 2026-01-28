---
name: Attribution Engine
slug: attribution-engine
version: 1.2
description: >-
  Helps creators clearly credit collaborators, tools, and partners in a way
  platforms understand. Reduces confusion, missed disclosures, and avoidable
  issues before content goes live.
metadata:
  creator:
    org: OtherPowers.co + MediaBlox
    author: Katie Bush
  clawdbot:
    skillKey: attribution-engine
    tags: [attribution, transparency, provenance, creators, platforms]
    safety:
      posture: organizational-utility-only
      red_lines:
        - legal-advice
        - ownership-determination
        - risk-scoring
        - enforcement-guarantees
        - bypass-instructions
    runtime_constraints:
      - mandatory-disclaimer-first-turn: true
      - platform-aware-output: true
      - source-grounded-definitions: true
---

# Attribution Engine

## 1. What this skill does

Attribution Engine helps creators prepare clear, platform-aware credits and
disclosures before publishing.

It focuses on **clarity**, **consistency**, and **platform alignment**, so your
work travels cleanly across feeds, remixes, and reposts without unnecessary
confusion later.

This skill does not tell you what you are legally required to do.  
It helps you organize and format information using each platform’s own rules.

---

## 2. Important note before we begin

Before using this skill, you will see a short notice:

> This tool helps format attribution and disclosure information using publicly
> available platform guidance.  
> It does not provide legal advice, determine compliance, or guarantee outcomes.
> You remain responsible for how and where content is published.

---

## 3. Why attribution matters in 2026

Attribution is no longer just courtesy.

Platforms now use attribution and disclosure signals to decide:
- how content is labeled
- how far it travels
- whether it is limited, flagged, or reviewed

Small mismatches, like forgetting a native toggle or using the wrong AI label,
can quietly reduce reach or trigger reviews.

This skill helps you catch those issues early.

---

## 4. Core concepts (plain language)

### Attribution
Who should be credited publicly for the work.

Example:
- Performer
- Producer
- Visual artist
- Brand partner
- Tool or system used

### Disclosure
Whether viewers need to be told something important about how the content was
made or funded.

Examples:
- AI-assisted editing
- Synthetic or altered media
- Paid or gifted brand relationships

### Provenance
How the content came into being.

Examples:
- Fully human-authored
- Human-authored with AI assistance
- Fully AI-generated

---

## 5. Human vs AI labels (avoiding over-labeling)

Not all AI use is the same.

Over-labeling simple edits as “AI-generated” can cause platforms to treat your
work as low-effort or mass-produced.

This skill helps distinguish between:

- **AI-Generated**  
  Content created autonomously by a system with no meaningful human editorial
  control.

- **Human-Authored, AI-Assisted**  
  Content where a person made the creative decisions and used tools for help
  such as cleanup, mastering, or compositing.

Example:
> “Human-authored with AI-assisted mastering.”

This helps preserve trust without self-demotion.

---

## 6. Commercial relationships and brand credits

Hashtags alone are no longer enough.

If a post involves a material connection, such as:
- sponsorship
- gifted products
- affiliate links
- paid usage

most platforms expect you to use their **native branded content tools**.

This skill will:
- flag when attribution suggests a commercial relationship
- remind you to enable the platform’s built-in partnership or branded toggle

Example warning you may see:
> This credit appears promotional. Make sure the platform’s native paid
> partnership setting is enabled before publishing.

---

## 7. Platform-aware formatting

Each platform treats attribution differently.

The Attribution Engine adapts output based on:
- character limits
- “read more” cutoffs
- native labels and toggles
- visible vs hidden metadata

Supported platforms include:
- YouTube
- TikTok
- Instagram
- Spotify
- YouTube Music
- SoundCloud
- Tidal
- Netflix
- Amazon Music

You can also name any other platform. The skill will reference that platform’s
current public documentation when available.

---

## 8. Metadata does not always survive uploads

Many platforms strip file metadata during upload.

To reduce loss:
- the skill can generate a **visible attribution string** for captions or
  descriptions
- and a **reference ID** you can keep internally

Example visible string:
> Ref OP-2026-ALPHA | Auth R. Mutt | Human-AI Collaborative

This helps attribution survive reposts and re-uploads.

---

## 9. Collaborators and consent clarity

Attribution records are not contracts.

Listing collaborators here:
- does not define ownership
- does not imply revenue splits
- does not replace agreements

This skill treats attribution as **documentation**, not legal representation.

---

## 10. How this fits with other skills

Attribution Engine works best alongside:

- **Creator Rights Assistant**  
  Organizes rights, licenses, and internal records at creation time.

- **Content ID Guide**  
  Helps you understand and organize information when automated claims appear.

Together, they support a calmer, more predictable content lifecycle.

---

## 11. What this skill does not do

This skill does not:
- validate licenses
- determine ownership
- predict platform actions
- guarantee reach or safety
- advise on how to bypass systems

It exists to reduce avoidable mistakes and save time.

---

## 12. Simple example

**Input:**  
Video with original music, light AI color correction, and a gifted product.

**Output:**  
- Suggested credit string for YouTube description
- Reminder to enable branded content toggle
- Human-authored, AI-assisted disclosure language
- Platform-specific formatting notes

No guessing. No legal claims. Just clarity.

---

## 13. Summary

Attribution Engine helps creators explain their work clearly in the language
platforms expect.

It reduces confusion, protects context, and supports transparency without
over-labeling or over-promising.

Clean inputs lead to calmer outcomes.


