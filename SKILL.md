---
name: skills-store
description: |
  A skill store for discovering, installing, and managing Claude Skills.
  Use this skill when users want to search for skills, install new skills, list installed skills,
  show skill details, or validate skills. Supports installing from GitHub registry and local directories.
  Provides a centralized way to manage the Claude Skills ecosystem.
---

# Skills Store

Skills Store is a central hub for discovering, installing, and managing Claude Skills. It provides a simple interface to search for skills across the ecosystem, install them from GitHub or local sources, and keep track of your installed skills.

## When to Use This Skill

Trigger this skill when users:

- Want to **find** a skill for a specific task ("search for PDF skills", "find skills for presentations")
- Want to **install** a skill ("install the pdf skill", "add algorithmic-art skill")
- Want to **list** or **manage** their installed skills ("show installed skills", "list my skills")
- Want to **view details** about a skill ("show info about pdf skill", "describe the frontend-design skill")
- Want to **validate** a skill ("check if this skill is valid", "validate my custom skill")

## Key Features

### 1. Search Skills
Search for skills by name, description, or tags. Filter by category or source type.

**User requests:**
- "Search for PDF skills"
- "Find skills related to documents"
- "Show me creative skills"

**Action:** Run `python scripts/search_skills.py "<query>"`

### 2. List Installed Skills
View all installed skills with their status and metadata.

**User requests:**
- "List installed skills"
- "Show my skills"
- "What skills do I have?"

**Action:** Run `python scripts/list_skills.py`

### 3. Install Skills
Download and install skills from GitHub or local directories.

**User requests:**
- "Install the pdf skill"
- "Add algorithmic-art skill"
- "Install skill from /path/to/skill"

**Action:**
- For registry skills: `python scripts/install_skill.py <skill_name>`
- For local skills: `python scripts/install_skill.py <name> --local <path>`

### 4. Show Skill Details
Display comprehensive information about a skill.

**User requests:**
- "Show details of pdf skill"
- "Tell me about the frontend-design skill"
- "What does the xlsx skill do?"

**Action:** Run `python scripts/show_skill_info.py <skill_name>`

### 5. Validate Skills
Check if a skill meets the required standards.

**User requests:**
- "Validate the pdf skill"
- "Check if my skill is valid"
- "Verify /path/to/skill"

**Action:** Run `python scripts/validate_skill.py <skill_name_or_path>`

## Directory Structure

```
skills-store/
├── SKILL.md                     # This file
├── skills/                      # Installed skills directory
├── scripts/                     # Management scripts
│   ├── search_skills.py         # Search for skills
│   ├── list_skills.py           # List installed skills
│   ├── install_skill.py         # Install a skill
│   ├── show_skill_info.py       # Show skill details
│   ├── validate_skill.py        # Validate a skill
│   └── utils/                   # Utility modules
├── data/                        # Data files
│   ├── skills-registry.json     # Skills index
│   └── installed-skills.json    # Installed skills record
└── references/                  # Documentation
    ├── user-guide.md            # User guide
    └── registry-schema.md       # Registry schema
```

## Registry System

### skills-registry.json

The skills registry (`data/skills-registry.json`) is a manually maintained index of available skills. Each skill entry contains:

- **name**: Unique skill identifier
- **description**: What the skill does
- **source**: Where to get the skill (GitHub repo or local path)
- **metadata**: Author, license, tags, category

Example entry:
```json
{
  "name": "pdf",
  "description": "Comprehensive PDF manipulation toolkit...",
  "source": {
    "type": "github",
    "repo": "anthropics/anthropic-skills",
    "path": "document-skills/unknown/skills/pdf"
  },
  "metadata": {
    "author": "Anthropic",
    "tags": ["document", "pdf"],
    "category": "document"
  }
}
```

### installed-skills.json

Tracks which skills are installed locally. Auto-generated and maintained.

## Skill Validation

All skills must meet these requirements:

1. **SKILL.md file** must exist in the skill directory
2. **YAML frontmatter** at the top of SKILL.md with:
   - `name`: Skill identifier (lowercase, hyphens)
   - `description`: What the skill does and when to use it
3. **Content** after frontmatter with usage instructions
4. **Safe paths** (no `..` path traversal)
5. **Reasonable size** (< 10MB recommended)

Example SKILL.md structure:
```markdown
---
name: my-skill
description: A brief description of what this skill does
---

# My Skill

Detailed usage instructions...
```

## Usage Examples

### Example 1: Installing a Skill

**User:** "I need to work with PDF documents"

**Claude:**
```
I'll help you find a PDF skill. Let me search for PDF-related skills.

[runs: python scripts/search_skills.py "pdf"]

Found the "pdf" skill! It provides comprehensive PDF manipulation
including extracting text, merging, splitting, and filling forms.

Would you like me to install it?
```

**User:** "Yes, install it"

**Claude:**
```
[runs: python scripts/install_skill.py pdf]

✅ Successfully installed 'pdf' to D:\my\vibe-coding\skills-store\skills\pdf

You can now use PDF manipulation capabilities!
```

### Example 2: Managing Skills

**User:** "What skills do I have installed?"

**Claude:**
```
[runs: python scripts/list_skills.py --validate]

📦 Installed Skills (3):

1. 📦 pdf
   📁 Path: D:\my\vibe-coding\skills-store\skills\pdf
   📅 Installed: 2026-01-02 15:30
   🔗 Source: github (anthropics/anthropic-skills)
   ✅ Valid

2. 📦 docx
   📁 Path: D:\my\vibe-coding\skills-store\skills\docx
   ...
```

### Example 3: Installing from Local Directory

**User:** "Install my custom skill from D:\my-skills\my-skill"

**Claude:**
```
[runs: python scripts/install_skill.py my-skill --local "D:\my-skills\my-skill"]

📋 Installing 'my-skill' from local directory...
   Source: D:\my-skills\my-skill

🔍 Validating source skill...
✅ Validation passed

📋 Copying files...
✅ Successfully installed 'my-skill'
```

## Integration with Claude

Skills installed via Skills Store are stored in the `skills/` directory. To make them available to Claude:

1. **For this session:** Skills are immediately available after installation
2. **For persistent availability:** The `skills/` directory can be added to Claude's plugin path

Currently, skills are managed independently. Future versions may integrate directly with Claude's plugin system.

## Extending the Registry

To add a new skill to the registry:

1. Edit `data/skills-registry.json`
2. Add a new entry under `skills`
3. Include name, description, source, and metadata
4. Run `python scripts/validate_skill.py <name>` to verify

Example:
```json
{
  "skills": {
    "my-new-skill": {
      "name": "my-new-skill",
      "description": "Does something amazing",
      "source": {
        "type": "github",
        "repo": "user/repo",
        "path": "skills/my-new-skill"
      },
      "metadata": {
        "author": "Your Name",
        "tags": ["category", "tags"],
        "category": "development"
      }
    }
  }
}
```

## Troubleshooting

### Skill not found in registry
- Check `data/skills-registry.json` exists
- Verify the skill name is spelled correctly
- Run `python scripts/search_skills.py ""` to list all skills

### Installation fails
- Check internet connection for GitHub downloads
- Verify the repository and path are correct
- Check for sufficient disk space
- Review error messages for details

### Validation fails
- Ensure SKILL.md exists in the skill directory
- Verify YAML frontmatter is present and valid
- Check that `name` and `description` fields exist
- Review validation output for specific issues

## Future Enhancements

Planned features for future versions:

- **Automatic registry updates** from GitHub repositories
- **Version management** for skills
- **Dependency resolution** and installation
- **Direct Claude plugin integration**
- **Web interface** for browsing and installing skills
- **Community contributions** via pull requests to registry
- **Skill ratings** and usage statistics

## Contributing

To contribute to Skills Store:

1. **Add skills to the registry:** Edit `data/skills-registry.json`
2. **Report issues:** Document bugs or feature requests
3. **Improve scripts:** Enhance functionality in `scripts/`
4. **Share skills:** Publish your skills and add them to the registry

## Related Skills

- **skill-creator**: For creating new skills from scratch
- **mcp-builder**: For building MCP servers

## License

This skill store is part of the skills-store project and helps manage the Claude Skills ecosystem.
