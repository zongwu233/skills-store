"""
Remote Registry Fetcher Module

This module handles fetching the skills registry from remote GitHub repositories.
"""

import json
import requests
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, Optional


class RemoteRegistryFetcher:
    """Fetches skills registry from remote GitHub repositories"""

    def __init__(self, config_path: str = None):
        """
        Initialize the remote registry fetcher

        Args:
            config_path: Path to remote registry config file
        """
        if config_path is None:
            project_root = Path(__file__).parent.parent.parent
            config_path = project_root / "data" / "remote-registry-config.json"

        self.config_path = Path(config_path)
        self.cache_path = self.config_path.parent / "remote-registry-cache.json"
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """Load remote registry configuration"""
        if not self.config_path.exists():
            # Create default configuration
            default_config = {
                "version": "1.0.0",
                "sources": [
                    {
                        "name": "skills-registry",
                        "type": "github",
                        "url": "https://github.com/zongwu233/skills-registry",
                        "branch": "main",
                        "skills_path": "skills/skills-registry.json",
                        "enabled": True,
                        "priority": 1
                    }
                ],
                "cache": {
                    "enabled": True,
                    "ttl_hours": 24,
                    "last_check": None,
                    "etag": None
                },
                "auto_sync": {
                    "enabled": True,
                    "on_search": True,
                    "on_list_all": True
                }
            }
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            return default_config

        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_config(self) -> None:
        """Save configuration to file"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)

    def should_refresh(self) -> bool:
        """
        Check if the remote registry should be refreshed

        Returns:
            True if cache is expired or doesn't exist
        """
        if not self.config['cache']['enabled']:
            return False

        # Check if cache exists
        if not self.cache_path.exists():
            return True

        # Check TTL
        last_check = self.config['cache'].get('last_check')
        if not last_check:
            return True

        try:
            last_check_dt = datetime.fromisoformat(last_check)
            ttl_hours = self.config['cache'].get('ttl_hours', 24)
            expiry_time = last_check_dt + timedelta(hours=ttl_hours)
            return datetime.now() > expiry_time
        except:
            return True

    def fetch_from_github(self, source: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Fetch registry from a GitHub repository

        Args:
            source: Source configuration dictionary

        Returns:
            Registry data or None if fetch failed
        """
        repo_url = source['url']
        branch = source.get('branch', 'main')
        skills_path = source['skills_path']

        # Convert GitHub URL to API URL
        # https://github.com/zongwu233/skills-registry
        # -> https://api.github.com/repos/zongwu233/skills-registry/contents/skills/skills-registry.json
        repo_parts = repo_url.replace('https://github.com/', '').split('/')
        if len(repo_parts) < 2:
            print(f"❌ Invalid GitHub URL: {repo_url}")
            return None

        owner, repo = repo_parts[0], repo_parts[1]
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{skills_path}?ref={branch}"

        headers = {}
        etag = self.config['cache'].get('etag')
        if etag:
            headers['If-None-Match'] = etag

        try:
            response = requests.get(api_url, headers=headers, timeout=10)

            if response.status_code == 304:
                # Not modified
                print("ℹ️  Remote registry not modified (304)")
                return None

            if response.status_code != 200:
                print(f"❌ Failed to fetch from {repo_url}: {response.status_code}")
                return None

            data = response.json()

            # Decode base64 content
            import base64
            content = base64.b64decode(data['content']).decode('utf-8')
            registry_data = json.loads(content)

            # Update ETag
            new_etag = response.headers.get('ETag')
            if new_etag:
                self.config['cache']['etag'] = new_etag

            return registry_data

        except Exception as e:
            print(f"❌ Error fetching from {repo_url}: {e}")
            return None

    def fetch(self, force: bool = False) -> Optional[Dict[str, Any]]:
        """
        Fetch the latest registry from remote sources

        Args:
            force: Force refresh even if cache is valid

        Returns:
            Latest registry data or None if no updates available
        """
        if not force and not self.should_refresh():
            return None

        print("🔄 Checking for remote registry updates...")

        # Get enabled sources sorted by priority
        sources = [s for s in self.config.get('sources', []) if s.get('enabled', True)]
        sources.sort(key=lambda x: x.get('priority', 999))

        for source in sources:
            print(f"📡 Fetching from {source['name']} ({source['url']})...")

            registry_data = self.fetch_from_github(source)
            if registry_data:
                # Update cache
                self.config['cache']['last_check'] = datetime.now().isoformat()
                self.save_config()

                # Save to cache file
                with open(self.cache_path, 'w', encoding='utf-8') as f:
                    json.dump(registry_data, f, indent=2, ensure_ascii=False)

                print(f"✅ Registry updated from {source['name']}")
                print(f"   Total skills: {len(registry_data.get('skills', {}))}")
                return registry_data

        print("⚠️  No updates available from remote sources")
        return None

    def get_cache(self) -> Optional[Dict[str, Any]]:
        """
        Get cached registry data

        Returns:
            Cached registry data or None if cache doesn't exist
        """
        if not self.cache_path.exists():
            return None

        with open(self.cache_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def merge_with_local(self, local_registry: Dict[str, Any], remote_registry: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge remote registry with local registry

        Args:
            local_registry: Local registry data
            remote_registry: Remote registry data

        Returns:
            Merged registry data
        """
        # Start with remote registry
        merged = remote_registry.copy()

        # Optionally preserve local-only skills
        local_skills = local_registry.get('skills', {})
        remote_skills = remote_registry.get('skills', {})

        # Add any local skills that aren't in remote
        for skill_name, skill_data in local_skills.items():
            if skill_name not in remote_skills:
                merged['skills'][skill_name] = skill_data

        # Update stats
        merged['stats'] = {
            'total_skills': len(merged['skills']),
            'last_sync': datetime.now().isoformat(),
            'local_skills': len(local_skills),
            'remote_skills': len(remote_skills)
        }

        return merged
