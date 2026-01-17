---
name: incident-pcn-evidence-appeal-corrective-actions-uk
description: Builds incident/PCN evidence packs with timelines, appeal drafts, corrective actions, and follow-up monitoring. USE WHEN handling PCNs or incidents needing documentation.
---

# Incident & PCN Handling Pack (UK)

## PURPOSE
Turn incident/PCN inputs into an evidence pack: clean manager brief, timeline, appeal cover draft, corrective actions, and follow-up monitoring.

## WHEN TO USE
- “Build a PCN appeal pack using CCTV and timeline notes.”
- “Summarise these incident notes into a clean manager brief.”
- “Create corrective actions and follow-up monitoring for this incident.”

DO NOT USE WHEN…
- The request is general driving advice or admin tasks (invoice chasing, calendar, IT support).
- No artefact is requested and details are too vague.

## INPUTS
- REQUIRED:
  - Incident/PCN basics: date/time, location, vehicle reg, driver, allegation/contravention
  - Evidence list (CCTV, photos, telematics, delivery notes, correspondence, portal screenshots)
  - Any deadlines (appeal window)
- OPTIONAL:
  - Existing timeline notes, witness statements, customer communications
  - Internal policy/SOP excerpts for corrective actions (paste text)
- EXAMPLES:
  - “PCN: bus lane; CCTV link notes; delivery timestamp proof; need appeal pack.”

## OUTPUTS
- `incident-manager-brief.md`
- `timeline.md`
- `appeal-pack-cover.md` (Word-ready)
- `corrective-actions.md`
- `follow-up-monitoring.md` (Excel-ready)
- Success criteria:
  - Clear chronology and evidence references
  - Appeal pack is factual and consistent with evidence
  - Corrective actions have owners and review dates

## WORKFLOW
1. Confirm whether this is a **PCN appeal**, an **internal incident**, or both.
   - IF unclear → **STOP AND ASK THE USER**.
2. Build manager brief using `assets/incident-manager-brief-template.md`.
3. Construct a timeline using `assets/timeline-template.md`.
   - IF key dates/times are missing → **STOP AND ASK THE USER** for them.
4. Evidence capture standard:
   - Apply `references/evidence-capture-standard.md` (label, store location, integrity notes).
5. Draft appeal cover using `assets/appeal-pack-cover-template.docx-ready.md`.
   - Keep factual; cite evidence refs; avoid speculative claims.
6. Propose corrective actions and monitoring using `assets/follow-up-monitoring-template.md`.
7. If asked to edit existing packs → **ASK FIRST**.

## OUTPUT FORMAT
```text
# timeline.md
| Date/time | Event | Source/evidence ref | Notes |
|----------|-------|----------------------|------|
```

## SAFETY & EDGE CASES
- Don’t fabricate evidence or outcomes.
- If evidence is weak or contradictory, present it as “unconfirmed” and list gaps.

## EXAMPLES
- Input: “PCN appeal with CCTV and notes”
  - Output: brief + timeline + appeal cover + actions + monitoring tracker
