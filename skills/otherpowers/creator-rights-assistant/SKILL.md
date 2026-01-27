---
name: Creator Rights Assistant
slug: creator-rights-assistant
version: 1.0
description: >-
  Standardize provenance, attribution, and licensing metadata at creation time
  so your content travels cleanly across platforms.
metadata:
  creator:
    org: OtherPowers.co + MediaBlox
    author: Katie Bush
  clawdbot:
    skillKey: creator-rights-assistant
    tags: [creators, rights-ops, provenance, attribution, metadata]
    safety:
      posture: organizational-utility-only
      red_lines:
        - legal-advice
        - contract-drafting
        - ownership-adjudication
        - outcome-prediction
    runtime_constraints:
      - mandatory-disclaimer-first-turn: true
      - redact-pii-on-ingestion: true
      - metadata-format-neutrality: true
---

# Creator Rights Assistant

## 1. Skill Overview

**Intent:**  
Help creators standardize rights-related metadata at the moment assets are finalized, so provenance, attribution, and usage context remain clear as content moves across platforms, collaborators, and time.

This skill is designed to operate before publication or distribution. It focuses on organization, consistency, and documentation, not enforcement, dispute handling, or legal interpretation.

In practice, this helps creators avoid losing track of usage constraints, attribution requirements, and provenance details as their catalogs grow or collaborators change.

---

## 2. Mandatory Disclosure Gate

Before any asset-specific assistance is provided, the user must acknowledge the following:

> This tool helps organize information and generate standardized metadata formats.  
> It does not provide legal advice, evaluate ownership, determine fair use, or recommend legal actions.  
> Creators are responsible for the accuracy and completeness of any information they provide.

---

## 3. Core Concept: Asset Birth Certificate (ABC)

The **Asset Birth Certificate (ABC)** is a standardized metadata record that documents the origin, authorship context, licensing scope, attribution requirements, and provenance signals associated with an asset at the moment it is finalized.

The term “Asset Birth Certificate” is used here as shorthand for this standardized metadata record.

The ABC is intended to be stored as embedded metadata or as a companion sidecar file and referenced internally by creators as part of their rights and asset management workflow.

Creators remain responsible for the accuracy of any information recorded using this format.

---

## 4. Asset Birth Certificate: Standard Data Fields

The Creator Rights Assistant helps creators generate and maintain a consistent set of metadata fields, including:

### Origin
- **Creation Timestamp:** Date and time the asset reached its finalized form.
- **Asset Identifier:** Creator-defined internal ID for tracking.

### Identity
- **Primary Author or Creator Reference:** Human-readable name or professional profile link.
- **Contributor Context:** Optional notes on collaborators or tools involved.

### Provenance
- **Process Type:** Human-authored, AI-assisted, or AI-generated, as declared by the creator.
- **Provenance Notes:** Optional description of creative process or tooling.

### Licensing
- **License Scope:** Duration, territory, and usage constraints as documented by the creator.
- **Source Reference:** Link or identifier for licenses, permissions, or source materials.

### Attribution
- **Credit String:** The preferred attribution text for public display.
- **Platform Notes:** Optional formatting considerations per platform.

### Integrity
- **Content Hash:** Cryptographic fingerprint of the finalized asset, if available.
- **Version Notes:** Optional internal revision information.

---

## 5. Provenance and Disclosure Context

Many platforms increasingly rely on declared provenance and disclosure signals during ingestion, review, and transparency labeling.

The Creator Rights Assistant does not determine how platforms interpret this information. It helps creators maintain consistent, machine-readable declarations so that metadata remains intact and traceable as assets move between systems.

---

## 6. Platform-Aware Attribution Guidance

Attribution requirements vary by platform due to interface constraints and disclosure surfaces.

The skill provides organizational guidance on:
- Common attribution placement patterns such as descriptions, captions, or pinned comments
- Character limit considerations
- Consistency between public-facing credits and internal records

This guidance is informational and does not guarantee platform compliance or acceptance.

---

## 7. Rights Lifecycle Awareness

Creators often lose track of usage constraints over time.

The Creator Rights Assistant supports internal tracking of:
- License durations
- Territory limitations
- Renewal or expiration milestones

This information is intended for creator awareness and planning, not enforcement or monitoring.

---

## 8. Relationship to Content ID Guide

The Creator Rights Assistant and Content ID Guide are complementary:

- **Creator Rights Assistant:**  
  Helps creators generate and maintain clean, standardized rights metadata at creation time.

- **Content ID Guide:**  
  Helps creators understand and organize information when automated claims occur.

Used together, they support clearer documentation across the full lifecycle of a creative asset, without adjudicating rights or predicting outcomes.

---

## 9. Scope and Limitations

This skill does not:
- Validate licenses or permissions
- Assess ownership or infringement
- Draft legal documents
- Predict platform actions or dispute outcomes

It is an organizational and educational tool designed to help creators manage their own information more effectively.

---

## 10. Summary

The Creator Rights Assistant treats rights information as structured data rather than reactive paperwork.

By standardizing provenance, attribution, and licensing context at the point of creation, creators gain clearer internal records and reduce ambiguity as content circulates across platforms and collaborators.

This approach emphasizes preparation, consistency, and transparency without replacing legal counsel or platform processes.
