# Skills Store - User Guide

Welcome to the Skills Store user guide! This guide will help you discover, install, and manage Claude Skills.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Searching for Skills](#searching-for-skills)
3. [Installing Skills](#installing-skills)
4. [Managing Installed Skills](#managing-installed-skills)
5. [Viewing Skill Details](#viewing-skill-details)
6. [Validating Skills](#validating-skills)
7. [Advanced Usage](#advanced-usage)
8. [Troubleshooting](#troubleshooting)

## Quick Start

### Prerequisites

- Python 3.7 or higher
- `requests` library: `pip install requests`
- `pyyaml` library: `pip install pyyaml`
- Internet connection (for GitHub downloads)

### Basic Workflow

```bash
# 1. Search for a skill
python scripts/search_skills.py "pdf"

# 2. Install the skill
python scripts/install_skill.py pdf

# 3. List your installed skills
python scripts/list_skills.py

# 4. View skill details
python scripts/show_skill_info.py pdf
```

## Searching for Skills

### Basic Search

Search for skills by keyword:

```bash
python scripts/search_skills.py "pdf"
```

This searches through:
- Skill names
- Descriptions
- Tags

### Filter by Category

Only show skills in a specific category:

```bash
python scripts/search_skills.py "document" --category document
```

Available categories:
- `document` - Document processing skills
- `creative` - Creative and design skills
- `development` - Development tools

### Filter by Source

Only show skills from a specific source:

```bash
python scripts/search_skills.py "art" --source github
```

### JSON Output

Get results in JSON format for scripting:

```bash
python scripts/search_skills.py "pdf" --json
```

### List All Skills

To see all available skills, search with an empty string:

```bash
python scripts/search_skills.py ""
```

## Installing Skills

### Install from Registry

Most skills can be installed directly from the registry:

```bash
python scripts/install_skill.py pdf
```

This will:
1. Look up the skill in the registry
2. Download it from GitHub
3. Validate the skill
4. Install it to the `skills/` directory
5. Update the installed skills registry

### Force Reinstall

To reinstall an existing skill:

```bash
python scripts/install_skill.py pdf --force
```

### Install from Local Directory

Install a skill from a local directory:

```bash
python scripts/install_skill.py my-custom-skill --local /path/to/skill
```

This is useful for:
- Testing skills you're developing
- Installing skills from local backups
- Sharing skills without publishing to GitHub

### Install from Specific Branch

Install from a non-default branch:

```bash
python scripts/install_skill.py my-skill --branch develop
```

## Managing Installed Skills

### List All Installed Skills

```bash
python scripts/list_skills.py
```

Output includes:
- Skill name
- Installation path
- Installation date
- Source information
- Validation status

### List with Validation

Validate all installed skills while listing:

```bash
python scripts/list_skills.py --validate
```

This will check each skill and update its validation status.

### JSON Output

```bash
python scripts/list_skills.py --json
```

## Viewing Skill Details

### View Registry Skill

Show information about a skill in the registry:

```bash
python scripts/show_skill_info.py pdf
```

This displays:
- Name and description
- Source information (repo, URL, path)
- Metadata (author, license, tags, category)
- Installation status
- File structure (if installed)

### View Installed Skill

Show details of an installed skill:

```bash
python scripts/show_skill_info.py pdf --installed
```

This includes:
- All registry information
- Installation details (path, date)
- SKILL.md preview (first 30 lines)
- Complete file structure

## Validating Skills

### Validate Installed Skill

Check if an installed skill meets requirements:

```bash
python scripts/validate_skill.py pdf
```

### Validate by Path

Validate a skill directory by path:

```bash
python scripts/validate_skill.py /path/to/skill --path
```

### Validation Criteria

A valid skill must have:

1. ✅ **SKILL.md file** exists
2. ✅ **YAML frontmatter** with:
   - `name` field
   - `description` field
3. ✅ **Valid YAML** syntax
4. ✅ **Safe path** (no `..` traversal)
5. ⚠️ **Reasonable size** (< 10MB recommended)

### Validation Output

**Success:**
```
✅ Validation PASSED

The skill meets all requirements:
  ✓ SKILL.md exists
  ✓ YAML frontmatter is valid
  ✓ Required fields (name, description) are present
  ✓ Path is valid and safe
```

**Failure:**
```
❌ Validation FAILED

🚫 Errors (must be fixed):
   [ERROR] SKILL.md: Required file SKILL.md not found

📖 Requirements:
  1. Directory must exist
  2. SKILL.md file must be present
  ...
```

## Advanced Usage

### Manual Registry Management

#### Add a Skill to Registry

Edit `data/skills-registry.json`:

```json
{
  "skills": {
    "my-skill": {
      "name": "my-skill",
      "description": "My awesome skill",
      "source": {
        "type": "github",
        "repo": "username/repo",
        "url": "https://github.com/username/repo",
        "branch": "main",
        "path": "skills/my-skill"
      },
      "metadata": {
        "author": "Your Name",
        "license": "MIT",
        "tags": ["category", "tags"],
        "category": "development"
      }
    }
  }
}
```

#### Add Local Skill to Registry

```json
{
  "skills": {
    "local-skill": {
      "name": "local-skill",
      "description": "My local skill",
      "source": {
        "type": "local",
        "path": "D:\\my\\local-skills\\local-skill"
      },
      "metadata": {
        "author": "Your Name",
        "license": "MIT",
        "tags": ["local"],
        "category": "development"
      }
    }
  }
}
```

### Working Directly with Python

Import and use the utility modules:

```python
from scripts.utils.registry import SkillsRegistry, InstalledSkillsRegistry
from scripts.utils.skill_validator import validate_skill_directory

# Search for skills
registry = SkillsRegistry()
results = registry.search("pdf")
for skill in results:
    print(skill['name'], skill['description'])

# List installed skills
installed = InstalledSkillsRegistry()
installed.load()
skills = installed.list_all()
print(f"Installed {len(skills)} skills")

# Validate a skill
is_valid, errors = validate_skill_directory("/path/to/skill")
print(f"Valid: {is_valid}")
if not is_valid:
    for error in errors:
        print(f"  {error}")
```

## Troubleshooting

### Problem: "Registry file not found"

**Solution:**
Make sure `data/skills-registry.json` exists. If not, create it with the initial template.

### Problem: "Skill not found in registry"

**Solution:**
- Check the skill name is spelled correctly
- Run `python scripts/search_skills.py ""` to list all available skills
- Verify the skill exists in `data/skills-registry.json`

### Problem: "Failed to download from GitHub"

**Solution:**
- Check your internet connection
- Verify the repository URL is correct
- Check if the repository is public or requires authentication
- Try accessing the URL in a browser

### Problem: "Validation failed - SKILL.md not found"

**Solution:**
- Ensure the skill directory contains a `SKILL.md` file
- Check the file is named exactly `SKILL.md` (case-sensitive)
- Verify the download completed successfully

### Problem: "Invalid YAML in frontmatter"

**Solution:**
- Check that SKILL.md starts with `---`
- Ensure YAML syntax is correct (proper indentation)
- Validate YAML using an online validator
- Check for special characters that need escaping

### Problem: "Permission denied when installing"

**Solution:**
- Check you have write permissions to the `skills/` directory
- Try running with appropriate permissions
- On Windows, ensure the directory is not in use

### Problem: "Disk space error"

**Solution:**
- Free up disk space
- Install to a different location by modifying the config
- Clean up old or unused skills

## Best Practices

1. **Always validate** skills before using them in production
2. **Keep the registry updated** with the latest skills
3. **Use descriptive tags** when adding skills to the registry
4. **Test skills** after installation to ensure they work as expected
5. **Backup your skills directory** before major changes
6. **Review skill source code** before installing from untrusted sources
7. **Document custom skills** with clear SKILL.md files
8. **Use version control** for skills you're developing

## Getting Help

If you encounter issues not covered in this guide:

1. Check the error message carefully
2. Review the validation output
3. Consult the registry schema documentation
4. Examine the script source code for details
5. Report issues with detailed error messages

## Next Steps

- Explore available skills: `python scripts/search_skills.py ""`
- Install your first skill: `python scripts/install_skill.py <name>`
- Create your own skill using the skill-creator
- Contribute skills to the community registry
