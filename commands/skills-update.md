---
name: skills-update
description: Update an installed skill to the latest version from GitHub. Reinstalls the skill with new changes.
allowed-tools: "Bash(python scripts/install_skill.py:*)"
---

# Update a Skill

Update an installed skill to the latest version from GitHub.

## Usage

```
/skills update <skill_name>
```

## Arguments

- `skill_name` - Name of skill to update

## Examples

```
/skills update pdf
/skills update skill-creator
```

## Implementation

When user requests to update a skill:

1. Run: `python scripts/install_skill.py <skill_name> --force`
2. Script downloads latest version from GitHub
3. Validates the updated skill
4. Replaces files in `skills/<skill_name>/`
5. Updates symlink in `plugin-skills/<skill_name>/`
6. Updates `data/installed-skills.json`
7. Skill reflects latest changes immediately

## Output Format

```
🔄 Updating 'pdf' to latest version...

📥 Downloading 'pdf' from GitHub...
   Repo: anthropics/skills
   Path: skills/pdf
   Branch: main

🔍 Validating downloaded skill...
✅ Validation passed

✅ Created symbolic link in plugin-skills/ for Claude Code discovery

✅ Successfully installed 'pdf'
   Location: skills/pdf

✅ Skill 'pdf' has been updated!
```

## What Gets Updated

- All skill files from the GitHub repository
- SKILL.md (instructions and metadata)
- Supporting scripts, references, and assets
- Symbolic link to plugin-skills/

## What Doesn't Change

- Installation path
- Skill name
- Registry configuration

## Error Handling

- **Skill not installed**
  - Display error that skill is not installed
  - Suggest installing with `/skills install`

- **Update failed**
  - Display GitHub API error
  - Offer to retry or keep current version

- **Validation failed**
  - New version has invalid structure
  - Keep old version, don't update
  - Display validation errors

## Automatic Updates

Currently, skills must be manually updated.

Future versions may support:
- Automatic update checking
- Batch updates (`/skills update --all`)
- Update notifications

## Rollback

If an update breaks a skill, you can reinstall the previous version:

1. Check git history of the skill's repository
2. Find the commit hash of the working version
3. Reinstall from that commit (not yet supported)

Or manually restore from backup if you have one.
