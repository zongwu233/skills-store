# Skills Registry Schema

This document describes the schema for the `skills-registry.json` and `installed-skills.json` files used by Skills Store.

## Table of Contents

1. [Overview](#overview)
2. [skills-registry.json](#skills-registryjson)
3. [installed-skills.json](#installed-skillsjson)
4. [Examples](#examples)
5. [Validation Rules](#validation-rules)

## Overview

The Skills Store uses two JSON files for tracking skills:

1. **skills-registry.json**: Index of all available skills (manually maintained)
2. **installed-skills.json**: Record of installed skills (auto-generated)

Both files use JSON format with UTF-8 encoding.

## skills-registry.json

This is the main registry file that catalogs all available skills. It is typically manually maintained but can be generated from scripts.

### Root Structure

```json
{
  "version": "1.0.0",
  "last_updated": "2026-01-02T15:30:00Z",
  "skills": { ... },
  "categories": { ... },
  "stats": { ... }
}
```

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `version` | string | Yes | Registry format version (semantic versioning) |
| `last_updated` | string | Yes | ISO 8601 timestamp of last update |
| `skills` | object | Yes | Map of skill_id → skill_info |
| `categories` | object | No | Map of category_id → category_info |
| `stats` | object | No | Registry statistics |

### Skill Object

```json
{
  "name": "pdf",
  "description": "Comprehensive PDF manipulation toolkit...",
  "source": { ... },
  "metadata": { ... }
}
```

#### Skill Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Unique skill identifier (lowercase, hyphens) |
| `description` | string | Yes | What the skill does and when to use it |
| `source` | object | Yes | Where to get the skill |
| `metadata` | object | No | Additional skill information |

### Source Object

Describes where to obtain the skill. The structure varies by `type`.

#### GitHub Source

```json
{
  "type": "github",
  "repo": "anthropics/anthropic-skills",
  "url": "https://github.com/anthropics/anthropic-skills",
  "branch": "main",
  "path": "document-skills/unknown/skills/pdf"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | Must be "github" |
| `repo` | string | Yes | Repository in "owner/repo" format |
| `url` | string | Yes | Full GitHub repository URL |
| `branch` | string | No | Git branch (default: "main") |
| `path` | string | Yes | Path to skill directory within repo |

#### Local Source

```json
{
  "type": "local",
  "path": "D:\\my\\local-skills\\my-skill"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | Must be "local" |
| `path` | string | Yes | Absolute or relative path to skill directory |

### Metadata Object

```json
{
  "author": "Anthropic",
  "license": "MIT",
  "tags": ["document", "pdf", "manipulation"],
  "category": "document"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `author` | string | No | Skill author name |
| `license` | string | No | License identifier (SPDX format) |
| `tags` | array | No | List of searchable tags |
| `category` | string | No | Category identifier |

### Categories Object

```json
{
  "document": {
    "name": "Document Processing",
    "description": "Skills for working with documents",
    "count": 4
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Human-readable category name |
| `description` | string | Yes | Category description |
| `count` | number | Yes | Number of skills in category |

### Stats Object

```json
{
  "total_skills": 8,
  "total_sources": 1,
  "last_sync": "2026-01-02T15:30:00Z"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `total_skills` | number | Yes | Total number of skills in registry |
| `total_sources` | number | Yes | Number of distinct sources |
| `last_sync` | string | Yes | ISO 8601 timestamp of last sync |

## installed-skills.json

This file tracks which skills are installed locally. It is auto-generated and maintained by Skills Store.

### Root Structure

```json
{
  "version": "1.0.0",
  "installed_skills": { ... },
  "config": { ... }
}
```

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `version` | string | Yes | Format version (should match registry version) |
| `installed_skills` | object | Yes | Map of skill_name → installed_skill_info |
| `config` | object | Yes | Configuration settings |

### Installed Skill Object

```json
{
  "name": "pdf",
  "install_path": "D:\\my\\vibe-coding\\skills-store\\skills\\pdf",
  "source": { ... },
  "installed_at": "2026-01-02T10:00:00Z",
  "last_updated": "2026-01-02T10:00:00Z",
  "is_valid": true,
  "validation_errors": null
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Skill name (matches registry) |
| `install_path` | string | Yes | Local installation path |
| `source` | object | Yes | Source info (subset of registry source) |
| `installed_at` | string | Yes | ISO 8601 timestamp of installation |
| `last_updated` | string | Yes | ISO 8601 timestamp of last update |
| `is_valid` | boolean | Yes | Whether skill passes validation |
| `validation_errors` | string/null | No | Error message if invalid |

### Config Object

```json
{
  "local_skills_path": "D:\\my\\vibe-coding\\skills-store\\skills",
  "auto_update": false,
  "update_interval_hours": 24
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `local_skills_path` | string | Yes | Default installation directory |
| `auto_update` | boolean | Yes | Whether to auto-update skills |
| `update_interval_hours` | number | Yes | Update check interval |

## Examples

### Complete Registry Example

```json
{
  "version": "1.0.0",
  "last_updated": "2026-01-02T15:30:00Z",
  "skills": {
    "pdf": {
      "name": "pdf",
      "description": "Comprehensive PDF manipulation toolkit for extracting, merging, splitting, and filling forms",
      "source": {
        "type": "github",
        "repo": "anthropics/anthropic-skills",
        "url": "https://github.com/anthropics/anthropic-skills",
        "branch": "main",
        "path": "document-skills/unknown/skills/pdf"
      },
      "metadata": {
        "author": "Anthropic",
        "license": "Proprietary",
        "tags": ["document", "pdf", "manipulation", "forms"],
        "category": "document"
      }
    }
  },
  "categories": {
    "document": {
      "name": "Document Processing",
      "description": "Skills for working with documents (PDF, DOCX, PPTX, XLSX)",
      "count": 4
    }
  },
  "stats": {
    "total_skills": 1,
    "total_sources": 1,
    "last_sync": "2026-01-02T15:30:00Z"
  }
}
```

### Complete Installed Skills Example

```json
{
  "version": "1.0.0",
  "installed_skills": {
    "pdf": {
      "name": "pdf",
      "install_path": "D:\\my\\vibe-coding\\skills-store\\skills\\pdf",
      "source": {
        "type": "github",
        "repo": "anthropics/anthropic-skills",
        "branch": "main"
      },
      "installed_at": "2026-01-02T10:00:00Z",
      "last_updated": "2026-01-02T10:00:00Z",
      "is_valid": true,
      "validation_errors": null
    }
  },
  "config": {
    "local_skills_path": "D:\\my\\vibe-coding\\skills-store\\skills",
    "auto_update": false,
    "update_interval_hours": 24
  }
}
```

## Validation Rules

### Skill Names

- Must be unique within the registry
- Should contain only lowercase letters, numbers, and hyphens
- Should not start or end with a hyphen
- Should not contain consecutive hyphens
- Recommended max length: 50 characters

### Descriptions

- Must be a non-empty string
- Should clearly describe what the skill does
- Should mention when to use the skill
- Recommended max length: 200 characters for summary

### Sources

#### GitHub
- `repo` must be in "owner/repo" format
- `url` must be a valid GitHub repository URL
- `branch` must be a valid branch name
- `path` must be a valid directory path

#### Local
- `path` must be a valid file system path
- Can be absolute or relative
- Should exist at validation time

### Tags

- Must be an array of strings
- Each tag should be lowercase
- Tags should be searchable keywords
- Recommended max 10 tags per skill

### Categories

- Must be one of the predefined categories
- Current categories: `document`, `creative`, `development`
- Custom categories can be added

### Timestamps

- Must be ISO 8601 format
- Must include timezone (use 'Z' for UTC)
- Example: `2026-01-02T15:30:00Z`

## Schema Evolution

### Versioning

The `version` field uses semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes to schema structure
- **MINOR**: Additions to schema (backward compatible)
- **PATCH**: Bug fixes or documentation updates

### Current Version: 1.0.0

This is the initial stable schema format.

### Future Changes

Potential future additions:
- Skill versioning
- Dependencies field
- Rating and statistics
- Installation count
- Last updated timestamp per skill

### Backward Compatibility

Skills Store will attempt to maintain backward compatibility:
- New fields are optional
- Old fields are deprecated before removal
- Migration scripts provided for major versions

## Validation

Use the provided validation script to check registry files:

```bash
python tools/validate_registry.py
```

This checks:
- JSON syntax validity
- Required fields presence
- Field type correctness
- Value format compliance
- Reference integrity (e.g., categories exist)

## Related Documentation

- [User Guide](user-guide.md) - How to use Skills Store
- [SKILL.md](../SKILL.md) - Main skill documentation
- [Tool Documentation](../tools/README.md) - Registry management tools
