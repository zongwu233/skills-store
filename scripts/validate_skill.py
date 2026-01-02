#!/usr/bin/env python3
"""
Validate Skill Script

Validate a skill directory to ensure it meets the required standards.
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

from utils.skill_validator import SkillValidator, validate_skill_directory
from utils.registry import InstalledSkillsRegistry


def validate_installed_skill(skill_name: str):
    """Validate an installed skill"""
    installed_registry = InstalledSkillsRegistry()
    installed_registry.load()

    skill = installed_registry.get(skill_name)

    if not skill:
        print(f"❌ Skill '{skill_name}' is not installed.")
        print("")
        print("List installed skills:")
        print("  python list_skills.py")
        return False

    install_path_relative = skill.get('install_path')
    if not install_path_relative:
        print(f"❌ No installation path found for '{skill_name}'")
        return False

    # Convert to absolute path
    install_path = installed_registry.get_absolute_path(install_path_relative)

    print(f"🔍 Validating installed skill: {skill_name}")
    print(f"📁 Path: {install_path}")
    print("")

    return validate_directory(str(install_path), update_registry=True, skill_name=skill_name)


def validate_directory(skill_path: str, update_registry: bool = False, skill_name: str = None):
    """Validate a skill directory"""
    validator = SkillValidator()
    is_valid, errors = validator.validate_skill_directory(skill_path)

    if is_valid:
        print("✅ Validation PASSED")
        print("")
        print("The skill meets all requirements:")
        print("  ✓ SKILL.md exists")
        print("  ✓ YAML frontmatter is valid")
        print("  ✓ Required fields (name, description) are present")
        print("  ✓ Path is valid and safe")

        # Check for warnings
        warnings = [e for e in errors if e.severity == 'warning']
        if warnings:
            print("")
            print("⚠️  Warnings:")
            for warning in warnings:
                print(f"   {warning}")

        # Update registry if requested
        if update_registry and skill_name:
            try:
                installed_registry = InstalledSkillsRegistry()
                installed_registry.load()
                installed_registry.update_validity(skill_name, is_valid)
                print("")
                print(f"✅ Updated registry for '{skill_name}'")
            except Exception as e:
                print(f"⚠️  Could not update registry: {e}")

        return True

    else:
        print("❌ Validation FAILED")
        print("")

        # Separate errors and warnings
        errors_list = [e for e in errors if e.severity == 'error']
        warnings = [e for e in errors if e.severity == 'warning']

        if errors_list:
            print("🚫 Errors (must be fixed):")
            for error in errors_list:
                print(f"   {error}")
            print("")

        if warnings:
            print("⚠️  Warnings:")
            for warning in warnings:
                print(f"   {warning}")
            print("")

        print("📖 Requirements:")
        print("  1. Directory must exist")
        print("  2. SKILL.md file must be present")
        print("  3. SKILL.md must start with YAML frontmatter (---)")
        print("  4. Frontmatter must contain 'name' and 'description' fields")
        print("  5. Path must not contain '..' (path traversal)")
        print("  6. Total size should be < 10MB")
        print("")

        print("🔧 How to fix:")
        print("  1. Ensure SKILL.md exists in the skill directory")
        print("  2. Add YAML frontmatter at the top of SKILL.md:")
        print("     ---")
        print("     name: my-skill")
        print("     description: A brief description of what this skill does")
        print("     ---")
        print("")

        # Update registry if requested
        if update_registry and skill_name:
            try:
                installed_registry = InstalledSkillsRegistry()
                installed_registry.load()
                installed_registry.update_validity(
                    skill_name,
                    is_valid,
                    ', '.join([str(e) for e in errors_list])
                )
                print(f"✅ Updated registry for '{skill_name}'")
            except Exception as e:
                print(f"⚠️  Could not update registry: {e}")

        return False


def main():
    """Main entry point"""
    if len(sys.argv) < 2 or sys.argv[1] in ['--help', '-h']:
        print("Usage: python validate_skill.py <skill_name_or_path> [options]")
        print("")
        print("Arguments:")
        print("  skill_name_or_path    Name of installed skill, or path to skill directory")
        print("")
        print("Options:")
        print("  --path               Treat argument as a directory path (not skill name)")
        print("")
        print("Examples:")
        print("  python validate_skill.py pdf")
        print("  python validate_skill.py /path/to/skill --path")
        sys.exit(0 if len(sys.argv) >= 2 else 1)

    skill_arg = sys.argv[1]
    treat_as_path = '--path' in sys.argv[2:]

    try:
        if treat_as_path:
            # Validate by path
            if not Path(skill_arg).exists():
                print(f"❌ Path does not exist: {skill_arg}")
                sys.exit(1)

            success = validate_directory(skill_arg, update_registry=False)
        else:
            # Validate installed skill by name
            success = validate_installed_skill(skill_arg)

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
