---
name: skills-list
description: List all installed skills with their status, validation, and metadata. Shows installation path, source, and validity check.
allowed-tools: "Bash(python scripts/list_skills.py:*)"
---

# List Installed Skills

Display all installed skills with their current status.

## Usage

```
/skills list [options]
```

## Options

- `--validate` - Re-validate all skills and show detailed errors
- `--json` - Output as JSON (machine-readable)

## Examples

```
/skills list
/skills list --validate
/skills list --json
```

## Implementation

When user requests to list installed skills:

1. Run: `python scripts/list_skills.py [options]`
2. Script queries `data/installed-skills.json`
3. Displays skills with validation status
4. Shows installation path, source, and validity

## Output Format

```
📦 Installed Skills (2):

1. 📦 pdf
   📁 Path: skills/pdf
   📅 Installed: 2026-01-03 01:00
   🔗 Source: github (anthropics/skills)
   ✅ Valid

2. 📦 docx
   📁 Path: skills/docx
   📅 Installed: 2026-01-03 01:05
   🔗 Source: github (anthropics/skills)
   ✅ Valid
```
