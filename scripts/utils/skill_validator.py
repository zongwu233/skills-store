"""
Skill Validation Module

This module handles validation of skill directories and SKILL.md files.
"""

import re
from pathlib import Path
from typing import Dict, Tuple, List, Any
import yaml


class SkillValidationError:
    """Represents a validation error"""

    def __init__(self, field: str, message: str, severity: str = "error"):
        """
        Initialize a validation error

        Args:
            field: Field name where error occurred
            message: Error message
            severity: Error severity (error, warning, info)
        """
        self.field = field
        self.message = message
        self.severity = severity

    def __str__(self):
        return f"[{self.severity.upper()}] {self.field}: {self.message}"


class SkillValidator:
    """Validates skill directories and SKILL.md files"""

    # Required fields in SKILL.md frontmatter
    REQUIRED_FIELDS = ['name', 'description']

    # Maximum allowed skill size (10MB)
    MAX_SKILL_SIZE_BYTES = 10 * 1024 * 1024

    def __init__(self):
        """Initialize the validator"""
        self.errors: List[SkillValidationError] = []
        self.warnings: List[SkillValidationError] = []

    def validate_skill_directory(self, skill_path: str) -> Tuple[bool, List[SkillValidationError]]:
        """
        Validate a skill directory

        Args:
            skill_path: Path to the skill directory

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        self.errors = []
        self.warnings = []

        path = Path(skill_path)

        # Check if path exists
        if not path.exists():
            self.errors.append(SkillValidationError(
                "path",
                f"Skill directory does not exist: {skill_path}"
            ))
            return False, self.errors

        # Check if it's a directory
        if not path.is_dir():
            self.errors.append(SkillValidationError(
                "path",
                f"Path is not a directory: {skill_path}"
            ))
            return False, self.errors

        # Check for path traversal attempts
        if '..' in str(path):
            self.errors.append(SkillValidationError(
                "path",
                f"Path contains path traversal characters: {skill_path}"
            ))
            return False, self.errors

        # Check total size
        total_size = sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
        if total_size > self.MAX_SKILL_SIZE_BYTES:
            self.warnings.append(SkillValidationError(
                "size",
                f"Skill size ({total_size / 1024 / 1024:.2f}MB) exceeds recommended limit ({self.MAX_SKILL_SIZE_BYTES / 1024 / 1024}MB)",
                "warning"
            ))

        # Check for SKILL.md
        skill_md_path = path / "SKILL.md"
        if not skill_md_path.exists():
            self.errors.append(SkillValidationError(
                "SKILL.md",
                f"Required file SKILL.md not found in {skill_path}"
            ))
            return False, self.errors

        # Validate SKILL.md
        self._validate_skill_md(skill_md_path)

        # Check for optional directories
        self._validate_optional_directories(path)

        return len(self.errors) == 0, self.errors + self.warnings

    def _validate_skill_md(self, skill_md_path: Path) -> None:
        """
        Validate SKILL.md file

        Args:
            skill_md_path: Path to SKILL.md file
        """
        try:
            with open(skill_md_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if file is empty
            if not content.strip():
                self.errors.append(SkillValidationError(
                    "SKILL.md",
                    "SKILL.md file is empty"
                ))
                return

            # Extract YAML frontmatter
            frontmatter = self._extract_frontmatter(content)

            if frontmatter is None:
                self.errors.append(SkillValidationError(
                    "SKILL.md",
                    "No YAML frontmatter found. SKILL.md must start with ---"
                ))
                return

            # Parse YAML
            try:
                metadata = yaml.safe_load(frontmatter)
            except yaml.YAMLError as e:
                self.errors.append(SkillValidationError(
                    "SKILL.md",
                    f"Invalid YAML in frontmatter: {str(e)}"
                ))
                return

            if not isinstance(metadata, dict):
                self.errors.append(SkillValidationError(
                    "SKILL.md",
                    "YAML frontmatter must be a dictionary/object"
                ))
                return

            # Check required fields
            for field in self.REQUIRED_FIELDS:
                if field not in metadata:
                    self.errors.append(SkillValidationError(
                        f"frontmatter.{field}",
                        f"Required field '{field}' is missing"
                    ))
                elif not metadata[field] or not str(metadata[field]).strip():
                    self.errors.append(SkillValidationError(
                        f"frontmatter.{field}",
                        f"Required field '{field}' is empty"
                    ))

            # Validate name format
            if 'name' in metadata:
                name = metadata['name']
                if not re.match(r'^[a-z0-9-]+$', name):
                    self.warnings.append(SkillValidationError(
                        "frontmatter.name",
                        "Skill name should contain only lowercase letters, numbers, and hyphens",
                        "warning"
                    ))

            # Check content after frontmatter
            content_after_frontmatter = content.split('---', 2)[-1].strip()
            if not content_after_frontmatter:
                self.warnings.append(SkillValidationError(
                    "SKILL.md",
                    "SKILL.md has no content after frontmatter",
                    "warning"
                ))

        except Exception as e:
            self.errors.append(SkillValidationError(
                "SKILL.md",
                f"Error reading SKILL.md: {str(e)}"
            ))

    def _extract_frontmatter(self, content: str) -> str:
        """
        Extract YAML frontmatter from markdown content

        Args:
            content: Markdown file content

        Returns:
            YAML frontmatter string or None if not found
        """
        # Check if content starts with ---
        if not content.startswith('---'):
            return None

        # Find the closing ---
        parts = content.split('---', 2)
        if len(parts) < 3:
            return None

        return parts[1].strip()

    def _validate_optional_directories(self, skill_path: Path) -> None:
        """
        Validate optional skill directories

        Args:
            skill_path: Path to skill directory
        """
        optional_dirs = {
            'scripts': ['py', 'sh', 'bash'],
            'reference': ['md', 'txt'],
            'assets': []  # Any files allowed
        }

        for dir_name, allowed_extensions in optional_dirs.items():
            dir_path = skill_path / dir_name
            if dir_path.exists():
                # Check if it's a directory
                if not dir_path.is_dir():
                    self.warnings.append(SkillValidationError(
                        dir_name,
                        f"{dir_name} exists but is not a directory",
                        "warning"
                    ))
                    continue

                # Check file extensions if specified
                if allowed_extensions:
                    for file_path in dir_path.rglob('*'):
                        if file_path.is_file():
                            ext = file_path.suffix.lstrip('.')
                            if ext and ext not in allowed_extensions:
                                self.warnings.append(SkillValidationError(
                                    f"{dir_name}/files",
                                    f"File {file_path.name} has unexpected extension .{ext}",
                                    "warning"
                                ))

    def parse_skill_md(self, skill_path: str) -> Dict[str, Any]:
        """
        Parse SKILL.md and return metadata

        Args:
            skill_path: Path to skill directory

        Returns:
            Dictionary containing parsed metadata
        """
        skill_md_path = Path(skill_path) / "SKILL.md"

        if not skill_md_path.exists():
            return {}

        try:
            with open(skill_md_path, 'r', encoding='utf-8') as f:
                content = f.read()

            frontmatter = self._extract_frontmatter(content)
            if frontmatter is None:
                return {}

            metadata = yaml.safe_load(frontmatter)
            return metadata if isinstance(metadata, dict) else {}

        except Exception:
            return {}

    def format_errors(self, errors: List[SkillValidationError]) -> str:
        """
        Format validation errors for display

        Args:
            errors: List of validation errors

        Returns:
            Formatted error message string
        """
        if not errors:
            return "✅ No errors found"

        lines = []
        for error in errors:
            lines.append(str(error))

        return '\n'.join(lines)


def validate_skill_directory(skill_path: str) -> Tuple[bool, str]:
    """
    Convenience function to validate a skill directory

    Args:
        skill_path: Path to the skill directory

    Returns:
        Tuple of (is_valid, message)
    """
    validator = SkillValidator()
    is_valid, errors = validator.validate_skill_directory(skill_path)
    message = validator.format_errors(errors)
    return is_valid, message


if __name__ == "__main__":
    # Test the validator
    import sys

    if len(sys.argv) < 2:
        print("Usage: python skill_validator.py <skill_path>")
        sys.exit(1)

    skill_path = sys.argv[1]
    is_valid, message = validate_skill_directory(skill_path)

    print(f"Validating: {skill_path}")
    print(message)

    sys.exit(0 if is_valid else 1)
