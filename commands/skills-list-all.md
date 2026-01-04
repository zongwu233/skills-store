---
name: skills-list-all
description: List all available skills in the registry. Shows all skills with their descriptions, categories, tags, and sources.
allowed-tools: "Bash(python scripts/list_all_skills.py:*)"
---

# List All Available Skills

Display all skills available in the centralized registry.

## Usage

```
/skills list-all [options]
```

## Options

- `--category <name>` - Filter by category (document, development, productivity, etc.)
- `--source <type>` - Filter by source type (github, local)
- `--json` - Output as JSON (machine-readable)

## Examples

```
/skills list-all
/skills list-all --category document
/skills list-all --source github
/skills list-all --json
```

## Implementation

When user requests to list all available skills:

1. Run: `python scripts/list_all_skills.py [options]`
2. Script queries `data/skills-registry.json`
3. Displays all skills with descriptions and metadata
4. Shows category, tags, and source information

## Output Format

```
📦 All Available Skills (21):

1. 📦 pdf
   Comprehensive PDF manipulation toolkit for extracting text and tables...
   📁 Category: document
   🔗 Source: github (anthropics/skills)
   🏷️  Tags: document, pdf, manipulation, forms

2. 📦 docx
   Comprehensive document creation and editing toolkit...
   📁 Category: document
   🔗 Source: github (anthropics/skills)
   🏷️  Tags: document, docx, editing, collaboration

...
```

## Categories

- **document** - Document processing (PDF, DOCX, PPTX, XLSX)
- **development** - Development tools and utilities
- **productivity** - Productivity and workflow tools
- **scientific** - Scientific computing and ML
- **creative** - Creative and design tools
- **automation** - Automation and workflow
