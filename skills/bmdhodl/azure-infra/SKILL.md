---
name: azure-infra
description: Chat-based Azure infrastructure assistance using Azure CLI and portal context. Use for querying, auditing, and monitoring Azure resources (VMs, Storage, IAM, Functions, AKS, App Service, Key Vault, Azure Monitor, billing, etc.), and for proposing safe changes with explicit confirmation before any write/destructive action.
---

# Azure Infra

## Overview
Use the local Azure CLI to answer questions about Azure resources. Default to read‑only queries. Only propose or run write/destructive actions after explicit user confirmation.

## Quick Start
1. Ensure login: `az account show` (if not logged in, run `az login --use-device-code`).
2. If multiple subscriptions exist, ask the user to pick one; otherwise use the default subscription.
3. Use read‑only commands to answer the question.
4. If the user asks for changes, outline the exact command and ask for confirmation before running.

## Safety Rules (must follow)
- Treat all actions as **read‑only** unless the user explicitly requests a change **and** confirms it.
- For any potentially destructive change (delete/terminate/destroy/modify/scale/billing/IAM credentials), require a confirmation step.
- Prefer `--dry-run` when available and show the plan before execution.
- Never reveal or log secrets (keys, client secrets, tokens).

## Task Guide (common requests)
- **Inventory / list**: use `list`/`show`/`get` commands.
- **Health / errors**: use Azure Monitor metrics/logs queries.
- **Security checks**: RBAC roles, public storage, NSG exposure, Key Vault access.
- **Costs**: Cost Management (read‑only).
- **Changes**: show exact CLI command and require confirmation.

## Subscription & Tenant Handling
- If the user specifies a subscription/tenant, honor it.
- Otherwise use the default subscription from `az account show`.
- When results are subscription‑scoped, state the subscription used.

## References
See `references/azure-cli-queries.md` for common command patterns.

## Assets
- `assets/icon.svg` — custom icon (dark cloud + terminal prompt, Azure‑blue accent)
