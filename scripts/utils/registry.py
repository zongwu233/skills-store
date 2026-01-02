"""
Skills Registry Management Module

This module handles loading, saving, and querying the skills registry.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime


class SkillsRegistry:
    """Manages the skills registry"""

    def __init__(self, registry_path: str = None):
        """
        Initialize the registry manager

        Args:
            registry_path: Path to skills-registry.json file
        """
        if registry_path is None:
            # Default to data/skills-registry.json relative to project root
            project_root = Path(__file__).parent.parent.parent
            registry_path = project_root / "data" / "skills-registry.json"

        self.registry_path = Path(registry_path)
        self.data = None

    def load(self) -> Dict[str, Any]:
        """
        Load the skills registry from disk

        Returns:
            Dictionary containing the registry data

        Raises:
            FileNotFoundError: If registry file doesn't exist
            json.JSONDecodeError: If registry file is invalid JSON
        """
        if not self.registry_path.exists():
            raise FileNotFoundError(f"Registry file not found: {self.registry_path}")

        with open(self.registry_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        return self.data

    def save(self, data: Dict[str, Any] = None) -> None:
        """
        Save the skills registry to disk

        Args:
            data: Registry data to save. If None, uses current self.data
        """
        if data is not None:
            self.data = data

        if self.data is None:
            raise ValueError("No data to save")

        # Update last_updated timestamp
        self.data['last_updated'] = datetime.now().isoformat()

        with open(self.registry_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def search(self, query: str, category: str = None, source_type: str = None) -> List[Dict[str, Any]]:
        """
        Search for skills by name, description, or tags

        Args:
            query: Search query string
            category: Optional category filter
            source_type: Optional source type filter (github, local)

        Returns:
            List of matching skill dictionaries
        """
        if self.data is None:
            self.load()

        query_lower = query.lower()
        results = []

        for skill_id, skill in self.data.get('skills', {}).items():
            # Apply filters
            if category and skill.get('metadata', {}).get('category') != category:
                continue

            if source_type and skill.get('source', {}).get('type') != source_type:
                continue

            # Search in name, description, and tags
            name = skill.get('name', '').lower()
            description = skill.get('description', '').lower()
            tags = [tag.lower() for tag in skill.get('metadata', {}).get('tags', [])]

            if (query_lower in name or
                query_lower in description or
                any(query_lower in tag for tag in tags)):
                results.append(skill)

        return results

    def get_skill(self, skill_name: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific skill by name

        Args:
            skill_name: Name of the skill to retrieve

        Returns:
            Skill dictionary or None if not found
        """
        if self.data is None:
            self.load()

        return self.data.get('skills', {}).get(skill_name)

    def list_all(self, category: str = None) -> List[Dict[str, Any]]:
        """
        List all skills in the registry

        Args:
            category: Optional category filter

        Returns:
            List of all skill dictionaries
        """
        if self.data is None:
            self.load()

        skills = self.data.get('skills', {})

        if category:
            return [skill for skill in skills.values()
                    if skill.get('metadata', {}).get('category') == category]

        return list(skills.values())

    def get_categories(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all categories from the registry

        Returns:
            Dictionary of categories
        """
        if self.data is None:
            self.load()

        return self.data.get('categories', {})

    def get_stats(self) -> Dict[str, Any]:
        """
        Get registry statistics

        Returns:
            Dictionary containing registry stats
        """
        if self.data is None:
            self.load()

        return self.data.get('stats', {})


class InstalledSkillsRegistry:
    """Manages the installed skills registry"""

    def __init__(self, registry_path: str = None):
        """
        Initialize the installed skills registry manager

        Args:
            registry_path: Path to installed-skills.json file
        """
        if registry_path is None:
            # Default to data/installed-skills.json relative to project root
            project_root = Path(__file__).parent.parent.parent
            registry_path = project_root / "data" / "installed-skills.json"

        self.registry_path = Path(registry_path)
        self.data = None

    def load(self) -> Dict[str, Any]:
        """
        Load the installed skills registry from disk

        Returns:
            Dictionary containing the registry data
        """
        if not self.registry_path.exists():
            # Create default empty registry
            self.data = {
                "version": "1.0.0",
                "installed_skills": {},
                "config": {
                    "local_skills_path": "skills",
                    "auto_update": False,
                    "update_interval_hours": 24
                }
            }
            self.save()
            return self.data

        with open(self.registry_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        return self.data

    def get_project_root(self) -> Path:
        """
        Get the project root directory

        Returns:
            Path to project root
        """
        return Path(__file__).parent.parent.parent

    def get_skills_dir(self) -> Path:
        """
        Get the skills directory (absolute path)

        Returns:
            Absolute path to skills directory
        """
        config = self.data.get('config', {})
        relative_path = config.get('local_skills_path', 'skills')
        return self.get_project_root() / relative_path

    def save(self) -> None:
        """Save the installed skills registry to disk"""
        if self.data is None:
            raise ValueError("No data to save")

        with open(self.registry_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def add(self, skill_name: str, install_path: str, source: Dict[str, Any]) -> None:
        """
        Add a skill to the installed registry

        Args:
            skill_name: Name of the skill
            install_path: Path where skill is installed (can be absolute or relative)
            source: Source information dictionary
        """
        if self.data is None:
            self.load()

        # Convert to relative path if absolute
        install_path_obj = Path(install_path)
        try:
            relative_path = install_path_obj.relative_to(self.get_project_root())
        except ValueError:
            # If path is not relative to project root, store as-is
            relative_path = install_path_obj

        self.data['installed_skills'][skill_name] = {
            "name": skill_name,
            "install_path": str(relative_path),
            "source": source,
            "installed_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "is_valid": True
        }

        self.save()

    def get_absolute_path(self, relative_path: str) -> Path:
        """
        Convert a relative path from registry to absolute path

        Args:
            relative_path: Relative path from registry

        Returns:
            Absolute path
        """
        path_obj = Path(relative_path)
        if path_obj.is_absolute():
            return path_obj
        return self.get_project_root() / path_obj

    def remove(self, skill_name: str) -> bool:
        """
        Remove a skill from the installed registry

        Args:
            skill_name: Name of the skill to remove

        Returns:
            True if skill was removed, False if not found
        """
        if self.data is None:
            self.load()

        if skill_name in self.data['installed_skills']:
            del self.data['installed_skills'][skill_name]
            self.save()
            return True

        return False

    def get(self, skill_name: str) -> Optional[Dict[str, Any]]:
        """
        Get an installed skill by name

        Args:
            skill_name: Name of the skill

        Returns:
            Installed skill dictionary or None if not found
        """
        if self.data is None:
            self.load()

        return self.data.get('installed_skills', {}).get(skill_name)

    def list_all(self) -> List[Dict[str, Any]]:
        """
        List all installed skills

        Returns:
            List of installed skill dictionaries
        """
        if self.data is None:
            self.load()

        return list(self.data.get('installed_skills', {}).values())

    def is_installed(self, skill_name: str) -> bool:
        """
        Check if a skill is installed

        Args:
            skill_name: Name of the skill

        Returns:
            True if skill is installed, False otherwise
        """
        if self.data is None:
            self.load()

        return skill_name in self.data.get('installed_skills', {})

    def update_validity(self, skill_name: str, is_valid: bool, error: str = None) -> None:
        """
        Update the validity status of an installed skill

        Args:
            skill_name: Name of the skill
            is_valid: Whether the skill is valid
            error: Optional error message if invalid
        """
        if self.data is None:
            self.load()

        if skill_name in self.data['installed_skills']:
            self.data['installed_skills'][skill_name]['is_valid'] = is_valid
            self.data['installed_skills'][skill_name]['validation_errors'] = error
            self.data['installed_skills'][skill_name]['last_updated'] = datetime.now().isoformat()
            self.save()
