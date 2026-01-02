"""
GitHub API Client Module

This module handles downloading skills from GitHub repositories.
"""

import os
import requests
import shutil
import zipfile
from pathlib import Path
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin


class GitHubClient:
    """Client for interacting with GitHub API"""

    def __init__(self, token: str = None):
        """
        Initialize GitHub client

        Args:
            token: Optional GitHub personal access token for authenticated requests
        """
        self.token = token
        self.api_base = "https://api.github.com"
        self.raw_base = "https://raw.githubusercontent.com"

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with optional authentication"""
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "skills-store"
        }

        if self.token:
            headers["Authorization"] = f"token {self.token}"

        return headers

    def download_directory(
        self,
        repo: str,
        directory_path: str,
        dest_dir: str,
        branch: str = "main"
    ) -> bool:
        """
        Download a directory from a GitHub repository

        Args:
            repo: Repository in format "owner/repo"
            directory_path: Path to directory in repo
            dest_dir: Local destination directory
            branch: Git branch (default: main)

        Returns:
            True if successful, False otherwise
        """
        try:
            dest_path = Path(dest_dir)
            dest_path.mkdir(parents=True, exist_ok=True)

            # Get directory contents
            contents = self._get_directory_contents(repo, directory_path, branch)

            if not contents:
                print(f"Warning: Directory {directory_path} appears to be empty")
                return True

            # Download each file
            for item in contents:
                if item['type'] == 'file':
                    self._download_file(
                        repo,
                        item['path'],
                        dest_path / item['name'],
                        branch
                    )
                elif item['type'] == 'dir':
                    # Recursively download subdirectory
                    self.download_directory(
                        repo,
                        item['path'],
                        dest_path / item['name'],
                        branch
                    )

            return True

        except Exception as e:
            print(f"Error downloading directory: {e}")
            return False

    def _get_directory_contents(
        self,
        repo: str,
        path: str,
        branch: str = "main"
    ) -> List[Dict[str, Any]]:
        """
        Get contents of a directory in a repository

        Args:
            repo: Repository in format "owner/repo"
            path: Path to directory
            branch: Git branch

        Returns:
            List of file/directory information
        """
        url = f"{self.api_base}/repos/{repo}/contents/{path}"
        params = {"ref": branch}

        response = requests.get(url, headers=self._get_headers(), params=params)
        response.raise_for_status()

        return response.json()

    def _download_file(
        self,
        repo: str,
        file_path: str,
        dest_path: Path,
        branch: str = "main"
    ) -> None:
        """
        Download a single file from GitHub

        Args:
            repo: Repository in format "owner/repo"
            file_path: Path to file in repo
            dest_path: Local destination path
            branch: Git branch
        """
        # Use raw.githubusercontent.com for direct file download
        url = f"{self.raw_base}/{repo}/{branch}/{file_path}"

        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()

        # Create parent directories if needed
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        # Write file
        with open(dest_path, 'wb') as f:
            f.write(response.content)

    def download_skill_zip(
        self,
        repo: str,
        skill_path: str,
        dest_dir: str,
        branch: str = "main"
    ) -> bool:
        """
        Download a skill directory as a ZIP archive and extract it

        Args:
            repo: Repository in format "owner/repo"
            skill_path: Path to skill in repo
            dest_dir: Local destination directory
            branch: Git branch

        Returns:
            True if successful, False otherwise
        """
        try:
            dest_path = Path(dest_dir)
            dest_path.mkdir(parents=True, exist_ok=True)

            # Download ZIP archive
            zip_url = f"{self.api_base}/repos/{repo}/zipball/{branch}"
            response = requests.get(zip_url, headers=self._get_headers(), stream=True)
            response.raise_for_status()

            # Save to temporary file
            temp_zip = dest_path / "temp_skill.zip"
            with open(temp_zip, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            # Extract ZIP
            with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
                # Find the skill directory in the archive
                skill_dir_name = None
                for name in zip_ref.namelist():
                    # The top-level directory is named like {repo}-{commit_hash}
                    parts = name.split('/')
                    if len(parts) > 1 and skill_path in parts:
                        skill_dir_name = parts[0]
                        break

                if skill_dir_name:
                    # Extract only the skill directory contents
                    for name in zip_ref.namelist():
                        if name.startswith(f"{skill_dir_name}/{skill_path}/"):
                            # Remove the repo prefix from paths
                            arcname = name[len(f"{skill_dir_name}/{skill_path}/"):]
                            if arcname:  # Skip empty path
                                zip_ref.extract(name, dest_path)
                                # Move to correct location
                                extracted_path = dest_path / name
                                target_path = dest_path / arcname
                                if extracted_path != target_path:
                                    target_path.parent.mkdir(parents=True, exist_ok=True)
                                    if extracted_path.is_file():
                                        shutil.move(str(extracted_path), str(target_path))
                                    elif extracted_path.is_dir() and extracted_path != dest_path / skill_dir_name:
                                        shutil.move(str(extracted_path), str(target_path))

                    # Clean up the extracted repo directory
                    repo_dir = dest_path / skill_dir_name
                    if repo_dir.exists():
                        shutil.rmtree(repo_dir)

            # Clean up temp file
            temp_zip.unlink()

            return True

        except Exception as e:
            print(f"Error downloading skill ZIP: {e}")
            return False

    def get_file_contents(
        self,
        repo: str,
        file_path: str,
        branch: str = "main"
    ) -> Optional[str]:
        """
        Get contents of a file from GitHub

        Args:
            repo: Repository in format "owner/repo"
            file_path: Path to file in repo
            branch: Git branch

        Returns:
            File contents as string, or None if error
        """
        try:
            url = f"{self.raw_base}/{repo}/{branch}/{file_path}"
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.text

        except Exception as e:
            print(f"Error getting file contents: {e}")
            return None

    def list_files_in_directory(
        self,
        repo: str,
        directory_path: str,
        branch: str = "main"
    ) -> List[str]:
        """
        List all files in a directory

        Args:
            repo: Repository in format "owner/repo"
            directory_path: Path to directory
            branch: Git branch

        Returns:
            List of file paths
        """
        try:
            contents = self._get_directory_contents(repo, directory_path, branch)
            return [item['path'] for item in contents if item['type'] == 'file']

        except Exception as e:
            print(f"Error listing files: {e}")
            return []

    def repository_exists(self, repo: str) -> bool:
        """
        Check if a repository exists

        Args:
            repo: Repository in format "owner/repo"

        Returns:
            True if repository exists, False otherwise
        """
        try:
            url = f"{self.api_base}/repos/{repo}"
            response = requests.get(url, headers=self._get_headers())
            return response.status_code == 200

        except Exception:
            return False


def download_skill(
    repo: str,
    skill_path: str,
    dest_dir: str,
    branch: str = "main",
    method: str = "directory"
) -> bool:
    """
    Convenience function to download a skill from GitHub

    Args:
        repo: Repository in format "owner/repo"
        skill_path: Path to skill in repo
        dest_dir: Local destination directory
        branch: Git branch
        method: Download method ('directory' or 'zip')

    Returns:
        True if successful, False otherwise
    """
    client = GitHubClient()

    if method == "zip":
        return client.download_skill_zip(repo, skill_path, dest_dir, branch)
    else:
        return client.download_directory(repo, skill_path, dest_dir, branch)


if __name__ == "__main__":
    # Test the client
    import sys

    if len(sys.argv) < 4:
        print("Usage: python github_client.py <repo> <skill_path> <dest_dir> [branch]")
        print("Example: python github_client.py anthropics/anthropic-skills document-skills/unknown/skills/pdf ./test-pdf")
        sys.exit(1)

    repo = sys.argv[1]
    skill_path = sys.argv[2]
    dest_dir = sys.argv[3]
    branch = sys.argv[4] if len(sys.argv) > 4 else "main"

    print(f"Downloading {skill_path} from {repo}...")
    success = download_skill(repo, skill_path, dest_dir, branch, method="directory")

    if success:
        print(f"✅ Successfully downloaded to {dest_dir}")
    else:
        print("❌ Failed to download")
        sys.exit(1)
