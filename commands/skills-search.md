---
name: skills-search
description: Search for skills in the registry by name, description, or tags. Filter by category or source type.
allowed-tools: "Bash(python scripts/search_skills.py:*)"
---

# Search for Skills

Search the centralized skills registry.

## Usage

```
/skills search <query> [options]
```

## Arguments

- `query` - Search query (empty string lists all skills)

## Options

- `--category <name>` - Filter by category (document, development, productivity, etc.)
- `--source <type>` - Filter by source type (github, local)
- `--json` - Output as JSON

## Examples

```
/skills search "pdf"
/skills search "" --category document
/skills search "automation" --source github
/skills search "" --json
```

## Implementation

When user searches for skills:

1. Run: `python scripts/search_skills.py <query> [options]`
2. Script searches `data/skills-registry.json`
3. Filters by category and/or source if specified
4. Displays matching skills with descriptions and metadata

## Output Format

```
🔍 Found 2 skills matching "pdf":

1. 📄 pdf
   Comprehensive PDF manipulation toolkit for extracting text and tables...
   🏷️  document, pdf, manipulation, forms
   📂 anthropics/skills
   ✅ Valid

2. 📄 pdf-tools
   Advanced PDF tools with OCR capabilities...
   🏷️  document, pdf, ocr
   📂 custom/repo
   ✅ Valid
```

## Categories

- **document** - Document processing (PDF, DOCX, PPTX, XLSX)
- **development** - Development tools and utilities
- **productivity** - Productivity and workflow tools
- **scientific** - Scientific computing and ML
- **creative** - Creative and design tools
- **automation** - Automation and workflow
