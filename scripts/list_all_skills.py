#!/usr/bin/env python3
"""
List All Skills Script

Display all skills available in the registry.
Auto-syncs with remote registry if configured.
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
from utils.remote_registry import RemoteRegistryFetcher


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
    # Parse arguments
    category = None
    source_type = None
    output_json = False
    no_sync = False

    i = 1
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
        elif sys.argv[i] == '--no-sync':
            no_sync = True
            i += 1
        else:
            print(f"Unknown option: {sys.argv[i]}", file=sys.stderr)
            sys.exit(1)

    # Check for remote updates (unless disabled)
    if not no_sync:
        try:
            fetcher = RemoteRegistryFetcher()
            if fetcher.config.get('auto_sync', {}).get('on_list_all', True):
                remote_data = fetcher.fetch()
                if remote_data:
                    # Update local registry
                    registry_obj = SkillsRegistry()
                    local_data = registry_obj.load()

                    # Merge with local
                    merged_data = fetcher.merge_with_local(local_data, remote_data)
                    registry_obj.save(merged_data)
                    print()
        except Exception as e:
            # Don't fail if remote sync fails
            pass

    # Load registry and get all skills
    try:
        registry = SkillsRegistry()
        # Search with empty string to get all skills, then filter
        results = registry.search("", category=category, source_type=source_type)

        if output_json:
            # Output as JSON
            print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            # Output as formatted text
            if not results:
                print("❌ No skills found")
                if category:
                    print(f"   in category '{category}'")
                if source_type:
                    print(f"   from source '{source_type}'")
                print("")
                print("Try:")
                print("  - Running '/skills list-all' without filters")
                print("  - Checking the registry file")
            else:
                print(f"📦 All Available Skills ({len(results)}):")
                print("")

                for i, skill in enumerate(results, 1):
                    print(f"{i}. {format_skill_summary(skill)}")
                    print("")

                print(f"💡 Tip: Use '/skills install <name>' to install a skill")
                print(f"💡 Tip: Use '/skills list' to see installed skills")

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
