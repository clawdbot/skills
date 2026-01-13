---
name: shared-memory
description: Share memories and state with other users. Use when user wants to share knowledge, create users/groups, grant permissions, set up family or team sharing, subscribe to memory changes, or manage access control on their memory knowledge base. This shared memory skill uses Ensue - a shared memory network for agents.
---

# Shared Memory

Share memories from your knowledge base with other users. Manage users, groups, and fine-grained permissions on namespaces.

## Quick Start

Use the wrapper script at `{baseDir}/scripts/shared-memory.sh` for all sharing operations.

```bash
# Create a user
{baseDir}/scripts/shared-memory.sh create-user alice

# Create a group and add user
{baseDir}/scripts/shared-memory.sh create-group family
{baseDir}/scripts/shared-memory.sh add-member family alice

# Grant the group access to a namespace
{baseDir}/scripts/shared-memory.sh grant group family read christine/shared/
{baseDir}/scripts/shared-memory.sh grant group family update christine/shared/
```

## Core Concepts

**Users**: Individual identities that can be granted access
**Groups**: Collections of users (e.g., "family", "team", "editors")
**Permissions**: Access rights (read/create/update/delete) on key patterns
**Key patterns**: Namespace prefixes that match all keys underneath (e.g., `christine/shared/` matches all keys under that path)

## Namespace Organization

Always organize namespaces with this hierarchy:

```
<username>/                    # Top level: user identity
├── private/                   # Only this user
│   ├── sessions/              # Learning sessions, logs
│   ├── notes/                 # Personal scratchpad
│   └── <project>/             # Private project work
├── shared/                    # Shared with others (family, team)
│   ├── recipes/
│   ├── shopping-list
│   ├── travel/
│   │   └── japan-2026/
│   └── <project>/
│       └── <subproject>/
└── public/                    # Shareable knowledge (read-only to others)
    ├── concepts/
    │   ├── computing/
    │   └── networking/
    └── toolbox/
```

**Rules:**
1. Username at top level (e.g., `christine/`, `mark/`)
2. Second level is access scope: `private/`, `shared/`, `public/`
3. Deeper levels are project-based, becoming more specific

This structure makes sharing intuitive:
- Grant access to `mark/shared/` → all shared content
- Grant access to `mark/shared/recipes/` → just recipes
- Grant access to `mark/public/` → read-only knowledge

## Common Workflows

### Couple/Family Sharing

Set up shared namespaces between family members:

```bash
# 1. Create user for partner
{baseDir}/scripts/shared-memory.sh create-user mark

# 2. Create family group
{baseDir}/scripts/shared-memory.sh create-group family
{baseDir}/scripts/shared-memory.sh add-member family mark

# 3. Grant family access to each other's shared/ namespace
{baseDir}/scripts/shared-memory.sh grant group family read christine/shared/
{baseDir}/scripts/shared-memory.sh grant group family create christine/shared/
{baseDir}/scripts/shared-memory.sh grant group family update christine/shared/
{baseDir}/scripts/shared-memory.sh grant group family delete christine/shared/

# 4. Do the same for mark's shared namespace
{baseDir}/scripts/shared-memory.sh grant group family read mark/shared/
{baseDir}/scripts/shared-memory.sh grant group family create mark/shared/
{baseDir}/scripts/shared-memory.sh grant group family update mark/shared/
{baseDir}/scripts/shared-memory.sh grant group family delete mark/shared/
```

Result:
```
christine/
├── private/       -> Only Christine
├── shared/        -> Family can access
└── public/        -> Christine's knowledge

mark/
├── private/       -> Only Mark
├── shared/        -> Family can access
└── public/        -> Mark's knowledge
```

### Team Sharing

Share project context with collaborators:

```bash
# Create users
{baseDir}/scripts/shared-memory.sh create-user alice
{baseDir}/scripts/shared-memory.sh create-user bob

# Create team group
{baseDir}/scripts/shared-memory.sh create-group dev-team
{baseDir}/scripts/shared-memory.sh add-member dev-team alice
{baseDir}/scripts/shared-memory.sh add-member dev-team bob

# Grant access to a shared project namespace
{baseDir}/scripts/shared-memory.sh grant group dev-team read christine/shared/acme-project/
{baseDir}/scripts/shared-memory.sh grant group dev-team update christine/shared/acme-project/
```

### Share Read-Only Knowledge

Let someone read your public concepts without editing:

```bash
{baseDir}/scripts/shared-memory.sh grant user mark read christine/public/
```

### Subscribe to Changes

Get notified when shared memories change:

```bash
# Subscribe to shopping list updates
{baseDir}/scripts/shared-memory.sh subscribe christine/shared/shopping-list

# List your subscriptions
{baseDir}/scripts/shared-memory.sh list-subscriptions

# Unsubscribe
{baseDir}/scripts/shared-memory.sh unsubscribe christine/shared/shopping-list
```

## Command Reference

### User Management

| Command | Description |
|---------|-------------|
| `create-user <username>` | Create a new user |
| `delete-user <username>` | Delete a user |

### Group Management

| Command | Description |
|---------|-------------|
| `create-group <name>` | Create a new group |
| `delete-group <name>` | Delete a group |
| `add-member <group> <user>` | Add user to group |
| `remove-member <group> <user>` | Remove user from group |

### Permission Management

| Command | Description |
|---------|-------------|
| `grant org <action> <pattern>` | Grant to entire organization |
| `grant user <name> <action> <pattern>` | Grant to specific user |
| `grant group <name> <action> <pattern>` | Grant to group |
| `revoke <grant_id>` | Revoke a permission grant |
| `list` | List all permission grants |
| `list-permissions` | List current user's effective permissions |

**Actions**: `read`, `create`, `update`, `delete`

**Patterns**: Namespace prefix (e.g., `christine/shared/` matches all keys starting with that path)

### Subscriptions

| Command | Description |
|---------|-------------|
| `subscribe <key>` | Get notified on changes |
| `unsubscribe <key>` | Stop notifications |
| `list-subscriptions` | List active subscriptions |

## Use Cases

### Two Agents, One Knowledge Base

Instead of completely separate knowledge bases, share specific namespaces:

- **Christine's agent**: Full access to `christine/`
- **Mark's agent**: Full access to `mark/`, plus access to `christine/shared/`

Both can:
- Add to shared shopping list
- Plan travel together
- Share household info

Each keeps private:
- Personal learning sessions
- Private notes
- Individual preferences

### Proactive Knowledge Sharing

When you learn something useful, share it:

```
You: "Save this concept about Docker to my shared folder so Mark can see it too"
Agent: [Saves to christine/shared/concepts/docker, Mark's agent can now reference it]
```

### Collaborative Projects

Team members' agents all see the same project context:

```
christine/shared/webapp-project/
├── decisions/       -> Why we chose React
├── architecture/    -> System design
└── conventions/     -> Code patterns
```

When any team member asks their agent about the project, it has full context.
