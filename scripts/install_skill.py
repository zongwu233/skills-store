#!/usr/bin/env python3
"""
Install Skill Script

Download and install a skill from GitHub or local directory.
"""

import sys
import io
import shutil
import subprocess
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Add parent directory to path to import utils
sys.path.insert(0, str(Path(__file__).parent))

from utils.registry import SkillsRegistry, InstalledSkillsRegistry
from utils.github_client import GitHubClient
from utils.skill_validator import SkillValidator


def main():
    """Main entry point"""
    if len(sys.argv) < 2 or sys.argv[1] in ['--help', '-h']:
        print("Usage: python install_skill.py <skill_name> [options]")
        print("")
        print("Options:")
        print("  --force        Reinstall if already installed")
        print("  --branch <br>  Specify git branch (default: main)")
        print("  --local <path> Install from local directory instead of GitHub")
        print("")
        print("Examples:")
        print("  python install_skill.py pdf")
        print("  python install_skill.py pdf --force")
        print("  python install_skill.py my-skill --local /path/to/skill")
        sys.exit(0 if len(sys.argv) >= 2 else 1)

    # Parse arguments
    skill_name = sys.argv[1]
    force = False
    branch = "main"
    local_path = None

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--force':
            force = True
            i += 1
        elif sys.argv[i] == '--branch' and i + 1 < len(sys.argv):
            branch = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--local' and i + 1 < len(sys.argv):
            local_path = sys.argv[i + 1]
            i += 2
        else:
            print(f"Unknown option: {sys.argv[i]}", file=sys.stderr)
            sys.exit(1)

    try:
        # Load registries
        skills_registry = SkillsRegistry()
        skills_registry.load()

        installed_registry = InstalledSkillsRegistry()
        installed_registry.load()

        # Check if already installed
        if installed_registry.is_installed(skill_name) and not force:
            installed = installed_registry.get(skill_name)
            print(f"⚠️  Skill '{skill_name}' is already installed.")
            print(f"   Location: {installed.get('install_path')}")
            print("")
            print("Use --force to reinstall")
            sys.exit(0)

        # Get configuration
        config = installed_registry.data.get('config', {})
        skills_base_dir = Path(config.get('local_skills_path', 'skills'))

        # Install from local or GitHub
        if local_path:
            success = install_from_local(
                skill_name,
                local_path,
                skills_base_dir,
                installed_registry
            )
        else:
            # Look up skill in registry
            skill_info = skills_registry.get_skill(skill_name)
            if not skill_info:
                print(f"❌ Skill '{skill_name}' not found in registry.")
                print("")
                print("Search for available skills:")
                print(f"  python search_skills.py \"{skill_name}\"")
                print("")
                print("Or list all skills:")
                print("  python search_skills.py \"\"")
                sys.exit(1)

            # Validate skill source
            source = skill_info.get('source', {})
            source_type = source.get('type')

            if source_type == 'github':
                success = install_from_github(
                    skill_name,
                    skill_info,
                    skills_base_dir,
                    installed_registry,
                    branch
                )
            elif source_type == 'local':
                # For 'local' type in registry, get the path
                source_path = source.get('path')
                if not source_path:
                    print(f"❌ Skill '{skill_name}' has invalid source configuration (missing path)")
                    sys.exit(1)

                success = install_from_local(
                    skill_name,
                    source_path,
                    skills_base_dir,
                    installed_registry
                )
            else:
                print(f"❌ Unsupported source type: {source_type}")
                sys.exit(1)

        if success:
            print(f"✅ Successfully installed '{skill_name}'")
            install_path = skills_base_dir / skill_name
            print(f"   Location: {install_path}")
            print("")
            print("You can now use this skill in Claude!")
        else:
            print(f"❌ Failed to install '{skill_name}'")
            sys.exit(1)

    except FileNotFoundError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


def install_from_github(
    skill_name: str,
    skill_info: dict,
    skills_base_dir: Path,
    installed_registry: InstalledSkillsRegistry,
    branch: str
) -> bool:
    """
    Install a skill from GitHub

    Args:
        skill_name: Name of the skill
        skill_info: Skill information from registry
        skills_base_dir: Base directory for installed skills
        installed_registry: Installed skills registry
        branch: Git branch

    Returns:
        True if successful, False otherwise
    """
    source = skill_info.get('source', {})
    repo = source.get('repo')
    path_in_repo = source.get('path')

    if not repo or not path_in_repo:
        print(f"❌ Invalid GitHub source configuration for '{skill_name}'")
        return False

    install_path = skills_base_dir / skill_name

    print(f"📥 Downloading '{skill_name}' from GitHub...")
    print(f"   Repo: {repo}")
    print(f"   Path: {path_in_repo}")
    print(f"   Branch: {branch}")
    print("")

    # Remove existing installation if force reinstall
    if install_path.exists():
        print(f"🗑️  Removing existing installation...")
        shutil.rmtree(install_path)

    # Download from GitHub
    client = GitHubClient()
    success = client.download_directory(repo, path_in_repo, str(install_path), branch)

    if not success:
        print(f"❌ Failed to download from GitHub")
        return False

    # Validate the downloaded skill
    print(f"🔍 Validating downloaded skill...")
    validator = SkillValidator()
    is_valid, errors = validator.validate_skill_directory(install_path)

    if not is_valid:
        print(f"❌ Validation failed:")
        for error in errors:
            print(f"   {error}")
        print("")
        print("Cleaning up...")
        shutil.rmtree(install_path)
        return False

    print(f"✅ Validation passed")

    # Register in installed skills
    source_info = {
        "type": "github",
        "repo": repo,
        "url": source.get('url', ''),
        "branch": branch
    }

    installed_registry.add(skill_name, str(install_path), source_info)

    # Create symlink for Claude Code auto-discovery
    create_skill_symlink(install_path, skill_name)

    return True


def install_from_local(
    skill_name: str,
    source_path: str,
    skills_base_dir: Path,
    installed_registry: InstalledSkillsRegistry
) -> bool:
    """
    Install a skill from a local directory

    Args:
        skill_name: Name of the skill
        source_path: Source directory path
        skills_base_dir: Base directory for installed skills
        installed_registry: Installed skills registry

    Returns:
        True if successful, False otherwise
    """
    source_dir = Path(source_path)

    if not source_dir.exists():
        print(f"❌ Source directory does not exist: {source_path}")
        return False

    if not source_dir.is_dir():
        print(f"❌ Source path is not a directory: {source_path}")
        return False

    print(f"📋 Installing '{skill_name}' from local directory...")
    print(f"   Source: {source_path}")
    print("")

    # Validate source
    print(f"🔍 Validating source skill...")
    validator = SkillValidator()
    is_valid, errors = validator.validate_skill_directory(source_dir)

    if not is_valid:
        print(f"❌ Validation failed:")
        for error in errors:
            print(f"   {error}")
        return False

    print(f"✅ Validation passed")

    # Copy to installation directory
    install_path = skills_base_dir / skill_name

    if install_path.exists():
        print(f"🗑️  Removing existing installation...")
        shutil.rmtree(install_path)

    print(f"📋 Copying files...")
    shutil.copytree(source_dir, install_path)

    # Register in installed skills
    source_info = {
        "type": "local",
        "path": str(source_dir.absolute())
    }

    installed_registry.add(skill_name, str(install_path), source_info)

    # Create symlink for Claude Code auto-discovery
    create_skill_symlink(install_path, skill_name)

    return True


def create_skill_symlink(skill_path: Path, skill_name: str) -> str:
    """
    Create a symlink from plugin-skills/ to the installed skill for Claude Code auto-discovery.

    Implements a three-tier fallback strategy:
    1. Symbolic link (Unix or Windows with Developer Mode)
    2. Directory junction (Windows, no special permissions needed)
    3. Copy (last resort, works everywhere)

    Args:
        skill_path: Path to the installed skill directory
        skill_name: Name of the skill

    Returns:
        Type of link created: "symlink", "junction", or "copy"
    """
    # Get plugin-skills directory
    script_dir = Path(__file__).parent
    plugin_skills_dir = script_dir.parent / "plugin-skills"
    plugin_skills_dir.mkdir(exist_ok=True)

    symlink_path = plugin_skills_dir / skill_name

    # Remove existing symlink or directory
    if symlink_path.exists() or symlink_path.is_symlink():
        if symlink_path.is_symlink():
            symlink_path.unlink()
        else:
            shutil.rmtree(symlink_path)

    # Try different linking methods
    link_type = None

    if sys.platform != 'win32':
        # Unix/Linux/macOS: Use standard symbolic links
        try:
            symlink_path.symlink_to(skill_path.absolute())
            link_type = "symlink"
            print(f"✅ Created symbolic link in plugin-skills/ for Claude Code discovery")
        except OSError as e:
            print(f"⚠️  Could not create symlink: {e}", file=sys.stderr)
            # Fallback to copy
            shutil.copytree(skill_path, symlink_path)
            link_type = "copy"
            print(f"✅ Copied skill to plugin-skills/ for Claude Code discovery")
    else:
        # Windows: Try symlink → junction → copy
        try:
            # Try symbolic link first (requires Developer Mode or Admin)
            symlink_path.symlink_to(skill_path.absolute())
            link_type = "symlink"
            print(f"✅ Created symbolic link in plugin-skills/ for Claude Code discovery")
        except OSError:
            try:
                # Try directory junction (works without Developer Mode)
                result = subprocess.run(
                    ['mklink', '/J', str(symlink_path), str(skill_path.absolute())],
                    shell=True,
                    check=True,
                    capture_output=True
                )
                link_type = "junction"
                print(f"✅ Created directory junction in plugin-skills/ for Claude Code discovery")
            except subprocess.CalledProcessError:
                # Final fallback: copy the directory
                shutil.copytree(skill_path, symlink_path)
                link_type = "copy"
                print(f"⚠️  Could not create symlink or junction on Windows")
                print(f"✅ Copied skill to plugin-skills/ for Claude Code discovery")
                print(f"   Note: Enable Developer Mode for symbolic links")

    return link_type


if __name__ == "__main__":
    main()
