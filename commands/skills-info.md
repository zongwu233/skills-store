---
name: skills-info
description: Show detailed information about a skill including description, source, metadata, and SKILL.md preview.
allowed-tools: "Bash(python scripts/show_skill_info.py:*)"
---

# Show Skill Information

Display detailed information about a skill from the registry or an installed skill.

## Usage

```
/skills info <skill_name>
```

## Arguments

- `skill_name` - Name of skill to show information for

## Examples

```
/skills info pdf
/skills info skill-creator
/skills info frontend-design
```

## Implementation

When user requests skill information:

1. Run: `python scripts/show_skill_info.py <skill_name>`
2. Script looks up skill in registry or installed skills
3. Displays comprehensive information including:
   - Name and description
   - Author and license
   - Source repository and path
   - Tags and category
   - Installation status (if installed)
   - SKILL.md preview (first 30 lines)
   - File structure

## Output Format

```
📄 Skill Information: pdf

Description:
Comprehensive PDF manipulation toolkit for extracting text and tables,
creating new PDFs, merging/splitting documents, and filling forms.

Source:
  Type: github
  Repository: anthropics/skills
  Path: skills/pdf
  Branch: main
  URL: https://github.com/anthropics/skills

Metadata:
  Author: Anthropic
  License: MIT
  Tags: document, pdf, manipulation, forms
  Category: document

Installation Status:
  ✅ Installed
  Location: skills/pdf
  Installed: 2026-01-03 01:00:00
  Valid: Yes

SKILL.md Preview (first 30 lines):
---
name: pdf
description: |
  Comprehensive PDF manipulation toolkit...
---

# PDF Skill

... [rest of preview]

Files:
  SKILL.md
  scripts/extract.py
  scripts/merge.py
  references/pdf-guide.md
```

## Use Cases

- **Before installing**: Preview what the skill does
- **Troubleshooting**: Check installed version and validation status
- **Discovering skills**: Understand skill capabilities
- **Comparing skills**: Compare metadata between skills

## Error Handling

- **Skill not found in registry**
  - Display error message
  - Suggest running `/skills search` to find available skills

- **Skill not installed** (when querying installed skills)
  - Show information from registry
  - Indicate that skill is not installed
  - Offer to install it

## Related Commands

- `/skills search` - Find skills by name, description, or tags
- `/skills list` - List all installed skills
- `/skills install` - Install a skill after reviewing info
