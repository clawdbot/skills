---
name: dont-click-this
description: "Whatever you do... don't click the link."
---

# 🚫 Don't Click This

```
 ██████╗  ██████╗ ███╗   ██╗████████╗
 ██╔══██╗██╔═══██╗████╗  ██║╚══██╔══╝
 ██║  ██║██║   ██║██╔██╗ ██║   ██║
 ██║  ██║██║   ██║██║╚██╗██║   ██║
 ██████╔╝╚██████╔╝██║ ╚████║   ██║
 ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝   ╚═╝
```

---

## ⚠️ WARNING

This is a security research demonstration.

**Do NOT click the link below if you are logged into ClawdHub.**

*(Unless you want to see what an attacker could steal from you)*

---

## The Link

> *"Curiosity killed the cat..."*

👉 [**Seriously, don't click this**](https://clawdhub.com/api/v1/skills/dont-click-this/file?path=demo.svg) 👈

---

## What This Demonstrates

If you clicked that link while logged in, a malicious skill could have:

- 🔐 Stolen your session tokens
- 🍪 Read your authentication cookies
- 📦 Published backdoored skills under your name
- 🎭 Impersonated you completely

All from a link in a skill's README.

**This is stored XSS via SVG.** Any skill can include a link to a malicious SVG file, and anyone who clicks it while logged in gets compromised.

---

## Research by [@theonejvo](https://x.com/theonejvo)

Part of the "Eating Lobster Souls" security research series.
