---
name: skills-store-manager
description: Guide for managing the Skills Store plugin. Use when users need help with plugin usage, troubleshooting, or understanding the skill management workflow.
---

# Skills Store Manager

Welcome to Skills Store - your package manager for Claude Skills!

## What is Skills Store?

Skills Store is a centralized registry and package manager for Claude Skills. It provides:

- 📦 **21+ curated skills** from 9 GitHub repositories
- 🔍 **Easy discovery** through search and categories
- ⚡ **One-click installation** with automatic validation
- ✅ **Quality assurance** with format and content validation
- 🔄 **Automatic discovery** - installed skills instantly available

## Quick Start

### Search for Skills

```
/skills search "pdf"
```

### Install a Skill

```
/skills install pdf
```

### List Installed Skills

```
/skills list
```

### Use the Skill

After installation, the skill is **immediately available** to Claude Code. Just ask:

```
Help me extract text from this PDF document
```

Claude will automatically discover and use the `pdf` skill!

## How It Works

### Plugin Architecture

```
skills-store/
├── skills/              # 实际存储位置
│   └── pdf/            # 真实文件
│
├── plugin-skills/      # Claude Code 扫描目录
│   └── pdf -> ../skills/pdf  # 符号链接
│
└── commands/           # 用户命令
    └── skills-install.md
```

### Installation Process

1. **Download**: Skill downloaded from GitHub to `skills/pdf/`
2. **Validate**: Automatic format and content validation
3. **Link**: Symlink created in `plugin-skills/pdf/`
4. **Discover**: Claude Code auto-discovers from `plugin-skills/`
5. **Available**: Skill ready to use immediately!

### Why Symlinks?

| Approach | Pros | Cons |
|----------|------|------|
| **Symlink** ✅ | • No duplication<br>• Instant updates<br>• Space efficient | • Windows needs permissions |
| **Copy** | • Works everywhere | • Duplication<br>• Manual sync |

We use symlinks with automatic fallback to copy on Windows.

## Command Reference

### /skills

Main command dispatcher. Shows help and available subcommands.

```
/skills
```

### /skills list

List all installed skills with validation status.

```
/skills list
/skills list --validate
/skills list --json
```

**Output**:
```
📦 Installed Skills (2):

1. 📦 pdf
   📁 Path: skills/pdf
   📅 Installed: 2026-01-03 01:00
   🔗 Source: github (anthropics/skills)
   ✅ Valid
```

### /skills search

Search for skills by name, description, or tags.

```
/skills search "pdf"
/skills search "" --category document
/skills search "automation" --source github
```

**Categories**:
- document - Document processing
- development - Development tools
- productivity - Productivity tools
- scientific - Scientific computing
- creative - Creative tools

### /skills install

Install a skill from the registry or local directory.

```
/skills install pdf
/skills install pdf --force
/skills install my-skill --local /path/to/skill
```

**What happens**:
1. Skill downloaded to `skills/<name>/`
2. Validation runs automatically
3. Symlink created in `plugin-skills/<name>/`
4. Skill immediately available to Claude Code

### /skills uninstall

Remove an installed skill.

```
/skills uninstall pdf
```

**What gets removed**:
- Symlink from `plugin-skills/`
- Skill files from `skills/`
- Entry from `installed-skills.json`

### /skills update

Update an installed skill to latest version.

```
/skills update pdf
```

This is equivalent to `/skills install pdf --force`.

### /skills info

Show detailed information about a skill.

```
/skills info pdf
```

Shows:
- Description and metadata
- Source repository and path
- Installation status
- SKILL.md preview
- File structure

## Troubleshooting

### Skill not discovered by Claude Code?

**Symptom**: Installed skill but Claude doesn't see it.

**Solutions**:

1. Check symlink exists:
```bash
ls plugin-skills/
```

2. Verify symlink points to valid skill:
```bash
ls -la plugin-skills/pdf
```

3. Try reinstalling:
```bash
/skills install pdf --force
```

### Symlink creation failed on Windows?

**Symptom**: Warning about symlink creation, skill works but not discovered.

**Solutions**:

1. **Enable Developer Mode**:
   - Settings → Update & Security → For developers
   - Enable "Developer Mode"

2. **Run as Administrator**:
   - Right-click terminal → "Run as administrator"

3. **Use copy fallback**:
   - Already automatic! Skill will be copied instead.

### Permission errors?

**Symptom**: "Access denied" when creating symlinks.

**Solution**:
- Use the copy fallback (automatic)
- Or enable Developer Mode on Windows

### Skill validation failed?

**Symptom**: Installation fails with validation errors.

**Common issues**:
- Missing SKILL.md file
- Invalid YAML frontmatter
- Missing required fields (name, description)

**Solutions**:
1. Check the skill's repository structure
2. Ensure SKILL.md exists at root
3. Verify YAML frontmatter format:
```yaml
---
name: skill-name
description: |
  Multi-line description
---
```

### GitHub API rate limit?

**Symptom**: Installation fails with 403 error.

**Solutions**:
1. Wait an hour (60 requests/hour for unauthenticated)
2. Set GitHub token:
```bash
export GITHUB_TOKEN=your_token_here
/skills install pdf
```

## Advanced Usage

### Install from Local Directory

```
/skills install my-custom-skill --local /path/to/skill
```

Use this for:
- Testing custom skills
- Installing from local development
- Skills not in the registry

### Force Reinstall

```
/skills install pdf --force
```

Use this when:
- Skill files are corrupted
- Want to update to latest version
- Symlink is broken

### Search by Category

```
/skills search "" --category document
```

Lists all skills in a category.

### Validate All Skills

```
/skills list --validate
```

Re-validates all installed skills and shows detailed errors.

## Contributing

Want to add your skill to the registry?

1. **Fork the repository**
   ```bash
   git clone https://github.com/your-username/skills-store
   cd skills-store
   ```

2. **Edit the registry**
   - Open `data/skills-registry.json`
   - Add your skill entry:
   ```json
   {
     "skills": {
       "my-skill": {
         "name": "my-skill",
         "description": "Does something amazing",
         "source": {
           "type": "github",
           "repo": "your-username/your-repo",
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

3. **Test your entry**
   ```bash
   /skills search "my-skill"
   /skills install my-skill
   ```

4. **Submit PR**
   - Push to your fork
   - Open pull request on GitHub

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for details.

## Registry Structure

The registry (`data/skills-registry.json`) contains:

```json
{
  "version": "1.0.0",
  "last_updated": "2026-01-03T01:00:00Z",
  "skills": {
    "skill-name": {
      "name": "skill-name",
      "description": "What it does",
      "source": {
        "type": "github",
        "repo": "owner/repo",
        "path": "skills/skill-name"
      },
      "metadata": {
        "author": "Author",
        "license": "MIT",
        "tags": ["tag1", "tag2"],
        "category": "development"
      }
    }
  },
  "stats": {
    "total_skills": 21,
    "total_sources": 9,
    "total_categories": 9
  }
}
```

## Data Files

### skills-registry.json

The main registry of available skills.

**Location**: `data/skills-registry.json`

**Purpose**: Central index of all skills in the store

**Updates**: Manually maintained, synchronized from GitHub

### installed-skills.json

Tracks which skills are installed locally.

**Location**: `data/installed-skills.json`

**Purpose**: Track installation state and metadata

**Auto-generated**: Yes, do not edit manually

**Format**:
```json
{
  "version": "1.0.0",
  "installed_skills": {
    "pdf": {
      "name": "pdf",
      "install_path": "skills/pdf",
      "source": {
        "type": "github",
        "repo": "anthropics/skills"
      },
      "installed_at": "2026-01-03T01:00:00",
      "is_valid": true
    }
  },
  "config": {
    "local_skills_path": "skills",
    "auto_update": false
  }
}
```

## Related Resources

- [User Guide](../../references/user-guide.md) - Comprehensive user documentation
- [Registry Schema](../../references/registry-schema.md) - Registry format specification
- [GitHub Repository](https://github.com/your-username/skills-store) - Source code and issues
- [CHANGELOG.md](../../CHANGELOG.md) - Version history and changes

## Version History

- **v0.2.0** - Plugin release with symlink integration
  - Added `/skills` commands
  - Automatic skill discovery via symlinks
  - Cross-platform support (Windows/macOS/Linux)

- **v0.1.0** - Initial standalone release
  - Python script-based management
  - Manual skill discovery

## Support

Need help?

1. **Check this guide** - Most issues are covered here
2. **Search existing issues** - [GitHub Issues](https://github.com/your-username/skills-store/issues)
3. **Ask a question** - Open a new GitHub issue
4. **Contribute** - Submit PRs for bugs or features

## Best Practices

### For Users

1. **Search before installing**
   ```
   /skills search "pdf"
   /skills info pdf
   /skills install pdf
   ```

2. **Validate after installation**
   ```
   /skills list --validate
   ```

3. **Keep skills updated**
   ```
   /skills update pdf
   ```

4. **Report issues**
   - Include error messages
   - Specify your platform (Windows/macOS/Linux)
   - Share the skill name and version

### For Contributors

1. **Test your skills**
   - Validate locally before submitting
   - Test on multiple platforms if possible
   - Include clear documentation

2. **Follow the schema**
   - Use correct registry format
   - Include all required fields
   - Add helpful metadata

3. **Document well**
   - Write clear descriptions
   - Include usage examples
   - Add troubleshooting tips

## Future Enhancements

Planned features for future versions:

- **Automatic registry updates** - Periodically fetch latest skills
- **Dependency management** - Handle skill dependencies
- **Version management** - Support multiple versions
- **Web interface** - Browse and install online
- **Community ratings** - Rate and review skills
- **Usage analytics** - Track most popular skills

---

*Last updated: 2026-01-03*
*Version: 0.2.0*
