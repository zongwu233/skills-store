#!/usr/bin/env python3
"""
List Installed Skills Script

List all installed skills with their status.
"""

import sys
import io
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Add parent directory to path to import utils
sys.path.insert(0, str(Path(__file__).parent))

from utils.registry import InstalledSkillsRegistry
from utils.skill_validator import SkillValidator


def format_installed_skill(skill: dict, index: int, registry: InstalledSkillsRegistry) -> str:
    """Format an installed skill for display"""
    name = skill.get('name', 'Unknown')
    install_path = skill.get('install_path', 'Unknown')

    # Convert to absolute path for display
    try:
        absolute_path = registry.get_absolute_path(install_path)
    except:
        absolute_path = Path(install_path)

    installed_at = skill.get('installed_at', '')
    is_valid = skill.get('is_valid', False)

    # Parse installation date
    try:
        if installed_at:
            dt = datetime.fromisoformat(installed_at)
            installed_str = dt.strftime("%Y-%m-%d %H:%M")
        else:
            installed_str = "Unknown"
    except:
        installed_str = "Unknown"

    # Get source info
    source_type = skill.get('source', {}).get('type', 'unknown')
    source_info = skill.get('source', {}).get('repo', 'local')

    # Status indicator
    status = "✅ Valid" if is_valid else "❌ Invalid"

    lines = [
        f"{index}. 📦 {name}",
        f"   📁 Path: {absolute_path}",
        f"   📅 Installed: {installed_str}",
        f"   🔗 Source: {source_type} ({source_info})",
        f"   {status}",
    ]

    return '\n'.join(lines)


def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h']:
        print("Usage: python list_skills.py [options]")
        print("")
        print("Options:")
        print("  --validate    Validate all installed skills and show details")
        print("  --json        Output as JSON")
        print("")
        print("Examples:")
        print("  python list_skills.py")
        print("  python list_skills.py --validate")
        sys.exit(0)

    # Parse arguments
    validate = False
    output_json = False

    for arg in sys.argv[1:]:
        if arg == '--validate':
            validate = True
        elif arg == '--json':
            output_json = True

    try:
        # Load installed skills registry
        installed_registry = InstalledSkillsRegistry()
        installed_registry.load()

        skills = installed_registry.list_all()

        if output_json:
            # Output as JSON
            import json
            print(json.dumps(skills, indent=2, ensure_ascii=False))
        else:
            # Output as formatted text
            if not skills:
                print("📭 No skills installed yet.")
                print("")
                print("Install a skill using:")
                print("  python install_skill.py <skill_name>")
                print("")
                print("Or search for available skills:")
                print("  python search_skills.py <query>")
            else:
                print(f"📦 Installed Skills ({len(skills)}):")
                print("")

                # Validate if requested
                if validate:
                    validator = SkillValidator()
                    print("🔍 Validating installed skills...")
                    print("")

                for i, skill in enumerate(skills, 1):
                    # Re-validate if requested
                    if validate:
                        install_path_relative = skill.get('install_path')
                        if install_path_relative:
                            # Convert to absolute path for validation
                            install_path = installed_registry.get_absolute_path(install_path_relative)
                            is_valid, errors = validator.validate_skill_directory(str(install_path))
                            skill['is_valid'] = is_valid
                            skill['validation_errors'] = [str(e) for e in errors]

                            # Update in registry
                            installed_registry.update_validity(
                                skill['name'],
                                is_valid,
                                ', '.join([str(e) for e in errors]) if errors else None
                            )

                    print(format_installed_skill(skill, i, installed_registry))
                    print("")

                    # Show validation errors if any
                    if validate and not skill.get('is_valid', True):
                        errors = skill.get('validation_errors', [])
                        if errors:
                            print("   ⚠️  Validation Errors:")
                            for error in errors:
                                print(f"      - {error}")
                            print("")

    except FileNotFoundError:
        print("❌ No installed skills registry found.")
        print("")
        print("This is normal if you haven't installed any skills yet.")
        print("Install a skill using: python install_skill.py <skill_name>")
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
