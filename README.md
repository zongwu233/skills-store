# Skills Store

> 📦 Claude Skills Package Manager - Discover, install, and manage Claude Skills with automatic discovery

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-0.2.0-green.svg)](https://github.com/zongwu233/skills-store/releases)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-blue.svg)](https://claude.com/claude-code)

---

A comprehensive package manager for Claude Skills with automatic discovery. Think of it as `npm` or `pip`, but specifically designed for Claude Skills.

**Current Version**: v0.2.0 | **Release Date**: January 3, 2026

---

## 🌟 Overview

Skills Store v0.2.0 is a full-featured Claude Code Plugin that provides automatic skill discovery, installation, and management. It transforms the skill management experience from manual scripts to seamless integration with Claude Code.

### Key Features

- 🔍 **Search** - Find skills by name, description, tags, or category
- 📦 **Install** - Download and install skills from GitHub or local directories
- 🔗 **Auto-Discovery** - Skills are immediately available after installation via symbolic links
- 📋 **List** - View all installed skills with validation status
- 📖 **Details** - Get comprehensive information about any skill
- ✅ **Validate** - Check if skills meet required standards
- 🌍 **Cross-Platform** - Works on Windows, macOS, and Linux with intelligent fallback
- 🎯 **Slash Commands** - Intuitive `/skills` command suite for easy management

---

## 📊 Current Statistics

| Metric | Count |
|--------|-------|
| **Total Skills** | 21+ |
| **Source Repositories** | 9 |
| **Categories** | 9 |
| **Slash Commands** | 7 |
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

---

## 🚀 Quick Start

### Option 1: As a Claude Code Plugin (Recommended)

```bash
# Install the plugin
/plugin marketplace add https://github.com/zongwu233/skills-store
/plugin install skills-store

# Search for skills
/skills search "pdf"

# Install a skill
/skills install pdf

# List installed skills
/skills list
```

### Option 2: Using Python Scripts

```bash
# Clone the repository
git clone https://github.com/zongwu233/skills-store.git
cd skills-store

# Install dependencies
pip install requests pyyaml

# Search for a skill
python scripts/search_skills.py "pdf"

# Install a skill
python scripts/install_skill.py pdf

# List installed skills
python scripts/list_skills.py
```

---

## 📖 How to Use

This guide covers both the Plugin method (recommended) and the Python script method.

### Plugin Method (Recommended)

The Plugin method provides the best user experience with automatic skill discovery.

#### 1. Search for Skills

```bash
# Search by keyword
/skills search "pdf"

# Search by category
/skills search "" --category document

# List all skills
/skills search ""
```

**Output Example**:
```
🔍 Found 1 skill(s) matching 'pdf':

1. 📦 pdf
   Comprehensive PDF manipulation toolkit for extracting text and tables...
   📁 Category: document
   🔗 Source: github (anthropics/skills)
   🏷️  Tags: document, pdf, manipulation, forms
```

#### 2. Get Skill Information

```bash
# View detailed information
/skills info pdf
```

**Output Example**:
```
📦 Skill Information: pdf

Description:
Comprehensive PDF manipulation toolkit for extracting text and tables...

Source:
  Type: github
  Repository: anthropics/skills
  Path: skills/pdf

Installation Status:
  ✅ Installed
  Location: skills/pdf
```

#### 3. Install a Skill

```bash
# Install from registry
/skills install pdf

# Install from local directory
/skills install my-skill --local /path/to/skill

# Force reinstall
/skills install pdf --force
```

**What Happens**:
1. Skill downloads to `skills/pdf/`
2. Automatic validation runs
3. Symbolic link created in `plugin-skills/pdf/`
4. **Skill is immediately available to Claude Code!**

#### 4. List Installed Skills

```bash
# List all installed skills
/skills list

# List with validation
/skills list --validate

# List as JSON
/skills list --json
```

**Output Example**:
```
📦 Installed Skills (2):

1. 📦 pdf
   📁 Path: skills/pdf
   📅 Installed: 2026-01-03 23:16
   🔗 Source: github (anthropics/skills)
   ✅ Valid

2. 📦 docx
   📁 Path: skills/docx
   📅 Installed: 2026-01-03 23:20
   🔗 Source: github (anthropics/skills)
   ✅ Valid
```

#### 5. Update a Skill

```bash
# Update to latest version
/skills update pdf
```

This is equivalent to `/skills install pdf --force`.

#### 6. Uninstall a Skill

```bash
# Remove a skill
/skills uninstall pdf
```

**What Gets Removed**:
- Symbolic link from `plugin-skills/`
- Skill files from `skills/`
- Entry from registry

### Python Script Method

If you prefer using Python scripts directly, all the same functionality is available:

```bash
# Search
python scripts/search_skills.py "pdf"

# Install
python scripts/install_skill.py pdf

# List
python scripts/list_skills.py

# Show details
python scripts/show_skill_info.py pdf

# Validate
python scripts/validate_skill.py pdf

# Uninstall
python scripts/uninstall_skill.py pdf
```

---

## 🏗️ Project Structure

```
skills-store/
├── .claude-plugin/              # Plugin configuration
│   ├── plugin.json              # Plugin manifest
│   └── hooks/
│       └── post-install.sh      # Setup automation
│
├── plugin-skills/               # Claude Code scanned skills
│   └── skills-store-manager/    # Main management skill
│       └── SKILL.md
│
├── commands/                    # Slash commands
│   ├── skills.md                # Main dispatcher
│   ├── skills-list.md
│   ├── skills-search.md
│   ├── skills-install.md
│   ├── skills-uninstall.md
│   ├── skills-update.md
│   └── skills-info.md
│
├── skills/                      # Actual skill storage
│   ├── pdf/
│   ├── docx/
│   └── skill-creator/
│
├── scripts/                     # Python management scripts
│   ├── search_skills.py         # Search for skills
│   ├── install_skill.py         # Install a skill
│   ├── uninstall_skill.py       # Uninstall a skill
│   ├── list_skills.py           # List installed skills
│   ├── show_skill_info.py       # Show skill details
│   ├── validate_skill.py        # Validate a skill
│   ├── update_registry.py       # Update registry
│   └── utils/                   # Utility modules
│       ├── registry.py          # Registry management
│       ├── github_client.py     # GitHub API client
│       └── skill_validator.py   # Validation logic
│
├── data/                        # Data files
│   ├── skills-registry.json     # Skills index
│   └── installed-skills.json    # Installed skills record
│
├── references/                  # Documentation
│   ├── user-guide.md            # User guide
│   └── registry-schema.md       # Registry schema
│
├── SKILL.md                     # Skills Store skill definition
├── README.md                    # This file
├── CHANGELOG.md                 # Version history
└── LICENSE                      # MIT License
```

---

## 🔧 Advanced Usage

### Installing from Local Directory

Install a skill from your local machine:

```bash
/skills install my-custom-skill --local /path/to/skill
```

Use this for:
- Testing custom skills
- Installing from local development
- Skills not in the registry

### Filtering by Category

Search skills within a specific category:

```bash
/skills search "" --category document
```

**Available Categories**:
- `document` - Document processing
- `development` - Development tools
- `productivity` - Productivity tools
- `scientific` - Scientific computing
- `creative` - Creative tools
- `automation` - Workflow automation

### Force Reinstall

Reinstall a skill even if it's already installed:

```bash
/skills install pdf --force
```

Use this when:
- Skill files are corrupted
- You want the latest version
- Symlink is broken

### Validation

Validate all installed skills:

```bash
/skills list --validate
```

This checks:
- SKILL.md exists
- YAML frontmatter is valid
- Required fields are present
- Paths are safe

---

## 🌍 Cross-Platform Support

Skills Store uses intelligent symlink strategies across platforms:

### Unix/Linux/macOS

```bash
# Creates symbolic links
✅ Created symbolic link in plugin-skills/
```

### Windows

Three-tier fallback strategy:

1. **Symbolic Link** (requires Developer Mode or Admin)
   ```bash
   ✅ Created symbolic link in plugin-skills/
   ```

2. **Directory Junction** (works everywhere)
   ```bash
   ✅ Created directory junction in plugin-skills/
   ```

3. **Copy** (last resort)
   ```bash
   ⚠️  Copied skill to plugin-skills/
      Note: Enable Developer Mode for symbolic links
   ```

---

## 📚 Registry System

### Adding Skills to the Registry

Edit `data/skills-registry.json`:

```json
{
  "skills": {
    "my-skill": {
      "name": "my-skill",
      "description": "My awesome skill that does amazing things",
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
        "tags": ["category", "tag1", "tag2"],
        "category": "development"
      }
    }
  }
}
```

See [Registry Schema Documentation](references/registry-schema.md) for complete details.

### Registry Fields

- `name` (required) - Unique skill identifier
- `description` (required) - What the skill does
- `source` (required) - Where to get the skill
  - `type` - "github" or "local"
  - `repo` - GitHub repository (for github type)
  - `path` - Path within repo
  - `url` - Repository URL
  - `branch` - Git branch (default: "main")
- `metadata` (optional)
  - `author` - Author name
  - `license` - License type
  - `tags` - Searchable tags
  - `category` - Skill category

---

## ✅ Skill Validation

All skills must meet these requirements:

1. ✅ **SKILL.md file** exists at root
2. ✅ **YAML frontmatter** present with required fields
3. ✅ **Valid YAML** syntax
4. ✅ **Required fields**: `name`, `description`
5. ✅ **Safe paths** - No `..` directory traversal
6. ⚠️ **Reasonable size** - < 10MB recommended

Example SKILL.md:

```markdown
---
name: my-skill
description: |
  A brief description of what this skill does and when to use it.
---

# My Skill

Detailed usage instructions...

## When to Use

Use this skill when users want to...

## Instructions

Step 1: Do this first
Step 2: Then do that
```

---

## 🐛 Troubleshooting

### Skill Not Discovered by Claude Code

**Symptom**: Installed skill but Claude doesn't see it.

**Solutions**:

1. Check symlink exists:
   ```bash
   ls -la plugin-skills/
   ```

2. Verify symlink points to valid skill:
   ```bash
   ls -la plugin-skills/pdf
   ```

3. Reinstall:
   ```bash
   /skills install pdf --force
   ```

### Symlink Creation Failed on Windows

**Symptom**: Warning about symlink creation.

**Solutions**:

1. **Enable Developer Mode**:
   - Settings → Update & Security → For developers
   - Enable "Developer Mode"

2. **Run as Administrator**:
   - Right-click terminal → "Run as administrator"

3. **Use automatic fallback**:
   - Already automatic! Skill will be copied instead

### "Registry file not found"

Make sure `data/skills-registry.json` exists. See the [Registry Schema Documentation](references/registry-schema.md) for the template.

### "Skill not found in registry"

- Check the skill name spelling
- Run `/skills search ""` to list all skills
- Verify the skill exists in `data/skills-registry.json`

### Encoding Issues on Windows

The scripts automatically handle Windows console encoding by setting UTF-8 output mode. If you still see encoding errors, make sure your terminal is configured for UTF-8.

---

## 🤝 Contributing

Contributions are welcome! You can:

1. **Add skills to the registry** - Edit `data/skills-registry.json`
2. **Report issues** - Document bugs or feature requests
3. **Improve scripts** - Enhance functionality in `scripts/`
4. **Share skills** - Publish your skills and add them to the registry
5. **Improve documentation** - Help make docs clearer

### Contribution Workflow

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📈 Development Roadmap

### v0.3.0 (Planned)

- [ ] Automatic registry updates
- [ ] Dependency management
- [ ] Version management (multiple skill versions)
- [ ] Batch operations (install/update multiple skills)
- [ ] Configuration file support
- [ ] Environment variable support

### Long-term Vision

- ⬆️ Web interface for browsing and installing
- 🔢 Skill versioning and conflict resolution
- 📦 Dependency resolution and auto-installation
- 🌐 Community ratings and usage statistics
- 🔍 Skill recommendation engine
- 📊 Usage analytics and insights

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

---

## 🔗 Related Projects

- **[skill-creator](https://github.com/anthropics/skills)** - Create new skills from scratch
- **[Claude Skills](https://github.com/anthropics/skills)** - Official skills repository
- **[mcp-builder](https://github.com/anthropics/skills)** - Build MCP servers

---

## 💬 Support

For issues, questions, or contributions:

- 📖 [Documentation](references/user-guide.md)
- 🐛 [Issue Tracker](https://github.com/zongwu233/skills-store/issues)
- 💬 [Discussions](https://github.com/zongwu233/skills-store/discussions)

---

## 🙏 Acknowledgments

Built with ❤️ for the Claude Skills community

Inspired by:
- [npm](https://www.npmjs.com/) - Node.js package manager
- [pip](https://pip.pypa.io/) - Python package manager
- [Homebrew](https://brew.sh/) - macOS package manager

---

**Made with ❤️ for the Claude Skills Community**

*For detailed technical implementation, see the inline code documentation*
*For version history and changes, see [CHANGELOG.md](CHANGELOG.md)*
