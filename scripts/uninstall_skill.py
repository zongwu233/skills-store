#!/usr/bin/env python3
"""
Uninstall Skill Script

Remove an installed skill and its symlink from the system.
"""

import sys
import io
import shutil
import os
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Add parent directory to path to import utils
sys.path.insert(0, str(Path(__file__).parent))

from utils.registry import InstalledSkillsRegistry


def main():
    """Main entry point"""
    if len(sys.argv) < 2 or sys.argv[1] in ['--help', '-h']:
        print("Usage: python uninstall_skill.py <skill_name>")
        print("")
        print("Remove an installed skill from the system.")
        print("")
        print("This will:")
        print("  1. Remove the symlink from plugin-skills/")
        print("  2. Remove the skill files from skills/")
        print("  3. Update the installed skills registry")
        print("")
        print("Example:")
        print("  python uninstall_skill.py pdf")
        sys.exit(0 if len(sys.argv) >= 2 else 1)

    skill_name = sys.argv[1]

    try:
        # Load registry
        installed_registry = InstalledSkillsRegistry()
        installed_registry.load()

        # Check if skill is installed
        if not installed_registry.is_installed(skill_name):
            print(f"⚠️  Skill '{skill_name}' is not installed.")
            print("")
            print("Installed skills:")
            installed = installed_registry.list_all()
            if installed:
                for skill in installed:
                    print(f"  - {skill['name']}")
            else:
                print("  (none)")
            sys.exit(0)

        # Get configuration
        config = installed_registry.data.get('config', {})
        skills_base_dir = Path(config.get('local_skills_path', 'skills'))

        # Remove symlink from plugin-skills/
        print(f"🗑️  Uninstalling '{skill_name}'...")
        print("")

        remove_skill_symlink(skill_name)

        # Remove skill files from skills/
        skill_path = skills_base_dir / skill_name

        if skill_path.exists():
            print(f"🗑️  Removing skill files from skills/...")
            shutil.rmtree(skill_path)
            print(f"✅ Removed {skill_path}")
        else:
            print(f"⚠️  Skill directory not found: {skill_path}")
            print("   (This is okay if the files were already removed manually)")

        # Update registry
        print("")
        print(f"📝 Updating installed skills registry...")
        installed_registry.remove(skill_name)
        print(f"✅ Removed '{skill_name}' from registry")

        print("")
        print(f"✅ Successfully uninstalled '{skill_name}'")

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


def remove_skill_symlink(skill_name: str):
    """
    Remove the symlink from plugin-skills/

    Args:
        skill_name: Name of the skill
    """
    # Get plugin-skills directory
    script_dir = Path(__file__).parent
    plugin_skills_dir = script_dir.parent / "plugin-skills"
    symlink_path = plugin_skills_dir / skill_name

    if not symlink_path.exists():
        print(f"⚠️  No symlink or copy found in plugin-skills/")
        print("   (This is okay if it was already removed manually)")
        return

    # Try to determine if it's a symlink/junction or a regular directory
    # On Windows, pathlib's is_symlink() and os.path.islink() may not detect junctions
    # So we try unlink first, then fallback to rmtree
    print(f"🔗 Removing from plugin-skills/...")

    # First try: unlink (for symlinks and junctions)
    try:
        symlink_path.unlink()
        print(f"✅ Removed symlink: {symlink_path}")
    except OSError:
        # Second try: rmtree (for regular directories/copies)
        try:
            shutil.rmtree(symlink_path)
            print(f"✅ Removed copy: {symlink_path}")
        except OSError as e:
            # Last resort: try os.rmdir for junctions
            try:
                os.rmdir(symlink_path)
                print(f"✅ Removed junction: {symlink_path}")
            except OSError:
                print(f"❌ Failed to remove {symlink_path}: {e}")
                raise


if __name__ == "__main__":
    main()
