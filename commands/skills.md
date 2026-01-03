---
name: skills
description: Main dispatcher for Skills Store commands. Manage Claude Skills lifecycle - search, install, list, uninstall, update skills from the centralized registry of 21+ skills.
---

# Skills Store

Manage Claude Skills from the centralized registry.

## Usage

```
/skills <subcommand> [options]
```

## Subcommands

- **list** - List installed skills with validation status
- **search** - Search for skills by name, description, or tags
- **install** - Install a skill from the registry
- **uninstall** - Remove an installed skill
- **update** - Update an installed skill to latest version
- **info** - Show detailed information about a skill

## Examples

```
/skills list
/skills search "pdf"
/skills install pdf
/skills uninstall pdf
/skills update pdf
/skills info pdf
```

## Quick Reference

Run any subcommand for detailed help:

```
/skills list --help
/skills search --help
/skills install --help
```

See [README.md](../README.md) for complete documentation.
