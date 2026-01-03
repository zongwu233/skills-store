---
name: skills-install
description: Install a skill from the registry or local directory. Automatically validates and creates symlinks for Claude Code discovery.
allowed-tools: "Bash(python scripts/install_skill.py:*)"
---

# Install a Skill

Install a skill from the registry or a local directory.

## Usage

```
/skills install <skill_name> [options]
```

## Arguments

- `skill_name` - Name of skill to install (as listed in registry)

## Options

- `--force` - Reinstall if already installed
- `--local <path>` - Install from local directory instead of GitHub
- `--branch <name>` - Specify git branch (default: main)

## Examples

```
/skills install pdf
/skills install pdf --force
/skills install my-skill --local /path/to/skill
/skills install custom-skill --branch dev
```

## Implementation

When user requests to install a skill:

1. Run: `python scripts/install_skill.py <skill_name> [options]`
2. Script looks up skill in `data/skills-registry.json`
3. Downloads from GitHub or copies from local directory
4. Validates the skill structure and content
5. Installs to `skills/<skill_name>/`
6. Creates symlink in `plugin-skills/<skill_name>/` for auto-discovery
7. Updates `data/installed-skills.json`
8. Skill becomes immediately available to Claude Code

## Output Format

```
📥 Downloading 'pdf' from GitHub...
   Repo: anthropics/skills
   Path: skills/pdf
   Branch: main

🔍 Validating downloaded skill...
✅ Validation passed

✅ Created symbolic link in plugin-skills/ for Claude Code discovery

✅ Successfully installed 'pdf'
   Location: skills/pdf

You can now use this skill in Claude!
```

## Error Handling

- **Skill not found in registry**
  - Suggest running `/skills search` to find available skills
  - Show search examples

- **Installation failed**
  - Display GitHub API error
  - Suggest checking network connection
  - Offer `--local` option as alternative

- **Validation failed**
  - Display specific validation errors
  - Explain what's missing (SKILL.md, required fields, etc.)
  - Suggest contacting skill author

- **Symlink creation failed** (Windows)
  - Warn about missing Developer Mode
  - Fallback to copy automatically
  - Explain limitations of copy approach

## Post-Installation

After installation, the skill is **immediately available** to Claude Code.

No restart required! Just start using it:

```
Help me extract text from this PDF document
```

Claude will automatically discover and use the newly installed skill.
