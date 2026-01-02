#!/usr/bin/env python3
"""
Search Skills Script

Search for skills in the registry by name, description, or tags.
"""

import sys
import io
import json
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Add parent directory to path to import utils
sys.path.insert(0, str(Path(__file__).parent))

from utils.registry import SkillsRegistry


def format_skill_summary(skill: dict) -> str:
    """Format a skill for display"""
    name = skill.get('name', 'Unknown')
    description = skill.get('description', 'No description')

    # Truncate description if too long
    if len(description) > 80:
        description = description[:77] + "..."

    source_type = skill.get('source', {}).get('type', 'unknown')
    repo = skill.get('source', {}).get('repo', 'local')

    tags = skill.get('metadata', {}).get('tags', [])
    category = skill.get('metadata', {}).get('category', 'general')

    lines = [
        f"📦 {name}",
        f"   {description}",
        f"   📁 Category: {category}",
        f"   🔗 Source: {source_type} ({repo})",
    ]

    if tags:
        lines.append(f"   🏷️  Tags: {', '.join(tags)}")

    return '\n'.join(lines)


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python search_skills.py <query> [options]")
        print("")
        print("Options:")
        print("  --category <category>  Filter by category")
        print("  --source <type>        Filter by source type (github, local)")
        print("  --json                 Output as JSON")
        print("")
        print("Examples:")
        print('  python search_skills.py "pdf"')
        print('  python search_skills.py "document" --category document')
        print('  python search_skills.py "art" --source github --json')
        sys.exit(1)

    # Parse arguments
    query = sys.argv[1]
    category = None
    source_type = None
    output_json = False

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--category' and i + 1 < len(sys.argv):
            category = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--source' and i + 1 < len(sys.argv):
            source_type = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--json':
            output_json = True
            i += 1
        else:
            print(f"Unknown option: {sys.argv[i]}", file=sys.stderr)
            sys.exit(1)

    # Load registry and search
    try:
        registry = SkillsRegistry()
        results = registry.search(query, category=category, source_type=source_type)

        if output_json:
            # Output as JSON
            print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            # Output as formatted text
            if not results:
                print(f"❌ No skills found matching '{query}'")
                if category:
                    print(f"   in category '{category}'")
                if source_type:
                    print(f"   from source '{source_type}'")
                print("")
                print("Try:")
                print("  - Using a more general search term")
                print("  - Removing --category or --source filters")
                print("  - Running 'python list_skills.py' to see all available skills")
            else:
                print(f"✅ Found {len(results)} skill(s) matching '{query}':")
                print("")

                for i, skill in enumerate(results, 1):
                    print(f"{i}. {format_skill_summary(skill)}")
                    print("")

    except FileNotFoundError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        print("")
        print("Make sure skills-registry.json exists in the data/ directory.")
        print("You may need to initialize it first.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
