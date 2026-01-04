# Remote Registry Integration

## Overview

Skills Store now supports automatic synchronization with the remote [Skills Registry](https://github.com/zongwu233/skills-registry) repository. This means you always have access to the latest skills without manual updates.

## Features

### ✅ Auto-Sync

When you run `/skills list-all` or `/skills search`, Skills Store automatically:

1. Checks if the remote registry has updates (based on TTL)
2. Fetches the latest skills registry if updates are available
3. Merges remote data with your local registry
4. Shows you the most up-to-date skills

### ⚙️ Configuration

Remote registry configuration is stored in `data/remote-registry-config.json`:

```json
{
  "version": "1.0.0",
  "sources": [
    {
      "name": "skills-registry",
      "type": "github",
      "url": "https://github.com/zongwu233/skills-registry",
      "branch": "main",
      "skills_path": "skills/skills-registry.json",
      "enabled": true,
      "priority": 1
    }
  ],
  "cache": {
    "enabled": true,
    "ttl_hours": 24,
    "last_check": null,
    "etag": null
  },
  "auto_sync": {
    "enabled": true,
    "on_search": true,
    "on_list_all": true
  }
}
```

### 🔧 Configuration Options

#### Sources

- `name`: Display name for the source
- `url`: GitHub repository URL
- `branch`: Git branch to fetch from
- `skills_path`: Path to skills-registry.json in the repository
- `enabled`: Whether to use this source
- `priority`: Lower number = higher priority (for multiple sources)

#### Cache

- `enabled`: Enable caching to reduce API calls
- `ttl_hours`: How long to cache before checking for updates (default: 24 hours)
- `last_check`: Timestamp of last check (auto-managed)
- `etag`: GitHub ETag for efficient updates (auto-managed)

#### Auto Sync

- `enabled`: Master switch for auto-sync
- `on_search`: Auto-sync when running `/skills search`
- `on_list_all`: Auto-sync when running `/skills list-all`

## Usage

### Default Behavior (Auto-Sync Enabled)

```bash
# These commands will automatically check for updates
/skills list-all
/skills search "pdf"
```

First run after TTL expires:
```
🔄 Checking for remote registry updates...
📡 Fetching from skills-registry (https://github.com/zongwu233/skills-registry)...
✅ Registry updated from skills-registry
   Total skills: 21

📦 All Available Skills (21):
...
```

Subsequent runs within TTL:
```
📦 All Available Skills (21):
...
```

### Disable Auto-Sync for a Command

```bash
# Use --no-sync flag to skip remote check
python scripts/list_all_skills.py --no-sync
python scripts/search_skills.py "pdf" --no-sync
```

### Manual Sync

Force a refresh regardless of TTL:

```python
from scripts.utils.remote_registry import RemoteRegistryFetcher

fetcher = RemoteRegistryFetcher()
remote_data = fetcher.fetch(force=True)
```

### Configure Different Sync Behavior

Edit `data/remote-registry-config.json`:

```json
{
  "auto_sync": {
    "enabled": true,
    "on_search": false,  // Don't sync on search
    "on_list_all": true  // Only sync on list-all
  },
  "cache": {
    "ttl_hours": 12  // Check every 12 hours instead of 24
  }
}
```

## Benefits

### 🎯 Always Up-to-Date

- Automatically get new skills from the community registry
- No manual updates needed
- Learn about new skills as soon as they're added

### ⚡ Smart Caching

- Reduces unnecessary API calls
- Uses GitHub ETags for efficient updates
- Configurable TTL to balance freshness and performance

### 🔀 Merge with Local Skills

- Your locally-added skills are preserved
- Remote skills are automatically integrated
- No conflicts or data loss

### 🛡️ Fault Tolerant

- If remote fetch fails, falls back to local registry
- No interruption to your workflow
- Errors are logged but don't break the commands

## How It Works

### Sync Flow

```
1. Run /skills list-all or /skills search
   ↓
2. Check if cache is expired (based on TTL)
   ↓
3. If expired: Fetch from GitHub API
   ↓
4. Compare ETag to check if modified
   ↓
5. If modified: Download and parse registry
   ↓
6. Merge remote data with local data
   ↓
7. Update local skills-registry.json
   ↓
8. Display results to user
```

### GitHub API Efficiency

The system uses GitHub's conditional requests with ETags:

- **First request**: Full download + save ETag
- **Subsequent requests**: Send ETag in `If-None-Match` header
- **304 Not Modified**: No download needed, use cache
- **200 OK**: New content available, download and update

This minimizes bandwidth and API rate limit usage.

## Troubleshooting

### Issue: Auto-sync not working

**Solution**:
1. Check config: `data/remote-registry-config.json`
2. Verify `auto_sync.enabled` is `true`
3. Check `on_search` or `on_list_all` as needed

### Issue: Always fetching from remote (ignoring cache)

**Solution**:
1. Check `cache.ttl_hours` setting
2. Verify `cache.enabled` is `true`
3. Check system time is correct

### Issue: Not getting latest skills

**Solution**:
1. Run with `--no-sync` flag once
2. Manually delete cache: `rm data/remote-registry-cache.json`
3. Run command again to force refresh

### Issue: GitHub API rate limit

**Solution**:
1. Increase `cache.ttl_hours` to reduce API calls
2. Disable auto-sync and run manual sync periodically
3. Set `GITHUB_TOKEN` environment variable for higher limits

## Advanced Usage

### Multiple Remote Sources

Configure multiple remote registries:

```json
{
  "sources": [
    {
      "name": "official-registry",
      "url": "https://github.com/zongwu233/skills-registry",
      "priority": 1,
      "enabled": true
    },
    {
      "name": "community-registry",
      "url": "https://github.com/otheruser/skills-registry",
      "priority": 2,
      "enabled": true
    }
  ]
}
```

Sources are fetched in priority order. The first successful response is used.

### Custom Registry Path

If your remote registry uses a different structure:

```json
{
  "sources": [
    {
      "skills_path": "custom/path/to/registry.json"
    }
  ]
}
```

### Disable Remote Sync Entirely

If you prefer a fully offline setup:

```json
{
  "auto_sync": {
    "enabled": false
  }
}
```

Or use `--no-sync` flag for every command.

## Migration from Local Registry

If you were using a local registry file:

1. **Backup your current registry**:
   ```bash
   cp data/skills-registry.json data/skills-registry.json.backup
   ```

2. **Enable remote sync**:
   ```bash
   # First sync will merge remote with your local
   /skills list-all
   ```

3. **Review the merged result**:
   ```bash
   # Check your local skills are preserved
   python scripts/list_skills.py
   ```

4. **Clean up (optional)**:
   ```bash
   # If satisfied, remove backup
   rm data/skills-registry.json.backup
   ```

## File Structure

```
skills-store/
├── data/
│   ├── skills-registry.json           # Main registry (merged local + remote)
│   ├── remote-registry-config.json    # Remote sync configuration
│   └── remote-registry-cache.json     # Cache of last remote fetch
├── scripts/
│   └── utils/
│       ├── registry.py                # Local registry management
│       └── remote_registry.py         # Remote fetcher (NEW)
└── REMOTE_REGISTRY.md                 # This file
```

## Performance Considerations

- **First run**: Takes ~1-2 seconds to fetch from GitHub
- **Cached runs**: No additional time (uses local cache)
- **TTL recommended**: 12-24 hours for balance
- **API usage**: Minimal due to ETag caching

## Security

- **Read-only**: Remote sync only fetches, never pushes
- **No authentication**: Uses public GitHub API (no token needed)
- **Validation**: All fetched data is validated before use
- **Fallback**: If remote fails, uses local registry

## Future Enhancements

Planned features for future versions:

- [ ] Webhook-based instant updates
- [ ] Differential updates (only changed skills)
- [ ] Multiple registry mirrors
- [ ] Signature verification
- [ ] Custom registry endpoints

## Support

For issues or questions:

- GitHub Issues: https://github.com/zongwu233/skills-store/issues
- Documentation: https://github.com/zongwu233/skills-store/blob/main/README.md
- Skills Registry: https://github.com/zongwu233/skills-registry
