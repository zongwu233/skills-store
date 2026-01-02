#!/usr/bin/env python3
"""
Show Skill Info Script

Display detailed information about a skill from the registry or an installed skill.
"""

import sys
import io
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Add parent directory to path to import utils
sys.path.insert(0, str(Path(__file__).parent))

from utils.registry import SkillsRegistry, InstalledSkillsRegistry
from utils.skill_validator import SkillValidator


def show_registry_skill(skill_name: str):
    """Show information about a skill from the registry"""
    registry = SkillsRegistry()
    registry.load()

    skill = registry.get_skill(skill_name)

    if not skill:
        print(f"❌ Skill '{skill_name}' not found in registry.")
        print("")
        print("Search for available skills:")
        print(f"  python search_skills.py \"{skill_name}\"")
        return False

    # Display skill information
    print(f"📦 {skill.get('name', 'Unknown')}")
    print("=" * 60)
    print("")

    print("📝 Description:")
    print(f"   {skill.get('description', 'No description')}")
    print("")

    # Source information
    source = skill.get('source', {})
    print("🔗 Source:")
    print(f"   Type: {source.get('type', 'Unknown')}")
    if source.get('type') == 'github':
        print(f"   Repository: {source.get('repo', 'Unknown')}")
        print(f"   URL: {source.get('url', 'Unknown')}")
        print(f"   Path in repo: {source.get('path', 'Unknown')}")
    elif source.get('type') == 'local':
        print(f"   Path: {source.get('path', 'Unknown')}")
    print("")

    # Metadata
    metadata = skill.get('metadata', {})
    print("📊 Metadata:")
    if metadata.get('author'):
        print(f"   Author: {metadata.get('author')}")
    if metadata.get('license'):
        print(f"   License: {metadata.get('license')}")
    if metadata.get('category'):
        print(f"   Category: {metadata.get('category')}")
    if metadata.get('tags'):
        print(f"   Tags: {', '.join(metadata.get('tags', []))}")
    print("")

    # Installation status
    installed_registry = InstalledSkillsRegistry()
    installed_registry.load()

    if installed_registry.is_installed(skill_name):
        installed = installed_registry.get(skill_name)
        install_path_relative = installed.get('install_path')
        install_path = installed_registry.get_absolute_path(install_path_relative)
        print("✅ Installation Status: Installed")
        print(f"   Location: {install_path}")
        print(f"   Installed: {installed.get('installed_at', 'Unknown')}")
        print(f"   Valid: {'Yes' if installed.get('is_valid', True) else 'No'}")
    else:
        print("❌ Installation Status: Not installed")
        print("")
        print(f"Install with: python install_skill.py {skill_name}")

    return True


def show_installed_skill(skill_name: str):
    """Show information about an installed skill"""
    installed_registry = InstalledSkillsRegistry()
    installed_registry.load()

    skill = installed_registry.get(skill_name)

    if not skill:
        print(f"❌ Skill '{skill_name}' is not installed.")
        print("")
        print("List installed skills:")
        print("  python list_skills.py")
        return False

    # Get absolute path
    install_path_relative = skill.get('install_path')
    install_path = installed_registry.get_absolute_path(install_path_relative)

    # Display basic information
    print(f"📦 {skill.get('name', 'Unknown')}")
    print("=" * 60)
    print("")

    print("📁 Installation:")
    print(f"   Path: {install_path}")
    print(f"   Installed: {skill.get('installed_at', 'Unknown')}")
    print(f"   Valid: {'✅ Yes' if skill.get('is_valid', True) else '❌ No'}")
    print("")

    # Source information
    source = skill.get('source', {})
    print("🔗 Source:")
    print(f"   Type: {source.get('type', 'Unknown')}")
    if source.get('type') == 'github':
        print(f"   Repository: {source.get('repo', 'Unknown')}")
        print(f"   Branch: {source.get('branch', 'main')}")
    elif source.get('type') == 'local':
        print(f"   Path: {source.get('path', 'Unknown')}")
    print("")

    # Show SKILL.md preview
    skill_md_path = install_path / "SKILL.md"

    if skill_md_path.exists():
        print("📄 SKILL.md Preview (first 30 lines):")
        print("")

        try:
            with open(skill_md_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()[:30]

            for i, line in enumerate(lines, 1):
                print(f"{i:3d} | {line.rstrip()}")

            if len(skill_md_path.read_text(encoding='utf-8').splitlines()) > 30:
                print("")
                print("... (truncated)")

        except Exception as e:
            print(f"Error reading SKILL.md: {e}")
    else:
        print("⚠️  SKILL.md not found")

    # Show file structure
    if install_path.exists():
        print("")
        print("📂 File Structure:")

        def show_tree(path, prefix=""):
            """Display directory tree"""
            try:
                items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
                for i, item in enumerate(items):
                    is_last = i == len(items) - 1
                    connector = "└── " if is_last else "├── "
                    print(f"{prefix}{connector}{item.name}")
                    if item.is_dir() and not item.name.startswith('.'):
                        extension = "    " if is_last else "│   "
                        show_tree(item, prefix + extension)
            except PermissionError:
                pass

        show_tree(install_path)

    return True


def main():
    """Main entry point"""
    if len(sys.argv) < 2 or sys.argv[1] in ['--help', '-h']:
        print("Usage: python show_skill_info.py <skill_name> [options]")
        print("")
        print("Options:")
        print("  --installed    Show info about an installed skill (default: search in registry)")
        print("")
        print("Examples:")
        print("  python show_skill_info.py pdf")
        print("  python show_skill_info.py pdf --installed")
        sys.exit(0 if len(sys.argv) >= 2 else 1)

    skill_name = sys.argv[1]
    check_installed = '--installed' in sys.argv[2:]

    try:
        if check_installed:
            success = show_installed_skill(skill_name)
        else:
            success = show_registry_skill(skill_name)

        sys.exit(0 if success else 1)

    except FileNotFoundError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
