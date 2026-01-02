# Skills Store

> 📦 Claude Skills 的包管理系统 - 发现、安装和管理 Claude Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-0.1.0-green.svg)](https://github.com/YOUR_USERNAME/skills-store/releases)

---

A central hub for discovering, installing, and managing Claude Skills.

**Current Version**: v0.1.0 | **Release Date**: 2026-01-03

## Overview

Skills Store provides a simple interface to search for skills across the ecosystem, install them from GitHub or local sources, and keep track of your installed skills. It's like npm or pip, but for Claude Skills!

## Features

- 🔍 **Search** - Find skills by name, description, or tags
- 📦 **Install** - Download and install skills from GitHub or local directories
- 📋 **List** - View all installed skills with their status
- 📖 **Details** - Get comprehensive information about any skill
- ✅ **Validate** - Check if skills meet required standards
- 🌍 **Cross-platform** - Works on Windows, macOS, and Linux
- 📱 **Portable** - Uses relative paths, works from any directory

## 📊 Current Statistics

| Metric | Count |
|--------|-------|
| **Total Skills** | 21 |
| **Source Repositories** | 9 |
| **Categories** | 9 |
| **Awesome Lists** | 4 |

### Supported Repositories

- **anthropics/skills** (8) - Official skills
- **obra/superpowers** (20+) - Productivity skills
- **alirezarezvani/claude-skills** (3) - Architecture, Product, DevOps
- **K-Dense-AI/claude-scientific-skills** (138) - Scientific computing
- **mrgoonie/claudekit-skills** (10) - Agent skills
- **czlonkowski/n8n-skills** (5) - Workflow automation
- **huggingface/skills** (5) - Machine learning
- **bear2u/my-skills** (3) - Common skills
- **yusufkaraaslan/Skill_Seekers** (1) - Documentation converter

## Quick Start

```bash
# Search for a skill
python scripts/search_skills.py "pdf"

# Install a skill
python scripts/install_skill.py pdf

# List installed skills
python scripts/list_skills.py

# View skill details
python scripts/show_skill_info.py pdf
```

## Project Structure

```
skills-store/
├── SKILL.md                     # Main skill definition
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
├── references/                  # Documentation
│   ├── user-guide.md            # User guide
│   └── registry-schema.md       # Registry schema
└── README.md                    # This file
```

## Documentation

- **[User Guide](references/user-guide.md)** - Complete usage instructions
- **[Registry Schema](references/registry-schema.md)** - Data format documentation
- **[SKILL.md](SKILL.md)** - Skill definition and usage
- **[CHANGELOG](CHANGELOG.md)** - Version history and release notes
- **[Creating Skills](CREATION_PROCESS.md)** - Design thoughts and implementation details
- **[Decision Log](DECISIONS.md)** - Key design decisions and rationale

## Requirements

- Python 3.7+
- `requests` library: `pip install requests`
- `pyyaml` library: `pip install pyyaml`
- Internet connection (for GitHub downloads)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/skills-store.git
   cd skills-store
   ```

2. Install dependencies:
   ```bash
   pip install requests pyyaml
   ```

3. You're ready to go!

## Usage Examples

### Search for Skills

```bash
# Search by keyword
python scripts/search_skills.py "pdf"

# Filter by category
python scripts/search_skills.py "document" --category document

# List all skills
python scripts/search_skills.py ""
```

### Install Skills

```bash
# Install from registry
python scripts/install_skill.py pdf

# Install from local directory
python scripts/install_skill.py my-skill --local /path/to/skill

# Force reinstall
python scripts/install_skill.py pdf --force
```

### Manage Skills

```bash
# List installed skills
python scripts/list_skills.py

# List with validation
python scripts/list_skills.py --validate

# View skill details
python scripts/show_skill_info.py pdf

# Validate a skill
python scripts/validate_skill.py pdf
```

## Registry System

### Adding Skills to the Registry

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
        "path": "skills/my-skill"
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

See [Registry Schema](references/registry-schema.md) for details.

## Skill Validation

All skills must meet these requirements:

1. ✅ **SKILL.md file** exists
2. ✅ **YAML frontmatter** with `name` and `description`
3. ✅ **Valid YAML** syntax
4. ✅ **Safe paths** (no `..` traversal)
5. ⚠️ **Reasonable size** (< 10MB recommended)

Example SKILL.md:

```markdown
---
name: my-skill
description: A brief description of what this skill does
---

# My Skill

Detailed usage instructions...
```

## Troubleshooting

### Encoding Issues on Windows

If you see encoding errors, the scripts automatically handle Windows console encoding by setting UTF-8 output mode.

### "Registry file not found"

Make sure `data/skills-registry.json` exists. See the Registry Schema documentation for the template.

### "Skill not found in registry"

- Check the skill name is spelled correctly
- Run `python scripts/search_skills.py ""` to list all skills
- Verify the skill exists in `data/skills-registry.json`

## Contributing

Contributions are welcome! You can:

1. **Add skills to the registry** - Edit `data/skills-registry.json`
2. **Report issues** - Document bugs or feature requests
3. **Improve scripts** - Enhance functionality in `scripts/`
4. **Share skills** - Publish your skills and add them to the registry

## Future Enhancements

### v0.2.0 (Planned)

- [ ] Uninstall command
- [ ] Update registry command
- [ ] Batch installation support
- [ ] Automatic registry updates
- [ ] Configuration file support
- [ ] Environment variable support

### Long-term Vision

- ⬆️ Automatic registry updates from GitHub
- 🔢 Version management for skills
- 📦 Dependency resolution and installation
- 🔗 Direct Claude Code integration
- 🌐 Web interface for browsing and installing
- ⭐ Community ratings and statistics

See [CHANGELOG.md](CHANGELOG.md) for detailed roadmap.

## License

This project helps manage the Claude Skills ecosystem. See individual skill licenses for details.

## Related Projects

- **[skill-creator](https://github.com/anthropics/anthropic-skills)** - Create new skills
- **[Claude Skills](https://github.com/anthropics/anthropic-skills)** - Official skills repository

## Support

For issues, questions, or contributions, please visit the project repository.

---

Made with ❤️ for the Claude Skills community
