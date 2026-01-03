---
name: skills-uninstall
description: Uninstall an installed skill and remove it from Claude Code discovery. Removes symlink and skill files.
allowed-tools: "Bash(python scripts/uninstall_skill.py:*)"
---

# Uninstall a Skill

Remove an installed skill from the system.

## Usage

```
/skills uninstall <skill_name>
```

## Arguments

- `skill_name` - Name of skill to uninstall

## Examples

```
/skills uninstall pdf
/skills uninstall my-custom-skill
```

## Implementation

When user requests to uninstall a skill:

1. Run: `python scripts/uninstall_skill.py <skill_name>`
2. Script checks if skill is installed
3. Removes symlink from `plugin-skills/<skill_name>/`
4. Removes skill files from `skills/<skill_name>/`
5. Updates `data/installed-skills.json`
6. Skill is no longer available to Claude Code

## Output Format

```
🗑️  Uninstalling 'pdf'...

🔗 Removing symlink from plugin-skills/...
✅ Removed symlink: plugin-skills/pdf

🗑️  Removing skill files from skills/...
✅ Removed skills/pdf

📝 Updating installed skills registry...
✅ Removed 'pdf' from registry

✅ Successfully uninstalled 'pdf'
```

## Error Handling

- **Skill not installed**
  - Display message that skill is not in registry
  - List currently installed skills
  - No error (idempotent operation)

- **Symlink not found**
  - Warn that symlink was already removed
  - Continue with removing skill files
  - No error (resilient to partial cleanup)

- **Skill files not found**
  - Warn that files were already removed
  - Continue with registry cleanup
  - No error (resilient to partial cleanup)

## Post-Uninstallation

After uninstallation:
- Skill is no longer available to Claude Code
- All files and symlinks are removed
- Registry is updated
- No residual configuration

## Reinstallation

To reinstall the same skill:

```
/skills install pdf
```

The skill will be freshly downloaded and installed.
